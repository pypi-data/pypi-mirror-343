#!/usr/bin/env python3

"""
Logging Utility Module for Quantum Risk Assessment

This module provides standardized logging configuration for the quantum risk assessment
components, ensuring consistent logging format and behavior across the project.

Author: Quantum-AI Team
"""

import logging
from typing import Optional

def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger with standardized formatting.
    
    Args:
        name: Optional name for the logger (defaults to root logger if None)
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger
    """
    # Configure the logger
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Get the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Only add handler if it doesn't already have one to prevent duplicate logs
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger 