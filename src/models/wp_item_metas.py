from sqlalchemy import BigInteger, Text, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .wp_base import WPBaseModel
from .custom_types import timestamp


class WPItemMeta(WPBaseModel):
    __tablename__ = "wp_frm_item_metas"
    __table_args__ = (
        Index("field_id", "field_id"),
        Index("item_id", "item_id"),
        Index("idx_field_id_item_id", "field_id", "item_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    meta_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    field_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("wp_frm_fields.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("wp_frm_items.id"), nullable=False)
    created_at: Mapped[timestamp]

    # Relationships:
    # Each meta belongs to one submitted item.
    item: Mapped["WPItem"] = relationship("WPItem", back_populates="metas")
    # Each meta belongs to one field.
    field: Mapped["WPField"] = relationship("WPField")
