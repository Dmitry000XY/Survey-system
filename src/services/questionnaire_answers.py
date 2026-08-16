from src.exceptions import ResourceNotFoundError
from src.repositories.questionnaire_answers import QuestionnaireAnswerRepository
from src.schemas.questionnaire_answers import (
    QuestionnaireAnswerCreate,
    QuestionnaireAnswerDetail,
    QuestionnaireAnswerOut,
    QuestionnaireAnswerUpdate,
)

from .base import BaseService


class QuestionnaireAnswerService(BaseService):
    resource_name = "questionnaire answer"

    def __init__(self, qa_repository: QuestionnaireAnswerRepository) -> None:
        self.qa_repository = qa_repository

    async def create_questionnaire_answer(
        self, questionnaire_answer: QuestionnaireAnswerCreate
    ) -> QuestionnaireAnswerOut:
        created = await self._run(
            self.qa_repository.create_questionnaire_answer(questionnaire_answer),
            conflict_message="The questionnaire answer references unavailable or conflicting data.",
        )
        return self._to_schema(created, QuestionnaireAnswerOut)

    async def get_all_questionnaire_answers(self) -> list[QuestionnaireAnswerOut]:
        answers = await self._run(self.qa_repository.get_all_questionnaire_answers())
        return self._to_schema_list(answers, QuestionnaireAnswerOut)

    async def get_questionnaire_answer(self, questionnaire_answer_id: int) -> QuestionnaireAnswerOut:
        answer = await self._run(self.qa_repository.get_questionnaire_answer(questionnaire_answer_id))
        return self._to_schema(
            self._require(answer, details={"questionnaire_answer_id": questionnaire_answer_id}),
            QuestionnaireAnswerOut,
        )

    async def get_questionnaire_answer_detail(self, questionnaire_answer_id: int) -> QuestionnaireAnswerDetail:
        answer = await self._run(self.qa_repository.get_questionnaire_answer_detail(questionnaire_answer_id))
        return self._to_schema(
            self._require(answer, details={"questionnaire_answer_id": questionnaire_answer_id}),
            QuestionnaireAnswerDetail,
        )

    async def update_questionnaire_answer(
        self,
        questionnaire_answer_id: int,
        new_data: QuestionnaireAnswerUpdate,
    ) -> QuestionnaireAnswerOut:
        updated = await self._run(
            self.qa_repository.update_questionnaire_answer(questionnaire_answer_id, new_data),
            conflict_message="The questionnaire answer references unavailable or conflicting data.",
        )
        return self._to_schema(
            self._require(updated, details={"questionnaire_answer_id": questionnaire_answer_id}),
            QuestionnaireAnswerOut,
        )

    async def delete_questionnaire_answer(self, questionnaire_answer_id: int) -> None:
        deleted = await self._run(self.qa_repository.delete_questionnaire_answer(questionnaire_answer_id))
        if not deleted:
            raise ResourceNotFoundError(
                self.resource_name,
                details={"questionnaire_answer_id": questionnaire_answer_id},
            )
