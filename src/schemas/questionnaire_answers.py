from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.answers import AnswerOut

__all__ = [
    "QuestionnaireAnswerBase",
    "QuestionnaireAnswerCreate",
    "QuestionnaireAnswerOut",
    "QuestionnaireAnswerDetail",
]


class QuestionnaireAnswerBase(BaseModel):
    user_id: int
    questionnaire_id: int
    questionnaire_version: int
    client_id: int


class QuestionnaireAnswerCreate(QuestionnaireAnswerBase):
    time_finished: datetime | None = None


class QuestionnaireAnswerOut(QuestionnaireAnswerBase):
    model_config = ConfigDict(from_attributes=True)

    questionnaire_answer_id: int
    time_started: datetime
    time_finished: datetime | None = None


# Детальная схема с вложенными ответами
class QuestionnaireAnswerDetail(QuestionnaireAnswerOut):
    answers: list[AnswerOut] = Field(default_factory=list)
