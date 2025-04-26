import importlib.util
import warnings
from typing import Dict, List, Optional, Union, Any

# Check if qiskit_ibm_runtime is available
has_qiskit_ibm_runtime = importlib.util.find_spec("qiskit_ibm_runtime") is not None

# Define version constants
USING_V2_API = False
if has_qiskit_ibm_runtime:
    try:
        from qiskit_ibm_runtime import SamplerV2
        USING_V2_API = True
    except ImportError:
        USING_V2_API = False

class QiskitRuntimeAdapter:
    """
    Adapter class to handle the transition between Qiskit Runtime V1 and V2 APIs.
    Provides a unified interface regardless of which version is being used.
    """
    
    @staticmethod
    def get_sampler(service, backend, **kwargs):
        """Get appropriate Sampler based on available API version"""
        # Standardize on 'use_session' boolean kwarg for session mode
        use_session = kwargs.pop('use_session', False)
        # Remove service, backend, and session from kwargs to avoid passing them as unexpected keyword arguments
        for k in ['service', 'backend', 'session']:
            if k in kwargs:
                kwargs.pop(k)
        # NOTE: As of Qiskit SDK v1.0+, the Options class is deprecated. All options should be passed as dictionaries.
        # This refactor removes all usage of Options and ensures future compatibility and production readiness.
        if USING_V2_API:
            from qiskit_ibm_runtime import SamplerV2, Session
            # Convert V1 style options to V2 if present
            if 'options' in kwargs:
                v1_options = kwargs.pop('options')
                # V2 expects options as a dictionary
                options = {}
                # Handle resilience settings
                if 'resilience_level' in v1_options:
                    options['resilience_level'] = v1_options['resilience_level']
                # Handle optimization settings
                if 'optimization_level' in v1_options:
                    options['optimization_level'] = v1_options['optimization_level']
                # Handle transpilation skip
                if 'skip_transpilation' in v1_options:
                    options['skip_transpilation'] = v1_options['skip_transpilation']
                # Add any other options
                for k, v in v1_options.items():
                    if k not in options:
                        options[k] = v
                kwargs['options'] = options
            if use_session:
                session = Session(service=service, backend=backend)
                return SamplerV2(mode=session, **kwargs)
            else:
                return SamplerV2(service=service, backend=backend, **kwargs)
        else:
            from qiskit_ibm_runtime import Sampler, Session
            if use_session:
                session = Session(service=service, backend=backend)
                return Sampler(session=session, **kwargs)
            else:
                return Sampler(backend=backend, service=service, **kwargs)
    
    @staticmethod
    def ensure_isa_circuits(circuits, backend):
        """
        Ensure circuits are in the Instruction Set Architecture (ISA) format
        required by V2 APIs since March 2024.
        """
        from qiskit import transpile
        
        if USING_V2_API:
            # Get the target for transpilation
            target = backend.target
            
            # Transpile the circuits to the target
            isa_circuits = transpile(
                circuits,
                target=target,
                optimization_level=1  # Use a reasonable default
            )
            return isa_circuits
        else:
            # For V1 API, return circuits as-is (transpilation handled internally)
            return circuits
    
    @staticmethod
    def process_sampler_result(result):
        """Process result from either V1 or V2 Sampler"""
        if USING_V2_API:
            # V2 API returns results in PUB format
            # Extract quasi-probabilities or counts based on the format
            if hasattr(result, 'quasi_dists'):
                return result.quasi_dists
            else:
                return result.data
        else:
            # V1 API structure
            return result.quasi_dists if hasattr(result, 'quasi_dists') else result.data
    
    @staticmethod
    def configure_options(resilience_level=1, optimization_level=1, **kwargs):
        """Create options object in the appropriate format for V1 or V2 API (dictionary-based only)."""
        # NOTE: The Options class is deprecated in Qiskit 1.0+. All options must be passed as dictionaries.
        # This function now returns a dictionary for both V1 and V2 APIs.
        options = {
            'resilience_level': resilience_level,
            'optimization_level': optimization_level,
            **kwargs
        }
        # Extensive note: This change ensures future compatibility and aligns with project production-readiness rules.
        # See Qiskit 1.0+ release notes and project changelog for rationale.
        return options 