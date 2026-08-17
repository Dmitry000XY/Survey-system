from typing import Any, TypeVar

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable

from src.exceptions import RepositoryConflictError, RepositoryError

ModelT = TypeVar("ModelT")


class BaseRepository:
    """Shared database operations with persistence-layer error translation."""

    entity_name = "resource"

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get(self, model: type[ModelT], identity: Any, *, operation: str = "read") -> ModelT | None:
        try:
            return await self.session.get(model, identity)
        except SQLAlchemyError as exc:
            raise RepositoryError(self.entity_name, operation) from exc

    async def _execute(self, statement: Executable, *, operation: str):
        try:
            return await self.session.execute(statement)
        except IntegrityError as exc:
            raise RepositoryConflictError(self.entity_name, operation) from exc
        except SQLAlchemyError as exc:
            raise RepositoryError(self.entity_name, operation) from exc

    async def _flush(self, *, operation: str) -> None:
        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise RepositoryConflictError(self.entity_name, operation) from exc
        except SQLAlchemyError as exc:
            raise RepositoryError(self.entity_name, operation) from exc

    async def _delete(self, instance: object) -> None:
        try:
            await self.session.delete(instance)
            await self.session.flush()
        except IntegrityError as exc:
            raise RepositoryConflictError(self.entity_name, "delete") from exc
        except SQLAlchemyError as exc:
            raise RepositoryError(self.entity_name, "delete") from exc
