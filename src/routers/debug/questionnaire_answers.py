from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from src.dependencies.dependencies import get_questionnaire_answer_service
from src.schemas.questionnaire_answers import (
    QuestionnaireAnswerCreate,
    QuestionnaireAnswerOut,
    QuestionnaireAnswerDetail
)
from src.services.questionnaire_answers import QuestionnaireAnswerService

questionnaire_answers_router = APIRouter(tags=["Questionnaire answers"], prefix="/questionnaire-answers")
qa_service = Annotated[QuestionnaireAnswerService, Depends(get_questionnaire_answer_service)]


@questionnaire_answers_router.post("/", response_model=QuestionnaireAnswerOut, status_code=status.HTTP_201_CREATED)
async def create_questionnaire_answer(qa: Annotated[QuestionnaireAnswerCreate, Depends()], service: qa_service):
    return await service.create_questionnaire_answer(qa)


@questionnaire_answers_router.get("/", response_model=list[QuestionnaireAnswerOut])
async def get_all_questionnaire_answers(service: qa_service):
    return await service.get_all_questionnaire_answers()


@questionnaire_answers_router.get("/{qa_id}", response_model=QuestionnaireAnswerOut)
async def get_questionnaire_answer(qa_id: int, service: qa_service):
    qa = await service.get_questionnaire_answer(qa_id)
    if qa:
        return qa
    return Response(status_code=status.HTTP_404_NOT_FOUND)


# Эндпоинт для детальной анкеты с вложенными ответами
@questionnaire_answers_router.get("/detail/{qa_id}", response_model=QuestionnaireAnswerDetail)
async def get_questionnaire_answer_detail(qa_id: int, service: qa_service):
    qa = await service.get_questionnaire_answer(qa_id)
    if qa:
        return await service.get_questionnaire_answer_detail(qa_id)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@questionnaire_answers_router.put("/{qa_id}", response_model=QuestionnaireAnswerOut)
async def update_questionnaire_answer(qa_id: int, new_data: Annotated[QuestionnaireAnswerCreate, Depends()], service: qa_service):
    updated = await service.update_questionnaire_answer(qa_id, new_data)
    if updated:
        return updated
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@questionnaire_answers_router.delete("/{qa_id}")
async def delete_questionnaire_answer(qa_id: int, service: qa_service):
    await service.delete_questionnaire_answer(qa_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
