from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations import get_async_session
from src.repositories import (
    UserRepository, ClientRepository, UserClientRepository,
    QuestionnaireAnswerRepository, AnswerRepository, QuestionnaireRepository,
    QuestionRepository, SettingRepository
)
from src.services import (
    UserService, ClientService, UserClientService, QuestionnaireAnswerService,
    AnswerService, QuestionnaireService, QuestionService, SettingService
)

__all__ = [
    "get_user_service", "get_client_service", "get_user_client_service",
    "get_questionnaire_answer_service", "get_answer_service", "get_questionnaire_service",
    "get_question_service", "get_setting_service"
]

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_service(session: DBSession) -> UserService:
    return UserService(UserRepository(session))


def get_client_service(session: DBSession) -> ClientService:
    return ClientService(ClientRepository(session))


def get_user_client_service(session: DBSession) -> UserClientService:
    return UserClientService(UserClientRepository(session))


def get_questionnaire_answer_service(session: DBSession) -> QuestionnaireAnswerService:
    return QuestionnaireAnswerService(QuestionnaireAnswerRepository(session))


def get_answer_service(session: DBSession) -> AnswerService:
    return AnswerService(AnswerRepository(session))


def get_questionnaire_service(session: DBSession) -> QuestionnaireService:
    return QuestionnaireService(QuestionnaireRepository(session))


def get_question_service(session: DBSession) -> QuestionService:
    return QuestionService(QuestionRepository(session))


def get_setting_service(session: DBSession) -> SettingService:
    return SettingService(SettingRepository(session))
