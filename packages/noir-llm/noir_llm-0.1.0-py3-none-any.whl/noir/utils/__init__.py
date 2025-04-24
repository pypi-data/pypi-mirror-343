"""
Utility functions for Noir package.

This module provides utility functions for the Noir package.
"""

from typing import Dict, List, Any, Optional
import json
import os
import sys

def get_package_dir() -> str:
    """Get the directory where the Noir package is installed.
    
    Returns:
        The directory path
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_user_config_dir() -> str:
    """Get the user configuration directory for Noir.
    
    Returns:
        The directory path
    """
    if sys.platform == "win32":
        base_dir = os.path.expandvars("%APPDATA%")
    else:
        base_dir = os.path.expanduser("~/.config")
    
    config_dir = os.path.join(base_dir, "noir")
    os.makedirs(config_dir, exist_ok=True)
    
    return config_dir

def load_config() -> Dict[str, Any]:
    """Load the user configuration.
    
    Returns:
        The configuration dictionary
    """
    config_file = os.path.join(get_user_config_dir(), "config.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    return {}

def save_config(config: Dict[str, Any]) -> bool:
    """Save the user configuration.
    
    Args:
        config: The configuration dictionary
        
    Returns:
        True if the configuration was saved successfully, False otherwise
    """
    config_file = os.path.join(get_user_config_dir(), "config.json")
    
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        return True
    except IOError:
        return False

def get_config_value(key: str, default: Any = None) -> Any:
    """Get a value from the user configuration.
    
    Args:
        key: The configuration key
        default: The default value to return if the key is not found
        
    Returns:
        The configuration value, or the default value if not found
    """
    config = load_config()
    return config.get(key, default)

def set_config_value(key: str, value: Any) -> bool:
    """Set a value in the user configuration.
    
    Args:
        key: The configuration key
        value: The value to set
        
    Returns:
        True if the value was set successfully, False otherwise
    """
    config = load_config()
    config[key] = value
    return save_config(config)
