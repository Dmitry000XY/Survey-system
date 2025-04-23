from sqlalchemy import CheckConstraint, Boolean, Integer, ARRAY, Enum as PGEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import serialpk, intpk, int_notnull, str64_idx, str128_idx, timestamp, QuestionnaireTagEnum
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
    tags: Mapped[list[QuestionnaireTagEnum]] = mapped_column(
        ARRAY(PGEnum(
            QuestionnaireTagEnum,
            name="questionnaire_tag_enum",
            create_type=True
        ), dimensions=1),
        nullable=False,
        server_default="{}"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    questionnaire_hash: Mapped[str128_idx]
    time_created: Mapped[timestamp]

    questionnaire_answers: Mapped[list["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer", back_populates="questionnaire", cascade="all, delete-orphan"
    )
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="questionnaire", cascade="all, delete-orphan", order_by="Question.question_order"
    )
