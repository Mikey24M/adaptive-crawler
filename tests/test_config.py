from crawler.config import Settings


def test_settings_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.request_timeout == 10.0
    assert settings.home_field_edge == 1.8
    assert settings.rest_day_edge_per_day == 0.35
    assert settings.travel_penalty_per_500_miles == 0.6
    assert settings.key_player_edge_multiplier == 0.3
    assert settings.injury_edge_multiplier == 0.9
    assert settings.confidence_smoothing == 7.5


def test_settings_allow_environment_overrides(monkeypatch) -> None:
    monkeypatch.setenv("NFL_PREDICTOR_HOME_FIELD_EDGE", "2.25")
    monkeypatch.setenv("NFL_PREDICTOR_TRAVEL_PENALTY_PER_500_MILES", "0.8")
    monkeypatch.setenv("NFL_PREDICTOR_CONFIDENCE_SMOOTHING", "6.0")

    settings = Settings(_env_file=None)

    assert settings.home_field_edge == 2.25
    assert settings.travel_penalty_per_500_miles == 0.8
    assert settings.confidence_smoothing == 6.0
