from pydantic import BaseModel

__all__ = ["UserClientBase", "UserClientCreate", "UserClientOut"]


class UserClientBase(BaseModel):
    user_id: int
    client_id: int
    user_client_id: int


class UserClientCreate(UserClientBase):
    pass


class UserClientOut(UserClientBase):
    class Config:
        from_attributes = True
