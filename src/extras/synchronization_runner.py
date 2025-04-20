import asyncio
import logging

from src.configurations.constants import SYNC_INTERVAL_SECONDS
from src.configurations.database import get_async_session
from src.configurations.wp_database import get_wp_async_session
from src.dependencies.dependencies import get_synchronization_service

logger = logging.getLogger(__name__)


async def _synchronization_loop() -> None:
    """
    Бесконечный цикл синхронизации:
    1. Получает сессии основной и WP БД
    2. Создаёт сервис синхронизации
    3. Вызывает sync_all(), логирует успех или ошибку
    4. Ждёт SYNC_INTERVAL_SECONDS перед следующей итерацией
    """
    while True:
        try:
            async for session in get_async_session():
                async for wp_session in get_wp_async_session():
                    service = get_synchronization_service(session, wp_session)
                    logger.info("Starting synchronization iteration")
                    await service.sync_all()
                    logger.info("Synchronization iteration completed successfully")
        except Exception as error:
            logger.exception("Synchronization iteration failed: %s", error)
        await asyncio.sleep(SYNC_INTERVAL_SECONDS)


def start_synchronization() -> None:
    """
    Запускает фоновую задачу синхронизации.
    """
    asyncio.create_task(_synchronization_loop())
    logger.info("Synchronization background loop started with interval %s seconds", SYNC_INTERVAL_SECONDS)
