from abc import ABC, abstractmethod

from domain.models.audio_file import AudioFile


class AudioStorageRepository(ABC):
    @abstractmethod
    def download(self, audio_file: AudioFile) -> str:
        ...

    @abstractmethod
    def cleanup(self, local_path: str) -> None:
        ...
