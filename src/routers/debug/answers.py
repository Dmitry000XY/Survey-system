from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from src.dependencies.dependencies import get_answer_service
from src.schemas.answers import AnswerCreate, AnswerOut
from src.services.answers import AnswerService

answers_router = APIRouter(tags=["Answers"], prefix="/answers")
answer_service = Annotated[AnswerService, Depends(get_answer_service)]


@answers_router.post("/", response_model=AnswerOut, status_code=status.HTTP_201_CREATED)
async def create_answer(answer: Annotated[AnswerCreate, Depends()], service: answer_service):
    return await service.create_answer(answer)


@answers_router.get("/", response_model=list[AnswerOut])
async def get_all_answers(service: answer_service):
    return await service.get_all_answers()


@answers_router.get("/{question_id}/{questionnaire_answer_id}", response_model=AnswerOut)
async def get_answer(question_id: int, questionnaire_answer_id: int, service: answer_service):
    ans = await service.get_answer(question_id, questionnaire_answer_id)
    if ans:
        return ans
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@answers_router.put("/{question_id}/{questionnaire_answer_id}", response_model=AnswerOut)
async def update_answer(question_id: int, questionnaire_answer_id: int, new_data: Annotated[AnswerCreate, Depends()],
                        service: answer_service):
    updated = await service.update_answer(question_id, questionnaire_answer_id, new_data)
    if updated:
        return updated
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@answers_router.delete("/{question_id}/{questionnaire_answer_id}")
async def delete_answer(question_id: int, questionnaire_answer_id: int, service: answer_service):
    await service.delete_answer(question_id, questionnaire_answer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
