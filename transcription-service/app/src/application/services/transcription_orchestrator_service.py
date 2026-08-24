from datetime import datetime, timezone

from domain.models.transcript import Transcript
from domain.ports.audio_storage_repository import AudioStorageRepository
from domain.ports.message_queue_repository import MessageQueueRepository
from domain.ports.transcript_repository import TranscriptRepository
from domain.ports.transcription_service import TranscriptionService


class TranscriptionOrchestratorService:
    def __init__(
        self,
        message_queue_repository: MessageQueueRepository,
        audio_storage_repository: AudioStorageRepository,
        transcription_service: TranscriptionService,
        transcript_repository: TranscriptRepository,
        clock=lambda: datetime.now(timezone.utc),
    ):
        self._message_queue_repository = message_queue_repository
        self._audio_storage_repository = audio_storage_repository
        self._transcription_service = transcription_service
        self._transcript_repository = transcript_repository
        self._clock = clock

    def process_pending_messages(self) -> int:
        messages = self._message_queue_repository.receive()
        processed = 0

        for message in messages:
            local_path = self._audio_storage_repository.download(message.audio_file)
            try:
                text = self._transcription_service.transcribe(local_path)
                transcript = Transcript(
                    bucket=message.audio_file.bucket,
                    key=message.audio_file.key,
                    text=text,
                    created_at=self._clock(),
                )
                self._transcript_repository.save(transcript)
                self._message_queue_repository.delete(message)
                processed += 1
            finally:
                self._audio_storage_repository.cleanup(local_path)

        return processed
