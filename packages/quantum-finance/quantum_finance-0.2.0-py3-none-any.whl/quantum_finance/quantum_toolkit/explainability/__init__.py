"""
Quantum Algorithm Explainability Tools

This module provides quantum algorithm explainability tools functionality for the quantum framework,
focusing on comparing and explaining the differences between quantum and classical approaches.

Key components:
- ComparisonEngine: Compare quantum and classical prediction approaches
- ExplainabilityIntegrator: Bridge between existing risk models and explainability tools
- RiskExplainer: Explain and visualize risk assessment factors and results
- RiskVisualization: Advanced visualization components for quantum risk assessments
"""

# Package metadata
__version__ = '0.1.0'

# Import key classes for easier access
from .comparison_engine import ComparisonEngine
from .integrator import ExplainabilityIntegrator
from .risk_explainer import RiskExplainer
from .risk_visualization import RiskVisualization

# Define public API
__all__ = [
    'ComparisonEngine',
    'ExplainabilityIntegrator',
    'RiskExplainer',
    'RiskVisualization'
]
