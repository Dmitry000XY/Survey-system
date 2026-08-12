import asyncio
import logging

from src.configurations import database_session, wp_database_session
from src.configurations.constants import SYNC_INTERVAL_SECONDS
from src.dependencies import get_synchronization_service

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
            async with database_session() as session, wp_database_session() as wp_session:
                service = get_synchronization_service(session, wp_session)
                logger.info("Starting synchronization iteration")
                await service.sync_all()
                logger.info("Synchronization iteration completed successfully")
        except Exception as error:
            logger.exception("Synchronization iteration failed: %s", error)
        await asyncio.sleep(SYNC_INTERVAL_SECONDS)


def start_synchronization() -> asyncio.Task[None]:
    """
    Запускает фоновую задачу синхронизации.
    """
    task = asyncio.create_task(_synchronization_loop(), name="questionnaire-synchronization")
    logger.info("Synchronization background loop started with interval %s seconds", SYNC_INTERVAL_SECONDS)
    return task


async def stop_synchronization(task: asyncio.Task[None]) -> None:
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Synchronization background loop stopped")
