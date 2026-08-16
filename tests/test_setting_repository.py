import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import cast
from unittest.mock import AsyncMock

from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.settings import Setting
from src.repositories.settings import SettingRepository


def test_ensure_settings_uses_an_atomic_postgresql_insert() -> None:
    setting = Setting(id=1, last_synchronization_time=datetime(1970, 1, 1, tzinfo=UTC))
    result = SimpleNamespace(scalar_one_or_none=lambda: setting)
    session = SimpleNamespace(execute=AsyncMock(return_value=result), get=AsyncMock())
    repository = SettingRepository(cast(AsyncSession, session))

    ensured, created = asyncio.run(repository.ensure_settings())

    statement = session.execute.await_args.args[0]
    sql = str(statement.compile(dialect=postgresql.dialect()))
    assert "ON CONFLICT (id) DO NOTHING" in sql
    assert ensured is setting
    assert created is True
    session.get.assert_not_awaited()


def test_ensure_settings_returns_the_existing_singleton_after_a_conflict() -> None:
    setting = Setting(id=1, last_synchronization_time=datetime(1970, 1, 1, tzinfo=UTC))
    result = SimpleNamespace(scalar_one_or_none=lambda: None)
    session = SimpleNamespace(
        execute=AsyncMock(return_value=result),
        get=AsyncMock(return_value=setting),
    )
    repository = SettingRepository(cast(AsyncSession, session))

    ensured, created = asyncio.run(repository.ensure_settings())

    assert ensured is setting
    assert created is False
    session.get.assert_awaited_once_with(Setting, 1)
