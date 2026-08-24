from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from domain.models.transcript import Transcript
from domain.ports.transcript_repository import TranscriptRepository
from infrastructure.persistence.orm_models import Base, TranscriptModel


class SQLAlchemyTranscriptRepository(TranscriptRepository):
    def __init__(self, session_factory: sessionmaker, engine: Engine):
        self._session_factory = session_factory
        self._engine = engine

    def ensure_schema(self) -> None:
        Base.metadata.create_all(self._engine)

    def save(self, transcript: Transcript) -> None:
        with self._session_factory() as session:
            session.add(
                TranscriptModel(
                    bucket=transcript.bucket,
                    key=transcript.key,
                    text=transcript.text,
                    created_at=transcript.created_at,
                )
            )
            session.commit()
