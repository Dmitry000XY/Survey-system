from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.configurations.constants import INITIAL_SYNCHRONIZATION_TIME

__all__ = ["SettingBase", "SettingUpdate", "SettingOut"]


class SettingBase(BaseModel):
    last_synchronization_time: datetime = INITIAL_SYNCHRONIZATION_TIME


class SettingUpdate(SettingBase):
    pass


# В схеме для настроек нет смысла возвращать id, так как таблица всегда содержит единственную запись
class SettingOut(SettingBase):
    model_config = ConfigDict(from_attributes=True)
