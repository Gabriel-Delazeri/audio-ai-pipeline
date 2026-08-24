from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from domain.models.transcript import Transcript
from infrastructure.persistence.sqlalchemy_transcript_repository import SQLAlchemyTranscriptRepository


@pytest.fixture
def session():
    return MagicMock()


@pytest.fixture
def session_factory(session):
    factory = MagicMock()
    factory.return_value.__enter__.return_value = session
    return factory


@pytest.fixture
def engine():
    return MagicMock()


@pytest.fixture
def repository(session_factory, engine):
    return SQLAlchemyTranscriptRepository(session_factory=session_factory, engine=engine)


@pytest.fixture
def transcript():
    return Transcript(
        bucket="audio",
        key="test.m4a",
        text="hello world",
        created_at=datetime(2026, 8, 24, tzinfo=timezone.utc),
    )


class TestSQLAlchemyTranscriptRepositoryEnsureSchema:
    def test_calls_create_all_with_engine(self, repository, engine):
        with patch("infrastructure.persistence.sqlalchemy_transcript_repository.Base") as base_mock:
            repository.ensure_schema()
            base_mock.metadata.create_all.assert_called_once_with(engine)


class TestSQLAlchemyTranscriptRepositorySave:
    def test_adds_transcript_model_to_session(self, repository, session, transcript):
        repository.save(transcript)

        added = session.add.call_args.args[0]
        assert added.bucket == "audio"
        assert added.key == "test.m4a"
        assert added.text == "hello world"
        assert added.created_at == transcript.created_at

    def test_commits_session_after_save(self, repository, session, transcript):
        repository.save(transcript)
        session.commit.assert_called_once()
