from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

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
    "QuestionnaireDeactivationRequest",
    "QuestionnaireDeactivationResult",
]


class QuestionnaireBase(BaseModel):
    questionnaire_name: str = Field(..., max_length=255)
    wordpress_id: PositiveInt
    tags: list[QuestionnaireTagEnum] = Field(..., description="List of questionnaire tags")
    is_active: bool = True
    questionnaire_hash: str = Field(
        ...,
        min_length=QUESTIONNAIRE_HASH_LENGTH,
        max_length=QUESTIONNAIRE_HASH_LENGTH,
    )


class QuestionnaireCreate(QuestionnaireBase):
    questionnaire_id: PositiveInt
    questionnaire_version: PositiveInt


class QuestionnaireCreateWithQuestions(QuestionnaireCreate):
    questions: list[QuestionBase]


class QuestionnaireCreateNew(QuestionnaireBase):
    pass


class QuestionnaireCreateWithQuestionsNew(QuestionnaireCreateNew):
    questions: list[QuestionBase]


class QuestionnaireUpdate(BaseModel):
    questionnaire_name: str | None = Field(None, max_length=255)
    wordpress_id: PositiveInt | None = None
    tags: list[QuestionnaireTagEnum] | None = None
    is_active: bool | None = None
    questionnaire_hash: str | None = Field(
        None,
        min_length=QUESTIONNAIRE_HASH_LENGTH,
        max_length=QUESTIONNAIRE_HASH_LENGTH,
    )


class QuestionnaireOut(QuestionnaireBase):
    model_config = ConfigDict(from_attributes=True)

    questionnaire_id: int
    questionnaire_version: int
    time_created: datetime


class QuestionnaireDetail(QuestionnaireOut):
    questions: list[QuestionOut] = Field(default_factory=list)


class QuestionnaireDeactivationRequest(BaseModel):
    questionnaire_ids: list[PositiveInt] = Field(min_length=1)


class QuestionnaireDeactivationResult(BaseModel):
    affected_versions: int
