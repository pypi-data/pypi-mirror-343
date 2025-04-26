'''Module: integration_flow
This module demonstrates an integration of the dynamic circuit generation and meta-learning update functionality.
It simulates building a quantum circuit with initial rotation parameters, computing a dummy loss (for demonstration), and
updating the parameters using the MetaLearner. The updated parameters are then used to generate a new circuit.
'''

import numpy as np
from src.dynamic_circuit import build_quantum_circuit, ring_entanglement
from src.meta_learning import MetaLearner


def simulate_loss(params):
    """
    Simulate a dummy loss function based on the rotation parameters.
    For demonstration purposes, we use a simple quadratic loss: sum(0.5 * param^2).

    Parameters:
        params (np.array): Array of rotation parameters.

    Returns:
        float: The computed loss value.
    """
    loss = 0.5 * np.sum(np.square(params))
    return loss


def integration_demo(n_qubits, n_layers, initial_params, meta_lr=0.05):
    """
    Run an integration demo:
      - Build a quantum circuit using initial rotation parameters.
      - Compute a dummy loss from those parameters.
      - Update the parameters using meta-learning update.
      - Rebuild the quantum circuit with updated parameters.

    Parameters:
        n_qubits (int): Number of qubits in the circuit.
        n_layers (int): Number of layers in the circuit.
        initial_params (list or array): Flat list of initial rotation parameters (length should be n_qubits * n_layers).
        meta_lr (float): Meta-learning rate to use for parameter updates.

    Returns:
        tuple: (initial_circuit, updated_circuit, loss_before, loss_after, initial_params, updated_params)
    """
    # Build the initial circuit using the given parameters
    initial_circuit = build_quantum_circuit(n_qubits, n_layers, initial_params, ring_entanglement)
    
    # Compute loss from the initial parameters using the dummy loss function
    loss_before = simulate_loss(np.array(initial_params))
    print(f"[Integration] Initial loss: {loss_before}")
    
    # Initialize the MetaLearner with the provided meta learning rate
    learner = MetaLearner(meta_lr=meta_lr)
    
    # Update parameters using the meta-learning update rule, based on the dummy loss
    updated_params = learner.update_params(np.array(initial_params), loss_before)
    
    # Build a new circuit using the updated parameters
    updated_circuit = build_quantum_circuit(n_qubits, n_layers, updated_params, ring_entanglement)
    
    # Compute loss for the updated parameters to observe improvement
    loss_after = simulate_loss(np.array(updated_params))
    print(f"[Integration] Updated loss: {loss_after}")
    
    return initial_circuit, updated_circuit, loss_before, loss_after, initial_params, updated_params


if __name__ == '__main__':
    # Example usage of the integration demo
    n_qubits = 3
    n_layers = 2
    # Initial rotation parameters: flat list of length n_qubits * n_layers (here, 6 parameters)
    initial_params = [0.5, -0.2, 0.1, 0.3, -0.1, 0.2]
    print(f"[Integration Demo] Running integration demo with n_qubits={n_qubits}, n_layers={n_layers}")
    integration_demo(n_qubits, n_layers, initial_params) 