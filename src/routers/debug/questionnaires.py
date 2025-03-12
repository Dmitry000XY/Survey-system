from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from src.dependencies.dependencies import get_questionnaire_service
from src.schemas.questionnaires import QuestionnaireCreate, QuestionnaireOut, QuestionnaireDetail
from src.services.questionnaires import QuestionnaireService

questionnaires_router = APIRouter(tags=["Questionnaires"], prefix="/questionnaires")
questionnaire_service = Annotated[QuestionnaireService, Depends(get_questionnaire_service)]


@questionnaires_router.post("/", response_model=QuestionnaireOut, status_code=status.HTTP_201_CREATED)
async def create_questionnaire(q: Annotated[QuestionnaireCreate, Depends()], service: questionnaire_service):
    return await service.create_questionnaire(q)


@questionnaires_router.get("/", response_model=list[QuestionnaireOut])
async def get_all_questionnaires(service: questionnaire_service):
    return await service.get_all_questionnaires()


@questionnaires_router.get("/{questionnaire_id}/{questionnaire_version}", response_model=QuestionnaireOut)
async def get_questionnaire(questionnaire_id: int, questionnaire_version: int, service: questionnaire_service):
    q = await service.get_questionnaire(questionnaire_id, questionnaire_version)
    if q:
        return q
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@questionnaires_router.get("/detail/{questionnaire_id}/{questionnaire_version}", response_model=QuestionnaireDetail)
async def get_questionnaire_detail(questionnaire_id: int, questionnaire_version: int, service: questionnaire_service):
    q = await service.get_questionnaire(questionnaire_id, questionnaire_version)
    if q:
        return await service.get_questionnaire_detail(questionnaire_id, questionnaire_version)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@questionnaires_router.put("/{questionnaire_id}/{questionnaire_version}", response_model=QuestionnaireOut)
async def update_questionnaire(questionnaire_id: int, questionnaire_version: int,
                               new_data: Annotated[QuestionnaireCreate, Depends()], service: questionnaire_service):
    updated = await service.update_questionnaire(questionnaire_id, questionnaire_version, new_data)
    if updated:
        return updated
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@questionnaires_router.delete("/{questionnaire_id}/{questionnaire_version}")
async def delete_questionnaire(questionnaire_id: int, questionnaire_version: int, service: questionnaire_service):
    await service.delete_questionnaire(questionnaire_id, questionnaire_version)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
