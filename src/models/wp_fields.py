from sqlalchemy import BigInteger, String, Text, Integer, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .wp_base import WPBaseModel
from .custom_types import timestamp


class WPField(WPBaseModel):
    __tablename__ = "wp_frm_fields"
    __table_args__ = (
        Index("field_key", "field_key", unique=True),
        Index("form_id", "form_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    field_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    options: Mapped[str | None] = mapped_column(Text, nullable=True)
    field_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    required: Mapped[int | None] = mapped_column(Integer, nullable=True)
    field_options: Mapped[str | None] = mapped_column(Text, nullable=True)
    form_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wp_frm_forms.id"), nullable=True)
    created_at: Mapped[timestamp]

    # Relationship: Each field belongs to one form.
    form: Mapped["WPForm"] = relationship("WPForm", back_populates="fields")
