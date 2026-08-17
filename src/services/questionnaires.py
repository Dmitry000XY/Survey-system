from src.exceptions import ResourceNotFoundError
from src.repositories.questionnaires import QuestionnaireRepository
from src.schemas.questionnaires import QuestionnaireCreate, QuestionnaireDetail, QuestionnaireOut, QuestionnaireUpdate

from .base import BaseService


class QuestionnaireService(BaseService):
    resource_name = "questionnaire"

    def __init__(self, repository: QuestionnaireRepository) -> None:
        self.repository = repository

    async def create_questionnaire(self, questionnaire: QuestionnaireCreate) -> QuestionnaireOut:
        created = await self._run(
            self.repository.create_questionnaire(questionnaire),
            conflict_message="This questionnaire version or hash already exists.",
        )
        return self._to_schema(created, QuestionnaireOut)

    async def get_all_questionnaires(self) -> list[QuestionnaireOut]:
        questionnaires = await self._run(self.repository.get_all_questionnaires())
        return self._to_schema_list(questionnaires, QuestionnaireOut)

    async def get_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> QuestionnaireOut:
        questionnaire = await self._run(self.repository.get_questionnaire(questionnaire_id, questionnaire_version))
        return self._to_schema(
            self._require(
                questionnaire,
                details={"questionnaire_id": questionnaire_id, "questionnaire_version": questionnaire_version},
            ),
            QuestionnaireOut,
        )

    async def update_questionnaire(
        self,
        questionnaire_id: int,
        questionnaire_version: int,
        new_data: QuestionnaireUpdate,
    ) -> QuestionnaireOut:
        updated = await self._run(
            self.repository.update_questionnaire(questionnaire_id, questionnaire_version, new_data),
            conflict_message="The updated questionnaire conflicts with an existing version.",
        )
        return self._to_schema(
            self._require(
                updated,
                details={"questionnaire_id": questionnaire_id, "questionnaire_version": questionnaire_version},
            ),
            QuestionnaireOut,
        )

    async def delete_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> None:
        deleted = await self._run(self.repository.delete_questionnaire(questionnaire_id, questionnaire_version))
        if not deleted:
            raise ResourceNotFoundError(
                self.resource_name,
                details={"questionnaire_id": questionnaire_id, "questionnaire_version": questionnaire_version},
            )

    async def get_questionnaire_detail(self, questionnaire_id: int, questionnaire_version: int) -> QuestionnaireDetail:
        questionnaire = await self._run(
            self.repository.get_questionnaire_detail(questionnaire_id, questionnaire_version)
        )
        return self._to_schema(
            self._require(
                questionnaire,
                details={"questionnaire_id": questionnaire_id, "questionnaire_version": questionnaire_version},
            ),
            QuestionnaireDetail,
        )

    async def get_latest_versions(self) -> list[QuestionnaireOut]:
        questionnaires = await self._run(self.repository.get_latest_versions())
        return self._to_schema_list(questionnaires, QuestionnaireOut)

    async def deactivate_questionnaires(self, questionnaire_ids: list[int]) -> int:
        return await self._run(self.repository.deactivate_all_by_ids(questionnaire_ids))
