import os


_TEST_DATABASE_ENVIRONMENT = {
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_USER": "test",
    "DB_PASS": "test",
    "DB_NAME": "test",
    "WP_DB_HOST": "localhost",
    "WP_DB_PORT": "3306",
    "WP_DB_USER": "test",
    "WP_DB_PASS": "test",
    "WP_DB_NAME": "test",
}

for variable_name, value in _TEST_DATABASE_ENVIRONMENT.items():
    os.environ.setdefault(variable_name, value)
