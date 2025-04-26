#!/usr/bin/env python3

"""
Quantum-AI Interface Module

This module provides enhanced integration between quantum computing components
and AI prediction models, with a focus on:
1. Standardized data exchange formats that preserve quantum information properties
2. Uncertainty quantification and propagation through the AI pipeline
3. Improved feedback mechanisms between quantum circuits and AI models

Usage:
    from quantum_ai_interface import QuantumMeasurementResult, AiQuantumPredictor

Note:
    This module is being refactored into a proper package structure.
    Please import from the quantum_ai package instead:
    
    from quantum_ai import CircuitMetadata, UncertaintyMetrics, QuantumMeasurementResult, AiQuantumPredictor
"""

import logging
import warnings

# Logging is configured centrally via setup_logging; do not call basicConfig here
logger = logging.getLogger(__name__)

# Issue deprecation warning
warnings.warn(
    "This module is being refactored into the quantum_ai package. "
    "Please update your imports to use the new package structure.",
    DeprecationWarning, 
    stacklevel=2
)

# Import from the new module structure
from quantum_ai.datatypes.circuit_metadata import CircuitMetadata
from quantum_ai.datatypes.uncertainty_metrics import UncertaintyMetrics
from quantum_ai.core.measurement_result import QuantumMeasurementResult
from quantum_ai.predictors.ai_quantum_predictor import AiQuantumPredictor

# Re-export the classes for backward compatibility
__all__ = ['CircuitMetadata', 'UncertaintyMetrics', 'QuantumMeasurementResult', 'AiQuantumPredictor']