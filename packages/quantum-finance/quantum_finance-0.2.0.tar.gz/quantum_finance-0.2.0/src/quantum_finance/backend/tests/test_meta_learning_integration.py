import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import torch
import torch.nn as nn
import numpy as np

from quantum_finance.backend.quantum_transformer import QuantumTransformer, train_quantum_transformer


# Dummy quantum feed-forward class to simulate quantum_ffn, now as a subclass of nn.Module
class DummyQuantumFeedForward(nn.Module):
    def __init__(self, n_parameters=2):
        super(DummyQuantumFeedForward, self).__init__()
        self.n_parameters = n_parameters
        self.circuit_params = [0.0 for _ in range(n_parameters)]
    
    def update_parameters(self, new_params):
        self.circuit_params = new_params


# Define a dummy transformer model
# We'll instantiate a small model and override its layers' quantum_ffn with DummyQuantumFeedForward

def create_dummy_model():
    # Create a model with small dimensions: d_model=4, n_heads=1, n_layers=2, n_qubits=2
    model = QuantumTransformer(d_model=4, n_heads=1, n_layers=2, n_qubits=2)
    
    # Override forward method to use the input projection for a simple differentiable output
    model.forward = lambda x, task='train': model.input_proj(x)
    
    # Override each layer's quantum_ffn with DummyQuantumFeedForward
    for layer in model.layers:
        layer.quantum_ffn = DummyQuantumFeedForward(n_parameters=2)
    
    return model


# Create a dummy training dataset
# Each circuit dict must contain an 'input_state' and 'n_qubits'.
# For simplicity, we use a 2-qubit circuit, so input state should be of length 2**2 = 4

dummy_data = [
    {'input_state': [1, 0, 0, 0], 'gates': ['H'], 'n_qubits': 2}
    for _ in range(5)  # replicate to have multiple samples
]


def test_meta_learning_integration():
    model = create_dummy_model()
    
    # Run training for 20 epochs; meta-learning updates should occur at epoch 0 and 10
    trained_model = train_quantum_transformer(model, dummy_data, num_epochs=20, learning_rate=0.01)
    
    # After 20 epochs, we expect meta updates at epochs 0 and 10, so each dummy circuit parameter should have been increased by 0.1 twice, resulting in 0.2.
    expected_params = [0.2, 0.2]
    
    for layer in trained_model.layers:
        actual_params = layer.quantum_ffn.circuit_params
        assert actual_params == expected_params, f"Expected circuit parameters {expected_params}, but got {actual_params} in a layer."
    
    print("Meta-learning integration test passed: circuit parameters updated correctly.")


if __name__ == '__main__':
    test_meta_learning_integration() 