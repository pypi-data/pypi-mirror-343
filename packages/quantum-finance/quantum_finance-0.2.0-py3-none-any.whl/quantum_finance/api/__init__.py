"""
Quantum Financial API

A comprehensive unified API for quantum financial components that provides a seamless interface
between all the advanced components we've developed, enabling end-to-end market analysis and
risk assessment.

This package exports the main classes and enums needed to use the API:
- QuantumFinancialAPI: Main entry point for all functionality
- QuantumFinancialConfig: Configuration for the API components
- MarketData: Container for market data used across components
- AnalysisResult: Container for analysis results from components
- ComponentType: Enum defining the types of components available
"""

from .quantum_financial_api import (
    QuantumFinancialAPI,
    QuantumFinancialConfig,
    MarketData,
    AnalysisResult,
    ComponentType
)

__all__ = [
    'QuantumFinancialAPI',
    'QuantumFinancialConfig',
    'MarketData',
    'AnalysisResult',
    'ComponentType'
]

__version__ = '0.1.0'

"""
Agent Hustle API Integration Package
""" 