from datetime import UTC, datetime
from enum import StrEnum


INITIAL_SYNCHRONIZATION_TIME = datetime(1970, 1, 1, tzinfo=UTC)

# Настройки для пользователя
MIN_LOGIN_LENGTH = 3
MAX_LOGIN_LENGTH = 60

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
MIN_PASSWORD_HASH_LENGTH = 32
MAX_PASSWORD_HASH_LENGTH = 255

# Настройки для клиента
MIN_CLIENT_NAME_LENGTH = 1
MAX_CLIENT_NAME_LENGTH = 64
API_KEY_ENTROPY_BYTES = 48
API_KEY_LENGTH = 64  # Must be ceil(4 * API_KEY_ENTROPY_BYTES / 3)
API_KEY_GENERATION_ATTEMPTS = 3

# SHA-256 is stored as a lowercase hexadecimal string.
SHA256_HEX_LENGTH = 64
QUESTIONNAIRE_HASH_LENGTH = SHA256_HEX_LENGTH


# Теги для поиска в WP БД
SEARCH_TAG_VISIBLE = "bot"
SEARCH_TAG_REGISTRATION = "reg"
SEARCH_TAG_DAILY = "daily"
SEARCH_TAG_WEEKLY = "weekly"
SEARCH_TAG_MONTHLY = "monthly"
# Список всех тегов поиска (должен соответствовать ALL_QUESTIONNAIRE_TAGS)
ALL_SEARCH_TAGS = [
    SEARCH_TAG_VISIBLE,
    SEARCH_TAG_REGISTRATION,
    SEARCH_TAG_DAILY,
    SEARCH_TAG_WEEKLY,
    SEARCH_TAG_MONTHLY,
]


class QuestionnaireTagEnum(StrEnum):
    VISIBLE = "visible"
    REGISTRATION = "registration"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# Теги для сохранения в PostgreSQL
QUESTIONNAIRE_TAG_VISIBLE = QuestionnaireTagEnum.VISIBLE.value
QUESTIONNAIRE_TAG_REGISTRATION = QuestionnaireTagEnum.REGISTRATION.value
QUESTIONNAIRE_TAG_DAILY = QuestionnaireTagEnum.DAILY.value
QUESTIONNAIRE_TAG_WEEKLY = QuestionnaireTagEnum.WEEKLY.value
QUESTIONNAIRE_TAG_MONTHLY = QuestionnaireTagEnum.MONTHLY.value
ALL_QUESTIONNAIRE_TAGS = [tag.value for tag in QuestionnaireTagEnum]

# Список всех тегов (необходимо, чтобы ALL_SEARCH_TAGS и ALL_QUESTIONNAIRE_TAGS соответствовали друг другу)
ALL_TAGS = list(zip(ALL_SEARCH_TAGS, ALL_QUESTIONNAIRE_TAGS))


class AnswerTypeEnum(StrEnum):
    DIVIDER = "DIVIDER"
    NAME = "NAME"
    SELECT = "SELECT"
    EMAIL = "EMAIL"
    END_DIVIDER = "END_DIVIDER"
    TEXT = "TEXT"
    PASSWORD = "PASSWORD"
    DATE = "DATE"
    PHONE = "PHONE"
    RADIO = "RADIO"
    CHECKBOX = "CHECKBOX"
    TOGGLE = "TOGGLE"
    HTML = "HTML"
    USER_ID = "USER_ID"
    NUMBER = "NUMBER"
    CAPTCHA = "CAPTCHA"
    TEXTAREA = "TEXTAREA"


# Список всех типов вопросов, которые бывают в WPForms
ALL_QUESTION_TYPES = [answer_type.value.lower() for answer_type in AnswerTypeEnum]

# Из них – только эти мы показываем в боте
ALLOWED_QUESTION_TYPES = [
    # "divider",
    "name",
    "select",
    "email",
    # "end_divider",
    "text",
    "password",
    "date",
    "phone",
    "radio",
    "checkbox",
    "toggle",
    "html",
    "user_id",
    "number",
    # "captcha",
    "textarea",
]

SYNC_INTERVAL_SECONDS = 300
