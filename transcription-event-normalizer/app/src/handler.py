import json
import os

from adapters.s3_event_parser import S3EventParser
from adapters.sqs_publisher import SQSPublisher
from application.normalize_event import NormalizeTranscriptionEvent


def _build_use_case() -> NormalizeTranscriptionEvent:
    queue_url = os.environ["TRANSCRIPTION_QUEUE_URL"]
    return NormalizeTranscriptionEvent(
        parser=S3EventParser(),
        publisher=SQSPublisher(queue_url=queue_url),
    )


def handler(event, context):
    use_case = _build_use_case()
    for record in event["Records"]:
        s3_event = json.loads(record["body"])
        if "Event" in s3_event and s3_event["Event"] == "s3:TestEvent":
            continue
        use_case.execute(s3_event)
