from datetime import datetime
from typing import Annotated

from sqlalchemy import BigInteger, DateTime, Identity, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import mapped_column

# Целочисленные типы
serialpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
identitypk = Annotated[int, mapped_column(Integer, Identity(), primary_key=True)]
intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=False)]
int_notnull = Annotated[int, mapped_column(Integer, nullable=False)]

# External identifiers can exceed the signed 32-bit integer range.
bigintpk = Annotated[int, mapped_column(BigInteger, primary_key=True, autoincrement=False)]
bigint_notnull = Annotated[int, mapped_column(BigInteger, nullable=False)]

# Строковые типы фиксированной длины
str60 = Annotated[str, mapped_column(String(60), nullable=False)]
str64 = Annotated[str, mapped_column(String(64), nullable=False)]

# PostgreSQL timestamps use the database server clock and preserve the timezone.
timestamp = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
]
timestamp_nullable = Annotated[datetime | None, mapped_column(DateTime(timezone=True), nullable=True)]
timestamp_onupdate = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
]

# WordPress/MySQL timestamps retain the legacy mapping of the existing tables.
wp_timestamp = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.localtimestamp(),
        nullable=False,
    ),
]
wp_timestamp_onupdate = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.localtimestamp(),
        onupdate=func.localtimestamp(),
        nullable=False,
    ),
]
