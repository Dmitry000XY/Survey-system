from collections.abc import AsyncGenerator
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from src.configurations import close_database, close_wp_database, database_session, global_init, wp_global_init
from src.dependencies import get_setting_service
from src.extras.synchronization_runner import start_synchronization, stop_synchronization


async def _ensure_settings() -> None:
    async with database_session() as session:
        service = get_setting_service(session)
        await service.ensure_settings()


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator[None]:
    async with AsyncExitStack() as stack:
        global_init()
        stack.push_async_callback(close_database)

        wp_global_init()
        stack.push_async_callback(close_wp_database)

        await _ensure_settings()

        synchronization_task = start_synchronization()
        stack.push_async_callback(stop_synchronization, synchronization_task)

        yield
