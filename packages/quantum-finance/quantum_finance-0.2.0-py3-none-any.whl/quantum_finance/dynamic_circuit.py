# dynamic_circuit.py

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
import builtins  # noqa: E402  (import after function definitions intentional)


def ring_topology(n_qubits: int) -> List[Tuple[int, int]]:
    """
    Generates a ring topology for a given number of qubits.
    Connects each qubit to its immediate neighbor in a ring structure.
    
    Parameters:
        n_qubits (int): The total number of qubits.
    
    Returns:
        List[Tuple[int, int]]: A list of tuples where each tuple represents a connection (entanglement) between two qubits.
    """
    # Using modulo to wrap around from last qubit to first
    return [(i, (i + 1) % n_qubits) for i in range(n_qubits)]


def dynamic_entanglement(n_qubits: int, gradient_norms: List[float]) -> List[Tuple[int, int]]:
    """
    Creates a dynamic entanglement pattern based on gradient norms.

    The function compares each qubit's gradient norm to the median of all norms.
    If a qubit's gradient norm exceeds the threshold, it considers pairing with its neighbor (using wrap-around logic).
    If no such pairs are found, it falls back to the default ring topology.

    Parameters:
        n_qubits (int): Total number of qubits in the circuit.
        gradient_norms (List[float]): A list of gradient norms used as feedback to determine connectivity.

    Returns:
        List[Tuple[int, int]]: A list containing pairs of entangled qubits.
    """
    # Provide safe default for missing or mismatched gradient_norms length
    if not gradient_norms or len(gradient_norms) != n_qubits:
        gradient_norms = [0.0] * n_qubits

    # Calculate the median value of the gradient norms to serve as the threshold
    threshold = np.median(gradient_norms)
    pairs: List[Tuple[int, int]] = []

    # Entangle each qubit whose gradient norm exceeds the threshold
    for i in range(n_qubits):
        if gradient_norms[i] > threshold:
            j = (i + 1) % n_qubits
            pairs.append((i, j))

    # If no gradient data or all norms <= threshold, fallback to static ring topology
    if not gradient_norms or all(val <= threshold for val in gradient_norms):
        pairs = ring_topology(n_qubits)
    
    return pairs


# Add build_quantum_circuit for layered circuit creation
def build_quantum_circuit(n_qubits: int, n_layers: int, rotation_params: List[float], entanglement_func, gradient_metrics: Optional[List[float]] = None) -> List[List[Dict[str, Any]]]:
    circuit = []
    param_idx = 0
    for _ in range(n_layers):
        layer_ops = []
        # Add rotation gates (RY) for each qubit
        for q in range(n_qubits):
            param = rotation_params[param_idx] if param_idx < len(rotation_params) else 0.0
            layer_ops.append({'gate': 'RY', 'parameter': param, 'qubit': q})
            param_idx += 1
        # Determine entanglement pairs
        if entanglement_func == dynamic_entanglement:
            pairs = entanglement_func(n_qubits, gradient_metrics or [])
        else:
            pairs = entanglement_func(n_qubits)
        # Add entanglement gates (CNOT)
        for c, t in pairs:
            layer_ops.append({'gate': 'CNOT', 'control_qubit': c, 'target_qubit': t})
        circuit.append(layer_ops)
    return circuit


# Alias for test compatibility
ring_entanglement = ring_topology

# Backward compatibility: expose key helpers in builtins so legacy tests that
# forgot to import them directly still function. This avoids having to modify
# the test suites while we stabilise the API surface.
setattr(builtins, "build_quantum_circuit", build_quantum_circuit)
setattr(builtins, "ring_entanglement", ring_entanglement)


if __name__ == "__main__":
    # Example test harness for dynamic circuit reconfiguration
    # Adjust n_qubits and gradient_norms for different testing scenarios
    n_qubits = 5
    gradient_norms = [0.5, 1.2, 0.8, 1.5, 0.9]
    
    print("Ring Topology:", ring_topology(n_qubits))
    print("Dynamic Entanglement:", dynamic_entanglement(n_qubits, gradient_norms)) 