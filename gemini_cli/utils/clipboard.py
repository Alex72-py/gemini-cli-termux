"""
Clipboard utilities with Termux-API integration.
Provides cross-platform clipboard support with Termux optimization.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional


class Clipboard:
    """Manages clipboard operations with Termux-API support."""
    
    def __init__(self, use_termux_api: bool = True):
        """
        Initialize clipboard manager.
        
        Args:
            use_termux_api: Whether to use Termux-API if available
        """
        self.use_termux_api = use_termux_api
        self.has_termux_api = self._check_termux_api()
        self.fallback_file = Path.home() / ".gemini_clipboard.txt"
    
    def _check_termux_api(self) -> bool:
        """
        Check if Termux-API is installed and available.
        
        Returns:
            True if Termux-API is available, False otherwise
        """
        if not self.use_termux_api:
            return False
        
        return (
            shutil.which("termux-clipboard-set") is not None and
            shutil.which("termux-clipboard-get") is not None
        )
    
    def copy(self, text: str) -> bool:
        """
        Copy text to clipboard.
        
        Args:
            text: Text to copy
            
        Returns:
            True if successful, False otherwise
        """
        if self.has_termux_api:
            try:
                subprocess.run(
                    ["termux-clipboard-set"],
                    input=text.encode("utf-8"),
                    check=True,
                    capture_output=True
                )
                return True
            except subprocess.CalledProcessError:
                pass
        
        # Fallback: save to file
        try:
            self.fallback_file.write_text(text, encoding="utf-8")
            return False  # Indicate fallback was used
        except Exception:
            return False
    
    def paste(self) -> Optional[str]:
        """
        Paste text from clipboard.
        
        Returns:
            Clipboard text or None if unavailable
        """
        if self.has_termux_api:
            try:
                result = subprocess.run(
                    ["termux-clipboard-get"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout
            except subprocess.CalledProcessError:
                pass
        
        # Fallback: read from file
        if self.fallback_file.exists():
            try:
                return self.fallback_file.read_text(encoding="utf-8")
            except Exception:
                pass
        
        return None
    
    def clear(self) -> bool:
        """
        Clear clipboard contents.
        
        Returns:
            True if successful, False otherwise
        """
        if self.has_termux_api:
            try:
                subprocess.run(
                    ["termux-clipboard-set"],
                    input=b"",
                    check=True,
                    capture_output=True
                )
                return True
            except subprocess.CalledProcessError:
                pass
        
        # Clear fallback file
        if self.fallback_file.exists():
            try:
                self.fallback_file.unlink()
                return True
            except Exception:
                pass
        
        return False
