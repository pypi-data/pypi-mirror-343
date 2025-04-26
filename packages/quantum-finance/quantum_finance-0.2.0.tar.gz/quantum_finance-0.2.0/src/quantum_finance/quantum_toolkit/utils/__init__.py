"""
Quantum Toolkit Utilities

This module provides utility functions for the quantum toolkit.
"""

# Import key functions to expose at the package level
from .error_analysis import (
    calculate_fidelity,
    calculate_trace_distance
)

from .quantum_state_utils import (
    create_basis_state,
    create_equal_superposition_state,
    create_ghz_state,
    create_w_state,
    create_random_state,
    measure_state
)

# Add any adapter utilities if needed
try:
    from .qiskit_adapter import (
        qiskit_to_toolkit,
        toolkit_to_qiskit
    )
except ImportError:
    # Qiskit adapter might not be fully implemented
    pass

# Package metadata
__version__ = '0.1.0'

# Define public API
__all__ = [
    # Error analysis
    'calculate_fidelity',
    'calculate_trace_distance',
    
    # Quantum state utilities
    'create_basis_state',
    'create_equal_superposition_state',
    'create_ghz_state',
    'create_w_state',
    'create_random_state',
    'measure_state'
]

# Add Qiskit adapter functions if available
try:
    __all__ += [
        'qiskit_to_toolkit',
        'toolkit_to_qiskit'
    ]
except NameError:
    # Adapter functions weren't imported
    pass 