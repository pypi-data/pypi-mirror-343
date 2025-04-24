"""Evaluators for AWS sensors."""

from datetime import datetime
from json import loads
from typing import Optional, Iterator
from uuid import uuid4

from boto3 import client
from dagster import (
    DynamicPartitionsDefinition,
    SensorEvaluationContext,
    AssetMaterialization,
    SensorResult,
    SkipReason,
    RunRequest,
    Config,
)
from dora_core.utils import logger
from dora_aws.utils import s3_bucket_key

MAX_NUMBER_OF_MESSAGES = 10

log = logger(__name__)
sqs = client('sqs')
s3c = client('s3')

class S3Notification(Config):
    """Represents a notification for an S3 object.

    Attributes:
        file (str): The S3 file path.
        etag (Optional[str]): The entity tag of the S3 object.
        size (Optional[int]): The size of the S3 object in bytes.
        time (Optional[str]): The last modified time of the S3 object.
    """
    file: str
    etag: Optional[str]
    size: Optional[int]
    time: Optional[str]

def get_queue_url(url: str) -> str:
    """Retrieve the SQS queue URL from a given ARN.

    Args:
        url (str): The ARN of the SQS queue.

    Returns:
        str: The URL of the SQS queue.
    """
    _parts = url.split(':', maxsplit=-1)
    log.debug("Queue: %s", _parts[-1])
    return sqs.get_queue_url(
        QueueName=_parts[-1],
        QueueOwnerAWSAccountId=_parts[-2]).get('QueueUrl')

def get_s3_files(s3_path: str) -> Iterator[S3Notification]:
    """Retrieve a list of files from an S3 bucket.

    Args:
        s3_path (str): The S3 path to list files from.

    Yields:
        Iterator[S3Notification]: An iterator of S3Notification objects.
    """
    try:
        _bkt, _key = s3_bucket_key(s3_path)
        _key = "/".join(_key.split('/')[:-1])
        paginator = s3c.get_paginator('list_objects_v2')
        for response in paginator.paginate(Bucket=_bkt, Prefix=_key, FetchOwner=False):
            for content in response.get('Contents',dict()):
                _size = int(content.get('Size',0))
                _time = content.get('LastModified',datetime.now()).isoformat(
                    timespec='seconds')
                if _size > 0:
                    yield S3Notification(
                        file=f"s3://{_bkt}/{content.get('Key')}",
                        etag=content.get('ETag'),
                        size=_size,
                        time=_time)
    except AttributeError as _err:
        log.error("Cant get files for '%s': %s",s3_path, _err)

def get_sqs_messages(url: str) -> Iterator[S3Notification]:
    """Retrieve messages from an SQS queue.

    Args:
        url (str): The URL of the SQS queue.

    Yields:
        Iterator[S3Notification]: An iterator of S3Notification objects.
    """
    _response = sqs.receive_message(
        QueueUrl=url,
        MaxNumberOfMessages=MAX_NUMBER_OF_MESSAGES,
        AttributeNames=['All'],
        VisibilityTimeout=20,
        MessageAttributeNames=['All'],
    )
    for _message in _response.get('Messages',[]):
        _body = loads(_message['Body'])
        _bkt = _body['detail']['bucket']['name']
        _key = _body['detail']['object']['key']
        _src = _body.get('source','').split('.')[-1]
        yield S3Notification(
            file=f"{_src}://{_bkt}/{_key}",
            etag=_body['detail']['object'].get('etag',str(uuid4())),
            size=_body['detail']['object'].get('size',0),
            time=_body.get('time',''))
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=_message['ReceiptHandle'])

def queue_sensor_eval(context: SensorEvaluationContext):
    """Evaluate the sensor based on messages in the queue.

    Args:
        context (SensorEvaluationContext): The context of the sensor evaluation.

    Returns:
        SensorResult: The result of the sensor evaluation, including run requests and dynamic partitions requests.
        SkipReason: If no new files are found, a reason to skip the sensor evaluation.
    """
    _meta = context.repository_def.get_sensor_def(context.sensor_name).metadata
    _notifications = get_sqs_messages(_meta.get('sqs').text)
    _all_files = [f"{notif.time}|{notif.file}" for notif in _notifications]

    latest_tracked_file = context.cursor
    if latest_tracked_file is None:
        new_files = _all_files
    else:
        new_files = [file for file in _all_files if file > latest_tracked_file]
    # else:
    #     # If there is no cursor, we will assume that we have not seen any files yet
    #     _all_files = get_s3_files(s3_path=_meta.get('uri').text)
    #     new_files = [f"{notif.time}|{notif.file}" for notif in _all_files]
    # Sort the new files so we can easily pick the latest one
    new_files.sort()
    # If there are new files, we will launch a run for the latest one
    if len(new_files) > 0:
        # Update status of external assets
        context.instance.report_runless_asset_event(AssetMaterialization(_meta.get('volume').text))
        partitions_to_add = new_files
        context.log.debug(f"Requesting to add partitions: {len(partitions_to_add)}")
        # We only launch a run for the latest release, to avoid unexpected large numbers of runs the
        # first time the sensor turns on. This means that you might need to manually backfill
        # earlier releases.
        return SensorResult(
            run_requests=[
                RunRequest(partition_key=new_files[-1])
                ],
            cursor=new_files[-1],
            dynamic_partitions_requests=[
                DynamicPartitionsDefinition(name=_meta.get('target').text)
                .build_add_request(partitions_to_add)
            ],
        )
    # If there are no new releases, we return a SkipReason
    else:
        return SkipReason("No new releases")
