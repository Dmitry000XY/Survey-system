from typing import List
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import BaseModel
from .custom_types import serialpk, str64_idx, str32_idx, timestamp


class Client(BaseModel):
    __tablename__ = "clients"
    __table_args__ = (
        # Проверка: api_key (хэш) должен состоять ровно из 64 символов
        # CheckConstraint("char_length(api_key) = 64", name="ck_clients_api_key_len"),  # TODO
        # Проверка: имя клиента не должно быть пустым
        CheckConstraint("char_length(client_name) >= 1", name="ck_clients_name_nonempty"),
    )

    client_id: Mapped[serialpk]
    client_name: Mapped[str32_idx] = mapped_column(unique=True)
    # api_key – хэш в виде строки длиной 64 символа, с индексом для быстрого поиска
    api_key: Mapped[str64_idx]
    time_created: Mapped[timestamp]

    user_clients: Mapped[List["UserClient"]] = relationship(
        "UserClient", back_populates="client",  # cascade="all, delete-orphan"  # TODO
    )
    questionnaire_answers: Mapped[List["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer", back_populates="client",  # cascade="all, delete-orphan"  # TODO
    )
