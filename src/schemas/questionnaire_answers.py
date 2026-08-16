from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from src.schemas.answers import AnswerOut

__all__ = [
    "QuestionnaireAnswerBase",
    "QuestionnaireAnswerCreate",
    "QuestionnaireAnswerOut",
    "QuestionnaireAnswerDetail",
    "QuestionnaireAnswerUpdate",
]


class QuestionnaireAnswerBase(BaseModel):
    user_id: PositiveInt
    questionnaire_id: PositiveInt
    questionnaire_version: PositiveInt
    client_id: PositiveInt


class QuestionnaireAnswerCreate(QuestionnaireAnswerBase):
    time_finished: datetime | None = None


class QuestionnaireAnswerUpdate(BaseModel):
    time_finished: datetime | None = None


class QuestionnaireAnswerOut(QuestionnaireAnswerBase):
    model_config = ConfigDict(from_attributes=True)

    questionnaire_answer_id: int
    time_started: datetime
    time_finished: datetime | None = None


class QuestionnaireAnswerDetail(QuestionnaireAnswerOut):
    answers: list[AnswerOut] = Field(default_factory=list)
