from fastapi import Response, status
from src.repositories.questions import QuestionRepository


class QuestionService:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    async def create_question(self, question):
        return await self.question_repository.create_question(question)

    async def get_all_questions(self):
        return await self.question_repository.get_all_questions()

    async def get_question(self, question_id: int):
        question = await self.question_repository.get_question(question_id)
        if not question:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return question

    async def update_question(self, question_id: int, new_data):
        if await self.question_repository.get_question(question_id):
            return await self.question_repository.update_question(question_id, new_data)
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    async def delete_question(self, question_id: int):
        if await self.question_repository.get_question(question_id):
            await self.question_repository.delete_question(question_id)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
