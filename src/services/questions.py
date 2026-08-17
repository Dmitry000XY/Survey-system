from src.exceptions import ResourceNotFoundError
from src.repositories.questions import QuestionRepository
from src.schemas.questions import QuestionCreate, QuestionOut, QuestionUpdate

from .base import BaseService


class QuestionService(BaseService):
    resource_name = "question"

    def __init__(self, question_repository: QuestionRepository) -> None:
        self.question_repository = question_repository

    async def create_question(self, question: QuestionCreate) -> QuestionOut:
        created = await self._run(
            self.question_repository.create_question(question),
            conflict_message="A question with this order or WordPress ID already exists in the questionnaire version.",
        )
        return self._to_schema(created, QuestionOut)

    async def get_all_questions(self) -> list[QuestionOut]:
        questions = await self._run(self.question_repository.get_all_questions())
        return self._to_schema_list(questions, QuestionOut)

    async def get_question(self, question_id: int) -> QuestionOut:
        question = await self._run(self.question_repository.get_question(question_id))
        return self._to_schema(self._require(question, details={"question_id": question_id}), QuestionOut)

    async def update_question(self, question_id: int, new_data: QuestionUpdate) -> QuestionOut:
        updated = await self._run(
            self.question_repository.update_question(question_id, new_data),
            conflict_message="The updated question conflicts with another question in this questionnaire version.",
        )
        return self._to_schema(self._require(updated, details={"question_id": question_id}), QuestionOut)

    async def delete_question(self, question_id: int) -> None:
        deleted = await self._run(self.question_repository.delete_question(question_id))
        if not deleted:
            raise ResourceNotFoundError(self.resource_name, details={"question_id": question_id})
