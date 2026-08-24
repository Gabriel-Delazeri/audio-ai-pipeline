from datetime import datetime

from pydantic import BaseModel, ConfigDict

from domain.models.audio_file import AudioFile


class TranscriptionMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    audio_file: AudioFile
    requested_at: datetime
    receipt_handle: str
