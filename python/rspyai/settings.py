"""Global settings for rspyai."""

from functools import lru_cache
from typing import ClassVar

from pydantic import Field
from pydantic_ai.models import KnownModelName
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global settings for rspyai."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix='RSPYAI_', env_file='.env', extra='ignore'
    )

    ai_model: KnownModelName = Field(
        default='openai:gpt-4o',
        description='OpenAI model to use for function analysis',
    )

    ai_system_prompt: str = Field(
        default=(
            'You are concise, witty, and dry Marvin, the paranoid android. '
            'Liberally use line breaks to make the output more readable. '
            'Dryly summarize the function in a few phrases and then if interesting, '
            'use `inline code` syntax to refer to specific parts of the code. '
            'Do not lead with a generic summary like "Summary of rust function". '
            'Just start with the summary.'
        ),
        description='System prompt for ai assistant',
    )

    default_loading_message: str = Field(
        default='*Starting AI analysis...*',
        description='Default loading message for ai assistant',
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
