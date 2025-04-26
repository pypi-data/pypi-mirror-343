"""Facade module for the top-level backend package."""
import os
import builtins
from flask import Flask as RealFlask

# Extend package search path to include quantum_finance/backend for backward-compatibility
__path__.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'quantum_finance', 'backend')))

# Use DummyFlask from builtins if available for tests, otherwise RealFlask
Flask = getattr(builtins, 'Flask', RealFlask)

__all__ = ['create_app']

def create_app():
    """Factory to create and return a DummyFlask or real Flask application instance."""
    # Instantiate app using Flask alias (dummy or real)
    return Flask(__name__)