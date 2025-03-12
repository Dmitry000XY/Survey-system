from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from src.schemas.questions import QuestionOut
from src.configurations.constants import FIXED_HASH_LENGTH

__all__ = ["QuestionnaireBase", "QuestionnaireCreate", "QuestionnaireOut", "QuestionnaireDetail"]


class QuestionnaireBase(BaseModel):
    questionnaire_name: str = Field(..., max_length=64)
    wordpress_id: int | None = None
    questionnaire_hash: str = Field(..., min_length=FIXED_HASH_LENGTH, max_length=FIXED_HASH_LENGTH)


class QuestionnaireCreate(QuestionnaireBase):
    questionnaire_version: int


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
