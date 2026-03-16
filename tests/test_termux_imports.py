"""Regression tests for startup behavior in minimal Termux environments."""

import subprocess
import sys

import pytest


def test_cli_help_runs_without_google_sdk():
    """`--help` should work even when google-generativeai isn't installed."""
    result = subprocess.run(
        [sys.executable, "-m", "gemini_cli.main", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "gemini-termux" in result.stdout


def test_core_exports_available_without_eager_client_import():
    """Auth/Config exports should remain importable without API SDK deps."""
    from gemini_cli.core import Auth, Config

    assert Auth is not None
    assert Config is not None


def test_client_error_message_when_sdk_missing():
    """Instantiating GeminiClient should raise a clear install message when missing SDK."""
    from gemini_cli.core.client import GENAI_AVAILABLE, GeminiClient

    if GENAI_AVAILABLE:
        pytest.skip("google-generativeai is installed in this environment")

    with pytest.raises(RuntimeError, match="google-generativeai"):
        GeminiClient(api_key="test")
