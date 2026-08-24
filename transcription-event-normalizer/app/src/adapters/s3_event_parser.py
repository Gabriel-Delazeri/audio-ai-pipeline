from datetime import datetime, timezone
from urllib.parse import unquote_plus

from domain.entities import AudioFile, TranscriptionRequest
from domain.ports import EventParser


class S3EventParser(EventParser):
    def parse(self, raw_event: dict) -> TranscriptionRequest:
        record = raw_event["Records"][0]
        s3 = record["s3"]

        event_time = datetime.fromisoformat(
            record["eventTime"].replace("Z", "+00:00")
        )

        audio_file = AudioFile(
            bucket=s3["bucket"]["name"],
            key=unquote_plus(s3["object"]["key"]),
            size=s3["object"]["size"],
        )

        return TranscriptionRequest(audio_file=audio_file, requested_at=event_time)
