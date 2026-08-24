from domain.ports import EventParser, MessagePublisher


class NormalizeTranscriptionEvent:
    def __init__(self, parser: EventParser, publisher: MessagePublisher):
        self._parser = parser
        self._publisher = publisher

    def execute(self, raw_event: dict) -> None:
        request = self._parser.parse(raw_event)
        self._publisher.publish(request)
