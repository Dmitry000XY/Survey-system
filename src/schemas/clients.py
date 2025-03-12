from pydantic import BaseModel, Field
from datetime import datetime
from src.configurations.constants import MIN_CLIENT_NAME_LENGTH, MAX_CLIENT_NAME_LENGTH

__all__ = ["ClientBase", "ClientCreate", "ClientUpdate", "ClientOut", "ClientInDB", "ClientOutWithAPI"]


class ClientBase(BaseModel):
    client_name: str = Field(..., min_length=MIN_CLIENT_NAME_LENGTH, max_length=MAX_CLIENT_NAME_LENGTH)


# Schema for creating client: user provides only the client name.
class ClientCreate(ClientBase):
    pass


# Internal schema for repository: includes the generated API key.
class ClientInDB(ClientBase):
    api_key: str


# Schema for updating client: API key cannot be changed.
class ClientUpdate(BaseModel):
    client_name: str | None = Field(None, min_length=MIN_CLIENT_NAME_LENGTH, max_length=MAX_CLIENT_NAME_LENGTH)


# Schema for outgoing data: API key is not returned.
class ClientOut(ClientBase):
    client_id: int
    time_created: datetime

    class Config:
        from_attributes = True


# Schema for outgoing data when creating client: includes the generated API key.
class ClientOutWithAPI(ClientOut):
    api_key: str
