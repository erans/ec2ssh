ec2ssh.py - quicker SSH access to your instances
================================================

ec2ssh.py uses EC2's Name tag on instances to make it easier for you to connect to an instance using its name instead of ID or figuring out its public ip.


Usage
=====

usage: ec2ssh.py [-h] [-k AWS_ACCESS_KEY_ID] [-s AWS_SECRET_ACCESS_KEY]
                 [-f KEY_FILE] [-u USER] [-r REGION]
                 instance_name

SSH into an EC2 instance via its Name tag

positional arguments:
  instance_name         The instance name

optional arguments:
  -h, --help            show this help message and exit
  -k AWS_ACCESS_KEY_ID, --aws_access_key_id AWS_ACCESS_KEY_ID
                        Your access key Id (can also be set via
                        AWS_ACCESS_KEY_ID environment variable)
  -s AWS_SECRET_ACCESS_KEY, --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                        Your secret access key (can be set via
                        AWS_SECRET_ACCESS_KEY environment variable)
  -f KEY_FILE, --key_file KEY_FILE
                        Path to the EC2 certificate file (can be set via
                        EC2_INSTANCE_KEY_FILE environment variable)
  -u USER, --user USER  User name to login with (default: ubuntu)
  -r REGION, --region REGION
                        The region as specified in AWS API (default: us-
                        east-1)

