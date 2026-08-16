import asyncio
from types import SimpleNamespace
from typing import cast
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import RepositoryConflictError, RepositoryError
from src.repositories.base import BaseRepository


def test_execute_translates_integrity_errors_to_repository_conflicts() -> None:
    database_error = IntegrityError("INSERT", {}, RuntimeError("unique constraint"))
    session = SimpleNamespace(execute=AsyncMock(side_effect=database_error))
    repository = BaseRepository(cast(AsyncSession, session))

    with pytest.raises(RepositoryConflictError) as exception_info:
        asyncio.run(repository._execute(select(1), operation="create"))

    assert exception_info.value.entity == "resource"
    assert exception_info.value.operation == "create"
    assert exception_info.value.__cause__ is database_error


def test_execute_translates_sqlalchemy_errors_to_repository_errors() -> None:
    database_error = SQLAlchemyError("connection failed")
    session = SimpleNamespace(execute=AsyncMock(side_effect=database_error))
    repository = BaseRepository(cast(AsyncSession, session))

    with pytest.raises(RepositoryError) as exception_info:
        asyncio.run(repository._execute(select(1), operation="read"))

    assert type(exception_info.value) is RepositoryError
    assert exception_info.value.entity == "resource"
    assert exception_info.value.operation == "read"
    assert exception_info.value.__cause__ is database_error
