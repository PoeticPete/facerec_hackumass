# A test python script for publishing to the easy lock topic
# Make sure the aws environment is setup before running
# Use aws configure to setup the environment


import json
import boto3

arn = "arn:aws:sns:us-east-1:361762219447:easy_lock"
message = {"foo": "bar"}
client = boto3.client('sns')
response = client.publish(
    TargetArn=arn,
    Message=json.dumps({
    'default': json.dumps(message),
    'key1': 'a',
    'key2': 'b',
    'key3': 'c'
    }),
    MessageStructure='json'
)
