import asyncio
from collections.abc import Callable, Coroutine
from types import SimpleNamespace
from typing import Any, TypeVar, cast
from unittest.mock import AsyncMock

import pytest

from src.exceptions import ResourceNotFoundError
from src.repositories.answers import AnswerRepository
from src.repositories.clients import ClientRepository
from src.repositories.questionnaire_answers import QuestionnaireAnswerRepository
from src.repositories.questionnaires import QuestionnaireRepository
from src.repositories.questions import QuestionRepository
from src.repositories.settings import SettingRepository
from src.repositories.users import UserRepository
from src.repositories.users_clients import UserClientRepository
from src.services.answers import AnswerService
from src.services.clients import ClientService
from src.services.questionnaire_answers import QuestionnaireAnswerService
from src.services.questionnaires import QuestionnaireService
from src.services.questions import QuestionService
from src.services.settings import SettingService
from src.services.users import UserService
from src.services.users_clients import UserClientService

ServiceCall = Callable[[], Coroutine[Any, Any, object]]
RepositoryT = TypeVar("RepositoryT")


def _repository(_repository_type: type[RepositoryT], **methods: object) -> RepositoryT:
    return cast(
        RepositoryT, SimpleNamespace(**{name: AsyncMock(return_value=value) for name, value in methods.items()})
    )


user_service = UserService(_repository(UserRepository, get_user=None, delete_user=False))
client_service = ClientService(_repository(ClientRepository, get_client=None, delete_client=False))
question_service = QuestionService(_repository(QuestionRepository, get_question=None, delete_question=False))
questionnaire_service = QuestionnaireService(
    _repository(QuestionnaireRepository, get_questionnaire=None, delete_questionnaire=False)
)
questionnaire_answer_service = QuestionnaireAnswerService(
    _repository(
        QuestionnaireAnswerRepository,
        get_questionnaire_answer=None,
        delete_questionnaire_answer=False,
    )
)
user_client_service = UserClientService(
    _repository(UserClientRepository, get_user_client=None, delete_user_client=False)
)
answer_service = AnswerService(
    _repository(AnswerRepository, get_answer=None, delete_answer=False),
    _repository(QuestionRepository),
    _repository(QuestionnaireAnswerRepository),
)
setting_service = SettingService(_repository(SettingRepository, get_setting=None))


@pytest.mark.parametrize(
    ("service_call", "resource", "details"),
    [
        (lambda: user_service.get_user(7), "user", {"user_id": 7}),
        (lambda: client_service.get_client(7), "client", {"client_id": 7}),
        (lambda: question_service.get_question(7), "question", {"question_id": 7}),
        (
            lambda: questionnaire_service.get_questionnaire(7, 2),
            "questionnaire",
            {"questionnaire_id": 7, "questionnaire_version": 2},
        ),
        (
            lambda: questionnaire_answer_service.get_questionnaire_answer(7),
            "questionnaire answer",
            {"questionnaire_answer_id": 7},
        ),
        (
            lambda: user_client_service.get_user_client(7, 2),
            "user-client link",
            {"user_id": 7, "client_id": 2},
        ),
        (
            lambda: answer_service.get_answer(7, 2),
            "answer",
            {"question_id": 7, "questionnaire_answer_id": 2},
        ),
        (lambda: setting_service.get_setting(), "settings", {}),
    ],
)
def test_missing_resources_have_consistent_service_errors(
    service_call: ServiceCall,
    resource: str,
    details: dict[str, int],
) -> None:
    with pytest.raises(ResourceNotFoundError) as exception_info:
        asyncio.run(service_call())

    assert exception_info.value.message == f"{resource.capitalize()} was not found."
    assert exception_info.value.details == details


@pytest.mark.parametrize(
    ("service_call", "details"),
    [
        (lambda: user_service.delete_user(7), {"user_id": 7}),
        (lambda: client_service.delete_client(7), {"client_id": 7}),
        (lambda: question_service.delete_question(7), {"question_id": 7}),
        (
            lambda: questionnaire_service.delete_questionnaire(7, 2),
            {"questionnaire_id": 7, "questionnaire_version": 2},
        ),
        (
            lambda: questionnaire_answer_service.delete_questionnaire_answer(7),
            {"questionnaire_answer_id": 7},
        ),
        (lambda: user_client_service.delete_user_client(7, 2), {"user_id": 7, "client_id": 2}),
        (
            lambda: answer_service.delete_answer(7, 2),
            {"question_id": 7, "questionnaire_answer_id": 2},
        ),
    ],
)
def test_missing_deletes_have_consistent_service_errors(
    service_call: ServiceCall,
    details: dict[str, int],
) -> None:
    with pytest.raises(ResourceNotFoundError) as exception_info:
        asyncio.run(service_call())

    assert exception_info.value.details == details
