from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.dependencies import get_client_service, get_setting_service, get_user_service
from src.exceptions import ResourceNotFoundError
from src.application import create_application


class _UserServiceStub:
    async def create_user(self, user):
        return SimpleNamespace(
            user_id=user.user_id,
            login=user.login,
            time_created=datetime(2026, 1, 1, tzinfo=UTC),
            time_updated=datetime(2026, 1, 1, tzinfo=UTC),
        )

    async def get_user(self, user_id: int):
        raise ResourceNotFoundError("user", details={"user_id": user_id})

    async def delete_user(self, _user_id: int) -> None:
        return None


class _FailingUserServiceStub(_UserServiceStub):
    async def get_user(self, user_id: int):
        del user_id
        raise RuntimeError("database credentials must not leak")


class _ClientServiceStub:
    async def create_client(self, client):
        return SimpleNamespace(
            client_id=7,
            client_name=client.client_name,
            time_created=datetime(2026, 1, 1, tzinfo=UTC),
            api_key="generated-api-key",
        )


class _SettingServiceStub:
    def __init__(self, *, created: bool) -> None:
        self.created = created

    async def ensure_settings(self):
        return SimpleNamespace(last_synchronization_time=datetime(1970, 1, 1, tzinfo=UTC)), self.created


def _create_debug_application() -> FastAPI:
    settings = SimpleNamespace(ENABLE_DEBUG_API=True)
    with patch("src.application.factory.get_settings", return_value=settings):
        return create_application()


def _client() -> TestClient:
    application = _create_debug_application()
    application.dependency_overrides[get_user_service] = lambda: _UserServiceStub()
    return TestClient(application)


def test_crud_payloads_are_request_bodies() -> None:
    schema = _create_debug_application().openapi()

    body_operations = [
        ("/api/debug/users", "post"),
        ("/api/debug/users/{user_id}", "patch"),
        ("/api/debug/clients", "post"),
        ("/api/debug/clients/{client_id}", "patch"),
        ("/api/debug/users-clients", "post"),
        ("/api/debug/answers", "post"),
        ("/api/debug/answers/{question_id}/{questionnaire_answer_id}", "patch"),
        ("/api/debug/questions", "post"),
        ("/api/debug/questions/{question_id}", "patch"),
        ("/api/debug/questionnaires", "post"),
        ("/api/debug/questionnaires/{questionnaire_id}/{questionnaire_version}", "patch"),
        ("/api/debug/questionnaires/deactivate", "post"),
        ("/api/debug/questionnaire-answers", "post"),
        ("/api/debug/questionnaire-answers/{questionnaire_answer_id}", "patch"),
        ("/api/debug/settings", "patch"),
    ]
    for path, method in body_operations:
        operation = schema["paths"][path][method]
        assert "requestBody" in operation
        assert all(parameter["in"] != "query" for parameter in operation.get("parameters", []))


def test_ensure_settings_has_no_request_body_and_reports_creation_status() -> None:
    schema = _create_debug_application().openapi()
    assert "requestBody" not in schema["paths"]["/api/debug/settings"]["put"]

    for created, expected_status in ((True, 201), (False, 200)):
        application = _create_debug_application()
        application.dependency_overrides[get_setting_service] = lambda: _SettingServiceStub(created=created)

        response = TestClient(application).put("/api/debug/settings")

        assert response.status_code == expected_status
        assert response.json() == {"last_synchronization_time": "1970-01-01T00:00:00Z"}


def test_openapi_documents_unified_error_responses() -> None:
    schema = _create_debug_application().openapi()
    response = schema["paths"]["/api/debug/users/{user_id}"]["get"]["responses"]["404"]

    assert set(response["content"]) == {"application/json"}
    assert response["content"]["application/json"]["schema"]["title"] == "APIErrorResponse"


def test_success_response_returns_resource_and_never_returns_password_hash() -> None:
    response = _client().post(
        "/api/debug/users",
        json={"user_id": 42, "login": "dmitry", "password_hash": "$P$B12345678abcdefghijklmnopqrstuv"},
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == 42
    assert "password_hash" not in response.text


def test_new_api_key_response_is_not_cacheable() -> None:
    application = _create_debug_application()
    application.dependency_overrides[get_client_service] = lambda: _ClientServiceStub()

    response = TestClient(application).post("/api/debug/clients", json={"client_name": "telegram"})

    assert response.status_code == 201
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["api_key"] == "generated-api-key"


def test_service_error_uses_unified_contract() -> None:
    response = _client().get("/api/debug/users/42")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {
        "title": "Not Found",
        "status": 404,
        "code": "resource_not_found",
        "message": "User was not found.",
        "details": {"user_id": 42},
    }


def test_validation_error_uses_unified_contract() -> None:
    response = _client().get("/api/debug/users/0")

    assert response.status_code == 422
    payload = response.json()
    assert response.headers["content-type"].startswith("application/json")
    assert payload["code"] == "request_validation_error"
    assert payload["message"] == "The request is invalid."
    assert payload["details"]["violations"]
    assert "input" not in payload["details"]["violations"][0]
    assert "message" in payload["details"]["violations"][0]


def test_framework_http_errors_use_unified_contract() -> None:
    response = _client().get("/missing-route")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()["code"] == "http_404"


def test_framework_http_server_errors_are_hidden_and_logged() -> None:
    application = _create_debug_application()

    @application.get("/explicit-server-error")
    async def explicit_server_error() -> None:
        raise HTTPException(status_code=500, detail="database credentials must not leak")

    client = TestClient(application, raise_server_exceptions=False)
    with patch("src.api.errors.logger.error") as log_error:
        response = client.get("/explicit-server-error")

    assert response.status_code == 500
    assert response.json() == {
        "title": "Internal Server Error",
        "status": 500,
        "code": "http_500",
        "message": "An unexpected error occurred.",
        "details": {},
    }
    assert "database credentials" not in response.text
    log_error.assert_called_once_with(
        "HTTP %s server error for %s %s",
        500,
        "GET",
        "/explicit-server-error",
    )


def test_delete_returns_an_empty_204_response() -> None:
    response = _client().delete("/api/debug/users/42")

    assert response.status_code == 204
    assert response.content == b""


def test_unexpected_errors_are_hidden_behind_unified_contract() -> None:
    application = _create_debug_application()
    application.dependency_overrides[get_user_service] = lambda: _FailingUserServiceStub()
    client = TestClient(application, raise_server_exceptions=False)

    response = client.get("/api/debug/users/42")

    assert response.status_code == 500
    assert response.json() == {
        "title": "Internal Server Error",
        "status": 500,
        "code": "internal_server_error",
        "message": "An unexpected error occurred.",
        "details": {},
    }
    assert "database credentials" not in response.text
