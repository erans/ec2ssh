#!/usr/bin/env python

__version__ = "0.1"

import os
import sys
import subprocess

try:
	import argparse
except ImportError:
	print "ERROR: You are running Python 2.6 or below, please install 'argparse' using 'pip install argparse' or 'easy_install argparse'"
	sys.exit(2)

try:
	import boto
	import boto.ec2
except ImportError:
	print "ERROR: you must install boto. Try 'pip install boto' or 'easy_install boto'"
	sys.exit(2)

def get_instance_ip(args):
	region = None

	regions = boto.ec2.regions()
	for r in regions:
		if r.name == args.region:
			region = r
			break

	if not region:
		print "ERROR: Invalid region '%s'" % args.region
		sys.exit(3)

	conn = boto.ec2.connect_to_region(region.name, aws_access_key_id=args.aws_access_key_id, aws_secret_access_key=args.aws_secret_access_key)

	instance = None

	reservations = conn.get_all_instances()
	instances = [i for r in reservations for i in r.instances]

	for i in instances:
		for t in i.tags:
			if t == u"Name" and i.tags[t] == args.instance_name:
				instance = i
				break

	if not instance:
		print "ERROR: Cannot find an instance in region: '%s' with name: '%s'" % (region.name, args.instance_name)
		sys.exit(4)

	return instance.ip_address

def run(args):
	ip = get_instance_ip(args)

	print "Connecting to %s@%s" % (args.user, ip)
	cmd_args = ["ssh", "-i", args.key_file, "%s@%s" % (args.user, ip)]
	p = subprocess.call(cmd_args)

def main():
	parser = argparse.ArgumentParser(description='SSH into an EC2 instance via its Name tag')
	parser.add_argument('instance_name', help='The instance name')
	parser.add_argument('-k', '--aws_access_key_id', help='Your access key Id (can also be set via AWS_ACCESS_KEY_ID environment variable)', default=None)
	parser.add_argument('-s', '--aws_secret_access_key', help="Your secret access key (can be set via AWS_SECRET_ACCESS_KEY environment variable)", default=None)
	parser.add_argument('-f', '--key_file', help='Path to the EC2 certificate file (can be set via EC2_INSTANCE_KEY_FILE environment variable)', default=None)
	parser.add_argument('-u', '--user', help="User name to login with (default: ubuntu)", default="ubuntu")
	parser.add_argument('-r', '--region', help="The region as specified in AWS API (default: us-east-1)", default="us-east-1")

	args = parser.parse_args()
	if args.aws_access_key_id is None and args.aws_secret_access_key is None:
		env_AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
		env_AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
		if not (env_AWS_ACCESS_KEY_ID and env_AWS_SECRET_ACCESS_KEY):
			print "ERROR: Missing AWS_ACCESS_KEY_ID parameter. Set it via command line or via the AWS_ACCESS_KEY_ID envrionment variable."
			print "ERROR: Missing AWS_SECRET_ACCESS_KEY parameter. Set it via command line or via the AWS_SECRET_ACCESS_KEY envrionment variable."
			sys.exit(2)
		else:
			args.aws_access_key_id = env_AWS_ACCESS_KEY_ID
			args.aws_secret_access_key = env_AWS_SECRET_ACCESS_KEY

	if args.key_file is None:
		env_EC2_INSTANCE_KEY_FILE = os.getenv("EC2_INSTANCE_KEY_FILE")
		if not (env_EC2_INSTANCE_KEY_FILE):
			print "ERROR: --key_file argument or EC2_INSTANCE_KEY_FILE envrionment variable are not set"
			sys.exit(2)
		else:
			args.key_file = env_EC2_INSTANCE_KEY_FILE

	run(args)

if __name__ == "__main__":
	main()
