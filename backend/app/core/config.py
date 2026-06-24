"""Typed application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


Environment = Literal["development", "staging", "production", "test"]
LogFormat = Literal["json", "console"]


class Settings(BaseSettings):
    """Application settings.

    Values are loaded from process environment and optional .env files. Keeping
    settings typed gives startup-time validation for required infrastructure.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "LIPU API"
    app_version: str = "0.1.0"
    app_env: Environment = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://lipu_user:lipu_password_dev@localhost:5432/lipu_dev"
    )
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_timeout: int = 30
    database_pool_recycle: int = 1800
    database_echo: bool = False

    redis_url: RedisDsn = Field(default="redis://localhost:6379/0")
    redis_decode_responses: bool = True
    redis_health_check_interval: int = 30
    redis_cache_ttl: int = 3600

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])
    allowed_hosts: list[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])

    log_level: str = "INFO"
    log_format: LogFormat = "json"

    sentry_dsn: AnyUrl | None = None

    request_id_header: str = "X-Request-ID"

    @field_validator("cors_origins", "cors_allow_methods", "cors_allow_headers", "allowed_hosts", mode="before")
    @classmethod
    def parse_csv_list(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("sentry_dsn", mode="before")
    @classmethod
    def blank_url_as_none(cls, value: str | AnyUrl | None) -> str | AnyUrl | None:
        if value == "":
            return None
        return value

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings for application-wide reuse."""

    return Settings()
