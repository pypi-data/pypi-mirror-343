"""
Hybrid Quantum-Classical Algorithms

This module provides hybrid quantum-classical algorithms functionality for the quantum framework.
"""

# Package metadata
__version__ = '0.1.0'

# Define public API by exporting hybrid module classes
from .stochastic_neural import StochasticNeuralBridge
from .neural import TrajectoryConditionedNetwork
from .regime_detection import MarketRegimeDetector

__all__ = [
    'StochasticNeuralBridge',
    'TrajectoryConditionedNetwork',
    'MarketRegimeDetector',
]
