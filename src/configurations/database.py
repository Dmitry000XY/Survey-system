from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from .session_manager import AsyncSessionManager
from .settings import get_settings

__all__ = ["close_database", "database_session", "get_async_session", "global_init"]

_session_manager = AsyncSessionManager()


def global_init() -> None:
    settings = get_settings()
    _session_manager.initialize(settings.database_url_asyncpg, echo=settings.ECHO)


async def close_database() -> None:
    await _session_manager.dispose()


def database_session() -> AbstractAsyncContextManager[AsyncSession]:
    """Return an application-level context manager for a database session."""
    return _session_manager.session()


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    """Provide a database session as a FastAPI yield dependency."""
    async with database_session() as session:
        yield session
