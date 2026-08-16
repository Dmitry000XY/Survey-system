from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.api.openapi import CONFLICT_RESPONSE, NOT_FOUND_OR_CONFLICT_RESPONSES, NOT_FOUND_RESPONSE
from src.dependencies import get_questionnaire_service
from src.schemas.questionnaires import (
    QuestionnaireCreate,
    QuestionnaireDeactivationRequest,
    QuestionnaireDeactivationResult,
    QuestionnaireDetail,
    QuestionnaireOut,
    QuestionnaireUpdate,
)
from src.services.questionnaires import QuestionnaireService

questionnaires_router = APIRouter(tags=["Questionnaires"], prefix="/questionnaires")
QuestionnaireServiceDependency = Annotated[QuestionnaireService, Depends(get_questionnaire_service)]
QuestionnaireId = Annotated[int, Path(gt=0)]
QuestionnaireVersion = Annotated[int, Path(gt=0)]


@questionnaires_router.post(
    "", response_model=QuestionnaireOut, status_code=status.HTTP_201_CREATED, responses=CONFLICT_RESPONSE
)
async def create_questionnaire(
    questionnaire: QuestionnaireCreate,
    service: QuestionnaireServiceDependency,
) -> QuestionnaireOut:
    return await service.create_questionnaire(questionnaire)


@questionnaires_router.get("", response_model=list[QuestionnaireOut], status_code=status.HTTP_200_OK)
async def get_all_questionnaires(
    service: QuestionnaireServiceDependency,
) -> list[QuestionnaireOut]:
    return await service.get_all_questionnaires()


@questionnaires_router.get("/latest", response_model=list[QuestionnaireOut], status_code=status.HTTP_200_OK)
async def get_latest_questionnaires(
    service: QuestionnaireServiceDependency,
) -> list[QuestionnaireOut]:
    return await service.get_latest_versions()


@questionnaires_router.post(
    "/deactivate", response_model=QuestionnaireDeactivationResult, status_code=status.HTTP_200_OK
)
async def deactivate_questionnaires(
    request: QuestionnaireDeactivationRequest,
    service: QuestionnaireServiceDependency,
) -> QuestionnaireDeactivationResult:
    affected = await service.deactivate_questionnaires(request.questionnaire_ids)
    return QuestionnaireDeactivationResult(affected_versions=affected)


@questionnaires_router.get(
    "/{questionnaire_id}/{questionnaire_version}",
    response_model=QuestionnaireOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_RESPONSE,
)
async def get_questionnaire(
    questionnaire_id: QuestionnaireId,
    questionnaire_version: QuestionnaireVersion,
    service: QuestionnaireServiceDependency,
) -> QuestionnaireOut:
    return await service.get_questionnaire(questionnaire_id, questionnaire_version)


@questionnaires_router.get(
    "/{questionnaire_id}/{questionnaire_version}/detail",
    response_model=QuestionnaireDetail,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_RESPONSE,
)
async def get_questionnaire_detail(
    questionnaire_id: QuestionnaireId,
    questionnaire_version: QuestionnaireVersion,
    service: QuestionnaireServiceDependency,
) -> QuestionnaireDetail:
    return await service.get_questionnaire_detail(questionnaire_id, questionnaire_version)


@questionnaires_router.patch(
    "/{questionnaire_id}/{questionnaire_version}",
    response_model=QuestionnaireOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_OR_CONFLICT_RESPONSES,
)
async def update_questionnaire(
    questionnaire_id: QuestionnaireId,
    questionnaire_version: QuestionnaireVersion,
    new_data: QuestionnaireUpdate,
    service: QuestionnaireServiceDependency,
) -> QuestionnaireOut:
    return await service.update_questionnaire(questionnaire_id, questionnaire_version, new_data)


@questionnaires_router.delete(
    "/{questionnaire_id}/{questionnaire_version}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=NOT_FOUND_RESPONSE,
)
async def delete_questionnaire(
    questionnaire_id: QuestionnaireId,
    questionnaire_version: QuestionnaireVersion,
    service: QuestionnaireServiceDependency,
) -> Response:
    await service.delete_questionnaire(questionnaire_id, questionnaire_version)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
