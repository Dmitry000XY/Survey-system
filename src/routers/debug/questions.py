from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status

from src.api.openapi import CONFLICT_RESPONSE, NOT_FOUND_OR_CONFLICT_RESPONSES, NOT_FOUND_RESPONSE
from src.dependencies import get_question_service
from src.schemas.questions import QuestionCreate, QuestionOut, QuestionUpdate
from src.services.questions import QuestionService

questions_router = APIRouter(tags=["Questions"], prefix="/questions")
QuestionServiceDependency = Annotated[QuestionService, Depends(get_question_service)]
QuestionId = Annotated[int, Path(gt=0)]


@questions_router.post("", response_model=QuestionOut, status_code=status.HTTP_201_CREATED, responses=CONFLICT_RESPONSE)
async def create_question(question: QuestionCreate, service: QuestionServiceDependency) -> QuestionOut:
    return await service.create_question(question)


@questions_router.get("", response_model=list[QuestionOut], status_code=status.HTTP_200_OK)
async def get_all_questions(service: QuestionServiceDependency) -> list[QuestionOut]:
    return await service.get_all_questions()


@questions_router.get(
    "/{question_id}", response_model=QuestionOut, status_code=status.HTTP_200_OK, responses=NOT_FOUND_RESPONSE
)
async def get_question(question_id: QuestionId, service: QuestionServiceDependency) -> QuestionOut:
    return await service.get_question(question_id)


@questions_router.patch(
    "/{question_id}",
    response_model=QuestionOut,
    status_code=status.HTTP_200_OK,
    responses=NOT_FOUND_OR_CONFLICT_RESPONSES,
)
async def update_question(
    question_id: QuestionId,
    new_data: QuestionUpdate,
    service: QuestionServiceDependency,
) -> QuestionOut:
    return await service.update_question(question_id, new_data)


@questions_router.delete(
    "/{question_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, responses=NOT_FOUND_RESPONSE
)
async def delete_question(question_id: QuestionId, service: QuestionServiceDependency) -> Response:
    await service.delete_question(question_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
