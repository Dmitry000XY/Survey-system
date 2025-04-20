from sqlalchemy import select, update
from src.models.wp_item_metas import WPItemMeta


class WPItemMetaRepository:
    def __init__(self, session):
        self.session = session

    async def create_item_meta(self, meta) -> WPItemMeta:
        self.session.add(meta)
        await self.session.flush()
        return meta

    async def get_item_meta(self, meta_id: int) -> WPItemMeta | None:
        return await self.session.get(WPItemMeta, meta_id)

    async def get_item_meta_by_item_and_field_id(self, item_id: int, field_id: int) -> list[WPItemMeta]:
        query = select(WPItemMeta).where(
            WPItemMeta.item_id == item_id,
            WPItemMeta.field_id == field_id
        )
        res = await self.session.execute(query)
        return res.scalars().all()  # TODO Only one result

    async def get_all_item_metas(self) -> list[WPItemMeta]:
        query = select(WPItemMeta)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def update_item_meta(self, meta_id: int, new_data) -> WPItemMeta | None:
        query = (
            update(WPItemMeta)
            .where(WPItemMeta.id == meta_id)
            .values(
                meta_value=new_data.meta_value,
                field_id=new_data.field_id,
                item_id=new_data.item_id
            )
            .returning(WPItemMeta)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_item_meta(self, meta_id: int) -> None:
        meta = await self.get_item_meta(meta_id)
        if meta:
            await self.session.delete(meta)
