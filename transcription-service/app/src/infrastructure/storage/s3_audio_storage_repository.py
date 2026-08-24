import os
import tempfile

import boto3

from domain.models.audio_file import AudioFile
from domain.ports.audio_storage_repository import AudioStorageRepository


class S3AudioStorageRepository(AudioStorageRepository):
    def __init__(self, client=None):
        self._client = client or boto3.client("s3", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))

    def download(self, audio_file: AudioFile) -> str:
        suffix = os.path.splitext(audio_file.key)[1]
        fd, local_path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        self._client.download_file(audio_file.bucket, audio_file.key, local_path)
        return local_path

    def cleanup(self, local_path: str) -> None:
        if os.path.exists(local_path):
            os.remove(local_path)
