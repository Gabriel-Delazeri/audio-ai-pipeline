from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from domain.models.transcript import Transcript


@pytest.fixture
def created_at():
    return datetime(2026, 8, 24, tzinfo=timezone.utc)


class TestTranscript:
    def test_creation(self, created_at):
        transcript = Transcript(bucket="audio", key="test.m4a", text="hello world", created_at=created_at)

        assert transcript.bucket == "audio"
        assert transcript.key == "test.m4a"
        assert transcript.text == "hello world"
        assert transcript.created_at == created_at

    def test_is_immutable(self, created_at):
        transcript = Transcript(bucket="audio", key="test.m4a", text="hello world", created_at=created_at)
        with pytest.raises(ValidationError):
            transcript.text = "other"
