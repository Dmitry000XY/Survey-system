from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.answers import Answer
from src.schemas.answers import AnswerCreate, AnswerUpdate

from .base import BaseRepository


class AnswerRepository(BaseRepository):
    entity_name = "answer"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_answer(self, answer_obj: AnswerCreate) -> Answer:
        new_answer = Answer(
            question_id=answer_obj.question_id,
            questionnaire_answer_id=answer_obj.questionnaire_answer_id,
            answer=answer_obj.answer,
        )
        self.session.add(new_answer)
        await self._flush(operation="create")
        return new_answer

    async def get_all_answers(self) -> list[Answer]:
        query = select(Answer)
        result = await self._execute(query, operation="list")
        return list(result.scalars().all())

    async def get_answer(self, question_id: int, questionnaire_answer_id: int) -> Answer | None:
        return await self._get(Answer, (question_id, questionnaire_answer_id))

    async def update_answer(
        self, question_id: int, questionnaire_answer_id: int, new_data: AnswerUpdate
    ) -> Answer | None:
        query = (
            update(Answer)
            .where((Answer.question_id == question_id) & (Answer.questionnaire_answer_id == questionnaire_answer_id))
            .values(answer=new_data.answer)
            .returning(Answer)
        )
        result = await self._execute(query, operation="update")
        return result.scalar_one_or_none()

    async def delete_answer(self, question_id: int, questionnaire_answer_id: int) -> bool:
        ans = await self.get_answer(question_id, questionnaire_answer_id)
        if ans is None:
            return False
        await self._delete(ans)
        return True
