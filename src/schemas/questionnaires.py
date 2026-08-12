from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.configurations.constants import QUESTIONNAIRE_HASH_LENGTH, QuestionnaireTagEnum
from src.schemas.questions import QuestionOut, QuestionBase

__all__ = [
    "QuestionnaireBase",
    "QuestionnaireCreate",
    "QuestionnaireCreateWithQuestions",
    "QuestionnaireCreateNew",
    "QuestionnaireCreateWithQuestionsNew",
    "QuestionnaireUpdate",
    "QuestionnaireOut",
    "QuestionnaireDetail",
]


class QuestionnaireBase(BaseModel):
    questionnaire_name: str = Field(..., max_length=255)
    wordpress_id: int
    tags: list[QuestionnaireTagEnum] = Field(..., description="List of questionnaire tags")
    is_active: bool = True
    questionnaire_hash: str = Field(
        ...,
        min_length=QUESTIONNAIRE_HASH_LENGTH,
        max_length=QUESTIONNAIRE_HASH_LENGTH,
    )


class QuestionnaireCreate(QuestionnaireBase):
    questionnaire_id: int
    questionnaire_version: int


class QuestionnaireCreateWithQuestions(QuestionnaireCreate):
    questions: list[QuestionBase]


class QuestionnaireCreateNew(QuestionnaireBase):
    pass


class QuestionnaireCreateWithQuestionsNew(QuestionnaireCreateNew):
    questions: list[QuestionBase]


class QuestionnaireUpdate(QuestionnaireBase):
    pass


class QuestionnaireOut(QuestionnaireBase):
    model_config = ConfigDict(from_attributes=True)

    questionnaire_id: int
    questionnaire_version: int
    time_created: datetime


# Схема с вложенными вопросами (зависимость)
class QuestionnaireDetail(QuestionnaireOut):
    questions: list[QuestionOut] = Field(default_factory=list)
