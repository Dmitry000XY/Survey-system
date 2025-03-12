from fastapi import Response, status
from src.repositories.settings import SettingRepository


class SettingService:
    def __init__(self, setting_repository: SettingRepository):
        self.setting_repository = setting_repository

    async def get_setting(self):
        setting = await self.setting_repository.get_setting()
        if not setting:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return setting

    async def update_setting(self, new_data):
        if await self.setting_repository.get_setting():
            return await self.setting_repository.update_setting(new_data)
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    async def create_setting(self, setting):
        # Если в таблице уже есть запись, возвращаем ошибку
        if await self.setting_repository.get_setting():
            return Response(
                status_code=status.HTTP_409_CONFLICT,
                content="Settings already exist. Only one settings row is allowed."
            )
        return await self.setting_repository.create_setting(setting)

    async def init_settings(self, new_data):
        existing = await self.setting_repository.get_setting()
        if existing:
            return existing, False
        created = await self.setting_repository.create_setting(new_data)
        return created, True
