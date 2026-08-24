import json
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from adapters.sqs_publisher import SQSPublisher
from domain.entities import AudioFile, TranscriptionRequest


QUEUE_URL = "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/transcription"


@pytest.fixture
def sqs_client():
    return MagicMock()


@pytest.fixture
def publisher(sqs_client):
    return SQSPublisher(queue_url=QUEUE_URL, client=sqs_client)


@pytest.fixture
def transcription_request():
    return TranscriptionRequest(
        audio_file=AudioFile(bucket="audio", key="test.m4a", size=1024),
        requested_at=datetime(2026, 8, 24, 0, 19, 23, tzinfo=timezone.utc),
    )


class TestSQSPublisher:
    def test_calls_send_message(self, publisher, sqs_client, transcription_request):
        publisher.publish(transcription_request)
        sqs_client.send_message.assert_called_once()

    def test_sends_to_correct_queue(self, publisher, sqs_client, transcription_request):
        publisher.publish(transcription_request)
        call_kwargs = sqs_client.send_message.call_args.kwargs
        assert call_kwargs["QueueUrl"] == QUEUE_URL

    def test_message_body_is_valid_json(self, publisher, sqs_client, transcription_request):
        publisher.publish(transcription_request)
        call_kwargs = sqs_client.send_message.call_args.kwargs
        body = json.loads(call_kwargs["MessageBody"])
        assert isinstance(body, dict)

    def test_message_body_contains_domain_fields(
        self, publisher, sqs_client, transcription_request
    ):
        publisher.publish(transcription_request)
        call_kwargs = sqs_client.send_message.call_args.kwargs
        body = json.loads(call_kwargs["MessageBody"])

        assert body["bucket"] == "audio"
        assert body["key"] == "test.m4a"
        assert body["size"] == 1024
        assert "requested_at" in body

    def test_propagates_client_exception(self, publisher, sqs_client, transcription_request):
        sqs_client.send_message.side_effect = RuntimeError("connection error")
        with pytest.raises(RuntimeError, match="connection error"):
            publisher.publish(transcription_request)
