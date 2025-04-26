"""
Error Analysis Utilities

This module provides functions for analyzing errors and calculating metrics
for quantum state quality evaluation.
"""

import numpy as np
from typing import Union, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def calculate_fidelity(state1: np.ndarray, state2: np.ndarray) -> float:
    """
    Calculate the fidelity between two quantum states.
    
    The fidelity is defined as F(ρ,σ) = |⟨ψ|φ⟩|² for pure states.
    
    Args:
        state1: First quantum state as a complex vector
        state2: Second quantum state as a complex vector
        
    Returns:
        Fidelity value between 0 and 1
    """
    # Ensure states are normalized
    if np.linalg.norm(state1) < 1e-10 or np.linalg.norm(state2) < 1e-10:
        logger.warning("One of the states has near-zero norm. Returning zero fidelity.")
        return 0.0
    
    # Normalize states
    state1_norm = state1 / np.linalg.norm(state1)
    state2_norm = state2 / np.linalg.norm(state2)
    
    # Ensure dimensions match
    if state1_norm.shape != state2_norm.shape:
        logger.warning(f"State dimensions don't match: {state1_norm.shape} vs {state2_norm.shape}. "
                     "Attempting to resolve...")
        min_dim = min(state1_norm.size, state2_norm.size)
        state1_norm = state1_norm.flatten()[:min_dim]
        state2_norm = state2_norm.flatten()[:min_dim]
        
        # Renormalize after truncation
        state1_norm = state1_norm / np.linalg.norm(state1_norm)
        state2_norm = state2_norm / np.linalg.norm(state2_norm)
    
    # Calculate inner product and fidelity
    inner_product = np.vdot(state1_norm, state2_norm)
    fidelity = np.abs(inner_product) ** 2
    
    return float(fidelity)

def calculate_trace_distance(state1: np.ndarray, state2: np.ndarray) -> float:
    """
    Calculate the trace distance between two quantum states.
    
    The trace distance is defined as D(ρ,σ) = (1/2)Tr|ρ-σ| for density matrices.
    This is a simpler version for pure states.
    
    Args:
        state1: First quantum state as a complex vector
        state2: Second quantum state as a complex vector
        
    Returns:
        Trace distance value between 0 and 1
    """
    # Ensure states are normalized
    if np.linalg.norm(state1) < 1e-10 or np.linalg.norm(state2) < 1e-10:
        logger.warning("One of the states has near-zero norm. Returning maximum trace distance.")
        return 1.0
    
    # Normalize states
    state1_norm = state1 / np.linalg.norm(state1)
    state2_norm = state2 / np.linalg.norm(state2)
    
    # Ensure dimensions match
    if state1_norm.shape != state2_norm.shape:
        min_dim = min(state1_norm.size, state2_norm.size)
        state1_norm = state1_norm.flatten()[:min_dim]
        state2_norm = state2_norm.flatten()[:min_dim]
        
        # Renormalize after truncation
        state1_norm = state1_norm / np.linalg.norm(state1_norm)
        state2_norm = state2_norm / np.linalg.norm(state2_norm)
    
    # Convert to density matrices for pure states
    dm1 = np.outer(state1_norm, np.conj(state1_norm))
    dm2 = np.outer(state2_norm, np.conj(state2_norm))
    
    # Calculate trace distance
    diff = dm1 - dm2
    # For Hermitian matrices, the trace norm is the sum of absolute eigenvalues
    eigenvalues = np.linalg.eigvalsh(diff)
    trace_distance = 0.5 * np.sum(np.abs(eigenvalues))
    
    return float(trace_distance) 