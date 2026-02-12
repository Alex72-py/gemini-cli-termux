"""
File handling utilities.
Supports various file formats for Gemini processing.
"""

from pathlib import Path
from typing import List, Optional
import mimetypes


class FileHandler:
    """Handles file operations and validation."""
    
    # Supported file types
    SUPPORTED_EXTENSIONS = {
        # Images
        ".png", ".jpg", ".jpeg", ".webp", ".gif",
        # Documents
        ".pdf", ".txt", ".md",
        # Data
        ".csv", ".json", ".xml",
    }
    
    # MIME type mapping
    MIME_TYPES = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".csv": "text/csv",
        ".json": "application/json",
        ".xml": "application/xml",
    }
    
    @staticmethod
    def is_supported(file_path: Path) -> bool:
        """
        Check if file type is supported.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if supported, False otherwise
        """
        return file_path.suffix.lower() in FileHandler.SUPPORTED_EXTENSIONS
    
    @staticmethod
    def get_mime_type(file_path: Path) -> Optional[str]:
        """
        Get MIME type for file.
        
        Args:
            file_path: Path to file
            
        Returns:
            MIME type string or None
        """
        ext = file_path.suffix.lower()
        return FileHandler.MIME_TYPES.get(ext)
    
    @staticmethod
    def validate_file(file_path: Path) -> bool:
        """
        Validate that file exists and is supported.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if valid, False otherwise
        """
        if not file_path.exists():
            return False
        
        if not file_path.is_file():
            return False
        
        if not FileHandler.is_supported(file_path):
            return False
        
        return True
    
    @staticmethod
    def get_file_info(file_path: Path) -> dict:
        """
        Get file information.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file info
        """
        stat = file_path.stat()
        return {
            "name": file_path.name,
            "size": stat.st_size,
            "mime_type": FileHandler.get_mime_type(file_path),
            "extension": file_path.suffix.lower(),
        }
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string
        """
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
