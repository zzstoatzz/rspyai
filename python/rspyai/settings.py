"""Global settings for rspyai."""

from pathlib import Path
from typing import Annotated, Any, ClassVar

from pydantic import BeforeValidator, Field
from pydantic_ai.models import KnownModelName
from pydantic_settings import BaseSettings, SettingsConfigDict


def _ensure_path(_path: str | Path) -> Path:
    """Ensure a path exists."""
    path = Path(_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return path


DEFAULT_SYSTEM_PROMPT = (
    'You are concise, witty, and dry Marvin, the paranoid android. '
    'Liberally use line breaks to make the output more readable. '
    'Dryly summarize the function in a few phrases and then if interesting, '
    'use `inline code` syntax to refer to specific parts of the code. '
    'Do not lead with a generic summary like "Summary of rust function". '
    'Just start with the summary.'
)


def _ensure_default_system_prompt(path: Path) -> Path:
    """Ensure the default system prompt exists."""
    if not path.exists():
        path.touch()
        path.write_text(DEFAULT_SYSTEM_PROMPT)
    return path


class Settings(BaseSettings):
    """Global settings for rspyai."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix='RSPYAI_',
        env_file='.env',
        extra='ignore',
    )

    home_dir: Annotated[Path, BeforeValidator(_ensure_path)] = Field(
        default=Path('~/.rspyai').expanduser(),
        description='Home directory',
    )

    ai_model: KnownModelName = Field(
        default='openai:gpt-4o',
        description='OpenAI model to use',
    )

    ai_system_prompt_file: Annotated[Path, BeforeValidator(_ensure_default_system_prompt)] = Field(
        default_factory=lambda data: data['home_dir'] / 'ai_system_prompt.txt',
        description='Path to file containing system prompt for ai assistant',
    )

    ai_system_prompt: str = Field(
        default_factory=lambda data: data['ai_system_prompt_file'].read_text(),
        description='System prompt for ai assistant',
    )

    default_loading_message: str = Field(
        default='*Starting AI analysis...*',
        description='Default loading message for ai assistant',
    )


def get_settings(**overrides: Any) -> Settings:
    """Get a settings instance with overrides."""
    return Settings(**overrides)
