"""
Quantum State Utilities

This module provides functions for creating and manipulating quantum states.
"""

import numpy as np
from typing import Optional, Union, List, Tuple
import logging

logger = logging.getLogger(__name__)

def create_basis_state(num_qubits: int, basis_idx: int = 0) -> np.ndarray:
    """
    Create a computational basis state |basis_idx⟩.
    
    Args:
        num_qubits: Number of qubits
        basis_idx: Index of the basis state (0 to 2^num_qubits - 1)
        
    Returns:
        Complex numpy array representing the quantum state
    """
    if basis_idx < 0 or basis_idx >= 2**num_qubits:
        raise ValueError(f"basis_idx must be between 0 and {2**num_qubits - 1}")
    
    state = np.zeros(2**num_qubits, dtype=complex)
    state[basis_idx] = 1.0
    return state

def create_equal_superposition_state(num_qubits: int) -> np.ndarray:
    """
    Create an equal superposition state (|+⟩^⊗n).
    
    Args:
        num_qubits: Number of qubits
        
    Returns:
        Complex numpy array representing the quantum state
    """
    state = np.ones(2**num_qubits, dtype=complex) / np.sqrt(2**num_qubits)
    return state

def create_ghz_state(num_qubits: int) -> np.ndarray:
    """
    Create a GHZ state (|00...0⟩ + |11...1⟩)/√2.
    
    Args:
        num_qubits: Number of qubits
        
    Returns:
        Complex numpy array representing the quantum state
    """
    state = np.zeros(2**num_qubits, dtype=complex)
    state[0] = 1.0 / np.sqrt(2)
    state[2**num_qubits - 1] = 1.0 / np.sqrt(2)
    return state

def create_w_state(num_qubits: int) -> np.ndarray:
    """
    Create a W state (|100...0⟩ + |010...0⟩ + ... + |000...1⟩)/√n.
    
    Args:
        num_qubits: Number of qubits
        
    Returns:
        Complex numpy array representing the quantum state
    """
    if num_qubits < 1:
        raise ValueError("Number of qubits must be positive")
    
    state = np.zeros(2**num_qubits, dtype=complex)
    # Set amplitude for each state with a single '1'
    for i in range(num_qubits):
        idx = 2**i  # Index with only the i-th bit set to 1
        state[idx] = 1.0
    
    # Normalize
    state /= np.sqrt(num_qubits)
    return state

def create_random_state(num_qubits: int, entangled: bool = False, seed: Optional[int] = None) -> np.ndarray:
    """
    Create a random quantum state.
    
    Args:
        num_qubits: Number of qubits
        entangled: If True, create a random entangled state
        seed: Random seed for reproducibility
        
    Returns:
        Complex numpy array representing the quantum state
    """
    if seed is not None:
        np.random.seed(seed)
    
    dim = 2**num_qubits
    
    if entangled:
        # Create a random complex vector (potentially entangled)
        real_part = np.random.normal(0, 1, dim)
        imag_part = np.random.normal(0, 1, dim)
        state = real_part + 1j * imag_part
    else:
        # Create a product state of random single-qubit states
        state = np.ones(1, dtype=complex)
        for _ in range(num_qubits):
            # Random single-qubit state
            alpha = np.random.random()
            phi = np.random.random() * 2 * np.pi
            single_qubit = np.array([np.cos(alpha), np.sin(alpha) * np.exp(1j * phi)])
            # Tensor product
            state = np.kron(state, single_qubit)
    
    # Normalize
    state /= np.linalg.norm(state)
    return state

def measure_state(state: np.ndarray, num_samples: int = 1024) -> dict:
    """
    Simulate measurement of a quantum state.
    
    Args:
        state: Quantum state as a complex vector
        num_samples: Number of measurements to perform
        
    Returns:
        Dictionary mapping measurement outcomes to their frequencies
    """
    probabilities = np.abs(state)**2
    dim = len(probabilities)
    num_qubits = int(np.log2(dim))
    
    # Sample from probability distribution
    samples = np.random.choice(dim, size=num_samples, p=probabilities)
    
    # Convert to binary strings and count
    counts = {}
    for sample in samples:
        # Convert to binary string
        binary = format(sample, f"0{num_qubits}b")
        counts[binary] = counts.get(binary, 0) + 1
    
    # Convert to frequencies
    for outcome in counts:
        counts[outcome] = counts[outcome] / num_samples
    
    return counts 