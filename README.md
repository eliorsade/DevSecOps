# Worldwide Inbound Connection via security groups Check
## Overview
This script will connect to AWS account and check all security groups in all regions for inbound connections from the world (0.0.0.0/0). The script runs in two modes, log mode and action mode.

# Modes
1. Log Mode:
- The script will find security groups with inbound connections from the world.
2. Action Mode:
- The script will run the same as log mode with also deleting the rules allowing inbound connections from the world.
Log File

### In both modes, a log file named log.txt will be created and uploaded to s3 bucket.

## Usage
You have to insert the following prerequisites:

### AWS Credentials:
- access key 
- secret key
  
### S3 Bucket:
- Insert the name of the S3 bucket where the log file will be uploaded.

### Python3 with Boto3:
- Ensure that Python3 is installed on your system along with the Boto3 library.
