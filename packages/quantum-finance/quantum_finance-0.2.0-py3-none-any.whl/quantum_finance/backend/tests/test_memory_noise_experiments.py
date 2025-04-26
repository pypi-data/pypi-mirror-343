import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import torch
import torch.nn as nn
import numpy as np

from quantum_finance.backend.quantum_memory import QuantumMemristor


def run_noise_experiment(state_size=10, n_qubits=4, learning_rate=0.01, decay_rate=0.999, noise_levels=[0.0, 0.01, 0.05, 0.1]):
    """
    Run experiments on QuantumMemristor with different memory_noise levels.
    For each noise level, run a forward and backward pass to update the state,
    and print out the conductance, memory capacity, and entanglement.
    """
    input_signal = torch.randn(5, 1, state_size, requires_grad=True)  # (seq_len, batch_size, state_size)
    
    for noise in noise_levels:
        print(f"\nTesting with memory_noise = {noise}")
        memristor = QuantumMemristor(state_size=state_size, n_qubits=n_qubits, learning_rate=learning_rate,
                                      decay_rate=decay_rate, memory_noise=noise)
        memristor.train()  # Enable training mode to allow state updates
        
        # Run forward pass
        output = memristor(input_signal)
        
        # Trigger backward pass for state update
        loss = output.sum()
        loss.backward()
        
        print("Conductance after update:", memristor.conductance)
        print("Memory capacity:", memristor.memory_capacity)
        print("Entanglement after update:", memristor.state.entanglement)
        print("-" * 50)


if __name__ == '__main__':
    run_noise_experiment() 