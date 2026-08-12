from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import bigint_notnull, bigintpk, intpk

if TYPE_CHECKING:
    from .clients import Client
    from .users import User


class UserClient(BaseModel):
    __tablename__ = "users_clients"
    __table_args__ = (UniqueConstraint("client_id", "user_client_id", name="uq_users_clients_external_identity"),)

    user_id: Mapped[bigintpk] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    client_id: Mapped[intpk] = mapped_column(ForeignKey("clients.client_id", ondelete="CASCADE"))
    user_client_id: Mapped[bigint_notnull]

    user: Mapped["User"] = relationship("User", back_populates="user_clients")
    client: Mapped["Client"] = relationship("Client", back_populates="user_clients")
