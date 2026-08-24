import os
import time

from application.services.transcription_orchestrator_service import TranscriptionOrchestratorService
from infrastructure.messaging.sqs_message_queue_repository import SQSMessageQueueRepository
from infrastructure.persistence.database import create_default_engine, create_session_factory
from infrastructure.persistence.sqlalchemy_transcript_repository import SQLAlchemyTranscriptRepository
from infrastructure.storage.s3_audio_storage_repository import S3AudioStorageRepository
from infrastructure.transcription.whisper_transcription_service import WhisperTranscriptionService

POLL_INTERVAL_SECONDS = 5


def build_dependencies():
    queue_url = os.environ["TRANSCRIPTION_QUEUE_URL"]

    engine = create_default_engine()
    session_factory = create_session_factory(engine)

    message_queue_repository = SQSMessageQueueRepository(queue_url=queue_url)
    audio_storage_repository = S3AudioStorageRepository()
    transcription_service = WhisperTranscriptionService(model_name=os.environ.get("WHISPER_MODEL", "base"))
    transcript_repository = SQLAlchemyTranscriptRepository(session_factory=session_factory, engine=engine)

    return message_queue_repository, audio_storage_repository, transcription_service, transcript_repository


def build_orchestrator_service() -> TranscriptionOrchestratorService:
    message_queue_repository, audio_storage_repository, transcription_service, transcript_repository = (
        build_dependencies()
    )
    return TranscriptionOrchestratorService(
        message_queue_repository=message_queue_repository,
        audio_storage_repository=audio_storage_repository,
        transcription_service=transcription_service,
        transcript_repository=transcript_repository,
    )


def run_once(orchestrator_service: TranscriptionOrchestratorService) -> int:
    return orchestrator_service.process_pending_messages()


def run_forever() -> None:  # pragma: no cover
    message_queue_repository, audio_storage_repository, transcription_service, transcript_repository = (
        build_dependencies()
    )
    transcript_repository.ensure_schema()

    orchestrator_service = TranscriptionOrchestratorService(
        message_queue_repository=message_queue_repository,
        audio_storage_repository=audio_storage_repository,
        transcription_service=transcription_service,
        transcript_repository=transcript_repository,
    )

    while True:
        processed = run_once(orchestrator_service)
        if processed == 0:
            time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":  # pragma: no cover
    run_forever()
