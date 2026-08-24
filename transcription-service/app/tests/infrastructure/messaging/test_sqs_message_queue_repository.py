import json
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from domain.models.transcription_message import TranscriptionMessage
from infrastructure.messaging.sqs_message_queue_repository import SQSMessageQueueRepository

QUEUE_URL = "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/transcription"


@pytest.fixture
def sqs_client():
    return MagicMock()


@pytest.fixture
def repository(sqs_client):
    return SQSMessageQueueRepository(queue_url=QUEUE_URL, client=sqs_client)


@pytest.fixture
def raw_message():
    body = {
        "bucket": "audio",
        "key": "test.m4a",
        "size": 1024,
        "requested_at": "2026-08-24T00:19:23+00:00",
    }
    return {"Body": json.dumps(body), "ReceiptHandle": "receipt-1"}


class TestSQSMessageQueueRepositoryReceive:
    def test_calls_receive_message_with_queue_url(self, repository, sqs_client):
        sqs_client.receive_message.return_value = {"Messages": []}
        repository.receive()
        call_kwargs = sqs_client.receive_message.call_args.kwargs
        assert call_kwargs["QueueUrl"] == QUEUE_URL

    def test_returns_empty_list_when_no_messages(self, repository, sqs_client):
        sqs_client.receive_message.return_value = {}
        assert repository.receive() == []

    def test_parses_message_into_domain_object(self, repository, sqs_client, raw_message):
        sqs_client.receive_message.return_value = {"Messages": [raw_message]}

        messages = repository.receive()

        assert len(messages) == 1
        message = messages[0]
        assert isinstance(message, TranscriptionMessage)
        assert message.audio_file.bucket == "audio"
        assert message.audio_file.key == "test.m4a"
        assert message.audio_file.size == 1024
        assert message.receipt_handle == "receipt-1"

    def test_parses_requested_at_as_datetime(self, repository, sqs_client, raw_message):
        sqs_client.receive_message.return_value = {"Messages": [raw_message]}
        message = repository.receive()[0]
        assert message.requested_at == datetime(2026, 8, 24, 0, 19, 23, tzinfo=timezone.utc)

    def test_parses_multiple_messages(self, repository, sqs_client, raw_message):
        sqs_client.receive_message.return_value = {"Messages": [raw_message, raw_message]}
        messages = repository.receive()
        assert len(messages) == 2


class TestSQSMessageQueueRepositoryDelete:
    def test_calls_delete_message_with_receipt_handle(self, repository, sqs_client, raw_message):
        sqs_client.receive_message.return_value = {"Messages": [raw_message]}
        message = repository.receive()[0]

        repository.delete(message)

        sqs_client.delete_message.assert_called_once_with(QueueUrl=QUEUE_URL, ReceiptHandle="receipt-1")
