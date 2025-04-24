"""
Base model class for Noir package.

This module provides the base class for all model implementations in Noir.
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Base class for all models in Noir."""
    
    def __init__(self, model_name: str, model_id: str, supports_websearch: bool = False, debug: bool = False):
        """Initialize a base model.
        
        Args:
            model_name: The display name of the model
            model_id: The API identifier for the model
            supports_websearch: Whether the model supports web search
            debug: Whether to print debug information
        """
        self.model_name = model_name
        self.model_id = model_id
        self.supports_websearch = supports_websearch
        self.debug = debug
        self.system_prompt = ""
        
    def get_model_name(self) -> str:
        """Get the model's display name.
        
        Returns:
            The model's display name
        """
        return self.model_name
    
    def get_model_id(self) -> str:
        """Get the model's API identifier.
        
        Returns:
            The model's API identifier
        """
        return self.model_id
    
    def supports_web_search(self) -> bool:
        """Check if the model supports web search.
        
        Returns:
            True if web search is supported, False otherwise
        """
        return self.supports_websearch
    
    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for the model.
        
        Args:
            prompt: The system prompt to set
        """
        self.system_prompt = prompt
    
    def get_system_prompt(self) -> str:
        """Get the current system prompt.
        
        Returns:
            The current system prompt
        """
        return self.system_prompt
    
    @abstractmethod
    def send_message(self, message: str, websearch: bool = False) -> str:
        """Send a message to the model.
        
        Args:
            message: The message to send
            websearch: Whether to enable web search
            
        Returns:
            The response from the model
        """
        pass
    
    @abstractmethod
    def clear_history(self) -> None:
        """Clear the conversation history."""
        pass
