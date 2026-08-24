from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AudioFile:
    bucket: str
    key: str
    size: int


@dataclass(frozen=True)
class TranscriptionRequest:
    audio_file: AudioFile
    requested_at: datetime

    def to_dict(self) -> dict:
        return {
            "bucket": self.audio_file.bucket,
            "key": self.audio_file.key,
            "size": self.audio_file.size,
            "requested_at": self.requested_at.isoformat(),
        }
