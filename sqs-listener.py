import boto3
import json
import os
from subprocess import call


class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

# Create SQS client
sqs = boto3.client('sqs', region_name="us-east-1")

queue_url = 'https://sqs.us-east-1.amazonaws.com/692685737698/twitch-google-home.fifo'

# Enable long polling on an existing SQS queue
sqs.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={'ReceiveMessageWaitTimeSeconds': '20'}
)

# Long poll for message on provided SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    WaitTimeSeconds=20
)

data = response.get('Messages')[0].get('Body')
p = Payload(data)
print(p.action)
print(p.payload)

command = "livestreamer --yes-run-as-root --http-header=Client-ID=fcbmhjqkely7kwcq4fg09btmhr907e --player-passthrough=http,hls,rtmp --player=\"python /stream2chromecast/stream2chromecast.py -devicename 192.168.1.158 -playurl\" twitch.tv/%s best" %(p.payload)

os.system(command)
