FROM python:3.10

ARG AWS_S3_BUCKET_NAME
ARG LOG_MODE
ENV AWS_S3_BUCKET_NAME=${AWS_S3_BUCKET_NAME}
ENV LOG_MODE=${LOG_MODE}

WORKDIR /script
COPY . /script
RUN pip install boto3 botocore
CMD ["python", "./main.py"]
