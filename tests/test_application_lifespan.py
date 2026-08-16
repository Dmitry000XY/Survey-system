import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application import lifespan as lifespan_module


def test_lifespan_initializes_settings_and_releases_resources_in_reverse_order(monkeypatch) -> None:
    events: list[str] = []
    session = object()
    synchronization_task = object()

    @asynccontextmanager
    async def database_session():
        events.append("session_enter")
        try:
            yield session
        finally:
            events.append("session_exit")

    class _SettingServiceStub:
        async def ensure_settings(self) -> None:
            events.append("ensure_settings")

    async def close_database() -> None:
        events.append("close_database")

    async def close_wp_database() -> None:
        events.append("close_wp_database")

    async def stop_synchronization(task: object) -> None:
        assert task is synchronization_task
        events.append("stop_synchronization")

    monkeypatch.setattr(lifespan_module, "global_init", lambda: events.append("global_init"))
    monkeypatch.setattr(lifespan_module, "wp_global_init", lambda: events.append("wp_global_init"))
    monkeypatch.setattr(lifespan_module, "database_session", database_session)
    monkeypatch.setattr(lifespan_module, "get_setting_service", lambda current: _SettingServiceStub())
    monkeypatch.setattr(lifespan_module, "start_synchronization", lambda: synchronization_task)
    monkeypatch.setattr(lifespan_module, "stop_synchronization", stop_synchronization)
    monkeypatch.setattr(lifespan_module, "close_wp_database", close_wp_database)
    monkeypatch.setattr(lifespan_module, "close_database", close_database)

    async def run_lifespan() -> None:
        async with lifespan_module.lifespan(FastAPI()):
            events.append("application_running")

    asyncio.run(run_lifespan())

    assert events == [
        "global_init",
        "wp_global_init",
        "session_enter",
        "ensure_settings",
        "session_exit",
        "application_running",
        "stop_synchronization",
        "close_wp_database",
        "close_database",
    ]
