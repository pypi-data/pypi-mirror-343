"""
Configuration management for the Quantum Financial API.

This package provides functions for loading and managing configuration
for the Quantum Financial API components.
"""

import os
import json
from typing import Dict, Any

def get_default_config_path() -> str:
    """Get the path to the default configuration file."""
    return os.path.join(os.path.dirname(__file__), "default_config.json")

def load_default_config() -> Dict[str, Any]:
    """Load the default configuration from the default_config.json file."""
    config_path = get_default_config_path()
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Default configuration file not found at {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config 