import asyncio
import pytest

from src.exceptions import DomainValidationError
from src.models.questionnaire_answers import QuestionnaireAnswer
from src.models.questions import Question
from src.repositories.answers import AnswerRepository
from src.repositories.questionnaire_answers import QuestionnaireAnswerRepository
from src.repositories.questions import QuestionRepository
from src.schemas.answers import AnswerCreate
from src.services.answers import AnswerService


class _AnswerRepositoryStub(AnswerRepository):
    def __init__(self) -> None:
        pass


class _QuestionRepositoryStub(QuestionRepository):
    def __init__(self) -> None:
        pass

    async def get_question(self, question_id: int) -> Question | None:
        del question_id
        return Question(questionnaire_id=1, questionnaire_version=2)


class _QuestionnaireAnswerRepositoryStub(QuestionnaireAnswerRepository):
    def __init__(self) -> None:
        pass

    async def get_questionnaire_answer(self, qa_id: int) -> QuestionnaireAnswer | None:
        del qa_id
        return QuestionnaireAnswer(questionnaire_id=1, questionnaire_version=3)


class _MissingQuestionRepositoryStub(_QuestionRepositoryStub):
    async def get_question(self, question_id: int) -> None:
        del question_id
        return None


class _MissingQuestionnaireAnswerRepositoryStub(_QuestionnaireAnswerRepositoryStub):
    async def get_questionnaire_answer(self, qa_id: int) -> None:
        del qa_id
        return None


def test_answer_must_belong_to_attempt_questionnaire_version() -> None:
    service = AnswerService(
        _AnswerRepositoryStub(),
        _QuestionRepositoryStub(),
        _QuestionnaireAnswerRepositoryStub(),
    )
    answer = AnswerCreate(question_id=10, questionnaire_answer_id=20, answer="yes")

    with pytest.raises(DomainValidationError) as exception_info:
        asyncio.run(service.create_answer(answer))

    assert exception_info.value.message == "The request violates a domain rule."
    assert exception_info.value.details == {
        "violations": [
            {
                "code": "questionnaire_version_mismatch",
                "message": "The question does not belong to the questionnaire version being answered.",
                "location": ["body", "question_id"],
            }
        ]
    }


@pytest.mark.parametrize(
    ("question_repository", "questionnaire_answer_repository", "expected_codes"),
    [
        (
            _MissingQuestionRepositoryStub(),
            _QuestionnaireAnswerRepositoryStub(),
            ["question_not_found"],
        ),
        (
            _QuestionRepositoryStub(),
            _MissingQuestionnaireAnswerRepositoryStub(),
            ["questionnaire_answer_not_found"],
        ),
        (
            _MissingQuestionRepositoryStub(),
            _MissingQuestionnaireAnswerRepositoryStub(),
            ["question_not_found", "questionnaire_answer_not_found"],
        ),
    ],
)
def test_missing_answer_references_are_reported_as_violations(
    question_repository: QuestionRepository,
    questionnaire_answer_repository: QuestionnaireAnswerRepository,
    expected_codes: list[str],
) -> None:
    service = AnswerService(
        _AnswerRepositoryStub(),
        question_repository,
        questionnaire_answer_repository,
    )
    answer = AnswerCreate(question_id=10, questionnaire_answer_id=20, answer="yes")

    with pytest.raises(DomainValidationError) as exception_info:
        asyncio.run(service.create_answer(answer))

    assert exception_info.value.details is not None
    violations = exception_info.value.details["violations"]
    assert [violation["code"] for violation in violations] == expected_codes
