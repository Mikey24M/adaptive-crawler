"""Centralized crawler settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven crawler configuration."""

    model_config = SettingsConfigDict(
        env_prefix="CRAWLER_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    max_pages: int = Field(default=100, ge=1)
    max_depth: int = Field(default=2, ge=0)
    request_timeout: float = Field(default=10.0, gt=0)
    request_delay: float = Field(default=0.5, ge=0)
    same_domain_only: bool = True
    respect_robots: bool = True
    retry_count: int = Field(default=2, ge=0)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance for the process."""

    return Settings()
