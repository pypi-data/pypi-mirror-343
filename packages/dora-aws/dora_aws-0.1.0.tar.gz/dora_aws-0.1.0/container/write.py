# -*- coding: utf-8 -*-
"""Lambda Function to process and materialize data using DuckDB and Iceberg."""
from base64 import b64decode
from datetime import datetime
from os import path

from boto3 import client
from duckdb import connect, BinderException
from pyiceberg.table.snapshots import Snapshot
from pyiceberg.catalog import load_catalog
from dagster_pipes import (
    PipesContext,
    PipesMappingParamsLoader,
    PipesMetadataValue,
    open_dagster_pipes,
)

from dora_core.utils import logger
from dora_core.asset import Table, TableType
from dora_core.engine import (
    EngineType,
    Engine,
    Append,
    Upsert,
    Overwrite,
    META_COLUMN_UNMAPPED,
    META_COLUMN_EXEC,
    META_COLUMN_DATE,
)
from dora_core.exceptions import QueryExecutionError

# pylint: disable=import-error
from common import (
    set_home,
    set_memory_limit,
    set_temp_dir,
    set_secret,
    load_table,
    report_test_result,
    install_extensions,
    copy_statement,
    iceberg_scan,
    CATALOG,
)

log = logger('read')

def _report_unmmapped_columns(pipes: PipesContext, results: list, asset_key: str) -> dict:
    """Report the unmapped columns in the table schema.
    
    Args:
        pipes (PipesContext): The context for logging and reporting.
        results (list): The list of unmapped columns.
        asset_key (str): The asset key for reporting.
    
    Returns:
        dict: The result of the asset check report.
    """
    columns = dict()
    for column in results:
        columns.update({column['column_name']:PipesMetadataValue(
            type="text",
            raw_value=column['column_type'])})
    columns.update({"Number of Unmmapped Columns":PipesMetadataValue(
        type="int",
        raw_value=len(results))})
    return pipes.report_asset_check(
        asset_key=asset_key,
        check_name=META_COLUMN_UNMAPPED,
        passed=len(results)==0,
        severity="WARN",
        metadata=columns
    )

def _start_merge(**kwargs) -> None:
    """Start the merge process using Athena.
    
    Args:
        pipes (PipesContext): The context for Dagster pipes.
        sql (str): The SQL query for merging.
        location (str): The S3 location for query results.
        dag (str): The DAG identifier.
        file (str): The file path of the dataset.
    
    Returns:
        dict: The response from Athena.
    """
    pipes:PipesContext = kwargs['pipes']
    _response = client('athena').start_query_execution(
        QueryString = kwargs['sql'],
        ResultConfiguration = { 'OutputLocation': kwargs['location']}
    )
    pipes.log.debug(_response)
    query_execution_id = _response['QueryExecutionId']
    http_status_code = _response['ResponseMetadata']['HTTPStatusCode']
    pipes.report_asset_materialization(
        metadata={
            META_COLUMN_EXEC:PipesMetadataValue(type="text", raw_value=kwargs['dag']),
            META_COLUMN_DATE:PipesMetadataValue(type="text", raw_value=kwargs['lts']),
            "operation": PipesMetadataValue(type="text", raw_value=TableType.MERGING.value),
            "source":PipesMetadataValue(type="url", raw_value=kwargs['file']),
            "Engine":PipesMetadataValue(type="text", raw_value="Athena"),
            "Status":PipesMetadataValue(type="int", raw_value=int(http_status_code)),
            "QueryExecutionId":PipesMetadataValue(type="text", raw_value=query_execution_id),
        },
    )
    return _response

def _error_file_name(location: str, test_name: str, raw_file: str) -> str:
    """Get the error file path based on the location, test name, and raw file.
    
    Args:
        location (str): The location of the table.
        test_name (str): The name of the test.
        raw_file (str): The raw file name.
    
    Returns:
        str: The error file path.
    """
    _raw_file = raw_file.split('/')[-1]+".csv"
    return path.join(location,'.errors',test_name,_raw_file)

def _report_materialization(**kwargs) -> dict:
    """Report the materialization of the table.
    
    Args:
        pipes (PipesContext): The context for logging and reporting.
        table (Table): The table being materialized.
        file (str): The file path of the dataset.
        lts (str): The last timestamp.
        dag (str): The DAG identifier.
        snapshot (Snapshot): The snapshot of the materialized table.
    
    Returns:
        dict: The result of the materialization report.
    """
    pipes:PipesContext = kwargs['pipes']
    table:Table = kwargs['table']
    snapshot:Snapshot = kwargs.get('snapshot',None)
    _meta={
        META_COLUMN_EXEC:PipesMetadataValue(type="text", raw_value=kwargs['dag']),
        META_COLUMN_DATE:PipesMetadataValue(type="text", raw_value=kwargs['lts']),
        "operation": PipesMetadataValue(type="text", raw_value=table.table_type.value),
        "source":PipesMetadataValue(type="url", raw_value=kwargs['file']),
        "dagster/partition_row_count":PipesMetadataValue(type="int", raw_value=int(0)),
    }
    if snapshot is None:
        pipes.report_asset_materialization(metadata=_meta)
        return dict()
    else:
        _total = snapshot.summary.get("total-records","0")
        _added = snapshot.summary.get("added-records","0")
        _snap = snapshot.model_dump_json()
        _meta.update(
            {
                "snapshot":PipesMetadataValue(type="json", raw_value=_snap),
                "dagster/row_count":PipesMetadataValue(type="int", raw_value=int(_total)),
                "dagster/partition_row_count":PipesMetadataValue(type="int", raw_value=int(_added)),
            }
        )
        pipes.report_asset_materialization(metadata=_meta,data_version=str(snapshot.schema_id))
        return _snap

def _materialize(
        pipes: PipesContext,
        eng: Engine,
        event_dag:str,
        input_file: str,
        input_date: str) -> dict:
    """Process data and materialize the table.
    
    Args:
        pipes (PipesContext): The context for logging and reporting.
        eng (Engine): The engine for processing.
        event_dag (str): The DAG identifier.
        input_file (str): The input file path.
        input_date (str): The input date.
    
    Returns:
        dict: The output of the materialization process.
    
    Raises:
        QueryExecutionError: If any query execution fails.
    """
    _output = dict()
    catalog = load_catalog(CATALOG, **{"type": "glue"})
    log.debug('Table Operation: %s', eng.table.table_type.value)
    with connect(":memory:") as con:
        # Set up the environment
        con.execute(set_home())
        con.execute(set_temp_dir())
        con.execute(set_memory_limit())
        con.execute(install_extensions())
        con.execute(set_secret())
        _args = dict(pipes=pipes,table=eng.table,file=input_file,lts=input_date,dag=event_dag)
        try:
            # Execute the read query
            _alias = list(iceberg_scan(eng.table, catalog))
            _read_query = eng.read(input_file=input_file, event_dag=event_dag, alias=_alias)
            con.execute(_read_query)
            _desc_raw = con.sql(eng.read_desc()).to_arrow_table().to_pydict()
            eng.set_raw_columns(_desc_raw['column_name'])
        except BinderException as _ex:
            _msg = f"Failed do read file '{input_file}' using '{_read_query}'"
            log.debug(_msg)
            raise QueryExecutionError(_msg) from _ex
        try:
            # Execute the cast query
            _cast_query = eng.cast(dag=event_dag, input_file=input_file, input_date=input_date)
            con.execute(_cast_query)
            desc_cast = con.sql(eng.cast_desc()).to_arrow_table().to_pydict()
            eng.set_cast_columns(desc_cast['column_name'])
        except BinderException as _ex:
            log.error(_cast_query)
            raise QueryExecutionError(f"Failed cast data:{_cast_query}") from _ex
        try:
            # Execute the test query
            _test_query = eng.test()
            con.execute(_test_query)
        except BinderException as _ex:
            log.error(_test_query)
            raise QueryExecutionError(f"Failed test data:{_test_query}") from _ex
        try:
            # Materialize the table
            _result_query = eng.resultset()
            log.debug("Materializing:%s",_result_query)
            response = eng.save(
                catalog=catalog,
                dataset=con.sql(_result_query).to_arrow_table(),
                dag=event_dag,
                engine=EngineType.ATHENA)
            if isinstance(response, str):
                _args.update({'sql':response, 'location':eng.stage_location})
                _output = _start_merge(**_args)
            else:
                _args.update({'snapshot':response})
                _output = _report_materialization(**_args)
        except BinderException as _ex:
            pipes.log.error(_result_query)
            raise QueryExecutionError("Failed saving data") from _ex
        for t_type, t_name, t_sql in eng.test_results(input_file=input_file):
            try:
                # Copy the error data to a file
                _err_file = _error_file_name(eng.table.location, t_name, input_file)
                _copy_query = copy_statement(source=eng.droped(t_type, t_name), target=_err_file)
                log.debug("Copying:%s",_copy_query)
                con.sql(_copy_query)
                # Report the test result
                log.debug("Checking:%s:%s",t_type.name,t_name)
                report_test_result(
                    pipes=pipes,
                    results=con.sql(t_sql).to_arrow_table().to_pydict(),
                    err_file=_error_file_name(eng.table.location, t_name, input_file),
                    err_type=t_type,
                    asset_key=eng.table.name)
            except BinderException as _ex:
                pipes.report_asset_check(
                    asset_key=eng.table.name,
                    check_name=t_name,
                    passed=False,
                    severity="WARN",
                    metadata={"Exception":PipesMetadataValue(type="text", raw_value=str(_ex))})
        # Report the unmapped columns
        if eng.table.is_query_star: # Only report if the table is a query star
            _unmmapped_query = eng.unmapped()
            log.debug("Checking:Unmapped:%s",_unmmapped_query)
            if _unmmapped_query is not None:
                try:
                    _report_unmmapped_columns(
                        pipes=pipes,
                        results=con.sql(_unmmapped_query).to_arrow_table().to_pylist(),
                        asset_key=eng.table.name)
                except BinderException as _ex:
                    pipes.report_asset_check(
                        asset_key=eng.table.name,
                        check_name=META_COLUMN_UNMAPPED,
                        passed='list is empty' in str(_ex),
                        severity="WARN",
                        metadata={"Exception":PipesMetadataValue(
                            type="text", raw_value=str(_ex))})
            else:
                pipes.report_asset_check(
                    asset_key=eng.table.name,
                    check_name=META_COLUMN_UNMAPPED,
                    passed=True,
                    severity="WARN")
        return _output

def lambda_handler(event, _context):
    """Lambda handler to process the event and materialize the table.
    
    Args:
        event (dict): The event payload.
        _context (LambdaContext): The context object.
    
    Returns:
        dict: The result of the materialization process.
    """
    # Force the context to be reinitialized on the next request
    # see: https://github.com/dagster-io/dagster/issues/22094
    PipesContext._instance = None # pylint: disable=W0212
    with open_dagster_pipes(params_loader=PipesMappingParamsLoader(event)) as pipes:
        log.debug('Write: %s', _context)
        pipes.log.debug(event)
        # Get values from the event payload
        _table_id = event["table"]
        log.debug('TABLE: %s', _table_id)
        event_dag = event["dag"]
        log.debug('DAG: %s', event_dag)
        _input_file = event.get("file", event_dag)
        log.debug('FILE: %s', _input_file)
        _sql = b64decode(event["sql"]).decode('utf-8')
        log.debug('SQL: %s', _sql.replace('\n','\\n'))
        # Get the time from the event payload or use the current time
        _input_date = event.get("time", datetime.now().isoformat(timespec='seconds'))
        log.debug('TIME: %s', _input_date)
        # Stream log message back to Dagster
        pipes.log.info(f"loading file '{_input_file}' at '{_input_date}'")
        _job ,table = load_table(sql=_sql, table_name=_table_id)
        if table.table_type == TableType.APPENDING:
            engine = Append(job=_job, table=table, engine=EngineType.DUCKDB)
        elif table.table_type == TableType.UPSERTING:
            engine = Upsert(job=_job, table=table, engine=EngineType.DUCKDB)
        elif table.table_type == TableType.OVERWRITING:
            engine = Overwrite(job=_job, table=table, engine=EngineType.DUCKDB)
        else:
            raise NotImplementedError(f"Table type '{table.table_type}' not implemented")
        return _materialize(
            pipes=pipes,
            eng=engine,
            event_dag=event_dag,
            input_file=_input_file,
            input_date=_input_date
        )

    # Force the context to be reinitialized on the next request
    # see: https://github.com/dagster-io/dagster/issues/22094
    PipesContext._instance = None # pylint: disable=W0212
