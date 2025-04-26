import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import torch
import numpy as np

# Import dynamic_topology_generator from quantum_transformer, and ring_topology from dynamic_circuit for expected output
from quantum_finance.backend.quantum_transformer import dynamic_topology_generator
from dynamic_circuit import ring_topology


def test_dynamic_topology_dynamic():
    """Test dynamic topology generation with varied gradient stats."""
    n_qubits = 4
    # Create a sample gradient_stats tensor
    # Each row represents gradient metrics for a qubit
    # The L2 norms are: [0.1, 0.5, 0.8, 1.0] leading to a median of 0.65
    # Expect dynamic pair: qubit 2 and 3 (0-indexed)
    data = [
        [0.1, 0.0, 0.0, 0.0],
        [0.5, 0.0, 0.0, 0.0],
        [0.8, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0]
    ]
    gradient_stats = torch.tensor(data, dtype=torch.float32)
    result = dynamic_topology_generator(n_qubits, gradient_stats)
    expected = [(2, 3)]
    assert result == expected, f"Dynamic topology test failed: Expected {expected}, got {result}"


def test_dynamic_topology_ring():
    """Test fallback to ring topology when no dynamic pairs are found."""
    n_qubits = 4
    # Create a tensor where all values are equal
    # L2 norm for each row will be constant, so no value will be strictly greater than the median
    gradient_stats = torch.ones((n_qubits, n_qubits), dtype=torch.float32)
    result = dynamic_topology_generator(n_qubits, gradient_stats)
    expected = ring_topology(n_qubits)
    assert result == expected, f"Ring topology fallback failed: Expected {expected}, got {result}"


if __name__ == '__main__':
    test_dynamic_topology_dynamic()
    test_dynamic_topology_ring()
    print('All dynamic topology tests passed!') 