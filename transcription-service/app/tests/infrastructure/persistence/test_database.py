import pytest

from infrastructure.persistence.database import build_database_url, create_session_factory


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "postgres")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_NAME", "transcriptions")


class TestBuildDatabaseUrl:
    def test_builds_url_with_default_port(self):
        url = build_database_url()
        assert url == "postgresql+psycopg2://postgres:postgres@localhost:5432/transcriptions"

    def test_builds_url_with_custom_port(self, monkeypatch):
        monkeypatch.setenv("DB_PORT", "6543")
        url = build_database_url()
        assert url == "postgresql+psycopg2://postgres:postgres@localhost:6543/transcriptions"


class TestCreateSessionFactory:
    def test_returns_sessionmaker_bound_to_engine(self):
        from sqlalchemy import create_engine

        engine = create_engine("sqlite:///:memory:")
        factory = create_session_factory(engine)

        assert factory.kw["bind"] is engine
