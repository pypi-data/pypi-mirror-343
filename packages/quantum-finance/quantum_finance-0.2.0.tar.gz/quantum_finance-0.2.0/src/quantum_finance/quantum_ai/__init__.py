#!/usr/bin/env python3

"""
Quantum AI Integration Package

This package provides tools and utilities for integrating quantum computing
with artificial intelligence, enabling hybrid quantum-classical algorithms
and quantum-enhanced machine learning.
"""

# Import core components
from quantum_ai.core.measurement_result import QuantumMeasurementResult
from quantum_ai.datatypes.circuit_metadata import CircuitMetadata
from quantum_ai.datatypes.uncertainty_metrics import UncertaintyMetrics
from quantum_ai.predictors.ai_quantum_predictor import AiQuantumPredictor

# Re-export key classes for easier imports
__all__ = [
    "QuantumMeasurementResult",
    "CircuitMetadata",
    "UncertaintyMetrics",
    "AiQuantumPredictor",
]

# Package metadata
__version__ = "0.1.0"
__author__ = "Quantum AI Team"
__email__ = "quantum-ai@example.com"
__license__ = "MIT"
