# Worldwide Inbound Connection via security groups Check
## Overview
This script will connect to AWS account and check all security groups in all regions for inbound connections from the world (0.0.0.0/0). The script runs in two modes, log mode and action mode.

## Modes
1. Log Mode:
- The script will find security groups with inbound connections from the world.
2. Action Mode:
- The script will find security group rules with inbound connections from the world and delete them.

#### In both modes, a log file named log.txt will be created and uploaded to s3 bucket.

## Usage
To execute the script, type the command:  
```bash 
python3 main.py
```

The script will automatticly connect to AWS account usign the credentials from GitHub Secrets.
It will check for all security groups in all regions.

### prerequisites

#### Python3 with Boto3:
- Python 3.10
- Boto3
- botocore
- 
### GitHub Secrets:

#### AWS Credentials:
- Access key 
- Secret key

#### DockerHub Credentials:
- Username
- Password
  
#### S3 Bucket:
- Insert the name of the S3 bucket where the log file will be uploaded.

#### AWS Authorization:
- List regions
- List SG in all regions
- List buckets
- Upload to S3
- Delete SG rules in all regions

#### GitHub Secrets:
- AWS_ACCESS_KEY_ID - AWS Access key 
- AWS_SECRET_ACCESS_KEY - AWS Secret key
- AWS_S3_BUCKET_NAME - S3 bucket name
- DOCKERHUB_USERNAME - DockerHub Username
- DOCKERHUB_PASSWORD - DockerHub Password
- LOG_MODE - True or False
