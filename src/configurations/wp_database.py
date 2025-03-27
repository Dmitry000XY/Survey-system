import logging

from typing import AsyncGenerator, Callable, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

import src.models  # noqa F401

from .wp_settings import wp_settings

logger = logging.getLogger("__name__")

__all__ = ["wp_global_init", "wp_get_async_session"]

__async_engine: Optional[AsyncEngine] = None
__session_factory: Optional[Callable[[], AsyncSession]] = None


def wp_global_init() -> None:
    global __async_engine, __session_factory

    if __session_factory:
        return

    if not __async_engine:
        __async_engine = create_async_engine(
            url=wp_settings.database_url_asyncmy,
            echo=wp_settings.ECHO
        )

    __session_factory = async_sessionmaker(__async_engine)


async def wp_get_async_session() -> AsyncGenerator:
    global __session_factory

    if not __session_factory:
        raise ValueError({"message": "You must call wp_global_init() before using this method."})

    session: AsyncSession = __session_factory()

    try:
        yield session
        await session.commit()
    except Exception as error:
        logger.error("Raises exception: %s", error)
        raise error
    finally:
        await session.rollback()
        await session.close()
