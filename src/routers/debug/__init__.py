from .users import users_router
from .clients import clients_router
from .users_clients import users_clients_router
from .questionnaire_answers import questionnaire_answers_router
from .answers import answers_router
from .questionnaires import questionnaires_router
from .questions import questions_router
from .settings import settings_router

__all__ = [
    "users_router", "clients_router", "users_clients_router",
    "questionnaire_answers_router", "answers_router", "questionnaires_router",
    "questions_router", "settings_router"
]
