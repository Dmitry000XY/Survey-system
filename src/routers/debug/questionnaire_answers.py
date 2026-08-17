from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.api.openapi import CONFLICT_RESPONSE, NOT_FOUND_OR_CONFLICT_RESPONSES, NOT_FOUND_RESPONSE
from src.dependencies import get_questionnaire_answer_service
from src.schemas.questionnaire_answers import (
    QuestionnaireAnswerCreate,
    QuestionnaireAnswerDetail,
    QuestionnaireAnswerOut,
    QuestionnaireAnswerUpdate,
)
from src.services.questionnaire_answers import QuestionnaireAnswerService

questionnaire_answers_router = APIRouter(tags=["Questionnaire answers"], prefix="/questionnaire-answers")
QuestionnaireAnswerServiceDependency = Annotated[
    QuestionnaireAnswerService,
    Depends(get_questionnaire_answer_service),
]
QuestionnaireAnswerId = Annotated[int, Path(gt=0)]


@questionnaire_answers_router.post(
    "",
    response_model=QuestionnaireAnswerOut,
    status_code=status.HTTP_201_CREATED,
    responses=CONFLICT_RESPONSE,
)
async def create_questionnaire_answer(
    questionnaire_answer: QuestionnaireAnswerCreate,
    service: QuestionnaireAnswerServiceDependency,
) -> QuestionnaireAnswerOut:
    return await service.create_questionnaire_answer(questionnaire_answer)


@questionnaire_answers_router.get("", response_model=list[QuestionnaireAnswerOut], status_code=status.HTTP_200_OK)
async def get_all_questionnaire_answers(
    service: QuestionnaireAnswerServiceDependency,
) -> list[QuestionnaireAnswerOut]:
    return await service.get_all_questionnaire_answers()


@questionnaire_answers_router.get(
    "/{questionnaire_answer_id}",
    response_model=QuestionnaireAnswerOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_RESPONSE,
)
async def get_questionnaire_answer(
    questionnaire_answer_id: QuestionnaireAnswerId,
    service: QuestionnaireAnswerServiceDependency,
) -> QuestionnaireAnswerOut:
    return await service.get_questionnaire_answer(questionnaire_answer_id)


@questionnaire_answers_router.get(
    "/{questionnaire_answer_id}/detail",
    response_model=QuestionnaireAnswerDetail,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_RESPONSE,
)
async def get_questionnaire_answer_detail(
    questionnaire_answer_id: QuestionnaireAnswerId,
    service: QuestionnaireAnswerServiceDependency,
) -> QuestionnaireAnswerDetail:
    return await service.get_questionnaire_answer_detail(questionnaire_answer_id)


@questionnaire_answers_router.patch(
    "/{questionnaire_answer_id}",
    response_model=QuestionnaireAnswerOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_OR_CONFLICT_RESPONSES,
)
async def update_questionnaire_answer(
    questionnaire_answer_id: QuestionnaireAnswerId,
    new_data: QuestionnaireAnswerUpdate,
    service: QuestionnaireAnswerServiceDependency,
) -> QuestionnaireAnswerOut:
    return await service.update_questionnaire_answer(questionnaire_answer_id, new_data)


@questionnaire_answers_router.delete(
    "/{questionnaire_answer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=NOT_FOUND_RESPONSE,
)
async def delete_questionnaire_answer(
    questionnaire_answer_id: QuestionnaireAnswerId,
    service: QuestionnaireAnswerServiceDependency,
) -> Response:
    await service.delete_questionnaire_answer(questionnaire_answer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
