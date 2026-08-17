import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import JSONResponse

from src.exceptions import (
    DomainValidationError,
    ResourceConflictError,
    ResourceNotFoundError,
    ServiceError,
    ServiceUnavailableError,
)
from src.schemas.api import APIErrorResponse

logger = logging.getLogger(__name__)

SERVICE_ERROR_STATUS = {
    ResourceNotFoundError: HTTPStatus.NOT_FOUND,
    ResourceConflictError: HTTPStatus.CONFLICT,
    DomainValidationError: HTTPStatus.UNPROCESSABLE_ENTITY,
    ServiceUnavailableError: HTTPStatus.SERVICE_UNAVAILABLE,
}


def _error_response(
    status_code: int,
    code: str,
    message: str,
    details: dict | None = None,
) -> JSONResponse:
    status = HTTPStatus(status_code) if status_code in HTTPStatus._value2member_map_ else None
    payload = APIErrorResponse(
        title=status.phrase if status else "HTTP error",
        status=status_code,
        code=code,
        message=message,
        details=details or {},
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(payload))


async def service_error_handler(_request: Request, exception: Exception) -> JSONResponse:
    if not isinstance(exception, ServiceError):
        raise exception
    exc = exception
    status_code = next(
        (status for error_type, status in SERVICE_ERROR_STATUS.items() if isinstance(exc, error_type)),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        logger.error("Service error: %s", exc, exc_info=exc)
    return _error_response(status_code, exc.code, exc.message, exc.details)


async def validation_error_handler(_request: Request, exception: Exception) -> JSONResponse:
    if not isinstance(exception, RequestValidationError):
        raise exception
    exc = exception
    violations = [
        {
            "code": error["type"],
            "message": error["msg"],
            "location": [str(part) for part in error["loc"]],
        }
        for error in exc.errors()
    ]
    return _error_response(
        HTTPStatus.UNPROCESSABLE_ENTITY,
        "request_validation_error",
        "The request is invalid.",
        {"violations": violations},
    )


async def http_error_handler(request: Request, exception: Exception) -> JSONResponse:
    if not isinstance(exception, StarletteHTTPException):
        raise exception
    exc = exception
    if exc.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        logger.error(
            "HTTP %s server error for %s %s",
            exc.status_code,
            request.method,
            request.url.path,
        )
        return _error_response(
            exc.status_code,
            f"http_{exc.status_code}",
            "An unexpected error occurred.",
        )

    phrase = HTTPStatus(exc.status_code).phrase if exc.status_code in HTTPStatus._value2member_map_ else "HTTP error"
    message = exc.detail if isinstance(exc.detail, str) else phrase
    return _error_response(exc.status_code, f"http_{exc.status_code}", message)


async def unexpected_error_handler(_request: Request, exception: Exception) -> JSONResponse:
    logger.error("Unhandled request error", exc_info=exception)
    return _error_response(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "internal_server_error",
        "An unexpected error occurred.",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register the API boundary's error translation in one place."""

    app.add_exception_handler(ServiceError, service_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)
