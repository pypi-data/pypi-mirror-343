"""
Model management for Noir package.

This module provides functions for discovering, registering, and accessing
different LLM models supported by Noir.
"""

from typing import Dict, List, Any, Optional
from noir.models.base import BaseModel

# Registry to store available models
_MODEL_REGISTRY = {}

def register_model(model_id: str, model_class: Any) -> None:
    """Register a model with the Noir package.

    Args:
        model_id: Unique identifier for the model
        model_class: The model class to register
    """
    _MODEL_REGISTRY[model_id] = model_class

def get_model(model_id: str, **kwargs) -> Optional[BaseModel]:
    """Get a model instance by its ID.

    Args:
        model_id: The ID of the model to retrieve
        **kwargs: Additional arguments to pass to the model constructor

    Returns:
        An instance of the requested model, or None if not found
    """
    if model_id not in _MODEL_REGISTRY:
        return None

    return _MODEL_REGISTRY[model_id](**kwargs)

def get_available_models(debug: bool = False) -> Dict[str, BaseModel]:
    """Get all available models.

    Args:
        debug: Whether to enable debug mode for the models

    Returns:
        A dictionary of model instances with model IDs as keys
    """
    return {model_id: model_class(debug=debug)
            for model_id, model_class in _MODEL_REGISTRY.items()}

def list_models() -> List[str]:
    """List all available model IDs.

    Returns:
        A list of available model IDs
    """
    return list(_MODEL_REGISTRY.keys())

# Import specific model implementations to register them
from noir.models.zai import GLM4Model, Z1Model, Z1RuminationModel
from noir.models.venice import MistralModel, Llama32Model

# Register models
register_model("glm-4-32b", GLM4Model)
register_model("z1-32b", Z1Model)
register_model("z1-rumination", Z1RuminationModel)
register_model("mistral-31-24b", MistralModel)
register_model("llama-3.2-3b", Llama32Model)
