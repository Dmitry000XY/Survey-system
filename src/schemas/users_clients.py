from pydantic import BaseModel, ConfigDict, PositiveInt

__all__ = ["UserClientBase", "UserClientCreate", "UserClientOut"]


class UserClientBase(BaseModel):
    user_id: PositiveInt
    client_id: PositiveInt
    user_client_id: PositiveInt


class UserClientCreate(UserClientBase):
    pass


class UserClientOut(UserClientBase):
    model_config = ConfigDict(from_attributes=True)
