"""
Configuration management for Gemini CLI.
Handles loading, saving, and managing user preferences.
"""

import os
import toml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class APIConfig:
    """API configuration settings."""
    model: str = "gemini-2.0-flash-exp"
    timeout: int = 60


@dataclass
class GenerationConfig:
    """Text generation parameters."""
    temperature: float = 0.9
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192


@dataclass
class UIConfig:
    """User interface settings."""
    theme: str = "monokai"
    syntax_highlighting: bool = True
    show_timestamps: bool = True
    streaming: bool = True


@dataclass
class HistoryConfig:
    """Conversation history settings."""
    enabled: bool = True
    max_entries: int = 1000
    auto_save: bool = True


@dataclass
class ClipboardConfig:
    """Clipboard integration settings."""
    use_termux_api: bool = True
    auto_copy_code: bool = False


class Config:
    """Manages application configuration."""
    
    # Default configuration
    DEFAULTS = {
        "api": {
            "model": "gemini-2.0-flash-exp",
            "timeout": 60,
        },
        "generation": {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        },
        "ui": {
            "theme": "monokai",
            "syntax_highlighting": True,
            "show_timestamps": True,
            "streaming": True,
        },
        "history": {
            "enabled": True,
            "max_entries": 1000,
            "auto_save": True,
        },
        "clipboard": {
            "use_termux_api": True,
            "auto_copy_code": False,
        },
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory for config files
        """
        # Setup paths (Termux-aware)
        self.home = Path.home()
        self.prefix = Path(os.getenv("PREFIX", "/data/data/com.termux/files/usr"))
        
        if config_dir is None:
            config_dir = self.home / ".config" / "gemini-cli"
        
        self.config_dir = Path(config_dir)
        self.cache_dir = self.home / ".cache" / "gemini-cli"
        self.data_dir = self.home / ".local" / "share" / "gemini-cli"
        
        # Create directories
        for directory in [self.config_dir, self.cache_dir, self.data_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.toml"
        self._config = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file or use defaults."""
        if self.config_file.exists():
            try:
                self._config = toml.load(self.config_file)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
                self._config = self.DEFAULTS.copy()
        else:
            self._config = self.DEFAULTS.copy()
    
    def save(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.config_file, "w") as f:
                toml.dump(self._config, f)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        return self._config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = self.DEFAULTS.copy()
        self.save()
    
    @property
    def api(self) -> APIConfig:
        """Get API configuration."""
        return APIConfig(**self._config.get("api", {}))
    
    @property
    def generation(self) -> GenerationConfig:
        """Get generation configuration."""
        return GenerationConfig(**self._config.get("generation", {}))
    
    @property
    def ui(self) -> UIConfig:
        """Get UI configuration."""
        return UIConfig(**self._config.get("ui", {}))
    
    @property
    def history(self) -> HistoryConfig:
        """Get history configuration."""
        return HistoryConfig(**self._config.get("history", {}))
    
    @property
    def clipboard(self) -> ClipboardConfig:
        """Get clipboard configuration."""
        return ClipboardConfig(**self._config.get("clipboard", {}))
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Get entire configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()
