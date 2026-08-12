from sqlalchemy import column
from sqlalchemy.dialects import mysql

from src.repositories.wp_forms import _OrderedGroupConcat


def test_group_concat_has_a_stable_secondary_order() -> None:
    expression = _OrderedGroupConcat(
        column("field_hash"),
        column("field_order"),
        column("field_id"),
    )

    sql = str(expression.compile(dialect=mysql.dialect()))

    assert sql == "GROUP_CONCAT(field_hash ORDER BY field_order, field_id)"
