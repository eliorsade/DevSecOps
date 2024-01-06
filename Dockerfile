FROM python:3.10

WORKDIR /script
COPY . /script
RUN pip install boto3 botocore
CMD ["python", "./main.py"]
