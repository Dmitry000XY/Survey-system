from datetime import datetime

from pydantic import BaseModel, ConfigDict, JsonValue

__all__ = ["AnswerBase", "AnswerCreate", "AnswerOut"]


class AnswerBase(BaseModel):
    question_id: int
    questionnaire_answer_id: int
    answer: JsonValue


class AnswerCreate(AnswerBase):
    pass


class AnswerOut(AnswerBase):
    model_config = ConfigDict(from_attributes=True)

    time_created: datetime
