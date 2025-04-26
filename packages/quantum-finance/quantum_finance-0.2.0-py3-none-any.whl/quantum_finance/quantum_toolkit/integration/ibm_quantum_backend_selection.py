#!/usr/bin/env python3

"""
Intelligent Backend Selection for IBM Quantum Integration

This module provides an intelligent backend selection system that considers
multiple factors when selecting the optimal IBM Quantum backend:
- Qubit count requirements
- Circuit depth and width
- Gate set compatibility 
- Qubit connectivity/topology
- Error rates (gate errors, readout errors)
- Queue length and expected wait time
- Backend availability and status

The system uses a weighted scoring approach that can be customized based on
application priorities.

Note: This file is a backward-compatibility wrapper for the actual implementation,
which has been moved to quantum.integration.backend_selection for better
organization.

Usage:
    from ibm_quantum_backend_selection import IntelligentBackendSelector
    
    # Initialize the selector
    selector = IntelligentBackendSelector()
    
    # Get backend recommendations for a circuit
    recommended_backends = selector.select_backend(circuit)
    
    # Use top recommendation
    best_backend = recommended_backends[0]['backend']

Author: Quantum-AI Team
"""

# Import all classes from the main implementation using relative import
from .backend_selection import (
    IntelligentBackendSelector,
    SelectionCriteria
)

# Create alias for backward compatibility
IBMQuantumBackendSelector = IntelligentBackendSelector

# Re-export all symbols for backward compatibility
__all__ = [
    'IntelligentBackendSelector',
    'SelectionCriteria',
    'IBMQuantumBackendSelector'
]

# End of file - Removed redundant class definition and imports