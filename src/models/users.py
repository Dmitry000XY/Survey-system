from typing import List
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import intpk, str32_idx, str64, timestamp, timestamp_onupdate_nullable


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = (
        # Проверка: пароль (хэш) должен состоять ровно из 64 символов (например, SHA256 в hex)
        # CheckConstraint("char_length(password) = 64", name="ck_users_password_len"),  # TODO
        # Проверка: логин должен быть не короче 3 символов
        CheckConstraint("char_length(login) >= 3", name="ck_users_login_min_length"),
    )

    # Идентификатор без автоинкремента
    user_id: Mapped[intpk]
    login: Mapped[str32_idx] = mapped_column(unique=True)
    password: Mapped[str64]  # хэш пароля в виде строки длиной 64 символа
    time_updated: Mapped[timestamp_onupdate_nullable]
    time_created: Mapped[timestamp]

    # Связи
    user_clients: Mapped[List["UserClient"]] = relationship(
        "UserClient", back_populates="user",  # cascade="all, delete-orphan"  # TODO
    )
    questionnaire_answers: Mapped[List["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer", back_populates="user",  # cascade="all, delete-orphan"  # TODO
    )
