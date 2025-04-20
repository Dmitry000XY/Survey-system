from fastapi import HTTPException, status
from src.repositories.questionnaires import QuestionnaireRepository
from src.schemas.questionnaires import QuestionnaireCreate, QuestionnaireUpdate


class QuestionnaireService:
    def __init__(self, repository: QuestionnaireRepository):
        self.repository = repository

    async def create_questionnaire(self, questionnaire: QuestionnaireCreate) -> object | None:
        return await self.repository.create_questionnaire(questionnaire)

    async def get_all_questionnaires(self) -> list[object]:
        return await self.repository.get_all_questionnaires()

    async def get_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> object | None:
        questionnaire = await self.repository.get_questionnaire(questionnaire_id, questionnaire_version)
        if not questionnaire:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found.")
        return questionnaire

    async def update_questionnaire(self, questionnaire_id: int, questionnaire_version: int,
                                   new_data: QuestionnaireUpdate) -> object | None:
        if await self.repository.get_questionnaire(questionnaire_id, questionnaire_version):
            return await self.repository.update_questionnaire(questionnaire_id, questionnaire_version, new_data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found.")

    async def delete_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> None:
        questionnaire = await self.repository.get_questionnaire(questionnaire_id, questionnaire_version)
        if questionnaire:
            await self.repository.delete_questionnaire(questionnaire_id, questionnaire_version)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found.")

    async def get_questionnaire_detail(self, questionnaire_id: int, questionnaire_version: int) -> object | None:
        questionnaire_detail = await self.repository.get_questionnaire_detail(questionnaire_id, questionnaire_version)
        if not questionnaire_detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire detail not found.")
        return questionnaire_detail

    async def get_latest_versions(self) -> list[object]:
        return await self.repository.get_latest_versions()

    async def deactivate_questionnaires(self, questionnaire_ids: list[int]) -> None:
        await self.repository.deactivate_all_by_ids(questionnaire_ids)
