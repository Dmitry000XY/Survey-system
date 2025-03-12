from typing import Annotated, Optional
from datetime import datetime
from sqlalchemy import Integer, String, TIMESTAMP, func
from sqlalchemy.orm import mapped_column

# Целочисленные типы
serialpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=False)]
int_notnull = Annotated[int, mapped_column(Integer, nullable=False)]

# Строковые типы фиксированной длины
str32 = Annotated[str, mapped_column(String(32), nullable=False)]
str64 = Annotated[str, mapped_column(String(64), nullable=False)]

# Строки с индексированием
str32_idx = Annotated[str, mapped_column(String(32), nullable=False, index=True)]
str64_idx = Annotated[str, mapped_column(String(64), nullable=False, index=True)]

# Timestamp типы
timestamp = Annotated[datetime, mapped_column(
    TIMESTAMP(timezone=True),
    server_default=func.localtimestamp(),
    nullable=False
)]
timestamp_nullable = Annotated[Optional[datetime], mapped_column(
    TIMESTAMP(timezone=True),
    nullable=True
)]
timestamp_onupdate = Annotated[datetime, mapped_column(
    TIMESTAMP(timezone=True),
    server_default=func.localtimestamp(),
    onupdate=func.localtimestamp(),
    nullable=False
)]
timestamp_onupdate_nullable = Annotated[Optional[datetime], mapped_column(
    TIMESTAMP(timezone=True),
    server_default=func.localtimestamp(),
    onupdate=func.localtimestamp(),
    nullable=True
)]
