from datetime import datetime, timezone

import pytest

from domain.entities import AudioFile, TranscriptionRequest


@pytest.fixture
def audio_file():
    return AudioFile(bucket="audio", key="test.m4a", size=1024)


@pytest.fixture
def requested_at():
    return datetime(2026, 8, 24, 0, 19, 23, tzinfo=timezone.utc)


@pytest.fixture
def transcription_request(audio_file, requested_at):
    return TranscriptionRequest(audio_file=audio_file, requested_at=requested_at)


class TestAudioFile:
    def test_creation(self, audio_file):
        assert audio_file.bucket == "audio"
        assert audio_file.key == "test.m4a"
        assert audio_file.size == 1024

    def test_is_immutable(self, audio_file):
        with pytest.raises(Exception):
            audio_file.bucket = "other"


class TestTranscriptionRequest:
    def test_creation(self, transcription_request, audio_file, requested_at):
        assert transcription_request.audio_file == audio_file
        assert transcription_request.requested_at == requested_at

    def test_is_immutable(self, transcription_request):
        with pytest.raises(Exception):
            transcription_request.audio_file = None

    def test_to_dict(self, transcription_request):
        result = transcription_request.to_dict()

        assert result["bucket"] == "audio"
        assert result["key"] == "test.m4a"
        assert result["size"] == 1024
        assert result["requested_at"] == "2026-08-24T00:19:23+00:00"

    def test_to_dict_keys(self, transcription_request):
        result = transcription_request.to_dict()
        assert set(result.keys()) == {"bucket", "key", "size", "requested_at"}
