from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum as PGEnum, ForeignKeyConstraint, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import JsonValue
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import identitypk, int_notnull, timestamp
from src.configurations.constants import AnswerTypeEnum

if TYPE_CHECKING:
    from .answers import Answer
    from .questionnaires import Questionnaire


class Question(BaseModel):
    __tablename__ = "questions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["questionnaire_id", "questionnaire_version"],
            ["questionnaires.questionnaire_id", "questionnaires.questionnaire_version"],
            name="fk_questions_questionnaire",
            ondelete="CASCADE",
        ),
        UniqueConstraint(
            "questionnaire_id",
            "questionnaire_version",
            "question_order",
            name="uq_questions_version_order",
        ),
        UniqueConstraint(
            "questionnaire_id",
            "questionnaire_version",
            "wordpress_id",
            name="uq_questions_version_wordpress_id",
        ),
        CheckConstraint("question_order >= 0", name="ck_questions_order_nonnegative"),
        CheckConstraint("wordpress_id > 0", name="ck_questions_wordpress_id_positive"),
        CheckConstraint("jsonb_typeof(answer_options) = 'array'", name="ck_questions_answer_options_array"),
        CheckConstraint("jsonb_typeof(dependencies) = 'object'", name="ck_questions_dependencies_object"),
        CheckConstraint(
            "dependencies ? 'show_hide' AND (dependencies->>'show_hide') IN ('SHOW', 'HIDE')",
            name="ck_questions_dependencies_show_hide",
        ),
        CheckConstraint(
            "dependencies ? 'all_any' AND (dependencies->>'all_any') IN ('ALL', 'ANY')",
            name="ck_questions_dependencies_all_any",
        ),
    )

    question_id: Mapped[identitypk]
    questionnaire_id: Mapped[int_notnull]
    questionnaire_version: Mapped[int] = mapped_column(Integer, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_order: Mapped[int] = mapped_column(Integer, nullable=False)
    answer_options: Mapped[list[dict[str, JsonValue]]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    answer_type: Mapped[AnswerTypeEnum] = mapped_column(PGEnum(AnswerTypeEnum, name="answer_type_enum"), nullable=False)
    dependencies: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: {"show_hide": "SHOW", "all_any": "ALL", "conditions": []},
        server_default=text('\'{"show_hide": "SHOW", "all_any": "ALL", "conditions": []}\'::jsonb'),
    )
    wordpress_id: Mapped[int_notnull]
    time_created: Mapped[timestamp]

    questionnaire: Mapped["Questionnaire"] = relationship("Questionnaire", back_populates="questions")
    answers_list: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        passive_deletes=True,
    )
