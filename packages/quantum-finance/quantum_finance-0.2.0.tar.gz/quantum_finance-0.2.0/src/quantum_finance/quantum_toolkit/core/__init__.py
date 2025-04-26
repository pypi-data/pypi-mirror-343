"""
Core Quantum Toolkit Components

This module provides the core components for quantum systems and circuits.
"""

# Import classes to expose at the package level
from .circuit import (
    QuantumCircuit,
    CircuitBase,
    Gate,
    create_circuit
)

from .trajectory import (
    Trajectory,
    ConfigurationPoint
)

# Package metadata
__version__ = '0.2.0'

# Define public API
__all__ = [
    'QuantumCircuit',
    'CircuitBase',
    'Gate',
    'create_circuit',
    'Trajectory',
    'ConfigurationPoint'
]

# Additional imports from memory submodule, if needed
try:
    from .memory import (
        QuantumMemoryPool,
        QuantumMemoryManager,
        optimize_circuit_memory
    )
    __all__ += [
        'QuantumMemoryPool',
        'QuantumMemoryManager',
        'optimize_circuit_memory'
    ]
except ImportError:
    # Memory module might not be fully implemented yet
    pass 