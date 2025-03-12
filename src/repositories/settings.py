from sqlalchemy import select, update
from src.models.settings import Setting


class SettingRepository:
    def __init__(self, session):
        self.session = session

    async def get_setting(self):
        query = select(Setting)
        res = await self.session.execute(query)
        return res.scalars().first()

    async def update_setting(self, new_data):
        query = (
            update(Setting)
            .where(Setting.id == 1)
            .values(last_synchronization_time=new_data.last_synchronization_time)
            .returning(Setting)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def create_setting(self, setting):
        new_setting = Setting(
            last_synchronization_time=setting.last_synchronization_time
        )
        self.session.add(new_setting)
        await self.session.flush()
        return new_setting
