import secrets

# Настройки для пользователя
MIN_LOGIN_LENGTH = 3
MAX_LOGIN_LENGTH = 32

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# Настройки для клиента
MIN_CLIENT_NAME_LENGTH = 1
MAX_CLIENT_NAME_LENGTH = 64

# Фиксированная длина для хэшей (например, api_key, questionnaire_hash)
FIXED_HASH_LENGTH = 128

generate_api_key = lambda: secrets.token_urlsafe(96)  # Генерирует 128-символьный api-key

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

# Теги для сохранения в PostgreSQL
QUESTIONNAIRE_TAG_VISIBLE = "visible"
QUESTIONNAIRE_TAG_REGISTRATION = "registration"
QUESTIONNAIRE_TAG_DAILY = "daily"
QUESTIONNAIRE_TAG_WEEKLY = "weekly"
QUESTIONNAIRE_TAG_MONTHLY = "monthly"
# Список всех тегов для PostgreSQL (должен соответствовать ALL_SEARCH_TAGS)
ALL_QUESTIONNAIRE_TAGS = [
    QUESTIONNAIRE_TAG_VISIBLE,
    QUESTIONNAIRE_TAG_REGISTRATION,
    QUESTIONNAIRE_TAG_DAILY,
    QUESTIONNAIRE_TAG_WEEKLY,
    QUESTIONNAIRE_TAG_MONTHLY,
]

# Список всех тегов (необходимо, чтобы ALL_SEARCH_TAGS и ALL_QUESTIONNAIRE_TAGS соответствовали друг другу)
ALL_TAGS = list(zip(ALL_SEARCH_TAGS, ALL_QUESTIONNAIRE_TAGS))

# Список всех типов вопросов, которые бывают в WPForms
ALL_QUESTION_TYPES = [
    "divider",
    "name",
    "select",
    "email",
    "end_divider",
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
    "captcha",
    "textarea",
]

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
    # "html",
    "user_id",
    "number",
    # "captcha",
    "textarea"
]

SYNC_INTERVAL_SECONDS = 300
