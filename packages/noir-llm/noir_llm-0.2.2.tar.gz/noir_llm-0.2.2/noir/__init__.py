"""
Noir - A Python package for accessing various LLM models

Noir provides a unified interface for interacting with different LLM providers,
allowing users to easily access and use various language models in their projects.
"""

__version__ = "0.2.2"

from noir.models import get_available_models, list_models
from noir.client import NoirClient

__all__ = [
    "get_available_models",
    "list_models",
    "NoirClient"
]
