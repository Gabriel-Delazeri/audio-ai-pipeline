from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from domain.models.audio_file import AudioFile
from domain.models.transcription_message import TranscriptionMessage


@pytest.fixture
def audio_file():
    return AudioFile(bucket="audio", key="test.m4a", size=1024)


@pytest.fixture
def requested_at():
    return datetime(2026, 8, 24, 0, 19, 23, tzinfo=timezone.utc)


class TestTranscriptionMessage:
    def test_creation(self, audio_file, requested_at):
        message = TranscriptionMessage(
            audio_file=audio_file, requested_at=requested_at, receipt_handle="handle-1"
        )

        assert message.audio_file == audio_file
        assert message.requested_at == requested_at
        assert message.receipt_handle == "handle-1"

    def test_is_immutable(self, audio_file, requested_at):
        message = TranscriptionMessage(
            audio_file=audio_file, requested_at=requested_at, receipt_handle="handle-1"
        )
        with pytest.raises(ValidationError):
            message.receipt_handle = "other"

    def test_parses_datetime_from_iso_string(self, audio_file):
        message = TranscriptionMessage(
            audio_file=audio_file,
            requested_at="2026-08-24T00:19:23+00:00",
            receipt_handle="handle-1",
        )
        assert message.requested_at == datetime(2026, 8, 24, 0, 19, 23, tzinfo=timezone.utc)
