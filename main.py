import boto3
import botocore
from botocore.exceptions import ClientError
import os
import sys


all_sg = []
filename = 'log.txt'

bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')
log_mode = os.environ.get('LOG_MODE')


print("Hello! welcome to the script that checks AWS account for SG with inbound rules to the world")
print("Let's begin with some pre-checking")
print("Checking AWS creds for connection")

# AWS checking
try:
    s3_client = boto3.client('s3')

except ClientError as error:
    print("Connecting to AWS failed:", error)
    sys.exit()


print("Checking s3 bucket exist")
# Check if S3 bucket name exist
s3 = boto3.resource('s3')
try:
    s3.meta.client.head_bucket(Bucket=bucket_name)
except botocore.exceptions.ClientError as no_bucket:
    error_code = no_bucket.response['Error']['Code']
    if error_code == '404':
        exists = False
        print("The bucket name", bucket_name, "does not exists \n Exiting the script")
        sys.exit()


print("Checking if log mode is on or off")
# Check log mode
if log_mode == "True":
    print("Script is running in log mode")
    log_mode = True
elif log_mode == "False":
    print("Script is running in action mode")
    log_mode = False
else:
    print("Log mode is not set to On/Off (True or False in the secret file)\nRunning in Log mode as default")


print("Finished all checks successfully")


# List my regions
try:
    client = boto3.client('ec2', region_name='us-east-1')
    response = client.describe_regions()
    all_regions = [region['RegionName'] for region in response['Regions']]

except ClientError as error:
    print("Getting list of regions failed:", error)
    sys.exit()


# List and check my SG in all regions


for region in all_regions:
    client_region = boto3.client('ec2', region_name=region)

    try:
        response = client_region.describe_security_groups()
        for sg in response['SecurityGroups']:
            for rule in sg['IpPermissions']:
                if any(ip_range.get('CidrIp') == '0.0.0.0/0' for ip_range in rule.get('IpRanges', [])):
                    with open(filename, "a") as logfile:
                        logfile.write("Region: " + region + " The SG: " + sg['GroupName'] + " " + sg['GroupId'] + " has inbound rule from the world\n")
                    if not log_mode:
                        print("Deleting rules", sg['GroupName'], sg['GroupId'], rule)
                        client_region.revoke_security_group_ingress(GroupId=sg['GroupId'], IpPermissions=[rule])

    except ClientError as error_region:
        print("In region", region, "There is an error:",  error_region)


# make file with no duplication
lines = []

with open(filename, 'r') as file:
    for i in file:
        if i not in lines:
            lines.append(i)

with open(filename, 'w') as file:
    for i in lines:
        file.write(i)


# Upload the log file to s3

def upload_file(file_name, bucket, object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client_upload = boto3.client('s3')
    try:
        response_s3 = s3_client_upload.upload_file(file_name, bucket, object_name)
    except ClientError as error_s3:
        print("Error in upload file to s3",  error_s3)
        return False
    return True


upload_file_to_s3 = upload_file(filename, bucket_name)


if upload_file_to_s3:
    print("File", filename, "was uploaded successfully")
else:
    print("File", filename, "failed to upload")

# Delete log file
os.remove(filename)
