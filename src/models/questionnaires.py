from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Boolean, CheckConstraint, Enum as PGEnum, Index, Integer, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import identitypk, int_notnull, timestamp
from src.configurations.constants import QUESTIONNAIRE_HASH_LENGTH, QuestionnaireTagEnum

if TYPE_CHECKING:
    from .questionnaire_answers import QuestionnaireAnswer
    from .questions import Question


class Questionnaire(BaseModel):
    __tablename__ = "questionnaires"
    __table_args__ = (
        CheckConstraint("questionnaire_version > 0", name="ck_questionnaires_version_positive"),
        CheckConstraint("wordpress_id > 0", name="ck_questionnaires_wordpress_id_positive"),
        CheckConstraint(
            f"char_length(questionnaire_hash) = {QUESTIONNAIRE_HASH_LENGTH}",
            name="ck_questionnaires_hash_length",
        ),
        UniqueConstraint(
            "questionnaire_id",
            "questionnaire_hash",
            name="uq_questionnaires_id_hash",
        ),
        UniqueConstraint(
            "wordpress_id",
            "questionnaire_version",
            name="uq_questionnaires_wordpress_version",
        ),
        Index("ix_questionnaires_wordpress_id", "wordpress_id"),
        Index(
            "uq_questionnaires_one_active_version",
            "questionnaire_id",
            unique=True,
            postgresql_where=text("is_active"),
        ),
    )

    questionnaire_id: Mapped[identitypk]
    questionnaire_version: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        default=1,
        server_default=text("1"),
    )
    questionnaire_name: Mapped[str] = mapped_column(String(255), nullable=False)
    wordpress_id: Mapped[int_notnull]
    tags: Mapped[list[QuestionnaireTagEnum]] = mapped_column(
        ARRAY(
            PGEnum(
                QuestionnaireTagEnum,
                name="questionnaire_tag_enum",
                create_type=True,
                values_callable=lambda enum: [item.value for item in enum],
            ),
            dimensions=1,
        ),
        nullable=False,
        default=list,
        server_default=text("'{}'::questionnaire_tag_enum[]"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
    questionnaire_hash: Mapped[str] = mapped_column(String(QUESTIONNAIRE_HASH_LENGTH), nullable=False)
    time_created: Mapped[timestamp]

    questionnaire_answers: Mapped[list["QuestionnaireAnswer"]] = relationship(
        "QuestionnaireAnswer",
        back_populates="questionnaire",
        passive_deletes=True,
    )
    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="questionnaire",
        cascade="all, delete-orphan",
        order_by="Question.question_order",
        passive_deletes=True,
    )
