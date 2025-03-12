from fastapi import Response, status
from src.repositories.answers import AnswerRepository


class AnswerService:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    async def create_answer(self, answer_obj):
        return await self.answer_repository.create_answer(answer_obj)

    async def get_all_answers(self):
        return await self.answer_repository.get_all_answers()

    async def get_answer(self, question_id: int, questionnaire_answer_id: int):
        answer = await self.answer_repository.get_answer(question_id, questionnaire_answer_id)
        if not answer:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return answer

    async def update_answer(self, question_id: int, questionnaire_answer_id: int, new_data):
        if await self.answer_repository.get_answer(question_id, questionnaire_answer_id):
            return await self.answer_repository.update_answer(question_id, questionnaire_answer_id, new_data)
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    async def delete_answer(self, question_id: int, questionnaire_answer_id: int):
        if await self.answer_repository.get_answer(question_id, questionnaire_answer_id):
            await self.answer_repository.delete_answer(question_id, questionnaire_answer_id)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
