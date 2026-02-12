"""
Basic tests for Gemini CLI components.
Run with: python -m pytest tests/
"""

import pytest
from pathlib import Path
from gemini_cli.core import Auth, Config
from gemini_cli.utils import Clipboard, FileHandler


class TestAuth:
    """Test authentication functionality."""
    
    def test_auth_creation(self, tmp_path):
        """Test auth manager creation."""
        auth = Auth(config_dir=tmp_path)
        assert auth.config_dir == tmp_path
        assert auth.api_key_file == tmp_path / "api_key"
    
    def test_save_and_load_api_key(self, tmp_path):
        """Test saving and loading API key."""
        auth = Auth(config_dir=tmp_path)
        test_key = "test_api_key_12345"
        
        # Save
        assert auth.save_api_key(test_key)
        
        # Load
        loaded_key = auth.get_api_key()
        assert loaded_key == test_key
    
    def test_delete_api_key(self, tmp_path):
        """Test deleting API key."""
        auth = Auth(config_dir=tmp_path)
        auth.save_api_key("test_key")
        
        assert auth.delete_api_key()
        assert not auth.is_authenticated()


class TestConfig:
    """Test configuration management."""
    
    def test_config_creation(self, tmp_path):
        """Test config manager creation."""
        config = Config(config_dir=tmp_path)
        assert config.config_dir == tmp_path
    
    def test_default_values(self, tmp_path):
        """Test default configuration values."""
        config = Config(config_dir=tmp_path)
        assert config.api.model == "gemini-2.0-flash-exp"
        assert config.generation.temperature == 0.9
        assert config.ui.streaming == True
    
    def test_set_and_get(self, tmp_path):
        """Test setting and getting config values."""
        config = Config(config_dir=tmp_path)
        
        config.set("api", "model", "gemini-1.5-pro")
        assert config.get("api", "model") == "gemini-1.5-pro"


class TestFileHandler:
    """Test file handling utilities."""
    
    def test_supported_extensions(self):
        """Test file extension validation."""
        assert FileHandler.is_supported(Path("test.png"))
        assert FileHandler.is_supported(Path("test.pdf"))
        assert not FileHandler.is_supported(Path("test.exe"))
    
    def test_mime_type(self):
        """Test MIME type detection."""
        assert FileHandler.get_mime_type(Path("test.png")) == "image/png"
        assert FileHandler.get_mime_type(Path("test.pdf")) == "application/pdf"
    
    def test_file_size_formatting(self):
        """Test file size formatting."""
        assert FileHandler.format_file_size(1024) == "1.0 KB"
        assert FileHandler.format_file_size(1048576) == "1.0 MB"


class TestClipboard:
    """Test clipboard functionality."""
    
    def test_clipboard_creation(self):
        """Test clipboard manager creation."""
        clipboard = Clipboard(use_termux_api=False)
        assert clipboard.has_termux_api == False
    
    def test_fallback_copy(self, tmp_path):
        """Test fallback clipboard copy."""
        clipboard = Clipboard(use_termux_api=False)
        clipboard.fallback_file = tmp_path / "clipboard.txt"
        
        test_text = "Hello, World!"
        clipboard.copy(test_text)
        
        # Check fallback file
        assert clipboard.fallback_file.exists()
        assert clipboard.fallback_file.read_text() == test_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
