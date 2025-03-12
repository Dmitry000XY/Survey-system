from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from src.dependencies.dependencies import get_question_service
from src.schemas.questions import QuestionCreate, QuestionOut
from src.services.questions import QuestionService

questions_router = APIRouter(tags=["Questions"], prefix="/questions")
question_service = Annotated[QuestionService, Depends(get_question_service)]


@questions_router.post("/", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
async def create_question(question: Annotated[QuestionCreate, Depends()], service: question_service):
    return await service.create_question(question)


@questions_router.get("/", response_model=list[QuestionOut])
async def get_all_questions(service: question_service):
    return await service.get_all_questions()


@questions_router.get("/{question_id}", response_model=QuestionOut)
async def get_question(question_id: int, service: question_service):
    q = await service.get_question(question_id)
    if q:
        return q
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@questions_router.put("/{question_id}", response_model=QuestionOut)
async def update_question(question_id: int, new_data: Annotated[QuestionCreate, Depends()], service: question_service):
    updated = await service.update_question(question_id, new_data)
    if updated:
        return updated
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@questions_router.delete("/{question_id}")
async def delete_question(question_id: int, service: question_service):
    await service.delete_question(question_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
