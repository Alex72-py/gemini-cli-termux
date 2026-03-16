"""Core functionality for Gemini CLI."""

from importlib import import_module

from gemini_cli.core.auth import Auth
from gemini_cli.core.config import Config

__all__ = ["Auth", "Config", "GeminiClient"]


def __getattr__(name: str):
    """Lazily expose GeminiClient so non-API features work without SDK deps."""
    if name == "GeminiClient":
        return import_module("gemini_cli.core.client").GeminiClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
