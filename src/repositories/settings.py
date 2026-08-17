from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import RepositoryError
from src.models.settings import Setting
from src.schemas.settings import SettingUpdate

from .base import BaseRepository


class SettingRepository(BaseRepository):
    entity_name = "settings"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_setting(self) -> Setting | None:
        return await self._get(Setting, 1)

    async def update_setting(self, new_data: SettingUpdate) -> Setting | None:
        values = new_data.model_dump(exclude_unset=True, exclude_none=True)
        if not values:
            return await self.get_setting()
        query = update(Setting).where(Setting.id == 1).values(**values).returning(Setting)
        result = await self._execute(query, operation="update")
        return result.scalar_one_or_none()

    async def ensure_settings(self) -> tuple[Setting, bool]:
        statement = insert(Setting).values(id=1).on_conflict_do_nothing(index_elements=[Setting.id]).returning(Setting)
        result = await self._execute(statement, operation="initialize")
        created = result.scalar_one_or_none()
        if created is not None:
            return created, True

        existing = await self._get(Setting, 1, operation="initialize")
        if existing is None:
            raise RepositoryError(self.entity_name, "initialize")
        return existing, False
