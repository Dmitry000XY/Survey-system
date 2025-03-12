from pydantic import BaseModel
from datetime import datetime

__all__ = ["SettingBase", "SettingUpdate", "SettingOut"]


class SettingBase(BaseModel):
    last_synchronization_time: datetime


class SettingUpdate(SettingBase):
    pass


# В схеме для настроек нет смысла возвращать id, так как таблица всегда содержит единственную запись
class SettingOut(SettingBase):
    class Config:
        from_attributes = True
