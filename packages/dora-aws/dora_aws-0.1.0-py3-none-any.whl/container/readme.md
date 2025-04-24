### Docker Build and Run
Build and run the Docker image locally.

```sh
poetry  export -f requirements.txt \
        --output container/requirements.txt \
        --without-urls --with-credentials \
        --without-hashes --no-cache --ansi
```

```sh
docker build --platform linux/amd64 \
             --file container/Dockerfile \
             --build-arg DORA_VERSION=0.0.1 \
             -t doraimg/duckdb:0.0.1 .
docker push doraimg/duckdb:0.0.1
```

```sh
docker run --platform linux/amd64 -p 9090:8080 doraimg/duckdb:0.0.1
```

```sh
curl "http://localhost:9090/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'
```

```sh
docker push doraimg/duckdb:0.0.1
```

```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 756791736285.dkr.ecr.us-east-1.amazonaws.com
docker tag doraimg/duckdb:0.0.1 756791736285.dkr.ecr.us-east-1.amazonaws.com/dora:0.0.1
docker push 756791736285.dkr.ecr.us-east-1.amazonaws.com/dora:0.0.1
```

### Integrating Lambda with Dagster
Pipes allows your code to interact with Dagster outside of a full Dagster environment.
> See more:<https://docs.dagster.io/concepts/dagster-pipes/aws-lambda>

```sh
docker image prune -f
docker build --platform linux/amd64 \
             --file container/Dockerfile \
             --build-arg DORA_VERSION=0.0.1 \
             -t 756791736285.dkr.ecr.us-east-1.amazonaws.com/dora:0.0.1 .
docker push 756791736285.dkr.ecr.us-east-1.amazonaws.com/dora:0.0.1
```