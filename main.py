import boto3
import botocore
from botocore.exceptions import ClientError
import os
import sys


all_sg = []
sg = ''
filename = 'log.txt'
bucket_in_s3 = ''

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
while True:
    if log_mode == 'Y' or log_mode == 'y':
        log_mode = True
        print("Script is running in log mode")
        break
    elif log_mode == 'N' or log_mode == 'n':
        log_mode = False
        print("Script is running in action mode")
        break
    else:
        print("Log mode is not set to On/Off (Y/y or N/n in the secret file) \n Exiting the script")
        sys.exit()

print("Finished checking successfully")


# List my regions
try:
    client = boto3.client('ec2')
    response = client.describe_regions()
    all_regions = [region['RegionName'] for region in response['Regions']]

except ClientError as error:
    print("Getting list of regions failed:", error)
    sys.exit()

# Checks for SG if it has inbound from 0.0.0.0/0


def inbound_from_world(sg_check):
    for i in sg_check['IpPermissions']:
        for o in i.get('IpRanges', []):
            if o.get('CidrIp') == '0.0.0.0/0':
                return True
    return False

# List and check my SG in all regions


for region in all_regions:
    client_region = boto3.client('ec2', region_name=region)

    try:
        response = client_region.describe_security_groups()
        for sg in response['SecurityGroups']:
            has_inbound = inbound_from_world(sg)
            if has_inbound:
                print("Group ID:", sg['GroupId'])
            for rule in sg['IpPermissions']:
                if any(ip_range.get('CidrIp') == '0.0.0.0/0' for ip_range in rule.get('IpRanges', [])):
                    print(rule)
                    # Write to the log file an SG that was found
                    with open(filename, "a") as logfile:
                        logfile.write("The SG: " + sg['GroupName'] + " " + sg['GroupId'] + " has inbound rule from the world\n")
                    if not log_mode:
                        print("Deleting rules")
#                       Deleting the inbound rules
#                       client.revoke_security_group_ingress(
#                        GroupId=sg['GroupId'],
#                        IpPermissions=[rule]
#                    )

    except ClientError as error_region:
        print("In region", region, "There is an error:",  error_region)


# Upload the log file to s3

def upload_file(file_name, bucket, object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    try:
        response_s3 = s3_client.upload_file(file_name, bucket, object_name)
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
