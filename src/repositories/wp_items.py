from sqlalchemy import select, update
from src.models.wp_items import WPItem


class WPItemRepository:
    def __init__(self, session):
        self.session = session

    async def create_item(self, item) -> WPItem:
        self.session.add(item)
        await self.session.flush()
        return item

    async def get_item(self, item_id: int) -> WPItem | None:
        return await self.session.get(WPItem, item_id)

    async def get_all_items(self) -> list[WPItem]:
        query = select(WPItem)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def update_item(self, item_id: int, new_data) -> WPItem | None:
        query = (
            update(WPItem)
            .where(WPItem.id == item_id)
            .values(
                item_key=new_data.item_key,
                name=new_data.name,
                description=new_data.description,
                ip=new_data.ip,
                form_id=new_data.form_id,
                post_id=new_data.post_id,
                user_id=new_data.user_id,
                parent_item_id=new_data.parent_item_id,
                is_draft=new_data.is_draft,
                updated_by=new_data.updated_by
            )
            .returning(WPItem)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_item(self, item_id: int) -> None:
        item = await self.get_item(item_id)
        if item:
            await self.session.delete(item)
