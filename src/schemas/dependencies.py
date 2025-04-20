from enum import Enum
from pydantic import BaseModel


class ShowHideEnum(str, Enum):
    SHOW = "SHOW"
    HIDE = "HIDE"


class AllAnyEnum(str, Enum):
    ALL = "ALL"
    ANY = "ANY"


class ConditionOperatorEnum(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="
    LIKE = "LIKE"
    NOT_LIKE = "NOT LIKE"
    STARTS_WITH = "LIKE%"
    ENDS_WITH = "%LIKE"


class Condition(BaseModel):
    field_id: int
    condition: ConditionOperatorEnum
    value: str


class Dependencies(BaseModel):
    show_hide: ShowHideEnum
    all_any: AllAnyEnum
    conditions: list[Condition]
