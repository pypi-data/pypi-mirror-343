#!/usr/bin/env python3
"""
W-State Theoretical Analysis

This script analyzes the theoretical properties of W-states without
relying on Qiskit simulators.
"""

import numpy as np
import matplotlib.pyplot as plt

def create_w_state_vector(num_qubits):
    """
    Create a theoretical W state vector.
    
    Args:
        num_qubits: Number of qubits
        
    Returns:
        np.array: The statevector of the W state
    """
    # Initialize a zero state vector
    state_vector = np.zeros(2**num_qubits, dtype=complex)
    
    # W state has equal amplitude in states with exactly one qubit in |1⟩
    amplitude = 1.0 / np.sqrt(num_qubits)
    
    # Populate the statevector
    for i in range(num_qubits):
        # Calculate position for a state with one 1 at position i
        # For example: |10⟩, |01⟩ in 2 qubits
        position = 2**i
        state_vector[position] = amplitude
        
    return state_vector

def analyze_w_state(num_qubits):
    """
    Perform a theoretical analysis of a W state.
    
    Args:
        num_qubits: Number of qubits in the W state
    """
    print(f"\n{'='*50}")
    print(f"W State Analysis ({num_qubits} qubits)")
    print(f"{'='*50}")
    
    # Create the theoretical W state vector
    state_vector = create_w_state_vector(num_qubits)
    
    # Calculate probabilities
    probabilities = np.abs(state_vector) ** 2
    
    # Print the W state vector
    print("\nW State Vector:")
    for i, amplitude in enumerate(state_vector):
        if abs(amplitude) > 1e-10:
            binary = format(i, f'0{num_qubits}b')
            print(f"  |{binary}⟩: {amplitude:.6f} (prob: {probabilities[i]:.6f})")
    
    # Define one-hot states
    one_hot_states = [
        ''.join('1' if i == j else '0' for i in range(num_qubits))
        for j in range(num_qubits)
    ]
    
    # Expected probability for each state in the W state
    expected_prob = 1.0 / num_qubits
    
    # Print theoretical probabilities
    print("\nTheoretical probabilities for W state:")
    print(f"{'State':<10} {'Probability':<15}")
    print(f"{'-'*10} {'-'*15}")
    
    for state in one_hot_states:
        idx = int(state, 2)
        prob = probabilities[idx]
        print(f"|{state}⟩{' ':<5} {prob:<15.6f}")
    
    # Verify the properties of a W state
    # 1. Verify normalization (sum of probabilities = 1)
    normalization = np.sum(probabilities)
    print(f"\nNormalization (sum of all probabilities): {normalization:.6f}")
    
    # 2. Verify only one-hot states have non-zero probabilities
    one_hot_indices = [int(state, 2) for state in one_hot_states]
    non_w_probs = sum(prob for i, prob in enumerate(probabilities) if i not in one_hot_indices)
    print(f"Non-W state probabilities: {non_w_probs:.6f}")
    
    # 3. Verify equal superposition (all one-hot states have equal probability)
    one_hot_probs = [probabilities[int(state, 2)] for state in one_hot_states]
    max_deviation = max(abs(prob - expected_prob) for prob in one_hot_probs)
    print(f"Maximum deviation from expected probability: {max_deviation:.6f}")
    
    # Create visual representation
    try:
        # Set up the plot
        plt.figure(figsize=(10, 6))
        
        # Create bar chart of probabilities
        states = [format(i, f'0{num_qubits}b') for i in range(2**num_qubits)]
        state_labels = [f"|{s}⟩" for s in states]
        
        # Create the bar chart with only visible probabilities
        visible_indices = [i for i, p in enumerate(probabilities) if p > 1e-10]
        visible_states = [state_labels[i] for i in visible_indices]
        visible_probs = [probabilities[i] for i in visible_indices]
        
        bars = plt.bar(visible_states, visible_probs)
        
        # Label and title the plot
        plt.xlabel('Quantum State')
        plt.ylabel('Probability')
        plt.title(f'Theoretical W State Probabilities ({num_qubits} qubits)')
        
        # Add a horizontal line for the expected probability
        plt.axhline(y=expected_prob, color='red', linestyle='--', 
                   label=f'Expected probability: {expected_prob:.4f}')
        
        # Add legend
        plt.legend()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the figure
        filename = f"w_state_theory_{num_qubits}_qubits.png"
        plt.savefig(filename)
        print(f"\nPlot saved as {filename}")
        
    except Exception as e:
        print(f"Error creating plot: {str(e)}")

if __name__ == "__main__":
    # Analyze W states for different qubit counts
    for qubits in [2, 3, 4, 5]:
        analyze_w_state(qubits)
    
    print("\nW state theoretical analysis complete!") 