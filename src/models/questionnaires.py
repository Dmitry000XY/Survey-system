from typing import List
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel
from .custom_types import serialpk, intpk, int_notnull, str64_idx, timestamp


class Questionnaire(BaseModel):
    __tablename__ = "questionnaires"
    __table_args__ = (
        # Проверка: questionnaire_hash должен состоять ровно из 64 символов
        CheckConstraint("char_length(questionnaire_hash) = 64", name="ck_questionnaire_hash_len"),
    )

    questionnaire_id: Mapped[serialpk]
    # Составной ключ – версия анкеты, без автоинкремента
    questionnaire_version: Mapped[intpk]
    questionnaire_name: Mapped[str64_idx]
    wordpress_id: Mapped[int_notnull]
    # Используем строковый тип с индексом для хэша анкеты
    questionnaire_hash: Mapped[str64_idx]
    time_created: Mapped[timestamp]

    questionnaire_answers: Mapped[List["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer", back_populates="questionnaire", cascade="all, delete-orphan"
    )
    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="questionnaire", cascade="all, delete-orphan"
    )
