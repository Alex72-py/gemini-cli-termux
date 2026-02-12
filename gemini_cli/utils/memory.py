"""
Conversation history and memory management.
Handles saving and loading chat sessions.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class ConversationMemory:
    """Manages conversation history storage and retrieval."""
    
    def __init__(self, data_dir: Optional[Path] = None, max_entries: int = 1000):
        """
        Initialize conversation memory.
        
        Args:
            data_dir: Directory for storing history
            max_entries: Maximum number of messages to keep
        """
        if data_dir is None:
            data_dir = Path.home() / ".local" / "share" / "gemini-cli"
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.data_dir / "history.json"
        self.max_entries = max_entries
        self.history = []
        
        self.load()
    
    def add_message(self, role: str, content: str, timestamp: Optional[str] = None) -> None:
        """
        Add a message to history.
        
        Args:
            role: Message role ('user' or 'model')
            content: Message content
            timestamp: Optional timestamp (generated if not provided)
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        
        self.history.append(message)
        
        # Trim if exceeds max entries
        if len(self.history) > self.max_entries:
            self.history = self.history[-self.max_entries:]
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get conversation history.
        
        Args:
            limit: Optional limit on number of messages
            
        Returns:
            List of messages
        """
        if limit:
            return self.history[-limit:]
        return self.history.copy()
    
    def clear(self) -> None:
        """Clear all conversation history."""
        self.history = []
    
    def save(self) -> bool:
        """
        Save history to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving history: {e}")
            return False
    
    def load(self) -> bool:
        """
        Load history from file.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.history_file.exists():
            return False
        
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)
            
            # Trim if exceeds max entries
            if len(self.history) > self.max_entries:
                self.history = self.history[-self.max_entries:]
            
            return True
        except Exception as e:
            print(f"Error loading history: {e}")
            return False
    
    def export_to_file(self, output_path: Path) -> bool:
        """
        Export conversation to a text file.
        
        Args:
            output_path: Path to save conversation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("# Gemini Conversation History\n\n")
                
                for msg in self.history:
                    timestamp = msg.get("timestamp", "")
                    role = msg["role"].upper()
                    content = msg["content"]
                    
                    f.write(f"## {role}")
                    if timestamp:
                        f.write(f" ({timestamp})")
                    f.write("\n\n")
                    f.write(content)
                    f.write("\n\n---\n\n")
            
            return True
        except Exception as e:
            print(f"Error exporting conversation: {e}")
            return False
    
    def get_context_for_api(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        Get recent history formatted for API.
        
        Args:
            limit: Number of recent messages to include
            
        Returns:
            List of messages in API format
        """
        recent = self.history[-limit:] if len(self.history) > limit else self.history
        
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in recent
        ]
