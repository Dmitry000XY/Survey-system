import logging

from typing import AsyncGenerator, Callable, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.models import BaseModel
import src.models  # noqa F401

from .settings import settings

logger = logging.getLogger("__name__")

__all__ = ["global_init", "get_async_session", "create_db_and_tables", "delete_db_and_tables"]

__async_engine: Optional[AsyncEngine] = None
__session_factory: Optional[Callable[[], AsyncSession]] = None


def global_init() -> None:
    global __async_engine, __session_factory

    if __session_factory:
        return

    if not __async_engine:
        __async_engine = create_async_engine(
            url=settings.database_url_asyncpg,
            echo=settings.ECHO
        )

    __session_factory = async_sessionmaker(__async_engine)


async def get_async_session() -> AsyncGenerator:
    global __session_factory

    if not __session_factory:
        raise ValueError({"message": "You must call global_init() before using this method."})

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


async def create_db_and_tables():
    global __async_engine

    if __async_engine is None:
        raise ValueError({"message": "You must call global_init() before using this method."})

    async with __async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def delete_db_and_tables():
    global __async_engine

    if __async_engine is None:
        raise ValueError({"message": "You must call global_init() before using this method."})

    async with __async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
