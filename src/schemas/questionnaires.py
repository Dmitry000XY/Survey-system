from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from src.schemas.questions import QuestionOut, QuestionBase
from src.configurations.constants import FIXED_HASH_LENGTH

__all__ = ["QuestionnaireBase", "QuestionnaireCreate", "QuestionnaireCreateWithQuestions", "QuestionnaireCreateNew",
           "QuestionnaireCreateWithQuestionsNew", "QuestionnaireUpdate", "QuestionnaireOut", "QuestionnaireDetail"]


class QuestionnaireBase(BaseModel):
    questionnaire_name: str = Field(..., max_length=64)
    wordpress_id: int | None = None
    is_active: bool = True
    questionnaire_hash: str = Field(..., min_length=FIXED_HASH_LENGTH, max_length=FIXED_HASH_LENGTH)


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
    questionnaire_id: int
    questionnaire_version: int
    time_created: datetime

    class Config:
        from_attributes = True


# Схема с вложенными вопросами (зависимость)
class QuestionnaireDetail(QuestionnaireOut):
    questions: List[QuestionOut] = []

    class Config:
        from_attributes = True
