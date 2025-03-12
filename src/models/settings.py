from sqlalchemy import Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .custom_types import timestamp


class Setting(BaseModel):
    __tablename__ = "settings"
    __table_args__ = (
        # Ограничиваем таблицу до одной строки: id всегда равен 1
        CheckConstraint("id = 1", name="ck_settings_singleton"),
    )

    # Фиксированный первичный ключ для обеспечения единственной строки (singleton)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    last_synchronization_time: Mapped[timestamp]
