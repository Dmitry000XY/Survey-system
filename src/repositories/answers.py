from sqlalchemy import select, update
from src.models.answers import Answer


class AnswerRepository:
    def __init__(self, session):
        self.session = session

    async def create_answer(self, answer_obj):
        new_answer = Answer(
            question_id=answer_obj.question_id,
            questionnaire_answer_id=answer_obj.questionnaire_answer_id,
            answer=answer_obj.answer
        )
        self.session.add(new_answer)
        await self.session.flush()
        return new_answer

    async def get_all_answers(self):
        query = select(Answer)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_answer(self, question_id: int, questionnaire_answer_id: int):
        return await self.session.get(Answer, (question_id, questionnaire_answer_id))

    async def update_answer(self, question_id: int, questionnaire_answer_id: int, new_data):
        query = (
            update(Answer)
            .where((Answer.question_id == question_id) & (Answer.questionnaire_answer_id == questionnaire_answer_id))
            .values(answer=new_data.answer)
            .returning(Answer)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_answer(self, question_id: int, questionnaire_answer_id: int):
        ans = await self.get_answer(question_id, questionnaire_answer_id)
        if ans:
            await self.session.delete(ans)
