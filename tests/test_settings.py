from pathlib import Path

import pytest

from rspyai.settings import DEFAULT_SYSTEM_PROMPT, get_settings


def test_model_override(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv('RSPYAI_AI_MODEL', 'claude-3-5-sonnet-latest')
    settings = get_settings()
    assert settings.ai_model == 'claude-3-5-sonnet-latest'


def test_home_dir_default(monkeypatch: pytest.MonkeyPatch, tmpdir: Path):
    monkeypatch.setenv('RSPYAI_HOME_DIR', str(tmpdir / 'test-home-dir'))
    settings = get_settings()
    assert settings.home_dir.exists()
    assert settings.home_dir == tmpdir / 'test-home-dir'


def test_home_dir_default_no_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv('RSPYAI_HOME_DIR', raising=False)
    settings = get_settings()
    assert settings.home_dir.exists()
    assert settings.home_dir == Path('~/.rspyai').expanduser()


def test_default_ai_system_prompt(monkeypatch: pytest.MonkeyPatch, tmpdir: Path):
    monkeypatch.setenv('RSPYAI_HOME_DIR', str(tmpdir / 'test-home-dir'))
    settings = get_settings()
    assert settings.ai_system_prompt_file.exists()
    assert settings.ai_system_prompt_file.read_text() == DEFAULT_SYSTEM_PROMPT
