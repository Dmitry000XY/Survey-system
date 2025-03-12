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
FIXED_HASH_LENGTH = 64

generate_api_key = lambda: secrets.token_urlsafe(48)  # Генерирует 64-символьный api-key
