import os
from unittest.mock import MagicMock

import pytest

from domain.models.audio_file import AudioFile
from infrastructure.storage.s3_audio_storage_repository import S3AudioStorageRepository


@pytest.fixture
def s3_client():
    return MagicMock()


@pytest.fixture
def repository(s3_client):
    return S3AudioStorageRepository(client=s3_client)


@pytest.fixture
def audio_file():
    return AudioFile(bucket="audio", key="test.m4a", size=1024)


class TestS3AudioStorageRepositoryDownload:
    def test_calls_download_file_with_bucket_and_key(self, repository, s3_client, audio_file):
        local_path = repository.download(audio_file)
        try:
            call_args = s3_client.download_file.call_args.args
            assert call_args[0] == "audio"
            assert call_args[1] == "test.m4a"
        finally:
            repository.cleanup(local_path)

    def test_returns_local_path_with_correct_suffix(self, repository, audio_file):
        local_path = repository.download(audio_file)
        try:
            assert local_path.endswith(".m4a")
        finally:
            repository.cleanup(local_path)

    def test_local_path_is_created_on_disk(self, repository, audio_file):
        local_path = repository.download(audio_file)
        try:
            assert os.path.exists(local_path)
        finally:
            repository.cleanup(local_path)


class TestS3AudioStorageRepositoryCleanup:
    def test_removes_existing_file(self, repository, audio_file):
        local_path = repository.download(audio_file)
        repository.cleanup(local_path)
        assert not os.path.exists(local_path)

    def test_does_not_raise_when_file_missing(self, repository):
        repository.cleanup("/tmp/does-not-exist.m4a")
