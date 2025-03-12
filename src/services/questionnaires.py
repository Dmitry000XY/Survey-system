from fastapi import Response, status
from src.repositories.questionnaires import QuestionnaireRepository


class QuestionnaireService:
    def __init__(self, questionnaire_repository: QuestionnaireRepository):
        self.questionnaire_repository = questionnaire_repository

    async def create_questionnaire(self, questionnaire):
        return await self.questionnaire_repository.create_questionnaire(questionnaire)

    async def get_all_questionnaires(self):
        return await self.questionnaire_repository.get_all_questionnaires()

    async def get_questionnaire(self, questionnaire_id: int, questionnaire_version: int):
        questionnaire = await self.questionnaire_repository.get_questionnaire(questionnaire_id, questionnaire_version)
        if not questionnaire:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return questionnaire

    async def get_questionnaire_detail(self, questionnaire_id: int, questionnaire_version: int):
        detailed_questionnaire = await self.questionnaire_repository.get_questionnaire_detail(questionnaire_id, questionnaire_version)
        if not detailed_questionnaire:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return detailed_questionnaire

    async def update_questionnaire(self, questionnaire_id: int, questionnaire_version: int, new_data):
        if await self.questionnaire_repository.get_questionnaire(questionnaire_id, questionnaire_version):
            return await self.questionnaire_repository.update_questionnaire(questionnaire_id, questionnaire_version,
                                                                            new_data)
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    async def delete_questionnaire(self, questionnaire_id: int, questionnaire_version: int):
        if await self.questionnaire_repository.get_questionnaire(questionnaire_id, questionnaire_version):
            await self.questionnaire_repository.delete_questionnaire(questionnaire_id, questionnaire_version)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
