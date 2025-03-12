from typing import List
from sqlalchemy import Integer, Text, JSON, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import serialpk, int_notnull, timestamp


class Question(BaseModel):
    __tablename__ = "questions"

    question_id: Mapped[serialpk]
    questionnaire_id: Mapped[int_notnull]
    questionnaire_version: Mapped[int_notnull]
    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_order: Mapped[int_notnull]
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)  # Возможные ответы в формате JSON
    dependencies: Mapped[dict] = mapped_column(JSON, nullable=False)  # Зависимости между вопросами в формате JSON
    wordpress_id: Mapped[int] = mapped_column(Integer, nullable=True)
    time_created: Mapped[timestamp]

    __table_args__ = (
        ForeignKeyConstraint(
            ["questionnaire_id", "questionnaire_version"],
            ["questionnaires.questionnaire_id", "questionnaires.questionnaire_version"]
        ),
    )

    questionnaire: Mapped["Questionnaire"] = relationship("Questionnaire", back_populates="questions")
    answers_list: Mapped[List["Answer"]] = relationship("Answer", back_populates="question")
