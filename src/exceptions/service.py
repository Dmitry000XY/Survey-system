from collections.abc import Mapping
from typing import Any


class ServiceError(Exception):
    """Base exception safe to translate into a public API error."""

    code = "service_error"

    def __init__(self, message: str, *, details: Mapping[str, Any] | None = None) -> None:
        self.message = message
        self.details = dict(details) if details is not None else None
        super().__init__(message)


class ResourceNotFoundError(ServiceError):
    code = "resource_not_found"

    def __init__(self, resource: str, *, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(f"{resource.capitalize()} was not found.", details=details)


class ResourceConflictError(ServiceError):
    code = "resource_conflict"


class DomainValidationError(ServiceError):
    code = "domain_validation_error"


class ServiceUnavailableError(ServiceError):
    code = "service_unavailable"

    def __init__(self) -> None:
        super().__init__("The service is temporarily unavailable.")
