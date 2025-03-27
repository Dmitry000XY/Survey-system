from sqlalchemy import BigInteger, String, Text, Boolean, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .wp_base import WPBaseModel
from .custom_types import timestamp, timestamp_onupdate


class WPItem(WPBaseModel):
    __tablename__ = "wp_frm_items"
    __table_args__ = (
        # Unique index on item_key
        Index("item_key", "item_key", unique=True),
        # Indexes for foreign keys and other columns
        Index("form_id", "form_id"),
        Index("post_id", "post_id"),
        Index("user_id", "user_id"),
        Index("parent_item_id", "parent_item_id"),
        # Composite index on is_draft and created_at
        Index("idx_is_draft_created_at", "is_draft", "created_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    item_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip: Mapped[str | None] = mapped_column(Text, nullable=True)
    form_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("wp_frm_forms.id"), nullable=True)
    post_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    parent_item_id: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    is_draft: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp_onupdate]

    # Relationships:
    # Each item belongs to one form.
    form: Mapped["WPForm"] = relationship("WPForm", back_populates="items")
    # Each item may have many meta records.
    metas: Mapped[list["WPItemMeta"]] = relationship("WPItemMeta", back_populates="item")
