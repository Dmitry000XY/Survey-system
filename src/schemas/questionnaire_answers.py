from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from src.schemas.answers import AnswerOut

__all__ = [
    "QuestionnaireAnswerBase",
    "QuestionnaireAnswerCreate",
    "QuestionnaireAnswerOut",
    "QuestionnaireAnswerDetail"
]


class QuestionnaireAnswerBase(BaseModel):
    user_id: int
    questionnaire_id: int
    questionnaire_version: int
    client_id: int


class QuestionnaireAnswerCreate(QuestionnaireAnswerBase):
    time_finished: Optional[datetime] = None


class QuestionnaireAnswerOut(QuestionnaireAnswerBase):
    questionnaire_answer_id: int
    time_started: datetime
    time_finished: Optional[datetime] = None

    class Config:
        from_attributes = True


# Детальная схема с вложенными ответами
class QuestionnaireAnswerDetail(QuestionnaireAnswerOut):
    answers: List[AnswerOut] = []

    class Config:
        from_attributes = True
