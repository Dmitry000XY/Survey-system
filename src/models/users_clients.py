from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import intpk, int_notnull


class UserClient(BaseModel):
    __tablename__ = "users_clients"

    user_id: Mapped[intpk] = mapped_column(ForeignKey("users.user_id"))
    client_id: Mapped[intpk] = mapped_column(ForeignKey("clients.client_id"))
    user_client_id: Mapped[int_notnull]

    user: Mapped["User"] = relationship("User", back_populates="user_clients")
    client: Mapped["Client"] = relationship("Client", back_populates="user_clients")
