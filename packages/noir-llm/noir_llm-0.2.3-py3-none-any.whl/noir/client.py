"""
Main client interface for Noir package.

This module provides the main client interface for interacting with
language models through the Noir package.
"""

from typing import Dict, List, Any, Optional
from noir.models import get_model, list_models

class NoirClient:
    """Main client interface for Noir package."""

    def __init__(self, model_id: Optional[str] = None, debug: bool = False):
        """Initialize the Noir client.

        Args:
            model_id: The ID of the model to use. If None, no model is selected.
            debug: Whether to enable debug mode (default: False)
        """
        self.debug = debug
        self.current_model = None

        if model_id:
            self.select_model(model_id)

    def select_model(self, model_id: str) -> bool:
        """Select a model to use.

        Args:
            model_id: The ID of the model to select

        Returns:
            True if the model was successfully selected, False otherwise
        """
        model = get_model(model_id, debug=self.debug)
        if model:
            self.current_model = model
            return True
        return False

    def get_current_model(self) -> Optional[str]:
        """Get the ID of the currently selected model.

        Returns:
            The ID of the currently selected model, or None if no model is selected
        """
        if self.current_model:
            return self.current_model.get_model_id()
        return None

    def get_available_models(self) -> List[str]:
        """Get a list of available model IDs.

        Returns:
            A list of available model IDs
        """
        return list_models()

    def set_system_prompt(self, prompt: str) -> bool:
        """Set the system prompt for the current model.

        Args:
            prompt: The system prompt to set

        Returns:
            True if the prompt was set successfully, False if no model is selected
        """
        if not self.current_model:
            return False

        self.current_model.set_system_prompt(prompt)
        return True

    def get_system_prompt(self) -> Optional[str]:
        """Get the system prompt for the current model.

        Returns:
            The current system prompt, or None if no model is selected
        """
        if not self.current_model:
            return None

        return self.current_model.get_system_prompt()

    def send_message(self, message: str, websearch: bool = False) -> Optional[str]:
        """Send a message to the current model.

        Args:
            message: The message to send
            websearch: Whether to enable web search

        Returns:
            The response from the model, or None if no model is selected
        """
        if not self.current_model:
            return None

        return self.current_model.send_message(message, websearch=websearch)

    def clear_history(self) -> bool:
        """Clear the conversation history for the current model.

        Returns:
            True if the history was cleared successfully, False if no model is selected
        """
        if not self.current_model:
            return False

        self.current_model.clear_history()
        return True
