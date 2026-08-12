from datetime import UTC, datetime

from src.configurations.constants import (
    ALL_QUESTIONNAIRE_TAGS,
    ALL_QUESTION_TYPES,
    ALLOWED_QUESTION_TYPES,
    AnswerTypeEnum,
    INITIAL_SYNCHRONIZATION_TIME,
    QuestionnaireTagEnum,
)


def test_initial_synchronization_time_is_unix_epoch_utc() -> None:
    assert INITIAL_SYNCHRONIZATION_TIME == datetime(1970, 1, 1, tzinfo=UTC)


def test_html_fields_are_synchronized_for_client_navigation() -> None:
    assert "html" in ALLOWED_QUESTION_TYPES


def test_database_enums_match_supported_constants() -> None:
    assert {item.value.lower() for item in AnswerTypeEnum} == set(ALL_QUESTION_TYPES)
    assert {item.value for item in QuestionnaireTagEnum} == set(ALL_QUESTIONNAIRE_TAGS)
