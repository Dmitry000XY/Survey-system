from fastapi import APIRouter

from .debug.users import users_router
from .debug.clients import clients_router
from .debug.users_clients import users_clients_router
from .debug.questionnaire_answers import questionnaire_answers_router
from .debug.answers import answers_router
from .debug.questionnaires import questionnaires_router
from .debug.questions import questions_router
from .debug.settings import settings_router

debug_router = APIRouter(tags=["Debug"], prefix="/api/debug")

debug_router.include_router(users_router)
debug_router.include_router(clients_router)
debug_router.include_router(users_clients_router)
debug_router.include_router(questionnaire_answers_router)
debug_router.include_router(answers_router)
debug_router.include_router(questionnaires_router)
debug_router.include_router(questions_router)
debug_router.include_router(settings_router)

# Если появится аутентификация, можно раскомментировать:
# from src.auth.auth import auth_router
# debug_router.include_router(auth_router)

openapi_tags = [
    {"name": "Debug", "description": "Debugging routes"},
    {"name": "Users", "description": "Operations with users"},
    {"name": "Clients", "description": "Operations with clients"},
    {"name": "Users clients", "description": "User-client relationship operations"},
    {"name": "Questionnaire answers", "description": "Operations with questionnaire answers"},
    {"name": "Answers", "description": "Operations with answers"},
    {"name": "Questionnaires", "description": "Operations with questionnaires"},
    {"name": "Questions", "description": "Operations with questions"},
    {"name": "Settings", "description": "Application settings"},
]

__all__ = ["debug_router", "openapi_tags"]
