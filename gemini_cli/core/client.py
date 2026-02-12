"""
Gemini API client for chat and generation.
Handles all interactions with Google's Generative AI API.
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional, Generator
from pathlib import Path
import mimetypes


class GeminiClient:
    """Client for interacting with Gemini API."""
    
    # Available models
    MODELS = [
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-thinking-exp",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
    ]
    
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash-exp",
        **generation_config
    ):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API key
            model: Model name to use
            **generation_config: Additional generation parameters
        """
        self.api_key = api_key
        self.model_name = model
        self.generation_config = generation_config
        
        # Configure API
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )
        
        # Chat session
        self.chat_session = None
    
    def start_chat(self, history: Optional[List[Dict[str, str]]] = None) -> None:
        """
        Start a new chat session.
        
        Args:
            history: Optional conversation history
        """
        formatted_history = []
        if history:
            for msg in history:
                formatted_history.append({
                    "role": msg["role"],
                    "parts": [msg["content"]]
                })
        
        self.chat_session = self.model.start_chat(history=formatted_history)
    
    def send_message(
        self,
        message: str,
        stream: bool = False
    ) -> Generator[str, None, None] | str:
        """
        Send a message in the current chat session.
        
        Args:
            message: Message to send
            stream: Whether to stream the response
            
        Returns:
            Response text or generator for streaming
        """
        if self.chat_session is None:
            self.start_chat()
        
        if stream:
            response = self.chat_session.send_message(message, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        else:
            response = self.chat_session.send_message(message)
            return response.text
    
    def send_message_with_files(
        self,
        message: str,
        files: List[Path],
        stream: bool = False
    ) -> Generator[str, None, None] | str:
        """
        Send a message with file attachments.
        
        Args:
            message: Message to send
            files: List of file paths to attach
            stream: Whether to stream the response
            
        Returns:
            Response text or generator for streaming
        """
        # Upload files
        uploaded_files = []
        for file_path in files:
            try:
                uploaded_file = genai.upload_file(path=str(file_path))
                uploaded_files.append(uploaded_file)
            except Exception as e:
                print(f"Warning: Could not upload {file_path}: {e}")
        
        # Prepare content parts
        parts = [message]
        parts.extend(uploaded_files)
        
        if self.chat_session is None:
            self.start_chat()
        
        if stream:
            response = self.chat_session.send_message(parts, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        else:
            response = self.chat_session.send_message(parts)
            return response.text
    
    def generate_content(
        self,
        prompt: str,
        stream: bool = False
    ) -> Generator[str, None, None] | str:
        """
        Generate content without chat context (one-shot).
        
        Args:
            prompt: Prompt to generate from
            stream: Whether to stream the response
            
        Returns:
            Generated text or generator for streaming
        """
        if stream:
            response = self.model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        else:
            response = self.model.generate_content(prompt)
            return response.text
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get chat history.
        
        Returns:
            List of messages with role and content
        """
        if self.chat_session is None:
            return []
        
        history = []
        for msg in self.chat_session.history:
            history.append({
                "role": msg.role,
                "content": msg.parts[0].text if msg.parts else ""
            })
        return history
    
    def clear_history(self) -> None:
        """Clear chat history and start fresh."""
        self.chat_session = None
    
    def set_model(self, model: str) -> None:
        """
        Change the model.
        
        Args:
            model: New model name
        """
        if model not in self.MODELS:
            raise ValueError(f"Unknown model: {model}. Available: {self.MODELS}")
        
        self.model_name = model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )
        
        # Reset chat session
        self.chat_session = None
    
    def update_generation_config(self, **kwargs) -> None:
        """
        Update generation configuration.
        
        Args:
            **kwargs: Generation parameters to update
        """
        self.generation_config.update(kwargs)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )
