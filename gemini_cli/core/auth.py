"""
Authentication and API key management for Gemini CLI.
Handles secure storage and retrieval of API keys.
"""

import os
from pathlib import Path
from typing import Optional


class Auth:
    """Manages API key authentication for Gemini."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize authentication manager.
        
        Args:
            config_dir: Directory for config files (default: ~/.config/gemini-cli)
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "gemini-cli"
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.api_key_file = self.config_dir / "api_key"
    
    def get_api_key(self) -> Optional[str]:
        """
        Get API key from environment or config file.
        
        Priority:
        1. GEMINI_API_KEY environment variable
        2. ~/.config/gemini-cli/api_key file
        
        Returns:
            API key string or None if not found
        """
        # Check environment variable first
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key.strip()
        
        # Check config file
        if self.api_key_file.exists():
            try:
                api_key = self.api_key_file.read_text().strip()
                if api_key:
                    return api_key
            except Exception as e:
                print(f"Warning: Could not read API key file: {e}")
        
        return None
    
    def save_api_key(self, api_key: str) -> bool:
        """
        Save API key to config file with secure permissions.
        
        Args:
            api_key: API key to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Write API key
            self.api_key_file.write_text(api_key.strip())
            
            # Set secure permissions (read/write for owner only)
            self.api_key_file.chmod(0o600)
            
            return True
        except Exception as e:
            print(f"Error saving API key: {e}")
            return False
    
    def delete_api_key(self) -> bool:
        """
        Delete stored API key file.
        
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if self.api_key_file.exists():
                self.api_key_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting API key: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        """
        Check if API key is configured.
        
        Returns:
            True if API key is available, False otherwise
        """
        return self.get_api_key() is not None
    
    def validate_api_key(self, api_key: str) -> bool:
        """
        Basic validation of API key format.
        
        Args:
            api_key: API key to validate
            
        Returns:
            True if format looks valid, False otherwise
        """
        if not api_key:
            return False
        
        api_key = api_key.strip()
        
        # Basic checks: should be alphanumeric, reasonable length
        if len(api_key) < 20:
            return False
        
        # Should start with common Google API key prefix patterns
        # This is just a basic check, not comprehensive
        return True
