from pydantic import BaseModel
from datetime import datetime
from typing import Dict

__all__ = ["AnswerBase", "AnswerCreate", "AnswerOut"]


class AnswerBase(BaseModel):
    question_id: int
    questionnaire_answer_id: int
    answer: Dict  # Явно указываем, что это JSON-структура в виде словаря


class AnswerCreate(AnswerBase):
    pass


class AnswerOut(AnswerBase):
    time_created: datetime

    class Config:
        from_attributes = True
