"""Dora container module."""
from typing import Tuple, Iterator
from os import environ, path, mkdir

from sqlglot import exp
from boto3 import client
from dagster_pipes import PipesContext, PipesMetadataValue # pylint: disable=E0401
from pyiceberg.catalog import Catalog

from dora_core.utils import logger
from dora_core.asset import Job, Table
from dora_core.engine import INPUT_FILE_COLUMN, CheckType
from dora_aws.utils import s3_bucket_key

# AWS Glue Catalog name environment variable
CATALOG = environ.get("CATALOG", "GlueCatalog")
# Max number of upserts using pyiceberg
MAXUPSERT = 30000
# Home directory for DuckDB
HOME_DIR = "/tmp/duckdb/"
# Max memory for DuckDB
MAX_MEMORY = environ.get("MAX_MEMORY",10240)

S3 = client('s3')
log = logger(__name__)

def set_home(directory: str = HOME_DIR) -> str:
    """Set home directory for DuckDB and install necessary extensions.
    
    Args:
        directory (str): The directory to set as home. Defaults to HOME_DIR.
    
    Returns:
        str: SQL commands to set home directory and install extensions.
    """
    if not path.exists(directory):
        mkdir(directory)
    return f"SET home_directory='{directory}';"

def set_memory_limit() -> str:
    """Set memory limit for DuckDB."""
    _memory_limit = int(MAX_MEMORY) * 0.8
    return f"SET memory_limit='{_memory_limit}MB';"

def set_temp_dir() -> str:
    """Set temporary directory for DuckDB."""
    return f"SET temp_directory = '{HOME_DIR}';"

def install_extensions() -> str:
    """Set Iceberg extension for DuckDB."""
    return """
    INSTALL httpfs;LOAD httpfs;
    INSTALL aws;LOAD aws;
    INSTALL iceberg;LOAD iceberg;
    INSTALL avro FROM community;LOAD avro;
    """

def set_secret() -> str:
    """Define S3 secrets for DuckDB.
    
    Returns:
        str: SQL command to create S3 secret in DuckDB.
    """
    return f"""
    CREATE SECRET aws_s3_access_secrets (
        TYPE S3,
        KEY_ID '{environ["AWS_ACCESS_KEY_ID"]}',
        SECRET '{environ["AWS_SECRET_ACCESS_KEY"]}',
        SESSION_TOKEN '{environ["AWS_SESSION_TOKEN"]}',
        REGION '{environ["AWS_REGION"]}'
    );"""

def copy_statement(source:str, target:str) -> str:
    """Set the COPY command for DuckDB.
    """
    _fmt = "FORMAT CSV, HEADER TRUE, DELIMITER ','"
    return f"COPY ({source}) TO '{target}' WITH ({_fmt})"


def load_table(sql:str, table_name:str) -> Tuple[Job, Table]:
    """Load table definition from SQL script.
    
    Args:
        sql (str): SQL Script
        table_id (str): Table asset identifier
    
    Returns:
        Tuple[Job, Table]: The job and table objects.
    
    Raises:
        ValueError: If the table is not found in the SQL file.
    """
    _job = Job(name="execution", sql=sql)
    for _table in _job.tables:
        if _table.name == table_name:
            log.debug('Loading table %s', _table.identifier)
            return (_job, _table)
    raise ValueError(f"Table '{table_name}' not found in '{sql}'")

def _severity(error_type:CheckType) -> str:
    """Set the severity level for the error type.
    
    Args:
        error_type (CheckType): The error type.
    
    Returns:
        str: The severity level.
    """
    if error_type == CheckType.FAIL:
        return "ERROR"
    if error_type == CheckType.DROP:
        return "WARN"
    return "WARN"

def report_test_result(pipes:PipesContext, results:dict, err_file:str, err_type:CheckType, asset_key:str) -> dict:
    """Report the test result.
    
    Args:
        pipes (PipesContext): The context for Dagster pipes.
        results (dict): The test results.
        err_file (str): The error file path.
        asset_key (str): The asset key for reporting.
    
    Returns:
        dict: The report asset check result.
    """
    _failures = int(results['failures'][0])
    _file = results[INPUT_FILE_COLUMN][0]
    _check_name = results['name'][0]
    _serverity = _severity(err_type)
    log.info("%s: %s failures for %s assert", _serverity, _failures, _check_name)
    # Set the metadata
    _metadata = {
            "failures":PipesMetadataValue(type="int", raw_value=_failures),
            "source":PipesMetadataValue(type="url", raw_value=_file),
    }
    # Set the error file
    if _failures==0: # Remove the errors file
        log.debug("Removing error file %s", err_file)
        _bkt, _key = s3_bucket_key(err_file)
        S3.delete_object(Bucket=_bkt,Key=_key)
        err_file = str()
    else:
        _metadata["errors"] = PipesMetadataValue(type="url", raw_value=err_file)
    # Report the test result
    pipes.report_asset_check(
        asset_key=asset_key,
        check_name=_check_name,
        passed=_failures==0,
        severity=_serverity,
        metadata=_metadata
    )

def iceberg_scan(table:Table, catalog:Catalog) -> Iterator[exp.TableAlias]:
    """Create a DuckDB expression to scan upstream Iceberg tables.
    
    Args:
        table (Table): Dora table bject.
        catalog (str): Iceberg catalog object.
    
    Returns:
        str: DuckDB expression to scan Iceberg table.
    """
    for _ref in table.ast.get_upstream():
        _tbl = catalog.load_table(f"{_ref.db}.{_ref.name}")
        if _ref.alias:
            _alias = exp.TableAlias(this=_ref.alias)
            yield _alias
        else:
            _alias = exp.TableAlias(this=_ref.this)
            yield _alias
        # Replace the table reference with the Iceberg scan
        _ref.replace(exp.Alias(
            alias=_alias,
            this=exp.Subquery(
                this=exp.Select(expressions=[exp.Star()]
                ).from_(exp.Table(
                    this=exp.Anonymous(
                        this="iceberg_scan",
                        expressions=[exp.Literal(this=_tbl.metadata_location, is_string=True)]
                    )
                ))
            )
        ))
