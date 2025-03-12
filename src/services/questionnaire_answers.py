from fastapi import Response, status
from src.repositories.questionnaire_answers import QuestionnaireAnswerRepository


class QuestionnaireAnswerService:
    def __init__(self, qa_repository: QuestionnaireAnswerRepository):
        self.qa_repository = qa_repository

    async def create_questionnaire_answer(self, qa):
        return await self.qa_repository.create_questionnaire_answer(qa)

    async def get_all_questionnaire_answers(self):
        return await self.qa_repository.get_all_questionnaire_answers()

    async def get_questionnaire_answer(self, qa_id: int):
        qa = await self.qa_repository.get_questionnaire_answer(qa_id)
        if not qa:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return qa

    async def get_questionnaire_answer_detail(self, qa_id: int):
        qa = await self.qa_repository.get_questionnaire_answer_detail(qa_id)
        if not qa:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return qa

    async def update_questionnaire_answer(self, qa_id: int, new_data):
        if await self.qa_repository.get_questionnaire_answer(qa_id):
            return await self.qa_repository.update_questionnaire_answer(qa_id, new_data)
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    async def delete_questionnaire_answer(self, qa_id: int):
        if await self.qa_repository.get_questionnaire_answer(qa_id):
            await self.qa_repository.delete_questionnaire_answer(qa_id)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
