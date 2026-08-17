from dataclasses import dataclass
from datetime import UTC, datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

from src.application import create_application
from src.configurations.constants import AnswerTypeEnum
from src.dependencies import (
    get_answer_service,
    get_client_service,
    get_question_service,
    get_questionnaire_answer_service,
    get_questionnaire_service,
    get_setting_service,
    get_user_client_service,
    get_user_service,
)
from src.schemas.answers import AnswerOut
from src.schemas.clients import ClientOut, ClientOutWithAPI
from src.schemas.questionnaire_answers import QuestionnaireAnswerDetail, QuestionnaireAnswerOut
from src.schemas.questionnaires import QuestionnaireDetail, QuestionnaireOut
from src.schemas.questions import QuestionOut
from src.schemas.settings import SettingOut
from src.schemas.users import UserOut
from src.schemas.users_clients import UserClientOut

NOW = datetime(2026, 1, 1, tzinfo=UTC)
PASSWORD_HASH = "$P$" + "a" * 31
QUESTIONNAIRE_HASH = "a" * 64

USER = UserOut(user_id=1, login="dmitry", time_created=NOW, time_updated=NOW)
CLIENT = ClientOut(client_id=1, client_name="telegram", time_created=NOW)
CLIENT_WITH_API = ClientOutWithAPI(
    client_id=1,
    client_name="telegram",
    time_created=NOW,
    api_key="generated-api-key",
)
USER_CLIENT = UserClientOut(user_id=1, client_id=1, user_client_id=100)
ANSWER = AnswerOut(question_id=1, questionnaire_answer_id=1, answer="yes", time_created=NOW)
QUESTION = QuestionOut(
    question_id=1,
    questionnaire_id=1,
    questionnaire_version=1,
    question="Question?",
    question_order=0,
    answer_type=AnswerTypeEnum.TEXT,
    wordpress_id=10,
    time_created=NOW,
)
QUESTIONNAIRE = QuestionnaireOut(
    questionnaire_id=1,
    questionnaire_version=1,
    questionnaire_name="Questionnaire",
    wordpress_id=10,
    tags=[],
    questionnaire_hash=QUESTIONNAIRE_HASH,
    time_created=NOW,
)
QUESTIONNAIRE_DETAIL = QuestionnaireDetail(**QUESTIONNAIRE.model_dump(), questions=[QUESTION])
QUESTIONNAIRE_ANSWER = QuestionnaireAnswerOut(
    questionnaire_answer_id=1,
    user_id=1,
    questionnaire_id=1,
    questionnaire_version=1,
    client_id=1,
    time_started=NOW,
)
QUESTIONNAIRE_ANSWER_DETAIL = QuestionnaireAnswerDetail(
    **QUESTIONNAIRE_ANSWER.model_dump(),
    answers=[ANSWER],
)
SETTINGS = SettingOut(last_synchronization_time=NOW)


class _DebugServiceStub:
    async def create_user(self, _user):
        return USER

    async def get_all_users(self):
        return [USER]

    async def get_user(self, _user_id: int):
        return USER

    async def update_user(self, _user_id: int, _new_data):
        return USER

    async def delete_user(self, _user_id: int) -> None:
        return None

    async def create_client(self, _client):
        return CLIENT_WITH_API

    async def get_all_clients(self):
        return [CLIENT]

    async def get_client(self, _client_id: int):
        return CLIENT

    async def update_client(self, _client_id: int, _new_data):
        return CLIENT

    async def delete_client(self, _client_id: int) -> None:
        return None

    async def create_user_client(self, _user_client):
        return USER_CLIENT

    async def get_user_client(self, _user_id: int, _client_id: int):
        return USER_CLIENT

    async def delete_user_client(self, _user_id: int, _client_id: int) -> None:
        return None

    async def create_answer(self, _answer):
        return ANSWER

    async def get_all_answers(self):
        return [ANSWER]

    async def get_answer(self, _question_id: int, _questionnaire_answer_id: int):
        return ANSWER

    async def update_answer(self, _question_id: int, _questionnaire_answer_id: int, _new_data):
        return ANSWER

    async def delete_answer(self, _question_id: int, _questionnaire_answer_id: int) -> None:
        return None

    async def create_question(self, _question):
        return QUESTION

    async def get_all_questions(self):
        return [QUESTION]

    async def get_question(self, _question_id: int):
        return QUESTION

    async def update_question(self, _question_id: int, _new_data):
        return QUESTION

    async def delete_question(self, _question_id: int) -> None:
        return None

    async def create_questionnaire(self, _questionnaire):
        return QUESTIONNAIRE

    async def get_all_questionnaires(self):
        return [QUESTIONNAIRE]

    async def get_latest_versions(self):
        return [QUESTIONNAIRE]

    async def deactivate_questionnaires(self, _questionnaire_ids: list[int]):
        return 1

    async def get_questionnaire(self, _questionnaire_id: int, _questionnaire_version: int):
        return QUESTIONNAIRE

    async def get_questionnaire_detail(self, _questionnaire_id: int, _questionnaire_version: int):
        return QUESTIONNAIRE_DETAIL

    async def update_questionnaire(self, _questionnaire_id: int, _questionnaire_version: int, _new_data):
        return QUESTIONNAIRE

    async def delete_questionnaire(self, _questionnaire_id: int, _questionnaire_version: int) -> None:
        return None

    async def create_questionnaire_answer(self, _questionnaire_answer):
        return QUESTIONNAIRE_ANSWER

    async def get_all_questionnaire_answers(self):
        return [QUESTIONNAIRE_ANSWER]

    async def get_questionnaire_answer(self, _questionnaire_answer_id: int):
        return QUESTIONNAIRE_ANSWER

    async def get_questionnaire_answer_detail(self, _questionnaire_answer_id: int):
        return QUESTIONNAIRE_ANSWER_DETAIL

    async def update_questionnaire_answer(self, _questionnaire_answer_id: int, _new_data):
        return QUESTIONNAIRE_ANSWER

    async def delete_questionnaire_answer(self, _questionnaire_answer_id: int) -> None:
        return None

    async def get_setting(self):
        return SETTINGS

    async def update_setting(self, _new_data):
        return SETTINGS

    async def ensure_settings(self):
        return SETTINGS, False


@dataclass(frozen=True)
class EndpointCase:
    method: str
    path: str
    status_code: int
    payload: dict[str, object] | None = None


USER_PAYLOAD = {"user_id": 1, "login": "dmitry", "password_hash": PASSWORD_HASH}
QUESTION_PAYLOAD = {
    "questionnaire_id": 1,
    "questionnaire_version": 1,
    "question": "Question?",
    "question_order": 0,
    "answer_options": [],
    "answer_type": "TEXT",
    "wordpress_id": 10,
}
QUESTIONNAIRE_PAYLOAD = {
    "questionnaire_id": 1,
    "questionnaire_version": 1,
    "questionnaire_name": "Questionnaire",
    "wordpress_id": 10,
    "tags": [],
    "is_active": True,
    "questionnaire_hash": QUESTIONNAIRE_HASH,
}
QUESTIONNAIRE_ANSWER_PAYLOAD = {
    "user_id": 1,
    "questionnaire_id": 1,
    "questionnaire_version": 1,
    "client_id": 1,
}

ENDPOINT_CASES = [
    EndpointCase("POST", "/api/debug/users", 201, USER_PAYLOAD),
    EndpointCase("GET", "/api/debug/users", 200),
    EndpointCase("GET", "/api/debug/users/1", 200),
    EndpointCase("PATCH", "/api/debug/users/1", 200, {"login": "updated"}),
    EndpointCase("DELETE", "/api/debug/users/1", 204),
    EndpointCase("POST", "/api/debug/clients", 201, {"client_name": "telegram"}),
    EndpointCase("GET", "/api/debug/clients", 200),
    EndpointCase("GET", "/api/debug/clients/1", 200),
    EndpointCase("PATCH", "/api/debug/clients/1", 200, {"client_name": "updated"}),
    EndpointCase("DELETE", "/api/debug/clients/1", 204),
    EndpointCase("POST", "/api/debug/users-clients", 201, {"user_id": 1, "client_id": 1, "user_client_id": 100}),
    EndpointCase("GET", "/api/debug/users-clients/1/1", 200),
    EndpointCase("DELETE", "/api/debug/users-clients/1/1", 204),
    EndpointCase("POST", "/api/debug/answers", 201, {"question_id": 1, "questionnaire_answer_id": 1, "answer": "yes"}),
    EndpointCase("GET", "/api/debug/answers", 200),
    EndpointCase("GET", "/api/debug/answers/1/1", 200),
    EndpointCase("PATCH", "/api/debug/answers/1/1", 200, {"answer": "no"}),
    EndpointCase("DELETE", "/api/debug/answers/1/1", 204),
    EndpointCase("POST", "/api/debug/questions", 201, QUESTION_PAYLOAD),
    EndpointCase("GET", "/api/debug/questions", 200),
    EndpointCase("GET", "/api/debug/questions/1", 200),
    EndpointCase("PATCH", "/api/debug/questions/1", 200, {"question": "Updated?"}),
    EndpointCase("DELETE", "/api/debug/questions/1", 204),
    EndpointCase("POST", "/api/debug/questionnaires", 201, QUESTIONNAIRE_PAYLOAD),
    EndpointCase("GET", "/api/debug/questionnaires", 200),
    EndpointCase("GET", "/api/debug/questionnaires/latest", 200),
    EndpointCase("POST", "/api/debug/questionnaires/deactivate", 200, {"questionnaire_ids": [1]}),
    EndpointCase("GET", "/api/debug/questionnaires/1/1", 200),
    EndpointCase("GET", "/api/debug/questionnaires/1/1/detail", 200),
    EndpointCase("PATCH", "/api/debug/questionnaires/1/1", 200, {"questionnaire_name": "Updated"}),
    EndpointCase("DELETE", "/api/debug/questionnaires/1/1", 204),
    EndpointCase("POST", "/api/debug/questionnaire-answers", 201, QUESTIONNAIRE_ANSWER_PAYLOAD),
    EndpointCase("GET", "/api/debug/questionnaire-answers", 200),
    EndpointCase("GET", "/api/debug/questionnaire-answers/1", 200),
    EndpointCase("GET", "/api/debug/questionnaire-answers/1/detail", 200),
    EndpointCase("PATCH", "/api/debug/questionnaire-answers/1", 200, {"time_finished": "2026-01-02T00:00:00Z"}),
    EndpointCase("DELETE", "/api/debug/questionnaire-answers/1", 204),
    EndpointCase("GET", "/api/debug/settings", 200),
    EndpointCase("PATCH", "/api/debug/settings", 200, {"last_synchronization_time": "2026-01-02T00:00:00Z"}),
    EndpointCase("PUT", "/api/debug/settings", 200),
]


def _create_client() -> TestClient:
    with patch("src.application.factory.get_settings") as get_settings:
        get_settings.return_value.ENABLE_DEBUG_API = True
        application = create_application()

    service = _DebugServiceStub()
    dependencies = [
        get_user_service,
        get_client_service,
        get_user_client_service,
        get_answer_service,
        get_question_service,
        get_questionnaire_service,
        get_questionnaire_answer_service,
        get_setting_service,
    ]
    for dependency in dependencies:
        application.dependency_overrides[dependency] = lambda: service

    return TestClient(application)


@pytest.mark.parametrize("case", ENDPOINT_CASES, ids=lambda case: f"{case.method} {case.path}")
def test_debug_endpoint_success_contract(case: EndpointCase) -> None:
    response = _create_client().request(case.method, case.path, json=case.payload)

    assert response.status_code == case.status_code, response.text
    if case.status_code == 204:
        assert response.content == b""
    else:
        assert response.headers["content-type"].startswith("application/json")
