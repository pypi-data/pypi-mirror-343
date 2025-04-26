#!/usr/bin/env python3
"""
Test script for 2-qubit W-state circuit implementation.

This script tests the new recursive W-state implementation
for 2 qubits and displays the results.
"""

import os
import sys
import numpy as np

# Add parent directory to path to allow imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Try importing from the dedicated W-state module first
try:
    from quantum.circuits.w_state import create_w_state_circuit as create_w_state
    print("Using dedicated W-state implementation")
except ImportError:
    # Fallback to standard implementation
    from quantum.circuits.standard import create_w_state
    print("Using standard W-state implementation")

# Create a 2-qubit W state
circuit = create_w_state(2)

# Print circuit information
print(f"Created 2-qubit W-state circuit")
print(f"Number of qubits: {circuit.num_qubits}")

# Try to print the circuit
try:
    print("\nCircuit representation:")
    print(circuit)
except Exception as e:
    print(f"Error printing circuit: {e}")

# Verify the circuit produces the correct state
try:
    from qiskit.quantum_info import Statevector, state_fidelity
    
    # Get the statevector from the circuit
    statevector = Statevector.from_instruction(circuit)
    
    # Calculate probabilities
    probabilities = np.abs(statevector.data) ** 2
    
    print("\nState probabilities:")
    for i, prob in enumerate(probabilities):
        if prob > 0.01:  # Only show states with significant probability
            binary = format(i, f"0{2}b")
            print(f"|{binary}⟩: {prob:.6f}")
    
    # Create theoretical W-state
    theoretical_state = np.zeros(4, dtype=complex)
    theoretical_state[1] = 1/np.sqrt(2)  # |01⟩
    theoretical_state[2] = 1/np.sqrt(2)  # |10⟩
    
    # Calculate fidelity
    fidelity = state_fidelity(statevector.data, theoretical_state)
    print(f"\nFidelity with theoretical W-state: {fidelity:.6f}")
    print(f"Test {'PASSED' if fidelity > 0.99 else 'FAILED'}")
    
except ImportError:
    print("\nQiskit quantum_info module not available for verification.")

print("\nThis circuit should create a W state (|01⟩ + |10⟩)/√2")
print("When measured, it should show approximately equal probabilities for |01⟩ and |10⟩") 