import boto3

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

print(response.Body)
