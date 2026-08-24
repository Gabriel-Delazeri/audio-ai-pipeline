from unittest.mock import MagicMock

import pytest

from infrastructure.transcription.whisper_transcription_service import WhisperTranscriptionService


@pytest.fixture
def model():
    mock = MagicMock()
    mock.transcribe.return_value = {"text": "  hello world  "}
    return mock


@pytest.fixture
def service(model):
    return WhisperTranscriptionService(model=model)


class TestWhisperTranscriptionService:
    def test_calls_model_transcribe_with_audio_path(self, service, model):
        service.transcribe("/tmp/audio.m4a")
        model.transcribe.assert_called_once_with("/tmp/audio.m4a")

    def test_returns_stripped_text(self, service):
        result = service.transcribe("/tmp/audio.m4a")
        assert result == "hello world"

    def test_reuses_injected_model_across_calls(self, service, model):
        service.transcribe("/tmp/audio.m4a")
        service.transcribe("/tmp/audio.m4a")
        assert model.transcribe.call_count == 2
