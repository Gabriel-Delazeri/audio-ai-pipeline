import json

import boto3

from domain.entities import TranscriptionRequest
from domain.ports import MessagePublisher


class SQSPublisher(MessagePublisher):
    def __init__(self, queue_url: str, client=None):
        self._queue_url = queue_url
        self._client = client or boto3.client("sqs")

    def publish(self, request: TranscriptionRequest) -> None:
        self._client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=json.dumps(request.to_dict()),
        )
