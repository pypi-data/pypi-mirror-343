"""
Quantum module for portfolio optimization and financial analysis.
"""

__version__ = '1.0.0'

# Package metadata
__author__ = 'Quantum-AI Team'

# Import core subpackages to make them accessible directly
try:
    from . import core
    from . import circuits
    from . import simulation
    from . import backtesting
    from . import stochastic
    from . import memory
    from . import integration
    from . import phase_tracking
    from . import error_correction
    from . import explainability
    from . import hybrid
    
    # Define public API
    __all__ = [
        'core',
        'circuits',
        'simulation',
        'backtesting',
        'stochastic',
        'memory',
        'integration',
        'phase_tracking',
        'error_correction',
        'explainability',
        'hybrid'
    ]
except ImportError as e:
    # Log import errors for debugging
    import logging
    logging.getLogger(__name__).warning(f"Error importing submodules: {e}")
    __all__ = [] 