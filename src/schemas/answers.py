from datetime import datetime

from pydantic import BaseModel, ConfigDict, JsonValue, PositiveInt

__all__ = ["AnswerBase", "AnswerCreate", "AnswerOut", "AnswerUpdate"]


class AnswerBase(BaseModel):
    question_id: PositiveInt
    questionnaire_answer_id: PositiveInt
    answer: JsonValue


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(BaseModel):
    answer: JsonValue


class AnswerOut(AnswerBase):
    model_config = ConfigDict(from_attributes=True)

    time_created: datetime
