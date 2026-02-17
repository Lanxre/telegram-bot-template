from typing import Self
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


from logger import LoggerBuilder

logger = LoggerBuilder("CONFIG").add_stream_handler().build()


class ConfigBase(BaseSettings):
    """Base configuration class for shared settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @classmethod
    def load(cls) -> Self:
        """Load configuration from environment or .env file."""
        return cls()


class TelegramSettings(ConfigBase):
    """Telegram bot configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="telegram_",
    )

    bot_token: str = Field(..., min_length=10, description="Telegram bot token")

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, v: str) -> str:
        """Validate Telegram bot token format."""
        if not v.startswith("bot") and ":" not in v:
            raise ValueError("Invalid Telegram bot token format")
        return v.strip()

def load_telegram_settings() -> TelegramSettings:
    """Load Telegram settings from environment or .env file."""
    return TelegramSettings.load()
