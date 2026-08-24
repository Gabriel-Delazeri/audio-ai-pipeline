import json
import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from domain.entities import AudioFile, TranscriptionRequest

QUEUE_URL = "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/transcription"

S3_EVENT = {
    "Records": [
        {
            "eventTime": "2026-08-24T00:19:23.334Z",
            "s3": {
                "bucket": {"name": "audio"},
                "object": {"key": "test.m4a", "size": 1024},
            },
        }
    ]
}

SQS_EVENT = {
    "Records": [
        {"body": json.dumps(S3_EVENT)},
    ]
}


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("TRANSCRIPTION_QUEUE_URL", QUEUE_URL)


class TestHandler:
    def test_processes_single_record(self):
        mock_client = MagicMock()
        with patch("adapters.sqs_publisher.boto3.client", return_value=mock_client):
            from handler import handler
            handler(SQS_EVENT, None)
        mock_client.send_message.assert_called_once()

    def test_processes_multiple_records(self):
        mock_client = MagicMock()
        event = {"Records": [{"body": json.dumps(S3_EVENT)}, {"body": json.dumps(S3_EVENT)}]}
        with patch("adapters.sqs_publisher.boto3.client", return_value=mock_client):
            from handler import handler
            handler(event, None)
        assert mock_client.send_message.call_count == 2

    def test_published_message_has_correct_fields(self):
        mock_client = MagicMock()
        with patch("adapters.sqs_publisher.boto3.client", return_value=mock_client):
            from handler import handler
            handler(SQS_EVENT, None)

        call_kwargs = mock_client.send_message.call_args.kwargs
        body = json.loads(call_kwargs["MessageBody"])

        assert body["bucket"] == "audio"
        assert body["key"] == "test.m4a"
        assert body["size"] == 1024
        assert "requested_at" in body
