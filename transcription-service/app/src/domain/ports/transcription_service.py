from abc import ABC, abstractmethod


class TranscriptionService(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> str:
        ...
