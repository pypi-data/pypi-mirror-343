"""
Quantum Phase Tracking and Estimation

This module provides quantum phase tracking and estimation functionality for the quantum framework.
"""

# Import classes to expose at the package level
from .adaptive_phase_tracker import AdaptivePhaseTracker, StateEstimate

# Package metadata
__version__ = '0.1.0'

# Define public API
__all__ = [
    'AdaptivePhaseTracker',
    'StateEstimate'
]
