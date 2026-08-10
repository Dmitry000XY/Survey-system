from importlib import import_module


def test_application_can_be_imported(monkeypatch):
    database_environment = {
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

    for name, value in database_environment.items():
        monkeypatch.setenv(name, value)

    main = import_module("src.main")

    assert main.app.title == "Survey system"
    assert main.app.version == "0.0.1"
