from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.models.questionnaire_answers import QuestionnaireAnswer


class QuestionnaireAnswerRepository:
    def __init__(self, session):
        self.session = session

    async def create_questionnaire_answer(self, qa) -> QuestionnaireAnswer:
        new_qa = QuestionnaireAnswer(
            user_id=qa.user_id,
            questionnaire_id=qa.questionnaire_id,
            questionnaire_version=qa.questionnaire_version,
            client_id=qa.client_id,
            time_finished=qa.time_finished  # time_started устанавливается автоматически
        )
        self.session.add(new_qa)
        await self.session.flush()
        return new_qa

    async def get_all_questionnaire_answers(self) -> list[QuestionnaireAnswer]:
        query = select(QuestionnaireAnswer)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_questionnaire_answer(self, qa_id: int) -> QuestionnaireAnswer | None:
        return await self.session.get(QuestionnaireAnswer, qa_id)

    async def update_questionnaire_answer(self, qa_id: int, new_data) -> QuestionnaireAnswer | None:
        query = (
            update(QuestionnaireAnswer)
            .where(QuestionnaireAnswer.questionnaire_answer_id == qa_id)
            .values(
                user_id=new_data.user_id,
                questionnaire_id=new_data.questionnaire_id,
                questionnaire_version=new_data.questionnaire_version,
                client_id=new_data.client_id,
                time_finished=new_data.time_finished
            )
            .returning(QuestionnaireAnswer)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_questionnaire_answer(self, qa_id: int):
        qa = await self.get_questionnaire_answer(qa_id)
        if qa:
            await self.session.delete(qa)

    async def get_questionnaire_answer_detail(self, qa_id: int) -> QuestionnaireAnswer | None:
        query = (
            select(QuestionnaireAnswer)
            .options(selectinload(QuestionnaireAnswer.answers))
            .where(QuestionnaireAnswer.questionnaire_answer_id == qa_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()