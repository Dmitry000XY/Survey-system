from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import BaseModel
from .custom_types import identitypk, str64, timestamp

if TYPE_CHECKING:
    from .questionnaire_answers import QuestionnaireAnswer
    from .users_clients import UserClient


class Client(BaseModel):
    __tablename__ = "clients"
    __table_args__ = (
        CheckConstraint("char_length(client_name) >= 1", name="ck_clients_name_nonempty"),
        CheckConstraint("char_length(api_key_hash) = 64", name="ck_clients_api_key_hash_length"),
    )

    client_id: Mapped[identitypk]
    client_name: Mapped[str64] = mapped_column(unique=True)
    api_key_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    time_created: Mapped[timestamp]

    user_clients: Mapped[list["UserClient"]] = relationship(
        "UserClient",
        back_populates="client",
        passive_deletes=True,
    )
    questionnaire_answers: Mapped[list["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer",
        back_populates="client",
        passive_deletes=True,
    )
