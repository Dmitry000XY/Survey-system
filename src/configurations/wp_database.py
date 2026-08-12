from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from .session_manager import AsyncSessionManager
from .wp_settings import get_wp_settings

__all__ = ["close_wp_database", "get_wp_async_session", "wp_database_session", "wp_global_init"]

_session_manager = AsyncSessionManager()


def wp_global_init() -> None:
    settings = get_wp_settings()
    _session_manager.initialize(settings.database_url_asyncmy, echo=settings.ECHO)


async def close_wp_database() -> None:
    await _session_manager.dispose()


def wp_database_session() -> AbstractAsyncContextManager[AsyncSession]:
    """Return an application-level context manager for a WordPress database session."""
    return _session_manager.session()


async def get_wp_async_session() -> AsyncGenerator[AsyncSession]:
    """Provide a WordPress database session as a FastAPI yield dependency."""
    async with wp_database_session() as session:
        yield session
