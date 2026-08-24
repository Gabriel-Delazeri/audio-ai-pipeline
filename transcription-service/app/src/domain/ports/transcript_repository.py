from abc import ABC, abstractmethod

from domain.models.transcript import Transcript


class TranscriptRepository(ABC):
    @abstractmethod
    def ensure_schema(self) -> None:
        ...

    @abstractmethod
    def save(self, transcript: Transcript) -> None:
        ...
