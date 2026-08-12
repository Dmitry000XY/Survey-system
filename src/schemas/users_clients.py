from pydantic import BaseModel, ConfigDict

__all__ = ["UserClientBase", "UserClientCreate", "UserClientOut"]


class UserClientBase(BaseModel):
    user_id: int
    client_id: int
    user_client_id: int


class UserClientCreate(UserClientBase):
    pass


class UserClientOut(UserClientBase):
    model_config = ConfigDict(from_attributes=True)
