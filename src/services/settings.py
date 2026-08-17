from src.repositories.settings import SettingRepository
from src.schemas.settings import SettingOut, SettingUpdate

from .base import BaseService


class SettingService(BaseService):
    resource_name = "settings"

    def __init__(self, setting_repository: SettingRepository) -> None:
        self.setting_repository = setting_repository

    async def get_setting(self) -> SettingOut:
        setting = await self._run(self.setting_repository.get_setting())
        return self._to_schema(self._require(setting, details={}), SettingOut)

    async def update_setting(self, new_data: SettingUpdate) -> SettingOut:
        updated = await self._run(self.setting_repository.update_setting(new_data))
        return self._to_schema(self._require(updated, details={}), SettingOut)

    async def ensure_settings(self) -> tuple[SettingOut, bool]:
        setting, created = await self._run(self.setting_repository.ensure_settings())
        return self._to_schema(setting, SettingOut), created
