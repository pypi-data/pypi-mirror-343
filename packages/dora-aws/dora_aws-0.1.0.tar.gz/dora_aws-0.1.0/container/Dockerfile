FROM public.ecr.aws/lambda/python:3.12
LABEL maintainer="compass.uol"
ARG DORA_VERSION
# Project Content
COPY ./dist ${LAMBDA_TASK_ROOT}/dist
# Dora package dependencies
COPY ./container/requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --upgrade pip && \
    pip install ${LAMBDA_TASK_ROOT}/dist/dora_core-${DORA_VERSION}-py3-none-any.whl && \
    pip install ${LAMBDA_TASK_ROOT}/dist/dora_aws-${DORA_VERSION}-py3-none-any.whl && \
    pip install -r requirements.txt  && \
    rm -rf /root/.cache/pip && \
    rm -rf ${LAMBDA_TASK_ROOT}/dist
# Copy lambda content
COPY ./container/*.py ${LAMBDA_TASK_ROOT}
