from abc import ABC, abstractmethod

from domain.models.transcription_message import TranscriptionMessage


class MessageQueueRepository(ABC):
    @abstractmethod
    def receive(self) -> list[TranscriptionMessage]:
        ...

    @abstractmethod
    def delete(self, message: TranscriptionMessage) -> None:
        ...
