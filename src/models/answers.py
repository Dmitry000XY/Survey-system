from typing import TYPE_CHECKING

from pydantic import JsonValue
from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import intpk, timestamp

if TYPE_CHECKING:
    from .questionnaire_answers import QuestionnaireAnswer
    from .questions import Question


class Answer(BaseModel):
    __tablename__ = "answers"
    __table_args__ = (Index("ix_answers_questionnaire_answer_id", "questionnaire_answer_id"),)

    question_id: Mapped[intpk] = mapped_column(ForeignKey("questions.question_id", ondelete="RESTRICT"))
    questionnaire_answer_id: Mapped[intpk] = mapped_column(
        ForeignKey("questionnaire_answers.questionnaire_answer_id", ondelete="CASCADE")
    )
    answer: Mapped[JsonValue] = mapped_column(JSONB, nullable=False)
    time_created: Mapped[timestamp]

    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="answers_list",
    )
    questionnaire_answer: Mapped["QuestionnaireAnswer"] = relationship(
        "QuestionnaireAnswer",
        back_populates="answers",
    )
