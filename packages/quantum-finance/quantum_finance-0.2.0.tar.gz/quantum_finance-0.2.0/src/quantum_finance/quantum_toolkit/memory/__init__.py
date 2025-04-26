"""
Quantum Memory Module

This module provides implementations for quantum memory management, including
persistent quantum state storage, coherence extension, and memory optimization.
"""

import logging

# Configure logger
logger = logging.getLogger(__name__)

# Import submodules
try:
    from .memsaur import (
        QuantumMemoryManager,
        MemoryHandle,
        MemoryStorageType,
        CoherenceExtender,
        TensorNetworkMemory
    )
    HAS_MEMSAUR = True
except ImportError as e:
    logger.warning(f"Could not import Memsaur implementation: {str(e)}")
    HAS_MEMSAUR = False

__all__ = [
    'QuantumMemoryManager',
    'MemoryHandle',
    'MemoryStorageType',
    'CoherenceExtender',
    'TensorNetworkMemory',
    'HAS_MEMSAUR'
]
