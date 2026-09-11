"""Centralized NFL predictor settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven predictor configuration."""

    model_config = SettingsConfigDict(
        env_prefix="NFL_PREDICTOR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    request_timeout: float = Field(default=10.0, gt=0)
    home_field_edge: float = Field(default=1.8, ge=0)
    rest_day_edge_per_day: float = Field(default=0.35, ge=0)
    travel_penalty_per_500_miles: float = Field(default=0.6, ge=0)
    key_player_edge_multiplier: float = Field(default=0.3, ge=0)
    injury_edge_multiplier: float = Field(default=0.9, ge=0)
    confidence_smoothing: float = Field(default=7.5, gt=0)

    user_agent: str = (
        "NFLGamePredictor/0.1 " "(+https://github.com/Mikey24M/adaptive-crawler)"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance for the process."""

    return Settings()
