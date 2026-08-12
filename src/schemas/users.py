from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.configurations.constants import MIN_LOGIN_LENGTH, MAX_LOGIN_LENGTH, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH

__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserOut"]


class UserBase(BaseModel):
    login: str = Field(min_length=MIN_LOGIN_LENGTH, max_length=MAX_LOGIN_LENGTH)


class UserCreate(UserBase):
    user_id: int
    password: str = Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)


class UserUpdate(BaseModel):
    login: str | None = Field(None, min_length=MIN_LOGIN_LENGTH, max_length=MAX_LOGIN_LENGTH)
    password: str | None = Field(None, min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    time_created: datetime
    time_updated: datetime
