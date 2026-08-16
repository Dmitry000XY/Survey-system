from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.api.openapi import CONFLICT_RESPONSE, NOT_FOUND_RESPONSE
from src.dependencies import get_answer_service
from src.schemas.answers import AnswerCreate, AnswerOut, AnswerUpdate
from src.services.answers import AnswerService

answers_router = APIRouter(tags=["Answers"], prefix="/answers")
AnswerServiceDependency = Annotated[AnswerService, Depends(get_answer_service)]
ResourceId = Annotated[int, Path(gt=0)]


@answers_router.post("", response_model=AnswerOut, status_code=status.HTTP_201_CREATED, responses=CONFLICT_RESPONSE)
async def create_answer(answer: AnswerCreate, service: AnswerServiceDependency) -> AnswerOut:
    return await service.create_answer(answer)


@answers_router.get("", response_model=list[AnswerOut], status_code=status.HTTP_200_OK)
async def get_all_answers(service: AnswerServiceDependency) -> list[AnswerOut]:
    return await service.get_all_answers()


@answers_router.get(
    "/{question_id}/{questionnaire_answer_id}",
    response_model=AnswerOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_RESPONSE,
)
async def get_answer(
    question_id: ResourceId,
    questionnaire_answer_id: ResourceId,
    service: AnswerServiceDependency,
) -> AnswerOut:
    return await service.get_answer(question_id, questionnaire_answer_id)


@answers_router.patch(
    "/{question_id}/{questionnaire_answer_id}",
    response_model=AnswerOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_RESPONSE,
)
async def update_answer(
    question_id: ResourceId,
    questionnaire_answer_id: ResourceId,
    new_data: AnswerUpdate,
    service: AnswerServiceDependency,
) -> AnswerOut:
    return await service.update_answer(question_id, questionnaire_answer_id, new_data)


@answers_router.delete(
    "/{question_id}/{questionnaire_answer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=NOT_FOUND_RESPONSE,
)
async def delete_answer(
    question_id: ResourceId,
    questionnaire_answer_id: ResourceId,
    service: AnswerServiceDependency,
) -> Response:
    await service.delete_answer(question_id, questionnaire_answer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
