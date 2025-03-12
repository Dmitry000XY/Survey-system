from pydantic import BaseModel
from datetime import datetime
from typing import Dict

__all__ = ["QuestionBase", "QuestionCreate", "QuestionOut"]


class QuestionBase(BaseModel):
    questionnaire_id: int
    questionnaire_version: int
    question: str
    question_order: int
    answers: Dict  # JSON-структура с вариантами ответов
    dependencies: Dict  # JSON-структура с зависимостями
    wordpress_id: int | None = None


class QuestionCreate(QuestionBase):
    pass


class QuestionOut(QuestionBase):
    question_id: int
    time_created: datetime

    class Config:
        from_attributes = True
