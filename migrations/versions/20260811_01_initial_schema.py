"""Create the internal survey schema.

Revision ID: 20260811_01
Revises:
Create Date: 2026-08-11
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260811_01"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

QUESTIONNAIRE_TAGS = ("visible", "registration", "daily", "weekly", "monthly")
ANSWER_TYPES = (
    "DIVIDER",
    "NAME",
    "SELECT",
    "EMAIL",
    "END_DIVIDER",
    "TEXT",
    "PASSWORD",
    "DATE",
    "PHONE",
    "RADIO",
    "CHECKBOX",
    "TOGGLE",
    "HTML",
    "USER_ID",
    "NUMBER",
    "CAPTCHA",
    "TEXTAREA",
)


def upgrade() -> None:
    bind = op.get_bind()
    questionnaire_tag_enum = postgresql.ENUM(
        *QUESTIONNAIRE_TAGS,
        name="questionnaire_tag_enum",
        create_type=False,
    )
    answer_type_enum = postgresql.ENUM(
        *ANSWER_TYPES,
        name="answer_type_enum",
        create_type=False,
    )
    questionnaire_tag_enum.create(bind, checkfirst=False)
    answer_type_enum.create(bind, checkfirst=False)

    op.create_table(
        "users",
        sa.Column("user_id", sa.BigInteger(), autoincrement=False, nullable=False),
        sa.Column("login", sa.String(length=60), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("time_updated", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("char_length(login) >= 3", name="ck_users_login_min_length"),
        sa.CheckConstraint("user_id > 0", name="ck_users_id_positive"),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("login"),
    )
    op.create_table(
        "clients",
        sa.Column("client_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("client_name", sa.String(length=64), nullable=False),
        sa.Column("api_key_hash", sa.String(length=64), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("char_length(api_key_hash) = 64", name="ck_clients_api_key_hash_length"),
        sa.CheckConstraint("char_length(client_name) >= 1", name="ck_clients_name_nonempty"),
        sa.PrimaryKeyConstraint("client_id"),
        sa.UniqueConstraint("api_key_hash"),
        sa.UniqueConstraint("client_name"),
    )
    op.create_table(
        "questionnaires",
        sa.Column("questionnaire_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("questionnaire_version", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("questionnaire_name", sa.String(length=255), nullable=False),
        sa.Column("wordpress_id", sa.Integer(), nullable=False),
        sa.Column(
            "tags",
            postgresql.ARRAY(questionnaire_tag_enum),
            server_default=sa.text("'{}'::questionnaire_tag_enum[]"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("questionnaire_hash", sa.String(length=64), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("char_length(questionnaire_hash) = 64", name="ck_questionnaires_hash_length"),
        sa.CheckConstraint("questionnaire_version > 0", name="ck_questionnaires_version_positive"),
        sa.CheckConstraint("wordpress_id > 0", name="ck_questionnaires_wordpress_id_positive"),
        sa.PrimaryKeyConstraint("questionnaire_id", "questionnaire_version"),
        sa.UniqueConstraint("questionnaire_id", "questionnaire_hash", name="uq_questionnaires_id_hash"),
        sa.UniqueConstraint(
            "wordpress_id",
            "questionnaire_version",
            name="uq_questionnaires_wordpress_version",
        ),
    )
    op.create_index("ix_questionnaires_wordpress_id", "questionnaires", ["wordpress_id"])
    op.create_index(
        "uq_questionnaires_one_active_version",
        "questionnaires",
        ["questionnaire_id"],
        unique=True,
        postgresql_where=sa.text("is_active"),
    )
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column(
            "last_synchronization_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("'1970-01-01 00:00:00+00'::timestamptz"),
            nullable=False,
        ),
        sa.CheckConstraint("id = 1", name="ck_settings_singleton"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute("INSERT INTO settings (id) VALUES (1)")
    op.create_table(
        "users_clients",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("user_client_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.client_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "client_id"),
        sa.UniqueConstraint("client_id", "user_client_id", name="uq_users_clients_external_identity"),
    )
    op.create_table(
        "questions",
        sa.Column("question_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("questionnaire_id", sa.Integer(), nullable=False),
        sa.Column("questionnaire_version", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("question_order", sa.Integer(), nullable=False),
        sa.Column(
            "answer_options",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column("answer_type", answer_type_enum, nullable=False),
        sa.Column(
            "dependencies",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text('\'{"show_hide": "SHOW", "all_any": "ALL", "conditions": []}\'::jsonb'),
            nullable=False,
        ),
        sa.Column("wordpress_id", sa.Integer(), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "jsonb_typeof(answer_options) = 'array'",
            name="ck_questions_answer_options_array",
        ),
        sa.CheckConstraint(
            "dependencies ? 'all_any' AND (dependencies->>'all_any') IN ('ALL', 'ANY')",
            name="ck_questions_dependencies_all_any",
        ),
        sa.CheckConstraint(
            "jsonb_typeof(dependencies) = 'object'",
            name="ck_questions_dependencies_object",
        ),
        sa.CheckConstraint(
            "dependencies ? 'show_hide' AND (dependencies->>'show_hide') IN ('SHOW', 'HIDE')",
            name="ck_questions_dependencies_show_hide",
        ),
        sa.CheckConstraint("question_order >= 0", name="ck_questions_order_nonnegative"),
        sa.CheckConstraint("wordpress_id > 0", name="ck_questions_wordpress_id_positive"),
        sa.ForeignKeyConstraint(
            ["questionnaire_id", "questionnaire_version"],
            ["questionnaires.questionnaire_id", "questionnaires.questionnaire_version"],
            name="fk_questions_questionnaire",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("question_id"),
        sa.UniqueConstraint(
            "questionnaire_id",
            "questionnaire_version",
            "question_order",
            name="uq_questions_version_order",
        ),
        sa.UniqueConstraint(
            "questionnaire_id",
            "questionnaire_version",
            "wordpress_id",
            name="uq_questions_version_wordpress_id",
        ),
    )
    op.create_table(
        "questionnaire_answers",
        sa.Column("questionnaire_answer_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("questionnaire_id", sa.Integer(), nullable=False),
        sa.Column("questionnaire_version", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("time_started", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("time_finished", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "time_finished IS NULL OR time_finished >= time_started",
            name="ck_questionnaire_answers_time_order",
        ),
        sa.ForeignKeyConstraint(["client_id"], ["clients.client_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["questionnaire_id", "questionnaire_version"],
            ["questionnaires.questionnaire_id", "questionnaires.questionnaire_version"],
            name="fk_questionnaire_answers_questionnaire",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("questionnaire_answer_id"),
    )
    op.create_index("ix_questionnaire_answers_client_id", "questionnaire_answers", ["client_id"])
    op.create_index(
        "ix_questionnaire_answers_questionnaire_version",
        "questionnaire_answers",
        ["questionnaire_id", "questionnaire_version"],
    )
    op.create_index("ix_questionnaire_answers_user_id", "questionnaire_answers", ["user_id"])
    op.create_table(
        "answers",
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("questionnaire_answer_id", sa.Integer(), nullable=False),
        sa.Column("answer", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.question_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["questionnaire_answer_id"],
            ["questionnaire_answers.questionnaire_answer_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("question_id", "questionnaire_answer_id"),
    )
    op.create_index("ix_answers_questionnaire_answer_id", "answers", ["questionnaire_answer_id"])


def downgrade() -> None:
    op.drop_index("ix_answers_questionnaire_answer_id", table_name="answers")
    op.drop_table("answers")
    op.drop_index("ix_questionnaire_answers_user_id", table_name="questionnaire_answers")
    op.drop_index("ix_questionnaire_answers_questionnaire_version", table_name="questionnaire_answers")
    op.drop_index("ix_questionnaire_answers_client_id", table_name="questionnaire_answers")
    op.drop_table("questionnaire_answers")
    op.drop_table("questions")
    op.drop_table("users_clients")
    op.drop_table("settings")
    op.drop_index("uq_questionnaires_one_active_version", table_name="questionnaires")
    op.drop_index("ix_questionnaires_wordpress_id", table_name="questionnaires")
    op.drop_table("questionnaires")
    op.drop_table("clients")
    op.drop_table("users")

    bind = op.get_bind()
    postgresql.ENUM(*ANSWER_TYPES, name="answer_type_enum").drop(bind, checkfirst=False)
    postgresql.ENUM(*QUESTIONNAIRE_TAGS, name="questionnaire_tag_enum").drop(bind, checkfirst=False)
