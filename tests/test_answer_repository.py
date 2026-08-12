import asyncio
from types import SimpleNamespace
from typing import Any, cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.questionnaire_answers import QuestionnaireAnswer
from src.models.questions import Question
from src.repositories.answers import AnswerRepository


class _SessionStub:
    async def get(self, model: type[Any], object_id: int) -> Any:
        if model is Question:
            return SimpleNamespace(questionnaire_id=1, questionnaire_version=2)
        if model is QuestionnaireAnswer:
            return SimpleNamespace(questionnaire_id=1, questionnaire_version=3)
        raise AssertionError(f"Unexpected model: {model}")


def test_answer_must_belong_to_attempt_questionnaire_version() -> None:
    repository = AnswerRepository(cast(AsyncSession, _SessionStub()))
    answer = SimpleNamespace(question_id=10, questionnaire_answer_id=20, answer="yes")

    with pytest.raises(ValueError, match="does not belong"):
        asyncio.run(repository.create_answer(answer))
