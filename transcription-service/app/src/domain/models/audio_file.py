from pydantic import BaseModel, ConfigDict


class AudioFile(BaseModel):
    model_config = ConfigDict(frozen=True)

    bucket: str
    key: str
    size: int
