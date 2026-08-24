import pytest
from pydantic import ValidationError

from domain.models.audio_file import AudioFile


class TestAudioFile:
    def test_creation(self):
        audio_file = AudioFile(bucket="audio", key="test.m4a", size=1024)

        assert audio_file.bucket == "audio"
        assert audio_file.key == "test.m4a"
        assert audio_file.size == 1024

    def test_is_immutable(self):
        audio_file = AudioFile(bucket="audio", key="test.m4a", size=1024)
        with pytest.raises(ValidationError):
            audio_file.bucket = "other"

    def test_raises_when_size_is_not_an_integer(self):
        with pytest.raises(ValidationError):
            AudioFile(bucket="audio", key="test.m4a", size="not-a-number")

    def test_raises_when_required_field_missing(self):
        with pytest.raises(ValidationError):
            AudioFile(bucket="audio", key="test.m4a")
