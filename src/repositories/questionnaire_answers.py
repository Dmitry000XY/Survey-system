from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.questionnaire_answers import QuestionnaireAnswer
from src.schemas.questionnaire_answers import QuestionnaireAnswerCreate, QuestionnaireAnswerUpdate

from .base import BaseRepository


class QuestionnaireAnswerRepository(BaseRepository):
    entity_name = "questionnaire answer"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_questionnaire_answer(self, qa: QuestionnaireAnswerCreate) -> QuestionnaireAnswer:
        new_qa = QuestionnaireAnswer(
            user_id=qa.user_id,
            questionnaire_id=qa.questionnaire_id,
            questionnaire_version=qa.questionnaire_version,
            client_id=qa.client_id,
            time_finished=qa.time_finished,
        )
        self.session.add(new_qa)
        await self._flush(operation="create")
        return new_qa

    async def get_all_questionnaire_answers(self) -> list[QuestionnaireAnswer]:
        query = select(QuestionnaireAnswer)
        result = await self._execute(query, operation="list")
        return list(result.scalars().all())

    async def get_questionnaire_answer(self, qa_id: int) -> QuestionnaireAnswer | None:
        return await self._get(QuestionnaireAnswer, qa_id)

    async def update_questionnaire_answer(
        self, qa_id: int, new_data: QuestionnaireAnswerUpdate
    ) -> QuestionnaireAnswer | None:
        values = new_data.model_dump(exclude_unset=True)
        if not values:
            return await self.get_questionnaire_answer(qa_id)
        query = (
            update(QuestionnaireAnswer)
            .where(QuestionnaireAnswer.questionnaire_answer_id == qa_id)
            .values(**values)
            .returning(QuestionnaireAnswer)
        )
        result = await self._execute(query, operation="update")
        return result.scalar_one_or_none()

    async def delete_questionnaire_answer(self, qa_id: int) -> bool:
        qa = await self.get_questionnaire_answer(qa_id)
        if qa is None:
            return False
        await self._delete(qa)
        return True

    async def get_questionnaire_answer_detail(self, qa_id: int) -> QuestionnaireAnswer | None:
        query = (
            select(QuestionnaireAnswer)
            .options(selectinload(QuestionnaireAnswer.answers))
            .where(QuestionnaireAnswer.questionnaire_answer_id == qa_id)
        )
        result = await self._execute(query, operation="read")
        return result.scalars().first()
