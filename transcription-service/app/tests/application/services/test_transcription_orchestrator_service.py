from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from application.services.transcription_orchestrator_service import TranscriptionOrchestratorService
from domain.models.audio_file import AudioFile
from domain.models.transcription_message import TranscriptionMessage

FIXED_NOW = datetime(2026, 8, 24, tzinfo=timezone.utc)


@pytest.fixture
def audio_file():
    return AudioFile(bucket="audio", key="test.m4a", size=1024)


@pytest.fixture
def message(audio_file):
    return TranscriptionMessage(audio_file=audio_file, requested_at=FIXED_NOW, receipt_handle="handle-1")


@pytest.fixture
def message_queue_repository(message):
    mock = MagicMock()
    mock.receive.return_value = [message]
    return mock


@pytest.fixture
def audio_storage_repository():
    mock = MagicMock()
    mock.download.return_value = "/tmp/test.m4a"
    return mock


@pytest.fixture
def transcription_service():
    mock = MagicMock()
    mock.transcribe.return_value = "hello world"
    return mock


@pytest.fixture
def transcript_repository():
    return MagicMock()


@pytest.fixture
def orchestrator_service(
    message_queue_repository, audio_storage_repository, transcription_service, transcript_repository
):
    return TranscriptionOrchestratorService(
        message_queue_repository=message_queue_repository,
        audio_storage_repository=audio_storage_repository,
        transcription_service=transcription_service,
        transcript_repository=transcript_repository,
        clock=lambda: FIXED_NOW,
    )


class TestTranscriptionOrchestratorService:
    def test_receives_messages_from_queue(self, orchestrator_service, message_queue_repository):
        orchestrator_service.process_pending_messages()
        message_queue_repository.receive.assert_called_once()

    def test_downloads_audio_for_each_message(self, orchestrator_service, audio_storage_repository, audio_file):
        orchestrator_service.process_pending_messages()
        audio_storage_repository.download.assert_called_once_with(audio_file)

    def test_transcribes_downloaded_audio(self, orchestrator_service, transcription_service):
        orchestrator_service.process_pending_messages()
        transcription_service.transcribe.assert_called_once_with("/tmp/test.m4a")

    def test_saves_transcript_with_domain_fields(self, orchestrator_service, transcript_repository):
        orchestrator_service.process_pending_messages()
        saved = transcript_repository.save.call_args.args[0]

        assert saved.bucket == "audio"
        assert saved.key == "test.m4a"
        assert saved.text == "hello world"
        assert saved.created_at == FIXED_NOW

    def test_deletes_message_after_success(self, orchestrator_service, message_queue_repository, message):
        orchestrator_service.process_pending_messages()
        message_queue_repository.delete.assert_called_once_with(message)

    def test_cleans_up_local_file(self, orchestrator_service, audio_storage_repository):
        orchestrator_service.process_pending_messages()
        audio_storage_repository.cleanup.assert_called_once_with("/tmp/test.m4a")

    def test_returns_number_of_processed_messages(self, orchestrator_service):
        assert orchestrator_service.process_pending_messages() == 1

    def test_returns_zero_when_no_messages(self, orchestrator_service, message_queue_repository):
        message_queue_repository.receive.return_value = []
        assert orchestrator_service.process_pending_messages() == 0

    def test_cleans_up_even_when_transcription_fails(
        self, orchestrator_service, audio_storage_repository, transcription_service
    ):
        transcription_service.transcribe.side_effect = RuntimeError("whisper error")

        with pytest.raises(RuntimeError, match="whisper error"):
            orchestrator_service.process_pending_messages()

        audio_storage_repository.cleanup.assert_called_once_with("/tmp/test.m4a")

    def test_does_not_delete_message_when_save_fails(
        self, orchestrator_service, transcript_repository, message_queue_repository
    ):
        transcript_repository.save.side_effect = RuntimeError("db error")

        with pytest.raises(RuntimeError, match="db error"):
            orchestrator_service.process_pending_messages()

        message_queue_repository.delete.assert_not_called()

    def test_processes_multiple_messages(
        self, orchestrator_service, message_queue_repository, audio_storage_repository, audio_file
    ):
        other_message = TranscriptionMessage(
            audio_file=AudioFile(bucket="audio", key="other.m4a", size=2048),
            requested_at=FIXED_NOW,
            receipt_handle="handle-2",
        )
        message_queue_repository.receive.return_value = [
            TranscriptionMessage(audio_file=audio_file, requested_at=FIXED_NOW, receipt_handle="handle-1"),
            other_message,
        ]

        processed = orchestrator_service.process_pending_messages()

        assert processed == 2
        assert audio_storage_repository.download.call_count == 2
