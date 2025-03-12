from typing import List
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import serialpk, int_notnull, timestamp, timestamp_nullable


class QuestionnaireAnswer(BaseModel):
    __tablename__ = "questionnaire_answers"

    questionnaire_answer_id: Mapped[serialpk]
    user_id: Mapped[int_notnull] = mapped_column(ForeignKey("users.user_id"))
    questionnaire_id: Mapped[int_notnull]
    questionnaire_version: Mapped[int_notnull]
    client_id: Mapped[int_notnull] = mapped_column(ForeignKey("clients.client_id"))
    time_started: Mapped[timestamp]
    time_finished: Mapped[timestamp_nullable]

    __table_args__ = (
        # Составной внешний ключ для связи с таблицей questionnaires
        ForeignKeyConstraint(
            ["questionnaire_id", "questionnaire_version"],
            ["questionnaires.questionnaire_id", "questionnaires.questionnaire_version"]
        ),
    )

    user: Mapped["User"] = relationship("User", back_populates="questionnaire_answers")
    client: Mapped["Client"] = relationship("Client", back_populates="questionnaire_answers")
    questionnaire: Mapped["Questionnaire"] = relationship("Questionnaire", back_populates="questionnaire_answers")
    answers: Mapped[List["Answer"]] = relationship(
        "Answer", back_populates="questionnaire_answer",  # cascade="all, delete-orphan"  # TODO
    )
