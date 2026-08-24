from abc import ABC, abstractmethod

from domain.entities import TranscriptionRequest


class EventParser(ABC):
    @abstractmethod
    def parse(self, raw_event: dict) -> TranscriptionRequest:
        ...


class MessagePublisher(ABC):
    @abstractmethod
    def publish(self, request: TranscriptionRequest) -> None:
        ...
