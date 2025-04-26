"""
Port Management Utility

This module provides utilities for managing port assignments and detecting/resolving
port conflicts in the application. It includes functionality to:

1. Check if a port is available
2. Find the next available port in a range
3. Log port usage across different application components
4. Automatically resolve port conflicts when they occur

Usage:
    from port_manager import PortManager
    
    # Create a port manager with default settings
    port_mgr = PortManager()
    
    # Get an available port
    port = port_mgr.get_available_port(preferred_port=5002)
    
    # Register a component's port usage
    port_mgr.register_port_usage("flask_backend", port)
"""

import os
import socket
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('port_manager')

class PortManager:
    """Manages port assignment and conflict resolution for the application."""
    
    def __init__(self, 
                 config_path: str = None, 
                 port_range: Tuple[int, int] = (5000, 5100)):
        """Initialize the port manager.
        
        Args:
            config_path: Path to the port configuration file. If None, uses default.
            port_range: Range of ports to consider (min, max) inclusive.
        """
        self.port_range = port_range
        
        if config_path is None:
            # Use a file in the same directory as this module
            self.config_path = Path(__file__).parent / 'port_config.json'
        else:
            self.config_path = Path(config_path)
            
        # Load existing configuration or create new one
        self.load_config()
    
    def load_config(self) -> None:
        """Load port configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                    logger.info(f"Loaded port configuration from {self.config_path}")
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in {self.config_path}, creating new config")
                self.create_default_config()
        else:
            logger.info(f"No config file found at {self.config_path}, creating new config")
            self.create_default_config()
    
    def create_default_config(self) -> None:
        """Create a default port configuration."""
        self.config = {
            "port_assignments": {},
            "last_scan_time": None,
            "port_range": self.port_range
        }
        self.save_config()
    
    def save_config(self) -> None:
        """Save the current configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
                logger.info(f"Saved port configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save port configuration: {e}")
    
    def is_port_available(self, port: int) -> bool:
        """Check if a port is available.
        
        Args:
            port: The port to check.
            
        Returns:
            bool: True if the port is available, False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return True
            except socket.error:
                return False
    
    def get_available_port(self, preferred_port: int = None) -> int:
        """Get an available port, preferring the specified port if available.
        
        Args:
            preferred_port: The port to use if available.
            
        Returns:
            int: An available port.
        """
        # Try the preferred port first
        if preferred_port is not None and self.is_port_available(preferred_port):
            logger.info(f"Preferred port {preferred_port} is available")
            return preferred_port
        
        # Otherwise scan for an available port in the range
        min_port, max_port = self.port_range
        for port in range(min_port, max_port + 1):
            if self.is_port_available(port):
                logger.info(f"Found available port: {port}")
                return port
        
        # If no ports are available, log an error and return the preferred port
        # (it will fail when used, but that's better than an arbitrary port)
        logger.error(f"No available ports in range {min_port}-{max_port}")
        return preferred_port or min_port
    
    def register_port_usage(self, component_name: str, port: int) -> None:
        """Register that a component is using a specific port.
        
        Args:
            component_name: Name of the component using the port.
            port: The port being used.
        """
        self.config["port_assignments"][component_name] = port
        self.save_config()
        logger.info(f"Registered port {port} for component '{component_name}'")
    
    def get_component_port(self, component_name: str) -> Optional[int]:
        """Get the port assigned to a component.
        
        Args:
            component_name: Name of the component.
            
        Returns:
            int or None: The port assigned to the component, or None if not found.
        """
        return self.config["port_assignments"].get(component_name)
    
    def list_port_assignments(self) -> Dict[str, int]:
        """Get all port assignments.
        
        Returns:
            dict: A dictionary mapping component names to port numbers.
        """
        return self.config["port_assignments"]

# Convenience function to get an available port
def get_available_port(preferred_port: int = None) -> int:
    """Get an available port, creating a PortManager instance if needed.
    
    Args:
        preferred_port: The preferred port to use if available.
        
    Returns:
        int: An available port.
    """
    port_mgr = PortManager()
    return port_mgr.get_available_port(preferred_port) 