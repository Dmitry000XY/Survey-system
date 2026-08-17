from collections.abc import Awaitable, Sequence
from typing import TypeVar

from pydantic import BaseModel

from src.exceptions import (
    RepositoryConflictError,
    RepositoryError,
    ResourceConflictError,
    ResourceNotFoundError,
    ServiceUnavailableError,
)

OperationResultT = TypeVar("OperationResultT")
SchemaT = TypeVar("SchemaT", bound=BaseModel)


class BaseService:
    """Translate persistence failures into application-layer errors."""

    resource_name = "resource"

    async def _run(
        self,
        operation: Awaitable[OperationResultT],
        *,
        conflict_message: str | None = None,
    ) -> OperationResultT:
        try:
            return await operation
        except RepositoryConflictError as exc:
            message = conflict_message or f"{self.resource_name.capitalize()} conflicts with existing data."
            raise ResourceConflictError(message) from exc
        except RepositoryError as exc:
            raise ServiceUnavailableError() from exc

    def _require(self, value: OperationResultT | None, *, details: dict[str, int]) -> OperationResultT:
        if value is None:
            raise ResourceNotFoundError(self.resource_name, details=details)
        return value

    @staticmethod
    def _to_schema(value: object, schema_type: type[SchemaT]) -> SchemaT:
        return schema_type.model_validate(value)

    @classmethod
    def _to_schema_list(cls, values: Sequence[object], schema_type: type[SchemaT]) -> list[SchemaT]:
        return [cls._to_schema(value, schema_type) for value in values]
