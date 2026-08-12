from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import bigintpk, str60, timestamp, timestamp_onupdate

if TYPE_CHECKING:
    from .questionnaire_answers import QuestionnaireAnswer
    from .users_clients import UserClient


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("char_length(login) >= 3", name="ck_users_login_min_length"),)

    # The primary key is the corresponding WordPress user ID.
    user_id: Mapped[bigintpk]
    login: Mapped[str60] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    time_updated: Mapped[timestamp_onupdate]
    time_created: Mapped[timestamp]

    # Связи
    user_clients: Mapped[list["UserClient"]] = relationship(
        "UserClient",
        back_populates="user",
        passive_deletes=True,
    )
    questionnaire_answers: Mapped[list["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer",
        back_populates="user",
        passive_deletes=True,
    )
