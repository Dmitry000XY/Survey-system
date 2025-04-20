from typing import List
from sqlalchemy import CheckConstraint, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import serialpk, intpk, int_notnull, str64_idx, str128_idx, timestamp
from src.configurations.constants import FIXED_HASH_LENGTH


class Questionnaire(BaseModel):
    __tablename__ = "questionnaires"
    __table_args__ = (
        # Проверка: questionnaire_hash должен состоять ровно из FIXED_HASH_LENGTH символов
        CheckConstraint(f"char_length(questionnaire_hash) = {FIXED_HASH_LENGTH}", name="ck_questionnaire_hash_len"),
    )

    questionnaire_id: Mapped[serialpk]
    # Составной ключ – версия анкеты, без автоинкремента
    questionnaire_version: Mapped[intpk] = mapped_column(Integer, primary_key=True, default=1)
    questionnaire_name: Mapped[str64_idx]
    wordpress_id: Mapped[int_notnull]
    # Используем строковый тип с индексом для хэша анкеты
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    questionnaire_hash: Mapped[str128_idx]
    time_created: Mapped[timestamp]

    questionnaire_answers: Mapped[List["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer", back_populates="questionnaire", cascade="all, delete-orphan"
    )
    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="questionnaire", cascade="all, delete-orphan"
    )
