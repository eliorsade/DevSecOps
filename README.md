# Worldwide Inbound Connection via security groups Check
## Overview
This script will connect to AWS account and check all security groups in all regions for inbound connections from the world (0.0.0.0/0). The script runs in two modes, log mode and action mode.

## Modes
1. Log Mode:
- The script will find security groups with inbound connections from the world.
2. Action Mode:
- The script will run the same as log mode with also deleting the rules allowing inbound connections from the world.
Log File

#### In both modes, a log file named log.txt will be created and uploaded to s3 bucket.

## Usage
You have to insert the following prerequisites in GitHub Secrets:

### AWS Credentials:
- Access key 
- Secret key

### DockerHub Credentials:
- Username
- Password
  
### S3 Bucket:
- Insert the name of the S3 bucket where the log file will be uploaded.

### AWS Authorization:
- List regions
- List SG in all regions
- List buckets
- Upload to S3
- Delete SG rules in all regions

### Python3 with Boto3:
- Ensure that Python3 is installed on your system along with the Boto3 library.

### GitHub Secrets:
AWS_ACCESS_KEY_ID - AWS Access key 
AWS_SECRET_ACCESS_KEY - AWS Secret key
AWS_S3_BUCKET_NAME - S3 bucket name
DOCKERHUB_USERNAME - DockerHub Username
DOCKERHUB_PASSWORD - DockerHub Password
LOG_MODE - Y/N | y/n 
