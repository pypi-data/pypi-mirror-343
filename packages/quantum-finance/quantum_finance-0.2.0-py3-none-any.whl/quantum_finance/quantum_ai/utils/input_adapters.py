#!/usr/bin/env python3

"""
Input Adapter Module

This module provides utility functions for adapting quantum measurement data
to formats suitable for AI model inputs.
"""

import logging
from typing import Optional, Tuple, Union, List, Dict

import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def adapt_quantum_input_for_model(
    input_data: np.ndarray, target_shape: Tuple[int, ...] = (60, 1)
) -> np.ndarray:
    """
    Adapt quantum measurement data to the shape expected by the AI model.

    This function is deprecated. Please use standardize_quantum_input instead.

    Args:
        input_data: Quantum measurement data as a numpy array
        target_shape: Target shape for the model input

    Returns:
        Reshaped input data suitable for the model
    """
    logger.warning(
        "adapt_quantum_input_for_model is deprecated. Please use standardize_quantum_input instead."
    )

    # Handle empty input
    if input_data is None or input_data.size == 0:
        # Return zeros with the target shape
        return np.zeros((1,) + target_shape)

    # Ensure input is a numpy array
    if not isinstance(input_data, np.ndarray):
        input_data = np.array(input_data)

    # Flatten the input if it's multi-dimensional
    flattened = input_data.flatten()

    # Calculate total elements in target shape
    target_elements = np.prod(target_shape)

    # Resize the input to match the target number of elements
    if flattened.size < target_elements:
        # Pad with zeros
        padded = np.zeros(target_elements)
        padded[: flattened.size] = flattened
        resized = padded
    elif flattened.size > target_elements:
        # Truncate
        resized = flattened[:target_elements]
    else:
        resized = flattened

    # Reshape to target shape and add batch dimension
    result = resized.reshape((1,) + target_shape)

    return result


def standardize_quantum_input(
    input_data: Union[np.ndarray, List, Dict[str, int]], 
    target_shape: Tuple[int, ...] = (60, 1),
    normalize: bool = True
) -> np.ndarray:
    """Standardizes quantum measurement input for the AI model.

    Args:
        input_data: Quantum measurement data which could be:
            - numpy array of probabilities or counts
            - list of values
            - dictionary of counts (e.g., {'00': 500, '01': 300, ...})
        target_shape: Target shape for the model input
        normalize: Whether to normalize values between 0-1

    Returns:
        Numpy array with standardized shape ready for model input
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Standardizing input with original type: {type(input_data)}")
    
    # Handle empty input
    if input_data is None or (hasattr(input_data, 'size') and input_data.size == 0):
        logger.warning("Empty input data received, creating zero array")
        return np.zeros((1,) + target_shape)

    # Handle dictionary input (common for quantum counts)
    if isinstance(input_data, dict):
        # Convert dictionary to array of probabilities
        total = sum(input_data.values())
        if total == 0:
            logger.warning("Dictionary with zero total count, creating uniform distribution")
            # Create a uniform distribution as a fallback
            values = np.ones(2**len(next(iter(input_data), "0")))
            values = values / values.sum()
        else:
            # Sort keys to ensure consistent ordering
            sorted_keys = sorted(input_data.keys())
            values = np.array([input_data.get(k, 0) / total for k in sorted_keys])
        input_data = values

    # Convert to numpy array if it's not already
    if not isinstance(input_data, np.ndarray):
        try:
            input_data = np.array(input_data, dtype=np.float32)
        except Exception as e:
            logger.error(f"Failed to convert input to numpy array: {e}")
            # Provide a fallback
            return np.zeros((1,) + target_shape)

    # Log shape for debugging
    logger.debug(f"Input shape before processing: {input_data.shape}")
    
    # Normalize values between 0-1 if requested
    if normalize and input_data.size > 0:
        min_val = input_data.min()
        max_val = input_data.max()
        
        # Only normalize if there's a range to normalize
        if max_val > min_val:
            input_data = (input_data - min_val) / (max_val - min_val)
    
    # Handle different input shapes
    # If 1D array, reshape to match target shape
    if len(input_data.shape) == 1:
        # If input is smaller than target, pad with zeros
        if input_data.size < target_shape[0]:
            logger.debug(f"Input size {input_data.size} smaller than target {target_shape[0]}, padding")
            padded = np.zeros(target_shape[0])
            padded[:input_data.size] = input_data
            input_data = padded
        # If input is larger than target, truncate
        elif input_data.size > target_shape[0]:
            logger.debug(f"Input size {input_data.size} larger than target {target_shape[0]}, truncating")
            input_data = input_data[:target_shape[0]]
            
        # Reshape to target shape
        input_data = input_data.reshape(target_shape)
    
    # If already 2D or higher, reshape carefully
    elif len(input_data.shape) >= 2:
        # For 2D input, if first dimension is not 1, add batch dimension
        if input_data.shape[0] != 1:
            # Add batch dimension
            input_data = np.expand_dims(input_data, axis=0)
    
    # Ensure we have a batch dimension (needed for TensorFlow models)
    if len(input_data.shape) < 3 and target_shape == (60, 1):
        # Check if we need to add the batch dimension
        if input_data.shape != (1,) + target_shape:
            input_data = np.expand_dims(input_data, axis=0)
    
    logger.debug(f"Final standardized input shape: {input_data.shape}")
    return input_data
