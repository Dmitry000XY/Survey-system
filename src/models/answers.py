from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import intpk, timestamp


class Answer(BaseModel):
    __tablename__ = "answers"

    question_id: Mapped[intpk] = mapped_column(ForeignKey("questions.question_id"))
    questionnaire_answer_id: Mapped[intpk] = mapped_column(
        ForeignKey("questionnaire_answers.questionnaire_answer_id")
    )
    # Поле answer имеет тип JSON для хранения структурированного ответа
    answer: Mapped[dict] = mapped_column(JSON, nullable=False)
    time_created: Mapped[timestamp]

    question: Mapped["Question"] = relationship("Question", back_populates="answers_list")
    questionnaire_answer: Mapped["QuestionnaireAnswer"] = relationship("QuestionnaireAnswer", back_populates="answers")
