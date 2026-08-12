from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, ForeignKeyConstraint, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import bigint_notnull, identitypk, int_notnull, timestamp, timestamp_nullable

if TYPE_CHECKING:
    from .answers import Answer
    from .clients import Client
    from .questionnaires import Questionnaire
    from .users import User


class QuestionnaireAnswer(BaseModel):
    __tablename__ = "questionnaire_answers"

    questionnaire_answer_id: Mapped[identitypk]
    user_id: Mapped[bigint_notnull] = mapped_column(ForeignKey("users.user_id", ondelete="RESTRICT"))
    questionnaire_id: Mapped[int_notnull]
    questionnaire_version: Mapped[int] = mapped_column(Integer, nullable=False)
    client_id: Mapped[int_notnull] = mapped_column(ForeignKey("clients.client_id", ondelete="RESTRICT"))
    time_started: Mapped[timestamp]
    time_finished: Mapped[timestamp_nullable]

    __table_args__ = (
        ForeignKeyConstraint(
            ["questionnaire_id", "questionnaire_version"],
            ["questionnaires.questionnaire_id", "questionnaires.questionnaire_version"],
            name="fk_questionnaire_answers_questionnaire",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "time_finished IS NULL OR time_finished >= time_started",
            name="ck_questionnaire_answers_time_order",
        ),
        Index("ix_questionnaire_answers_user_id", "user_id"),
        Index("ix_questionnaire_answers_client_id", "client_id"),
        Index(
            "ix_questionnaire_answers_questionnaire_version",
            "questionnaire_id",
            "questionnaire_version",
        ),
    )

    user: Mapped["User"] = relationship("User", back_populates="questionnaire_answers")
    client: Mapped["Client"] = relationship("Client", back_populates="questionnaire_answers")
    questionnaire: Mapped["Questionnaire"] = relationship("Questionnaire", back_populates="questionnaire_answers")
    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="questionnaire_answer",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
