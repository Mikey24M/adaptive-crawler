from crawler.config import Settings


def test_settings_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.max_pages == 100
    assert settings.max_depth == 2
    assert settings.request_timeout == 10.0
    assert settings.request_delay == 0.5
    assert settings.same_domain_only is True
    assert settings.respect_robots is True
    assert settings.retry_count == 2


def test_settings_allow_environment_overrides(monkeypatch) -> None:
    monkeypatch.setenv("CRAWLER_MAX_PAGES", "25")
    monkeypatch.setenv("CRAWLER_REQUEST_DELAY", "1.25")
    monkeypatch.setenv("CRAWLER_RESPECT_ROBOTS", "false")

    settings = Settings(_env_file=None)

    assert settings.max_pages == 25
    assert settings.request_delay == 1.25
    assert settings.respect_robots is False
