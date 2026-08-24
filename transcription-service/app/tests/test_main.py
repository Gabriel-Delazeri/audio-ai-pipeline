from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("TRANSCRIPTION_QUEUE_URL", "queue-url")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "postgres")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_NAME", "transcriptions")


class TestBuildDependencies:
    def test_builds_all_four_components(self):
        with patch("main.create_default_engine") as engine_fn, patch(
            "main.create_session_factory"
        ) as session_factory_fn, patch("main.SQSMessageQueueRepository") as consumer_cls, patch(
            "main.S3AudioStorageRepository"
        ) as storage_cls, patch("main.WhisperTranscriptionService") as transcription_cls, patch(
            "main.SQLAlchemyTranscriptRepository"
        ) as repo_cls:
            import main

            deps = main.build_dependencies()

            consumer_cls.assert_called_once_with(queue_url="queue-url")
            storage_cls.assert_called_once_with()
            transcription_cls.assert_called_once_with(model_name="base")
            repo_cls.assert_called_once_with(
                session_factory=session_factory_fn.return_value, engine=engine_fn.return_value
            )

            assert deps == (
                consumer_cls.return_value,
                storage_cls.return_value,
                transcription_cls.return_value,
                repo_cls.return_value,
            )

    def test_uses_whisper_model_from_env(self, monkeypatch):
        monkeypatch.setenv("WHISPER_MODEL", "large")
        with patch("main.create_default_engine"), patch("main.create_session_factory"), patch(
            "main.SQSMessageQueueRepository"
        ), patch("main.S3AudioStorageRepository"), patch(
            "main.WhisperTranscriptionService"
        ) as transcription_cls, patch("main.SQLAlchemyTranscriptRepository"):
            import main

            main.build_dependencies()
            transcription_cls.assert_called_once_with(model_name="large")


class TestBuildOrchestratorService:
    def test_builds_service_from_dependencies(self):
        mocks = (MagicMock(), MagicMock(), MagicMock(), MagicMock())
        with patch("main.build_dependencies", return_value=mocks):
            import main

            orchestrator_service = main.build_orchestrator_service()

            assert orchestrator_service._message_queue_repository is mocks[0]
            assert orchestrator_service._audio_storage_repository is mocks[1]
            assert orchestrator_service._transcription_service is mocks[2]
            assert orchestrator_service._transcript_repository is mocks[3]


class TestRunOnce:
    def test_executes_orchestrator_service_and_returns_result(self):
        import main

        orchestrator_service = MagicMock()
        orchestrator_service.process_pending_messages.return_value = 3

        result = main.run_once(orchestrator_service)

        orchestrator_service.process_pending_messages.assert_called_once()
        assert result == 3
