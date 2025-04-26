"""
Quantum AI Utilities Module

This module contains utility functions for the quantum-AI interface,
particularly for handling data conversion between quantum and AI components.
"""

import numpy as np
import logging
from typing import Tuple, Union, Optional, Dict, List, Any
from dataclasses import dataclass

# Configure logging - but make it less verbose
logging.basicConfig(level=logging.INFO)

@dataclass
class ShapeValidationResult:
    """Results from shape validation."""
    is_valid: bool
    message: str
    required_transforms: list
    original_shape: tuple
    target_shape: tuple
    
    def __str__(self) -> str:
        return (f"Shape Validation: {'✅' if self.is_valid else '❌'}\n"
                f"Message: {self.message}\n"
                f"Original Shape: {self.original_shape}\n"
                f"Target Shape: {self.target_shape}\n"
                f"Required Transforms: {', '.join(self.required_transforms)}")

def validate_quantum_input_shape(
    input_tensor: np.ndarray,
    expected_shape: Tuple[int, ...],
    allow_batch_dim: bool = True
) -> ShapeValidationResult:
    """
    Validate the shape of quantum measurement input against expected model input shape.
    
    Args:
        input_tensor: Input tensor from quantum measurement
        expected_shape: Expected shape (excluding batch dimension)
        allow_batch_dim: Whether to allow/expect a batch dimension
        
    Returns:
        ShapeValidationResult object containing validation details
    """
    current_shape = input_tensor.shape
    required_transforms = []
    
    # Handle batch dimension
    if allow_batch_dim:
        if len(current_shape) == len(expected_shape):
            required_transforms.append("add_batch_dim")
            validation_shape = (1,) + current_shape
        else:
            validation_shape = current_shape
    else:
        validation_shape = current_shape
    
    # Check dimensionality
    if len(validation_shape) != len(expected_shape) + (1 if allow_batch_dim else 0):
        return ShapeValidationResult(
            is_valid=False,
            message=f"Dimension mismatch: Got {len(validation_shape)}, expected {len(expected_shape) + (1 if allow_batch_dim else 0)}",
            required_transforms=["reshape"],
            original_shape=current_shape,
            target_shape=expected_shape
        )
    
    # Check each dimension
    for i, (current, expected) in enumerate(zip(validation_shape[1:] if allow_batch_dim else validation_shape, expected_shape)):
        if current != expected:
            if current < expected:
                required_transforms.append(f"pad_dim_{i}")
            else:
                required_transforms.append(f"truncate_dim_{i}")
    
    is_valid = len(required_transforms) == 0
    message = "Shape is valid" if is_valid else "Shape requires transformation"
    
    return ShapeValidationResult(
        is_valid=is_valid,
        message=message,
        required_transforms=required_transforms,
        original_shape=current_shape,
        target_shape=expected_shape
    )

def standardize_quantum_input(
    quantum_data: np.ndarray,
    target_shape: Tuple[int, ...],
    padding_mode: str = 'constant',
    padding_value: float = 0.0,
    allow_batch_dim: bool = True
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Standardize quantum measurement data to match model input requirements.
    
    This function handles:
    1. Shape validation
    2. Automatic reshaping
    3. Padding/truncation
    4. Batch dimension handling
    5. Type conversion
    
    Args:
        quantum_data: Raw quantum measurement data
        target_shape: Required model input shape (excluding batch dimension)
        padding_mode: How to pad ('constant', 'edge', 'reflect')
        padding_value: Value to use for constant padding
        allow_batch_dim: Whether to allow/expect a batch dimension
        
    Returns:
        Tuple of (standardized_tensor, transformation_info)
    """
    # Validate target_shape argument
    if not (isinstance(target_shape, tuple) and all(isinstance(d, int) for d in target_shape)):
        raise ValueError("Invalid target_shape; must be a tuple of integers.")
    # Ensure numpy array
    if not isinstance(quantum_data, np.ndarray):
        quantum_data = np.array(quantum_data)
    # Validate numeric data type
    if not np.issubdtype(quantum_data.dtype, np.number):
        raise TypeError("Unsupported data type; numeric array required.")
    # Record original shape before any transformations
    original_shape = quantum_data.shape
    # Squeeze leading singleton batch dimension for shape (1, X) when dims match
    if allow_batch_dim and quantum_data.ndim == len(target_shape) and quantum_data.shape[0] == 1:
        quantum_data = np.squeeze(quantum_data, axis=0)
        squeeze_applied = True
    else:
        squeeze_applied = False
    # Validate input shape after squeeze
    validation_result = validate_quantum_input_shape(
        quantum_data, target_shape, allow_batch_dim
    )
    # Initialize transformation info
    transform_info = {
        'original_shape': original_shape,
        'target_shape': target_shape,
        'transforms_applied': [],
        'validation_result': validation_result
    }
    # Record squeeze transformation
    if squeeze_applied:
        transform_info['transforms_applied'].append('squeezed_batch_dimension')
    
    # Apply necessary transformations
    current_data = quantum_data
    # Handle reshape for scalar or 1D inputs
    if 'reshape' in validation_result.required_transforms:
        missing_dims = len(target_shape) - quantum_data.ndim
        new_shape = (1,) + quantum_data.shape + (1,) * missing_dims
        current_data = quantum_data.reshape(new_shape)
        transform_info['transforms_applied'].append('reshaped')
        # Re-validate after reshape
        validation_result = validate_quantum_input_shape(current_data, target_shape, allow_batch_dim)
        transform_info['validation_result'] = validation_result

    # If now valid, ensure float32 and return
    if validation_result.is_valid:
        if current_data.dtype != np.float32:
            current_data = current_data.astype(np.float32)
            transform_info['transforms_applied'].append('converted_to_float32')
        transform_info['final_shape'] = current_data.shape
        return current_data, transform_info
    
    # Handle batch dimension
    if 'add_batch_dim' in validation_result.required_transforms:
        current_data = np.expand_dims(current_data, axis=0)
        transform_info['transforms_applied'].append('added_batch_dimension')
    
    # Handle padding/truncation for each dimension
    for transform in validation_result.required_transforms:
        if transform.startswith('pad_dim_'):
            dim = int(transform.split('_')[-1])
            pad_width = [(0, 0)] * len(current_data.shape)
            target_size = target_shape[dim]
            current_size = current_data.shape[dim + (1 if allow_batch_dim else 0)]
            pad_width[dim + (1 if allow_batch_dim else 0)] = (0, target_size - current_size)
            # Only allow valid np.pad modes
            valid_pad_modes = {'constant', 'edge', 'reflect'}
            if padding_mode not in valid_pad_modes:
                raise ValueError(f"Unsupported padding_mode '{padding_mode}'. Must be one of {valid_pad_modes}.")
            if padding_mode == 'constant':
                current_data = np.pad(
                    current_data,
                    pad_width,
                    mode='constant',
                    constant_values=padding_value
                )
            elif padding_mode == 'edge':
                current_data = np.pad(
                    current_data,
                    pad_width,
                    mode='edge'
                )
            elif padding_mode == 'reflect':
                current_data = np.pad(
                    current_data,
                    pad_width,
                    mode='reflect'
                )
            else:
                raise ValueError(f"Unsupported padding_mode '{padding_mode}'. Must be one of 'constant', 'edge', or 'reflect'.")
            transform_info['transforms_applied'].append(f'padded_dimension_{dim}')
        elif transform.startswith('truncate_dim_'):
            dim = int(transform.split('_')[-1])
            slicing = [slice(None)] * len(current_data.shape)
            slicing[dim + (1 if allow_batch_dim else 0)] = slice(0, target_shape[dim])
            current_data = current_data[tuple(slicing)]
            transform_info['transforms_applied'].append(f'truncated_dimension_{dim}')
    
    # Ensure float32 type for model input
    if current_data.dtype != np.float32:
        current_data = current_data.astype(np.float32)
        transform_info['transforms_applied'].append('converted_to_float32')
    
    transform_info['final_shape'] = current_data.shape
    return current_data, transform_info

def adapt_quantum_input_for_model(model_input, expected_shape):
    """
    DEPRECATED: Use standardize_quantum_input() instead.
    This function is maintained for backward compatibility.
    """
    logging.warning(
        "adapt_quantum_input_for_model is deprecated. "
        "Please use standardize_quantum_input instead."
    )
    standardized_input, _ = standardize_quantum_input(
        model_input,
        expected_shape,
        allow_batch_dim=True
    )
    return standardized_input

# ---
# [2025-04-15] Added run_parameter_sweep utility for robust parameter binding and execution
# This function enables production-ready parameter sweeps for any parameterized circuit,
# supporting both Qiskit Runtime V2 and local simulators. See inline notes for rationale.
# ---
def run_parameter_sweep(
    circuit,
    parameter_values_list,
    backend_or_service,
    shots=1024,
    use_runtime_sampler=False,
    job_tags=None,
    log_prefix="[run_parameter_sweep] "
):
    """
    Execute a parameter sweep for a parameterized quantum circuit.

    Args:
        circuit: Qiskit QuantumCircuit with parameters (ParameterVector or list of Parameters)
        parameter_values_list: List of dicts mapping Parameters to values, or list of lists (order matches circuit.parameters)
        backend_or_service: Qiskit backend (AerSimulator, IBMQ backend) or QiskitRuntimeService
        shots: Number of shots per circuit execution
        use_runtime_sampler: If True, use Qiskit Runtime Sampler (V2 API); else use local simulator
        job_tags: Optional list of tags for Qiskit Runtime jobs
        log_prefix: Prefix for log messages (for traceability)

    Returns:
        List of result objects (counts or quasi_dists), one per parameter set

    Notes:
        - This function is production-ready: no mocks, no demo data, robust error handling.
        - Supports both Qiskit Runtime V2 (Sampler) and local simulators (AerSimulator).
        - Parameter values can be dicts (Parameter: value) or lists (order matches circuit.parameters).
        - Extensive logging and error handling for traceability.
        - See docs/knowledge_base.md and 14_production_readiness.mdc for rationale.
    """
    import logging
    from qiskit.circuit import Parameter, ParameterVector
    from qiskit_ibm_runtime import Sampler as RuntimeSampler
    from qiskit_aer.primitives import Sampler as AerSampler
    from qiskit import transpile
    import numpy as np

    logger = logging.getLogger(__name__)
    logger.info(f"{log_prefix}Starting parameter sweep for {len(parameter_values_list)} parameter sets.")

    # Validate input
    if not hasattr(circuit, 'parameters') or len(circuit.parameters) == 0:
        raise ValueError(f"{log_prefix}Circuit must have parameters for parameter sweep.")
    if not isinstance(parameter_values_list, list) or len(parameter_values_list) == 0:
        raise ValueError(f"{log_prefix}parameter_values_list must be a non-empty list.")

    # Prepare results
    results = []

    # Choose execution mode
    if use_runtime_sampler:
        # Qiskit Runtime V2 Sampler (production-ready, real hardware or fake backend)
        logger.info(f"{log_prefix}Using Qiskit Runtime V2 Sampler.")
        sampler = RuntimeSampler(backend_or_service)
        for idx, param_values in enumerate(parameter_values_list):
            if isinstance(param_values, dict):
                # Use assign_parameters for Qiskit 1.0+ compatibility
                bound_circuit = circuit.assign_parameters(param_values)
            elif isinstance(param_values, (list, np.ndarray)):
                if len(param_values) != len(circuit.parameters):
                    raise ValueError(f"{log_prefix}Parameter list length mismatch for set {idx}.")
                param_dict = dict(zip(circuit.parameters, param_values))
                bound_circuit = circuit.assign_parameters(param_dict)
            else:
                raise TypeError(f"{log_prefix}Parameter values must be dict or list.")
            try:
                job = sampler.run([bound_circuit], shots=shots)
                result = job.result()
                if hasattr(result, 'quasi_dists'):
                    results.append(result.quasi_dists[0])
                elif hasattr(result, 'pub_results'):
                    pub = result.pub_results[0]
                    counts = pub.data.c.get_counts() if hasattr(pub.data, 'c') else pub.data.get_counts()
                    # Detect probability distribution (values sum to ~1.0) and scale to shots
                    total = sum(counts.values())
                    if abs(total - 1.0) < 1e-3:
                        # values are probabilities, scale to shot counts
                        counts = {k: int(round(v * shots)) for k, v in counts.items()}
                    results.append(counts)
                else:
                    results.append(result)
                logger.info(f"{log_prefix}Completed parameter set {idx+1}/{len(parameter_values_list)}.")
            except Exception as e:
                logger.error(f"{log_prefix}Error executing parameter set {idx+1}: {e}")
                results.append({'error': str(e)})
    else:
        # Local simulation: use the provided backend_or_service (e.g. AerSimulator)
        logger.info(f"{log_prefix}Using local simulator: {backend_or_service}.")
        sim_backend = backend_or_service

        for idx, param_values in enumerate(parameter_values_list):
            if isinstance(param_values, dict):
                # Use assign_parameters for Qiskit 1.0+ compatibility
                bound_circuit = circuit.assign_parameters(param_values)
            elif isinstance(param_values, (list, np.ndarray)):
                if len(param_values) != len(circuit.parameters):
                    raise ValueError(f"{log_prefix}Parameter list length mismatch for set {idx}.")
                param_dict = dict(zip(circuit.parameters, param_values))
                bound_circuit = circuit.assign_parameters(param_dict)
            else:
                raise TypeError(f"{log_prefix}Parameter values must be dict or list.")
            try:
                # Transpile for local backend and execute as a list of circuits
                transpiled_circ = transpile(bound_circuit, sim_backend)
                job = sim_backend.run([transpiled_circ], shots=shots)
                result = job.result()
                # Append counts dictionary for the first circuit if available
                if hasattr(result, 'get_counts'):
                    counts = result.get_counts()
                    # Detect probability distribution (values sum to ~1.0) and scale to shots
                    total = sum(counts.values())
                    if abs(total - 1.0) < 1e-3:
                        # values are probabilities, scale to shot counts
                        counts = {k: int(round(v * shots)) for k, v in counts.items()}
                    results.append(counts)
                else:
                    results.append(result)
                logger.info(f"{log_prefix}Completed parameter set {idx+1}/{len(parameter_values_list)}.")
            except Exception as e:
                logger.error(f"{log_prefix}Error executing parameter set {idx+1}: {e}")
                results.append({'error': str(e)})

    logger.info(f"{log_prefix}Parameter sweep complete. {len(results)} results collected.")
    # Note: assign_parameters is used instead of bind_parameters for Qiskit 1.0+ compatibility (see IBM docs and migration guides).
    return results 