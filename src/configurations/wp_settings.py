from pydantic_settings import BaseSettings, SettingsConfigDict


class WPSettings(BaseSettings):
    WP_DB_HOST: str
    WP_DB_PORT: int
    WP_DB_USER: str
    WP_DB_PASS: str
    WP_DB_NAME: str
    ECHO: bool = True  # TODO

    @property
    def database_url_asyncmy(self) -> str:
        return f"mysql+asyncmy://{self.WP_DB_USER}:{self.WP_DB_PASS}@{self.WP_DB_HOST}:{self.WP_DB_PORT}/{self.WP_DB_NAME}"

    @property
    def database_url_mysqldb(self) -> str:
        return f"mysql+mysqldb://{self.WP_DB_USER}:{self.WP_DB_PASS}@{self.WP_DB_HOST}:{self.WP_DB_PORT}/{self.WP_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')


wp_settings = WPSettings()
