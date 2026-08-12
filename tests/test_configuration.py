from sqlalchemy import URL

from src.configurations import get_settings, get_wp_settings


def test_application_settings_are_lazy_and_build_safe_urls(monkeypatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("DB_HOST", "postgres.example")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_USER", "survey")
    monkeypatch.setenv("DB_PASS", "p@ss:/word")
    monkeypatch.setenv("DB_NAME", "survey")

    settings = get_settings()

    assert settings.ECHO is False
    assert isinstance(settings.database_url_asyncpg, URL)
    assert settings.database_url_asyncpg.password == "p@ss:/word"
    assert "p@ss:/word" not in repr(settings)
    assert get_settings() is settings
    get_settings.cache_clear()


def test_wordpress_settings_use_the_shared_echo_flag(monkeypatch) -> None:
    get_wp_settings.cache_clear()
    monkeypatch.setenv("WP_DB_HOST", "mysql.example")
    monkeypatch.setenv("WP_DB_PORT", "3306")
    monkeypatch.setenv("WP_DB_USER", "wordpress")
    monkeypatch.setenv("WP_DB_PASS", "p@ss:/word")
    monkeypatch.setenv("WP_DB_NAME", "wordpress")
    monkeypatch.setenv("ECHO", "true")

    settings = get_wp_settings()

    assert settings.ECHO is True
    assert settings.database_url_asyncmy.password == "p@ss:/word"
    assert "p@ss:/word" not in repr(settings)
    get_wp_settings.cache_clear()
