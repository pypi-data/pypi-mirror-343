"""
Adapters Module

This module provides adapters that connect the unified API to specific technology implementations.
"""

# Conditional imports for adapters
try:
    from .circuit_adapter import CircuitCutterAdapter
    HAS_CIRCUIT_ADAPTER = True
except ImportError:
    HAS_CIRCUIT_ADAPTER = False

try:
    from .stochastic_adapter import StochasticMethodsAdapter
    HAS_STOCHASTIC_ADAPTER = True
except ImportError:
    HAS_STOCHASTIC_ADAPTER = False

try:
    from .memsaur_adapter import MemsaurAdapter
    HAS_MEMSAUR_ADAPTER = True
except ImportError:
    HAS_MEMSAUR_ADAPTER = False

try:
    from .backend_adapter import BackendSelectorAdapter
    HAS_BACKEND_ADAPTER = True
except ImportError:
    HAS_BACKEND_ADAPTER = False

# Unified flag to check if adapters are available
HAS_ADAPTERS = any([
    HAS_CIRCUIT_ADAPTER,
    HAS_STOCHASTIC_ADAPTER,
    HAS_MEMSAUR_ADAPTER,
    HAS_BACKEND_ADAPTER
]) 