from functools import cache

from pydantic import SecretStr
from sqlalchemy import URL

from .base_settings import ProjectSettings


class WPSettings(ProjectSettings):
    WP_DB_HOST: str
    WP_DB_PORT: int
    WP_DB_USER: str
    WP_DB_PASS: SecretStr
    WP_DB_NAME: str

    @property
    def database_url_asyncmy(self) -> URL:
        return URL.create(
            drivername="mysql+asyncmy",
            username=self.WP_DB_USER,
            password=self.WP_DB_PASS.get_secret_value(),
            host=self.WP_DB_HOST,
            port=self.WP_DB_PORT,
            database=self.WP_DB_NAME,
        )


@cache
def get_wp_settings() -> WPSettings:
    # noinspection PyArgumentList
    return WPSettings()
