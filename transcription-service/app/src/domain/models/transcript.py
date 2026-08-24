from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Transcript(BaseModel):
    model_config = ConfigDict(frozen=True)

    bucket: str
    key: str
    text: str
    created_at: datetime
