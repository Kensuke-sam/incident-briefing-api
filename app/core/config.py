from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="incident-briefing-api", validation_alias="APP_NAME")
    app_env: str = Field(default="local", validation_alias="APP_ENV")
    host: str = Field(default="0.0.0.0", validation_alias="HOST")
    port: int = Field(default=8000, validation_alias="PORT")
    database_url: str = Field(default="sqlite:///./app.db", validation_alias="DATABASE_URL")
    internal_api_key: str = Field(
        default="dev-internal-key",
        validation_alias="INTERNAL_API_KEY",
    )
    ai_provider: str = Field(default="mock", validation_alias="AI_PROVIDER")
    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        validation_alias="OPENAI_BASE_URL",
    )
    ai_timeout_seconds: float = Field(default=15.0, validation_alias="AI_TIMEOUT_SECONDS")
    cors_origins: list[str] = Field(default_factory=list, validation_alias="CORS_ORIGINS")
    max_text_chars: int = Field(default=8000, validation_alias="MAX_TEXT_CHARS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
