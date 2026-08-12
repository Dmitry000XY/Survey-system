from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from src.configurations.constants import INITIAL_SYNCHRONIZATION_TIME

from .base import BaseModel


class Setting(BaseModel):
    __tablename__ = "settings"
    __table_args__ = (
        # Ограничиваем таблицу до одной строки: id всегда равен 1
        CheckConstraint("id = 1", name="ck_settings_singleton"),
    )

    # Фиксированный первичный ключ для обеспечения единственной строки (singleton)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, server_default=text("1"))
    last_synchronization_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=INITIAL_SYNCHRONIZATION_TIME,
        server_default=text("'1970-01-01 00:00:00+00'::timestamptz"),
    )
