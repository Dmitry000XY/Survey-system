from functools import cache

from pydantic import SecretStr
from sqlalchemy import URL

from .base_settings import ProjectSettings


class Settings(ProjectSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: SecretStr
    DB_NAME: str
    ENABLE_DEBUG_API: bool = False

    @property
    def database_url_asyncpg(self) -> URL:
        return self._database_url("postgresql+asyncpg")

    @property
    def database_url_psycopg(self) -> URL:
        return self._database_url("postgresql+psycopg")

    def _database_url(self, drivername: str) -> URL:
        return URL.create(
            drivername=drivername,
            username=self.DB_USER,
            password=self.DB_PASS.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


@cache
def get_settings() -> Settings:
    # noinspection PyArgumentList
    return Settings()
