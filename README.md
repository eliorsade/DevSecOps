# Worldwide Inbound Connection via SG Check
## Overview
This script is designed to connect to your AWS account and check all Security Groups (SG) in all regions for inbound connections from the world (0.0.0.0/0). The script runs in two modes, log mode and action mode.

# Modes
1. Log Mode:
- In this mode, the script will identify Security Groups with inbound connections from the world and log their names.
2. Action Mode:
- In action mode, the script goes a step further by not only identifying but also deleting the rules allowing inbound connections from the world. The script will then log the Security Group names.
Log File

- In both modes, a log file named log.txt will be generated and uploaded to the specified AWS S3 bucket. This log file contains information about the Security Groups and their inbound connections.

## Usage
You have to insert the following prerequisites:

### AWS Credentials:
- access key 
- secret key
  
### S3 Bucket:
- Insert the name of the S3 bucket where the log file will be uploaded.

### Python3 with Boto3:
- Ensure that Python3 is installed on your system along with the Boto3 library.
