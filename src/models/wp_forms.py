from sqlalchemy import String, Text, Integer, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .wp_base import WPBaseModel
from .custom_types import serialpk, timestamp


class WPForm(WPBaseModel):
    __tablename__ = "wp_frm_forms"
    __table_args__ = (
        Index("form_key", "form_key", unique=True),
    )

    id: Mapped[serialpk]
    form_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_form_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    logged_in: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    editable: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    default_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str | None] = mapped_column(String(255), nullable=True)
    options: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[timestamp]

    # Relationships:
    # One form can have many fields (ordered by field_order)
    fields: Mapped[list["WPField"]] = relationship("WPField", back_populates="form",
                                                      order_by="WPField.field_order")
    # One form can have many submitted items
    items: Mapped[list["WPItem"]] = relationship("WPItem", back_populates="form")
