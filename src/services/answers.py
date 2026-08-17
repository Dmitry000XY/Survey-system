from src.exceptions import DomainValidationError, ResourceNotFoundError
from src.models.questionnaire_answers import QuestionnaireAnswer
from src.models.questions import Question
from src.repositories.answers import AnswerRepository
from src.repositories.questionnaire_answers import QuestionnaireAnswerRepository
from src.repositories.questions import QuestionRepository
from src.schemas.answers import AnswerCreate, AnswerOut, AnswerUpdate

from .base import BaseService


class AnswerService(BaseService):
    resource_name = "answer"

    def __init__(
        self,
        answer_repository: AnswerRepository,
        question_repository: QuestionRepository,
        questionnaire_answer_repository: QuestionnaireAnswerRepository,
    ) -> None:
        self.answer_repository = answer_repository
        self.question_repository = question_repository
        self.questionnaire_answer_repository = questionnaire_answer_repository

    @staticmethod
    def _validate_answer_context(
        question: Question | None,
        questionnaire_answer: QuestionnaireAnswer | None,
    ) -> None:
        if question is None or questionnaire_answer is None:
            violations: list[dict[str, object]] = []
            if question is None:
                violations.append(
                    {
                        "code": "question_not_found",
                        "message": "The referenced question does not exist.",
                        "location": ["body", "question_id"],
                    }
                )
            if questionnaire_answer is None:
                violations.append(
                    {
                        "code": "questionnaire_answer_not_found",
                        "message": "The referenced questionnaire attempt does not exist.",
                        "location": ["body", "questionnaire_answer_id"],
                    }
                )
            raise DomainValidationError(
                "The request violates a domain rule.",
                details={"violations": violations},
            )

        if (question.questionnaire_id, question.questionnaire_version) != (
            questionnaire_answer.questionnaire_id,
            questionnaire_answer.questionnaire_version,
        ):
            raise DomainValidationError(
                "The request violates a domain rule.",
                details={
                    "violations": [
                        {
                            "code": "questionnaire_version_mismatch",
                            "message": "The question does not belong to the questionnaire version being answered.",
                            "location": ["body", "question_id"],
                        }
                    ]
                },
            )

    async def create_answer(self, answer: AnswerCreate) -> AnswerOut:
        question = await self._run(self.question_repository.get_question(answer.question_id))
        questionnaire_answer = await self._run(
            self.questionnaire_answer_repository.get_questionnaire_answer(answer.questionnaire_answer_id)
        )
        self._validate_answer_context(question, questionnaire_answer)

        created = await self._run(
            self.answer_repository.create_answer(answer),
            conflict_message="The answer already exists or does not belong to this questionnaire attempt.",
        )
        return self._to_schema(created, AnswerOut)

    async def get_all_answers(self) -> list[AnswerOut]:
        answers = await self._run(self.answer_repository.get_all_answers())
        return self._to_schema_list(answers, AnswerOut)

    async def get_answer(self, question_id: int, questionnaire_answer_id: int) -> AnswerOut:
        answer = await self._run(self.answer_repository.get_answer(question_id, questionnaire_answer_id))
        return self._to_schema(
            self._require(
                answer,
                details={"question_id": question_id, "questionnaire_answer_id": questionnaire_answer_id},
            ),
            AnswerOut,
        )

    async def update_answer(
        self,
        question_id: int,
        questionnaire_answer_id: int,
        new_data: AnswerUpdate,
    ) -> AnswerOut:
        updated = await self._run(self.answer_repository.update_answer(question_id, questionnaire_answer_id, new_data))
        return self._to_schema(
            self._require(
                updated,
                details={"question_id": question_id, "questionnaire_answer_id": questionnaire_answer_id},
            ),
            AnswerOut,
        )

    async def delete_answer(self, question_id: int, questionnaire_answer_id: int) -> None:
        deleted = await self._run(self.answer_repository.delete_answer(question_id, questionnaire_answer_id))
        if not deleted:
            raise ResourceNotFoundError(
                self.resource_name,
                details={"question_id": question_id, "questionnaire_answer_id": questionnaire_answer_id},
            )
