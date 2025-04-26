"""
Quantum-AI Model Architecture Module

This module provides tools for validating and ensuring compatibility between
quantum measurements and AI model architectures. It includes:

1. Model architecture validation
2. Layer compatibility checking
3. Automated architecture adjustment
4. Shape requirement verification
"""

import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Layer
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass
import logging
from quantum_ai_utils import validate_quantum_input_shape, standardize_quantum_input

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelRequirements:
    """Requirements for model architecture compatibility."""
    input_shape: Tuple[int, ...]
    output_shape: Tuple[int, ...]
    expected_dtype: str = 'float32'
    supports_batch_dimension: bool = True
    requires_normalization: bool = False
    supports_variable_length: bool = False
    minimum_input_size: Optional[int] = None
    maximum_input_size: Optional[int] = None
    
    def __str__(self) -> str:
        return (
            f"Model Requirements:\n"
            f"  Input Shape: {self.input_shape}\n"
            f"  Output Shape: {self.output_shape}\n"
            f"  Data Type: {self.expected_dtype}\n"
            f"  Batch Support: {'Yes' if self.supports_batch_dimension else 'No'}\n"
            f"  Normalization Required: {'Yes' if self.requires_normalization else 'No'}\n"
            f"  Variable Length Support: {'Yes' if self.supports_variable_length else 'No'}\n"
            f"  Size Constraints: {self.minimum_input_size} to {self.maximum_input_size}"
        )

class ModelArchitectureValidator:
    """Validates and ensures model architecture compatibility."""
    
    def __init__(self, model: Union[Model, Sequential]):
        """Initialize with a Keras model."""
        self.model = model
        self.requirements = self._analyze_model_requirements()
        
    def _analyze_model_requirements(self) -> ModelRequirements:
        """Analyze the model to determine its requirements."""
        # Get input shape from the model
        if isinstance(self.model.input_shape, tuple):
            input_shape = self.model.input_shape[1:]  # Remove batch dimension
        else:
            # Handle multiple inputs case
            if isinstance(self.model.input_shape, list):
                # Take the first input shape for now
                input_shape = self.model.input_shape[0][1:] if self.model.input_shape else (None,)
            else:
                # Handle tuple of tuples or other cases
                try:
                    input_shape = tuple(shape[1:] for shape in self.model.input_shape)
                except (TypeError, IndexError):
                    # Fallback to a generic shape if we can't determine
                    input_shape = (None,)
        
        # Get output shape
        if isinstance(self.model.output_shape, tuple):
            output_shape = self.model.output_shape[1:]
        else:
            try:
                # Handle multiple outputs case
                if isinstance(self.model.output_shape, list):
                    output_shape = self.model.output_shape[0][1:] if self.model.output_shape else (None,)
                else:
                    # Handle tuple of tuples or other cases
                    output_shape = tuple(shape[1:] for shape in self.model.output_shape)
            except (TypeError, IndexError):
                # Fallback to a generic shape if we can't determine
                output_shape = (None,)
        
        # Analyze layer properties
        requires_normalization = any(
            'normalization' in layer.name.lower() 
            for layer in self.model.layers
        )
        
        # Check for recurrent/1D conv layers that might support variable length
        supports_variable_length = any(
            isinstance(layer, (tf.keras.layers.LSTM, tf.keras.layers.Conv1D))
            for layer in self.model.layers
        )
        
        # Get size constraints from Conv/Pool layers
        size_constraints = self._analyze_size_constraints()
        
        return ModelRequirements(
            input_shape=input_shape,
            output_shape=output_shape,
            requires_normalization=requires_normalization,
            supports_variable_length=supports_variable_length,
            minimum_input_size=size_constraints['min'],
            maximum_input_size=size_constraints['max']
        )
    
    def _analyze_size_constraints(self) -> Dict[str, Optional[int]]:
        """Analyze model layers to determine input size constraints."""
        min_size = None
        max_size = None
        
        for layer in self.model.layers:
            if hasattr(layer, 'kernel_size'):
                # Conv layers need at least kernel_size elements
                kernel_size = (
                    layer.kernel_size[0] 
                    if isinstance(layer.kernel_size, tuple) 
                    else layer.kernel_size
                )
                min_size = max(min_size or kernel_size, kernel_size)
            
            if hasattr(layer, 'pool_size'):
                # Pool layers need at least pool_size elements
                pool_size = (
                    layer.pool_size[0] 
                    if isinstance(layer.pool_size, tuple) 
                    else layer.pool_size
                )
                min_size = max(min_size or pool_size, pool_size)
        
        return {'min': min_size, 'max': max_size}
    
    def validate_input(self, quantum_data: np.ndarray) -> Tuple[bool, str, List[str]]:
        """
        Validate quantum data against model requirements.
        
        Args:
            quantum_data: Input data from quantum measurements
            
        Returns:
            Tuple of (is_valid, message, required_transforms)
        """
        # Handle 1D arrays by adding necessary dimensions
        if len(quantum_data.shape) == 1:
            # For 1D input, reshape based on the expected input shape
            logger.info(f"Received 1D array with shape {quantum_data.shape}, will reshape to match requirements")
            required_transforms = ['reshape_1d_array']
            return False, f"1D array needs reshaping to match {self.requirements.input_shape}", required_transforms
        
        # Validate shape
        shape_validation = validate_quantum_input_shape(
            quantum_data,
            self.requirements.input_shape,
            self.requirements.supports_batch_dimension
        )
        
        if not shape_validation.is_valid:
            return False, shape_validation.message, shape_validation.required_transforms
        
        # Validate dtype
        if quantum_data.dtype != np.dtype(self.requirements.expected_dtype):
            return (
                False,
                f"Data type mismatch: got {quantum_data.dtype}, expected {self.requirements.expected_dtype}",
                ['convert_dtype']
            )
        
        # Validate size constraints
        if self.requirements.minimum_input_size:
            if quantum_data.shape[1] < self.requirements.minimum_input_size:
                return (
                    False,
                    f"Input size too small: got {quantum_data.shape[1]}, minimum {self.requirements.minimum_input_size}",
                    ['pad_to_min_size']
                )
        
        if self.requirements.maximum_input_size:
            if quantum_data.shape[1] > self.requirements.maximum_input_size:
                return (
                    False,
                    f"Input size too large: got {quantum_data.shape[1]}, maximum {self.requirements.maximum_input_size}",
                    ['truncate_to_max_size']
                )
        
        # All validations passed
        return True, "Input is valid", []
    
    def prepare_input(self, quantum_data: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Prepare quantum data for model input.
        
        Args:
            quantum_data: Raw quantum measurement data
            
        Returns:
            Tuple of (prepared_data, transformation_info)
        """
        transform_info = {
            'transforms_applied': [],
            'original_shape': quantum_data.shape,
            'target_shape': self.requirements.input_shape
        }
        
        # Handle 1D arrays by appropriately reshaping to match requirements
        if len(quantum_data.shape) == 1:
            # Calculate the target size needed to reshape properly
            target_size = np.prod(self.requirements.input_shape)
            current_size = quantum_data.shape[0]
            
            # If data is too small, pad it
            if current_size < target_size:
                padded_data = np.pad(
                    quantum_data, 
                    (0, target_size - current_size),
                    mode='constant', 
                    constant_values=0.0
                )
                transform_info['transforms_applied'].append('padded_1d_array')
                transform_info['padding_added'] = target_size - current_size
                standardized_data = padded_data.reshape((1,) + self.requirements.input_shape)
            # If data is too large, truncate it
            elif current_size > target_size:
                truncated_data = quantum_data[:target_size]
                transform_info['transforms_applied'].append('truncated_1d_array')
                transform_info['data_truncated'] = current_size - target_size
                standardized_data = truncated_data.reshape((1,) + self.requirements.input_shape)
            # If data is exactly the right size, just reshape
            else:
                transform_info['transforms_applied'].append('reshaped_1d_array')
                standardized_data = quantum_data.reshape((1,) + self.requirements.input_shape)
        else:
            # First standardize the input using the normal method
            standardized_data, std_transform_info = standardize_quantum_input(
                quantum_data,
                self.requirements.input_shape,
                allow_batch_dim=self.requirements.supports_batch_dimension
            )
            # Merge the transformation info
            transform_info['transforms_applied'].extend(std_transform_info.get('transforms_applied', []))
            for key, value in std_transform_info.items():
                if key != 'transforms_applied':
                    transform_info[key] = value
        
        # Apply any additional required transformations
        if self.requirements.requires_normalization:
            standardized_data = (standardized_data - np.mean(standardized_data)) / np.std(standardized_data)
            transform_info['transforms_applied'].append('normalized')
        
        transform_info['final_shape'] = standardized_data.shape
        return standardized_data, transform_info
    
    def get_layer_info(self) -> List[Dict[str, Any]]:
        """Get detailed information about model layers."""
        layer_info = []
        
        for layer in self.model.layers:
            info = {
                'name': layer.name,
                'type': layer.__class__.__name__,
                'parameters': layer.count_params()
            }
            
            # Safe way to get input/output shapes that works with all layer types
            # Some layers like LSTM and InputLayer may not have direct input_shape attribute
            if hasattr(layer, '_input_shape'):
                info['input_shape'] = layer._input_shape
            elif hasattr(layer, 'input_spec') and layer.input_spec is not None:
                if hasattr(layer.input_spec, 'shape') and layer.input_spec.shape is not None:
                    info['input_shape'] = layer.input_spec.shape
                elif isinstance(layer.input_spec, list) and len(layer.input_spec) > 0:
                    if hasattr(layer.input_spec[0], 'shape') and layer.input_spec[0].shape is not None:
                        info['input_shape'] = layer.input_spec[0].shape
            
            # For output shape, safely get it
            try:
                if hasattr(layer, 'output_shape'):
                    info['output_shape'] = layer.output_shape
                elif hasattr(layer, 'output'):
                    info['output_shape'] = layer.output.shape
                else:
                    # Use input shape as fallback
                    info['output_shape'] = info.get('input_shape', 'unknown')
            except AttributeError:
                # Handle the case where output_shape is not available
                info['output_shape'] = 'unknown'
            
            # Add layer-specific information
            if hasattr(layer, 'activation'):
                info['activation'] = layer.activation.__name__
            if hasattr(layer, 'kernel_size'):
                info['kernel_size'] = layer.kernel_size
            if hasattr(layer, 'pool_size'):
                info['pool_size'] = layer.pool_size
            if hasattr(layer, 'rate'):
                info['dropout_rate'] = layer.rate
                
            layer_info.append(info)
        
        return layer_info
    
    def visualize_architecture(self, output_path: Optional[str] = None):
        """Visualize model architecture."""
        try:
            tf.keras.utils.plot_model(
                self.model,
                to_file=output_path or 'model_architecture.png',
                show_shapes=True,
                show_layer_names=True,
                show_layer_activations=True
            )
        except Exception as e:
            logger.warning(f"Could not generate model visualization: {e}")
    
    def suggest_architecture_improvements(self) -> List[str]:
        """Suggest possible improvements to the model architecture."""
        suggestions = []
        
        # Check for normalization
        if not self.requirements.requires_normalization:
            suggestions.append(
                "Consider adding BatchNormalization layers for better training stability"
            )
        
        # Check for dropout
        has_dropout = any(
            isinstance(layer, tf.keras.layers.Dropout)
            for layer in self.model.layers
        )
        if not has_dropout:
            suggestions.append(
                "Consider adding Dropout layers to prevent overfitting"
            )
        
        # Check for activation functions
        for layer in self.model.layers:
            if hasattr(layer, 'activation'):
                if layer.activation.__name__ == 'linear':
                    suggestions.append(
                        f"Consider adding non-linear activation to layer '{layer.name}'"
                    )
        
        return suggestions

def create_compatible_model(
    input_shape: Tuple[int, ...],
    output_shape: Tuple[int, ...],
    model_type: str = 'lstm',
    complexity: str = 'medium'
) -> Model:
    """
    Create a model architecture compatible with quantum data.
    
    Args:
        input_shape: Required input shape
        output_shape: Required output shape
        model_type: Type of model ('lstm', 'cnn', 'hybrid')
        complexity: Model complexity ('simple', 'medium', 'complex')
        
    Returns:
        A compatible Keras model
    """
    model = Sequential()
    
    if model_type == 'lstm':
        # LSTM architecture
        units = {
            'simple': [32],
            'medium': [64, 32],
            'complex': [128, 64, 32]
        }[complexity]
        
        for i, unit in enumerate(units):
            return_sequences = i < len(units) - 1
            if i == 0:
                model.add(tf.keras.layers.LSTM(
                    unit,
                    input_shape=input_shape,
                    return_sequences=return_sequences
                ))
            else:
                model.add(tf.keras.layers.LSTM(
                    unit,
                    return_sequences=return_sequences
                ))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.Dropout(0.2))
            
    elif model_type == 'cnn':
        # CNN architecture
        filters = {
            'simple': [32],
            'medium': [32, 64],
            'complex': [32, 64, 128]
        }[complexity]
        
        for i, filter_size in enumerate(filters):
            if i == 0:
                model.add(tf.keras.layers.Conv1D(
                    filter_size, 3,
                    activation='relu',
                    input_shape=input_shape
                ))
            else:
                model.add(tf.keras.layers.Conv1D(
                    filter_size, 3,
                    activation='relu'
                ))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.MaxPooling1D(2))
            
        model.add(tf.keras.layers.GlobalAveragePooling1D())
        
    elif model_type == 'hybrid':
        # Hybrid CNN-LSTM architecture
        if complexity == 'simple':
            model.add(tf.keras.layers.Conv1D(32, 3, activation='relu', input_shape=input_shape))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.LSTM(32))
        else:
            model.add(tf.keras.layers.Conv1D(64, 3, activation='relu', input_shape=input_shape))
            model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.MaxPooling1D(2))
            model.add(tf.keras.layers.Conv1D(32, 3, activation='relu'))
            model.add(tf.keras.layers.BatchNormalization())
            if complexity == 'complex':
                model.add(tf.keras.layers.Conv1D(32, 3, activation='relu'))
                model.add(tf.keras.layers.BatchNormalization())
            model.add(tf.keras.layers.LSTM(64, return_sequences=True))
            model.add(tf.keras.layers.LSTM(32))
    
    # Add final dense layers
    model.add(tf.keras.layers.Dense(32, activation='relu'))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(np.prod(output_shape)))
    model.add(tf.keras.layers.Reshape(output_shape))
    
    return model 