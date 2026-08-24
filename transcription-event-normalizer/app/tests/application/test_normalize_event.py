from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from application.normalize_event import NormalizeTranscriptionEvent
from domain.entities import AudioFile, TranscriptionRequest


@pytest.fixture
def audio_file():
    return AudioFile(bucket="audio", key="test.m4a", size=1024)


@pytest.fixture
def transcription_request(audio_file):
    return TranscriptionRequest(
        audio_file=audio_file,
        requested_at=datetime(2026, 8, 24, tzinfo=timezone.utc),
    )


@pytest.fixture
def parser(transcription_request):
    mock = MagicMock()
    mock.parse.return_value = transcription_request
    return mock


@pytest.fixture
def publisher():
    return MagicMock()


@pytest.fixture
def use_case(parser, publisher):
    return NormalizeTranscriptionEvent(parser=parser, publisher=publisher)


class TestNormalizeTranscriptionEvent:
    def test_calls_parser_with_raw_event(self, use_case, parser):
        raw_event = {"Records": []}
        use_case.execute(raw_event)
        parser.parse.assert_called_once_with(raw_event)

    def test_calls_publisher_with_parsed_request(
        self, use_case, publisher, transcription_request
    ):
        use_case.execute({"Records": []})
        publisher.publish.assert_called_once_with(transcription_request)

    def test_propagates_parser_exception(self, use_case, parser):
        parser.parse.side_effect = ValueError("invalid event")
        with pytest.raises(ValueError, match="invalid event"):
            use_case.execute({})

    def test_propagates_publisher_exception(self, use_case, publisher):
        publisher.publish.side_effect = RuntimeError("sqs error")
        with pytest.raises(RuntimeError, match="sqs error"):
            use_case.execute({})
