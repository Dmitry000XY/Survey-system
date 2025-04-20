from sqlalchemy import Integer, Text, JSON, ARRAY, String, ForeignKeyConstraint, CheckConstraint, Enum as PGEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_types import serialpk, int_notnull, timestamp, AnswerTypeEnum


class Question(BaseModel):
    __tablename__ = "questions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["questionnaire_id", "questionnaire_version"],
            ["questionnaires.questionnaire_id", "questionnaires.questionnaire_version"]
        ),
        # Проверяем, что значение ключа "show_hide" принадлежит допустимым значениям
        CheckConstraint(
            "(dependencies->>'show_hide') IN ('SHOW', 'HIDE')",
            name="ck_q_dependencies_show_hide"
        ),
        # Проверяем, что значение ключа "all_any" принадлежит допустимым значениям
        CheckConstraint(
            "(dependencies->>'all_any') IN ('ALL', 'ANY')",
            name="ck_q_dependencies_all_any"
        ),
        # Дополнительные проверки для структуры conditions можно добавить при необходимости
    )

    question_id: Mapped[serialpk]
    questionnaire_id: Mapped[int_notnull]
    questionnaire_version: Mapped[int_notnull]
    question: Mapped[str] = mapped_column(Text, nullable=False)
    question_order: Mapped[int_notnull]
    answers: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=list)
    answer_type: Mapped[AnswerTypeEnum] = mapped_column(PGEnum(AnswerTypeEnum, name="answer_type_enum"), nullable=False)
    dependencies: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    wordpress_id: Mapped[int] = mapped_column(Integer, nullable=True)
    time_created: Mapped[timestamp]

    questionnaire: Mapped["Questionnaire"] = relationship("Questionnaire", back_populates="questions")
    answers_list: Mapped[list["Answer"]] = relationship("Answer", back_populates="question")
