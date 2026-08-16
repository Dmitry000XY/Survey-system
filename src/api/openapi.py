from typing import Any

from src.schemas.api import APIErrorResponse

ErrorResponses = dict[int | str, dict[str, Any]]


def _error(description: str) -> dict[str, Any]:
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": APIErrorResponse.model_json_schema(),
            }
        },
    }


COMMON_ERROR_RESPONSES: ErrorResponses = {
    422: _error("Request or domain validation failed"),
    500: _error("Unexpected server error"),
    503: _error("Persistence service unavailable"),
}
NOT_FOUND_RESPONSE: ErrorResponses = {404: _error("Resource not found")}
CONFLICT_RESPONSE: ErrorResponses = {409: _error("Resource conflict")}
NOT_FOUND_OR_CONFLICT_RESPONSES: ErrorResponses = NOT_FOUND_RESPONSE | CONFLICT_RESPONSE
