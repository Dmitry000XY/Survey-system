import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.extras import synchronization_runner


class _SynchronizationServiceStub:
    def __init__(self, events: list[str]) -> None:
        self.events = events

    async def sync_all(self) -> None:
        self.events.append("sync")
        raise asyncio.CancelledError


def test_synchronization_loop_uses_session_context_managers(monkeypatch: pytest.MonkeyPatch) -> None:
    events: list[str] = []
    session = cast(AsyncSession, SimpleNamespace())
    wp_session = cast(AsyncSession, SimpleNamespace())

    @asynccontextmanager
    async def database_session() -> AsyncGenerator[AsyncSession]:
        events.append("database_enter")
        try:
            yield session
        finally:
            events.append("database_exit")

    @asynccontextmanager
    async def wp_database_session() -> AsyncGenerator[AsyncSession]:
        events.append("wordpress_enter")
        try:
            yield wp_session
        finally:
            events.append("wordpress_exit")

    def get_synchronization_service(
        received_session: AsyncSession,
        received_wp_session: AsyncSession,
    ) -> _SynchronizationServiceStub:
        assert received_session is session
        assert received_wp_session is wp_session
        return _SynchronizationServiceStub(events)

    monkeypatch.setattr(synchronization_runner, "database_session", database_session)
    monkeypatch.setattr(synchronization_runner, "wp_database_session", wp_database_session)
    monkeypatch.setattr(synchronization_runner, "get_synchronization_service", get_synchronization_service)

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(synchronization_runner._synchronization_loop())

    assert events == ["database_enter", "wordpress_enter", "sync", "wordpress_exit", "database_exit"]
