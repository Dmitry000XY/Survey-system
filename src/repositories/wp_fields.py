from sqlalchemy import select
from src.models.wp_fields import WPField


class WPFieldRepository:
    def __init__(self, session):
        self.session = session

    async def get_fields_by_form_id(self, form_id: int) -> list[WPField]:
        query = select(WPField).where(WPField.form_id == form_id).order_by(WPField.field_order)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_all_fields(self) -> list[WPField]:
        query = select(WPField)
        res = await self.session.execute(query)
        return res.scalars().all()
