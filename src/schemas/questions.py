from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from src.configurations.constants import AnswerTypeEnum
from src.schemas.dependencies import Dependencies

__all__ = ["AnswerOption", "QuestionBase", "QuestionCreate", "QuestionUpdate", "QuestionOut"]


class AnswerOption(BaseModel):
    label: str
    value: JsonValue


class QuestionBase(BaseModel):
    question: str
    question_order: int
    answer_options: list[AnswerOption] = Field(default_factory=list)
    answer_type: AnswerTypeEnum
    dependencies: Dependencies
    wordpress_id: int


class QuestionCreate(QuestionBase):
    questionnaire_id: int
    questionnaire_version: int


class QuestionUpdate(QuestionBase):
    pass


class QuestionOut(QuestionCreate):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    time_created: datetime
