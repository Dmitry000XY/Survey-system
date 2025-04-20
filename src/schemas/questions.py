from pydantic import BaseModel
from datetime import datetime

from src.models.questions import AnswerTypeEnum
from src.schemas.dependencies import Dependencies

__all__ = ["QuestionBase", "QuestionCreate", "QuestionUpdate", "QuestionOut"]


class QuestionBase(BaseModel):
    question: str
    question_order: int
    answers: list[str] | None
    answer_type: AnswerTypeEnum
    dependencies: Dependencies
    wordpress_id: int | None = None


class QuestionCreate(QuestionBase):
    questionnaire_id: int
    questionnaire_version: int


class QuestionUpdate(QuestionBase):
    pass


class QuestionOut(QuestionCreate):
    question_id: int
    time_created: datetime

    class Config:
        from_attributes = True
