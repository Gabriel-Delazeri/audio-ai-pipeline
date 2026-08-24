import json
import os
from datetime import datetime

import boto3

from domain.models.audio_file import AudioFile
from domain.models.transcription_message import TranscriptionMessage
from domain.ports.message_queue_repository import MessageQueueRepository


class SQSMessageQueueRepository(MessageQueueRepository):
    def __init__(self, queue_url: str, client=None, max_messages: int = 10, wait_time_seconds: int = 10):
        self._queue_url = queue_url
        self._client = client or boto3.client("sqs", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))
        self._max_messages = max_messages
        self._wait_time_seconds = wait_time_seconds

    def receive(self) -> list[TranscriptionMessage]:
        response = self._client.receive_message(
            QueueUrl=self._queue_url,
            MaxNumberOfMessages=self._max_messages,
            WaitTimeSeconds=self._wait_time_seconds,
        )

        messages = []
        for raw in response.get("Messages", []):
            body = json.loads(raw["Body"])
            messages.append(
                TranscriptionMessage(
                    audio_file=AudioFile(bucket=body["bucket"], key=body["key"], size=body["size"]),
                    requested_at=datetime.fromisoformat(body["requested_at"]),
                    receipt_handle=raw["ReceiptHandle"],
                )
            )

        return messages

    def delete(self, message: TranscriptionMessage) -> None:
        self._client.delete_message(
            QueueUrl=self._queue_url,
            ReceiptHandle=message.receipt_handle,
        )
