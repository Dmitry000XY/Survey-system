from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, SecretStr

from src.configurations.constants import (
    MAX_LOGIN_LENGTH,
    MAX_PASSWORD_HASH_LENGTH,
    MIN_LOGIN_LENGTH,
    MIN_PASSWORD_HASH_LENGTH,
)

__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserOut"]


class UserBase(BaseModel):
    login: str = Field(min_length=MIN_LOGIN_LENGTH, max_length=MAX_LOGIN_LENGTH)


class UserCreate(UserBase):
    """Persistence command whose password must already be WordPress-compatible hashed data."""

    user_id: PositiveInt
    password_hash: SecretStr = Field(
        min_length=MIN_PASSWORD_HASH_LENGTH,
        max_length=MAX_PASSWORD_HASH_LENGTH,
    )


class UserUpdate(BaseModel):
    """Persistence update; a supplied password must already be hashed."""

    login: str | None = Field(None, min_length=MIN_LOGIN_LENGTH, max_length=MAX_LOGIN_LENGTH)
    password_hash: SecretStr | None = Field(
        None,
        min_length=MIN_PASSWORD_HASH_LENGTH,
        max_length=MAX_PASSWORD_HASH_LENGTH,
    )


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    time_created: datetime
    time_updated: datetime
