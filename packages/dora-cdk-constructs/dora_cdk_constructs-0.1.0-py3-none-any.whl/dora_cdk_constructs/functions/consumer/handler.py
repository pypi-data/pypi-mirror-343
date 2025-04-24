"""This module contains the handler function for the consumer SQS Lambda function."""
from datetime import datetime
from logging import getLogger
from json import loads
from typing import Iterator
from os import environ

from boto3 import client

SQS = client('sqs')
LOG = getLogger(__name__)
SQS_MAX_MESSAGES = int(environ.get('SQS_MAX_MESSAGES', '10'))
SQS_VISIBILITY = int(environ.get('SQS_VISIBILITY', '5'))

def get_queue_url(uri: str) -> str:
    """Retrieve the SQS queue URL from a given ARN.

    Args:
        uri (str): The ARN of the SQS queue.

    Returns:
        str: The URL of the SQS queue.
    """
    _parts = uri.split(':', maxsplit=-1)
    LOG.debug("Queue: %s", _parts[-1])
    return SQS.get_queue_url(
        QueueName=_parts[-1],
        QueueOwnerAWSAccountId=_parts[-2]).get('QueueUrl')

def get_sqs_messages(url: str) -> Iterator[dict]:
    """Retrieve messages from an SQS queue.

    Args:
        url (str): The URL of the SQS queue.

    Yields:
        Iterator[S3Notification]: An iterator of S3Notification objects.
    """
    _response = SQS.receive_message(
        QueueUrl=url,
        MaxNumberOfMessages=SQS_MAX_MESSAGES,
        AttributeNames=['All'],
        VisibilityTimeout=SQS_VISIBILITY*60,
        MessageAttributeNames=['All'],
    )
    for _message in _response.get('Messages',[]):
        _body = loads(_message['Body'])
        _bkt = _body['detail']['bucket']['name']
        _key = _body['detail']['object']['key']
        _src = _body.get('source','').split('.')[-1]
        yield (f"{_src}://{_bkt}/{_key}", dict(
            size=int(_body['detail']['object'].get('size',0)),
            time=_body.get('time', datetime.now().isoformat()),
        ))
        SQS.delete_message(
            QueueUrl=url,
            ReceiptHandle=_message['ReceiptHandle'])

def run(event, context):
    """Lambda handler function."""
    LOG.debug("Context: %s", context)
    url = get_queue_url(event['uri'])
    LOG.debug("url: %s", url)
    response = dict()
    for _src, _msg in get_sqs_messages(url):
        response[_src] = _msg
    return response
