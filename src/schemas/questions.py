from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, JsonValue, PositiveInt

from src.configurations.constants import AnswerTypeEnum
from src.schemas.dependencies import Dependencies

__all__ = ["AnswerOption", "QuestionBase", "QuestionCreate", "QuestionUpdate", "QuestionOut"]


class AnswerOption(BaseModel):
    label: str
    value: JsonValue


class QuestionBase(BaseModel):
    question: str
    question_order: int = Field(ge=0)
    answer_options: list[AnswerOption] = Field(default_factory=list)
    answer_type: AnswerTypeEnum
    dependencies: Dependencies = Field(default_factory=Dependencies)
    wordpress_id: PositiveInt


class QuestionCreate(QuestionBase):
    questionnaire_id: PositiveInt
    questionnaire_version: PositiveInt


class QuestionUpdate(BaseModel):
    question: str | None = None
    question_order: int | None = Field(None, ge=0)
    answer_options: list[AnswerOption] | None = None
    answer_type: AnswerTypeEnum | None = None
    dependencies: Dependencies | None = None
    wordpress_id: PositiveInt | None = None


class QuestionOut(QuestionCreate):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    time_created: datetime
