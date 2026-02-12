"""
Gemini CLI for Termux
A native Python CLI for Google's Gemini AI, optimized for Termux on Android.

Author: Alex72-py
License: MIT
Repository: https://github.com/Alex72-py/gemini-cli-termux
"""

__version__ = "1.0.0"
__author__ = "Alex72-py"
__license__ = "MIT"

from gemini_cli.core.client import GeminiClient
from gemini_cli.core.config import Config
from gemini_cli.core.auth import Auth

__all__ = ["GeminiClient", "Config", "Auth", "__version__"]
