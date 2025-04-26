"""
Quantum Circuits Module

This module provides implementations of various quantum circuits, from
standard circuits like Bell states to specialized financial analysis circuits.
"""

from .base import (
    create_bell_state,
    create_ghz_state,
    create_w_state,
    create_random_circuit,
    create_quantum_fourier_transform,
    create_inverse_quantum_fourier_transform,
    run_circuit_simulation
)

from .standard import (
    create_bell_state as create_bell_state_standard,
    create_ghz_state as create_ghz_state_standard,
    create_w_state as create_w_state_standard,
    create_quantum_fourier_transform as create_quantum_fourier_transform_standard,
    create_inverse_quantum_fourier_transform as create_inverse_quantum_fourier_transform_standard
)

# Import new dedicated W-state implementation
try:
    from .w_state import (
        create_w_state_circuit,
        verify_w_state,
        test_w_state_fidelity
    )
except ImportError:
    # Fallback if the dedicated module is not available
    pass

# Import circuit optimization
try:
    from .optimization import (
        CircuitOptimizer,
        reduce_circuit_depth,
        cancel_gates,
        optimize_for_backend,
        get_cached_circuit,
        add_to_cache
    )
except ImportError:
    # Fallback if the optimization module is not available
    pass

# Import financial circuits - COMMENTED OUT as source file seems missing/misplaced
# try:
#     # Check if financial_circuits.py exists, otherwise assume it was in financial subpackage
#     # If it was moved, the path might be different, e.g., ..financial.circuits
#     try:
#         from .financial_circuits import (
#             FinancialCircuits,
#             CircuitType
#         )
#     except ImportError:
#         # Attempt import from the potentially refactored location
#         from quantum_toolkit.financial.circuits import (
#             FinancialCircuits,
#             CircuitType
#         )
    
__all__ = [
    # Base circuits
    'create_bell_state',
    'create_ghz_state',
    'create_w_state',
    'create_random_circuit',
    'create_quantum_fourier_transform',
    'create_inverse_quantum_fourier_transform',
    'run_circuit_simulation',
    # Standard circuits
    'create_bell_state_standard',
    'create_ghz_state_standard',
    'create_w_state_standard',
    'create_quantum_fourier_transform_standard',
    'create_inverse_quantum_fourier_transform_standard',
    # W-state dedicated implementation
    'create_w_state_circuit',
    'verify_w_state',
    'test_w_state_fidelity',
    # Circuit optimization
    'CircuitOptimizer',
    'reduce_circuit_depth',
    'cancel_gates',
    'optimize_for_backend',
    'get_cached_circuit',
    'add_to_cache'
    # Financial circuits - REMOVED as source file seems missing/misplaced
    # 'FinancialCircuits',
    # 'CircuitType'
]
# except ImportError:
#     # Handle the case where some modules might not be available
#     __all__ = []

__version__ = '0.1.0' 