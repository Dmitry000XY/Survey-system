from alembic import command
from alembic.config import Config
from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import configure_mappers
from sqlalchemy.schema import DefaultClause

from src.models import BaseModel


EXPECTED_TABLES = {
    "answers",
    "clients",
    "questionnaire_answers",
    "questionnaires",
    "questions",
    "settings",
    "users",
    "users_clients",
}


def _foreign_key(table_name: str, constraint_name: str):
    table = BaseModel.metadata.tables[table_name]
    return next(constraint for constraint in table.foreign_key_constraints if constraint.name == constraint_name)


def test_internal_schema_contains_only_domain_tables() -> None:
    assert set(BaseModel.metadata.tables) == EXPECTED_TABLES


def test_mappers_configure_without_database_access() -> None:
    configure_mappers()


def test_external_identifiers_use_bigint() -> None:
    users = BaseModel.metadata.tables["users"]
    users_clients = BaseModel.metadata.tables["users_clients"]

    assert isinstance(users.c.user_id.type, BigInteger)
    assert users.c.user_id.autoincrement is False
    assert isinstance(users_clients.c.user_client_id.type, BigInteger)


def test_internal_generated_identifiers_use_integer() -> None:
    clients = BaseModel.metadata.tables["clients"]
    questionnaires = BaseModel.metadata.tables["questionnaires"]
    questions = BaseModel.metadata.tables["questions"]
    questionnaire_answers = BaseModel.metadata.tables["questionnaire_answers"]

    assert type(clients.c.client_id.type) is Integer
    assert type(questionnaires.c.questionnaire_id.type) is Integer
    assert type(questionnaires.c.wordpress_id.type) is Integer
    assert type(questions.c.question_id.type) is Integer
    assert type(questions.c.wordpress_id.type) is Integer
    assert type(questionnaire_answers.c.questionnaire_answer_id.type) is Integer


def test_structured_values_use_jsonb() -> None:
    questions = BaseModel.metadata.tables["questions"]
    answers = BaseModel.metadata.tables["answers"]

    assert isinstance(questions.c.answer_options.type, JSONB)
    assert isinstance(questions.c.dependencies.type, JSONB)
    assert isinstance(answers.c.answer.type, JSONB)


def test_api_keys_are_stored_only_as_hashes() -> None:
    clients = BaseModel.metadata.tables["clients"]

    assert "api_key" not in clients.c
    assert isinstance(clients.c.api_key_hash.type, String)
    assert clients.c.api_key_hash.type.length == 64
    assert clients.c.api_key_hash.unique is True


def test_settings_start_from_unix_epoch() -> None:
    settings = BaseModel.metadata.tables["settings"]
    server_default = settings.c.last_synchronization_time.server_default

    assert settings.c.last_synchronization_time.nullable is False
    assert isinstance(server_default, DefaultClause)
    assert str(server_default.arg) == "'1970-01-01 00:00:00+00'::timestamptz"


def test_answers_do_not_duplicate_questionnaire_version() -> None:
    answers = BaseModel.metadata.tables["answers"]
    question_fk = next(fk for fk in answers.foreign_key_constraints if fk.referred_table.name == "questions")
    attempt_fk = next(fk for fk in answers.foreign_key_constraints if fk.referred_table.name == "questionnaire_answers")

    assert "questionnaire_id" not in answers.c
    assert "questionnaire_version" not in answers.c
    assert [column.name for column in question_fk.columns] == ["question_id"]
    assert question_fk.ondelete == "RESTRICT"
    assert [column.name for column in attempt_fk.columns] == ["questionnaire_answer_id"]
    assert attempt_fk.ondelete == "CASCADE"


def test_questionnaire_history_is_protected() -> None:
    questionnaire_fk = _foreign_key(
        "questionnaire_answers",
        "fk_questionnaire_answers_questionnaire",
    )
    questions_fk = _foreign_key("questions", "fk_questions_questionnaire")

    assert questionnaire_fk.ondelete == "RESTRICT"
    assert questions_fk.ondelete == "CASCADE"


def test_initial_migration_can_render_offline(capsys) -> None:
    config = Config("alembic.ini")

    command.upgrade(config, "head", sql=True)

    sql = capsys.readouterr().out
    assert "CREATE TABLE questionnaires" in sql
    assert "answer_options JSONB" in sql
    assert "CREATE TABLE answers" in sql
    assert "ON DELETE RESTRICT" in sql
