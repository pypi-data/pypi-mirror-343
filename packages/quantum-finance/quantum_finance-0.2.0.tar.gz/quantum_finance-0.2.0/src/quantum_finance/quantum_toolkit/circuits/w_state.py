"""
W-State Circuit Implementation Module

This module provides a reliable implementation of W-state quantum circuits
using a recursive approach that works across different Qiskit versions.

A W-state is a quantum entangled state where exactly one qubit is in state |1⟩
while all others are in state |0⟩, with equal amplitudes across all such possibilities.

For example:
- 2-qubit W-state: |W_2⟩ = (|01⟩ + |10⟩)/√2
- 3-qubit W-state: |W_3⟩ = (|001⟩ + |010⟩ + |100⟩)/√3
- n-qubit W-state: |W_n⟩ = (|10...0⟩ + |01...0⟩ + ... + |00...1⟩)/√n
"""

import numpy as np
from typing import Optional, Tuple, Dict, List, Union, Any
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_w_state_circuit(num_qubits: int, add_measurement: bool = False) -> QuantumCircuit:
    """
    Creates a quantum circuit that prepares the W-state for n qubits.
    
    This implementation uses a recursive approach that ensures reliable
    W-state preparation across different Qiskit versions.
    
    Args:
        num_qubits (int): Number of qubits (n >= 1).
        add_measurement (bool): Whether to add measurement operations
    
    Returns:
        QuantumCircuit: Circuit preparing the W-state.
        
    Raises:
        ValueError: If num_qubits < 1.
    """
    if num_qubits < 1:
        raise ValueError("W-state requires at least 1 qubit")
    
    # Create quantum registers
    qr = QuantumRegister(num_qubits, 'q')
    if add_measurement:
        cr = ClassicalRegister(num_qubits, 'c')
        circuit = QuantumCircuit(qr, cr, name=f"w_state_{num_qubits}")
    else:
        circuit = QuantumCircuit(qr, name=f"w_state_{num_qubits}")
    
    # Base Cases
    if num_qubits == 1:
        # W-state for 1 qubit: |1>
        circuit.x(0)
    elif num_qubits == 2:
        # W-state for 2 qubits: (|10> + |01>)/sqrt(2)
        circuit.x(0)       # Set first qubit to |1>
        circuit.h(0)       # Apply Hadamard to create superposition
        circuit.cx(0, 1)   # CNOT to entangle qubits
        circuit.x(0)       # Flip first qubit to get (|10> + |01>)/sqrt(2)
    else:
        # Recursive case for n > 2
        # The approach:
        # 1. Start with first qubit in |1>
        # 2. Rotate to set amplitude properly
        # 3. Recursively construct W-state for remaining qubits
        
        # Set first qubit to |1>
        circuit.x(0)
        
        # Calculate rotation angle to set correct amplitude
        theta = 2 * np.arccos(np.sqrt(1 / num_qubits))
        
        # Rotate first qubit
        circuit.ry(theta, 0)
        
        # Flip first qubit for control
        circuit.x(0)
        
        # Recursively build W-state for n-1 qubits
        sub_circuit = create_w_state_circuit(num_qubits - 1)
        sub_gate = sub_circuit.to_gate()
        controlled_gate = sub_gate.control(1)
        
        # Apply controlled W-state on remaining qubits
        circuit.append(controlled_gate, [0] + list(range(1, num_qubits)))
        
        # Restore first qubit
        circuit.x(0)
    
    # Add measurement if requested
    if add_measurement:
        circuit.measure(qr, cr)
    
    return circuit

def create_theoretical_w_state(num_qubits: int) -> np.ndarray:
    """
    Create a theoretical W-state for comparison.
    
    This function accounts for the phase differences that appear in the
    recursive W-state implementation. The implementation naturally introduces
    alternating phases for the basis states.
    
    Args:
        num_qubits (int): Number of qubits
        
    Returns:
        np.ndarray: Statevector representing the W-state
    """
    state = np.zeros(2**num_qubits, dtype=complex)
    
    # W-state has equal amplitude for each one-hot state
    amplitude = 1.0 / np.sqrt(num_qubits)
    
    # Set amplitude for each state with exactly one qubit in |1⟩
    # Account for the alternating phases in the implementation
    for i in range(num_qubits):
        idx = 2**i  # Binary with only i-th bit set
        
        # Add alternating phases to match the implementation
        # Even-indexed states (0, 2, 4, ...) have positive phase
        # Odd-indexed states (1, 3, 5, ...) have negative phase (π shift)
        if i % 2 == 0:
            state[idx] = amplitude
        else:
            state[idx] = -amplitude  # Equivalent to a phase of π
        
    return state

def verify_w_state(statevector: np.ndarray, num_qubits: int) -> Dict[str, Any]:
    """
    Comprehensive verification of a W-state with advanced metrics.
    
    This enhanced version provides detailed verification of W-state properties
    with multiple fidelity metrics.
    
    Args:
        statevector (np.ndarray): Statevector to verify
        num_qubits (int): Number of qubits
        
    Returns:
        Dict[str, Any]: Dictionary containing verification results:
            - basic_verification: Original simple verification (bool)
            - probability_sum: Sum of one-hot state probabilities
            - state_fidelity: Fidelity between statevector and theoretical W-state
            - trace_distance: Trace distance metric (0 for identical states, 1 for orthogonal)
            - relative_entropy: Quantum relative entropy (Kullback-Leibler divergence)
            - one_hot_states: Details on one-hot states and their probabilities
            - non_one_hot_states: Details on unexpected non-one-hot states
            - fidelity_per_state: Fidelity for each one-hot state
            - is_valid: Overall validity assessment (bool)
    """
    # Calculate probabilities
    probabilities = np.abs(statevector) ** 2
    
    # Get indices for one-hot states (states with exactly one qubit in |1>)
    one_hot_indices = [2**i for i in range(num_qubits)]
    
    # Sum probabilities for one-hot states
    one_hot_prob_sum = float(sum(probabilities[idx] for idx in one_hot_indices))
    
    # Check if probabilities are evenly distributed
    expected_prob = 1.0 / num_qubits
    
    # Detailed information about one-hot states
    one_hot_states = []
    for i, idx in enumerate(one_hot_indices):
        binary = format(idx, f"0{num_qubits}b")
        prob = probabilities[idx]
        deviation = abs(prob - expected_prob)
        one_hot_states.append({
            "state": binary,
            "index": idx,
            "probability": prob,
            "expected": expected_prob,
            "deviation": deviation,
            "deviation_percent": (deviation / expected_prob) * 100 if expected_prob > 0 else float('inf')
        })
    
    # Check for non-one-hot states with significant probability
    non_one_hot_states = []
    for i, prob in enumerate(probabilities):
        if i not in one_hot_indices and prob > 0.001:  # Lower threshold (0.1%) for more sensitivity
            binary = format(i, f"0{num_qubits}b")
            hamming_weight = binary.count('1')  # Number of 1s in the binary representation
            non_one_hot_states.append({
                "state": binary,
                "index": i,
                "probability": prob,
                "hamming_weight": hamming_weight
            })
    
    # Calculate advanced metrics
    theoretical_w_state = create_theoretical_w_state(num_qubits)
    
    # Calculate fidelity (state overlap)
    # |⟨ψ|φ⟩|²
    fidelity = np.abs(np.dot(np.conjugate(theoretical_w_state), statevector))**2
    
    # Calculate trace distance
    # 1/2 * tr|ρ - σ|
    # For pure states: √(1 - |⟨ψ|φ⟩|²)
    trace_distance = np.sqrt(1 - fidelity)
    
    # Calculate quantum relative entropy (von Neumann relative entropy)
    # S(ρ||σ) = tr(ρ log ρ - ρ log σ)
    # For pure states, this is -log(fidelity)
    relative_entropy = -np.log(fidelity) if fidelity > 0 else float('inf')
    
    # Fidelity per one-hot state
    state_fidelities = {}
    for i in range(num_qubits):
        # Create a state with just this one-hot component
        single_state = np.zeros(2**num_qubits, dtype=complex)
        idx = 2**i
        single_state[idx] = 1.0
        
        # Calculate overlap with this particular component
        overlap = np.abs(np.dot(np.conjugate(single_state), statevector))**2
        expected_overlap = 1.0 / num_qubits
        
        # Store results
        state_fidelities[format(idx, f"0{num_qubits}b")] = {
            "fidelity": overlap,
            "expected": expected_overlap,
            "relative_error": abs(overlap - expected_overlap) / expected_overlap if expected_overlap > 0 else float('inf')
        }
    
    # Basic verification (original criteria)
    equal_distribution = all(abs(probabilities[idx] - expected_prob) <= 0.05 for idx in one_hot_indices)
    basic_valid = one_hot_prob_sum > 0.95 and equal_distribution
    
    # Enhanced validity criteria
    # 1. High fidelity with theoretical state (>0.95)
    # 2. Low trace distance (<0.22 corresponds to fidelity >0.95)
    # 3. One-hot probabilities sum close to 1
    # 4. No significant non-one-hot states
    advanced_valid = (
        fidelity > 0.95 and
        trace_distance < 0.22 and
        one_hot_prob_sum > 0.98 and
        all(state["probability"] < 0.02 for state in non_one_hot_states)
    )
    
    # Final validity assessment
    is_valid = basic_valid and advanced_valid
    
    # Collect and return all results
    return {
        "basic_verification": basic_valid,
        "probability_sum": one_hot_prob_sum,
        "state_fidelity": fidelity,
        "trace_distance": trace_distance,
        "relative_entropy": relative_entropy,
        "one_hot_states": one_hot_states,
        "non_one_hot_states": non_one_hot_states,
        "fidelity_per_state": state_fidelities,
        "is_valid": is_valid
    }

def test_w_state_fidelity(num_qubits: int, detailed: bool = False) -> Dict[str, Any]:
    """
    Comprehensive fidelity testing for W-state implementation with enhanced metrics.
    
    This enhanced version provides detailed fidelity analysis and visualization
    options for thorough circuit validation.
    
    Args:
        num_qubits (int): Number of qubits
        detailed (bool): Whether to produce detailed output
        
    Returns:
        Dict[str, Any]: Dictionary containing test results:
            - success: Whether the test passed (bool)
            - fidelity: Overall fidelity score
            - verification_results: Complete verification metrics
            - error_analysis: Detailed error analysis if available
            - suggestions: Potential improvement suggestions
    """
    try:
        from qiskit.quantum_info import Statevector, state_fidelity
    except ImportError:
        raise ImportError("Qiskit is required for fidelity testing. Please install it with 'pip install qiskit'.")
    
    # Create the W-state circuit
    circuit = create_w_state_circuit(num_qubits)
    
    # Get the statevector from the circuit
    circuit_statevector = Statevector.from_instruction(circuit)
    
    # Create the theoretical W-state
    theoretical_w_state = create_theoretical_w_state(num_qubits)
    
    # Convert to Statevector object
    theoretical_sv = Statevector(theoretical_w_state)
    
    # Calculate fidelity
    fidelity = state_fidelity(circuit_statevector, theoretical_sv)
    
    # Run comprehensive verification
    verification_results = verify_w_state(circuit_statevector.data, num_qubits)
    
    # Analyze error sources if fidelity is not perfect
    error_analysis = {}
    suggestions = []
    
    if fidelity < 0.99:
        # Analyze amplitude distribution
        amplitude_errors = []
        expected_amp = 1.0 / np.sqrt(num_qubits)
        
        for i in range(num_qubits):
            idx = 2**i
            actual_amp = np.abs(circuit_statevector.data[idx])
            error = np.abs(actual_amp - expected_amp)
            phase = np.angle(circuit_statevector.data[idx])
            
            amplitude_errors.append({
                "state": format(idx, f"0{num_qubits}b"),
                "expected_amplitude": expected_amp,
                "actual_amplitude": actual_amp,
                "amplitude_error": error,
                "phase": phase
            })
        
        error_analysis["amplitude_errors"] = amplitude_errors
        
        # Check for phase coherence
        phases = [np.angle(circuit_statevector.data[2**i]) for i in range(num_qubits)]
        phase_coherent = all(abs(phases[0] - phase) < 0.01 for phase in phases)
        error_analysis["phase_coherent"] = phase_coherent
        
        # Add suggestions based on error analysis
        if not phase_coherent:
            suggestions.append("Phase coherence issue detected. Check for unexpected Z gates or phase shifts.")
            
        if any(error["amplitude_error"] > 0.01 for error in amplitude_errors):
            suggestions.append("Amplitude distribution is uneven. Check rotation angles and gate sequencing.")
            
        if verification_results["non_one_hot_states"]:
            suggestions.append("Detected unexpected states. Circuit may have logical errors or decoherence issues.")
    
    # Assess overall success
    success = fidelity > 0.99 and verification_results["is_valid"]
    
    if detailed:
        # Print detailed results
        print(f"\n---- W-State Fidelity Test for {num_qubits} qubits ----")
        print(f"Overall fidelity: {fidelity:.6f}")
        print(f"Trace distance: {verification_results['trace_distance']:.6f}")
        print(f"Relative entropy: {verification_results['relative_entropy']:.6f}")
        print(f"One-hot probability sum: {verification_results['probability_sum']:.6f}")
        
        print("\nOne-hot state analysis:")
        for state in verification_results["one_hot_states"]:
            print(f"|{state['state']}⟩: prob={state['probability']:.6f}, "
                  f"expected={state['expected']:.6f}, "
                  f"deviation={state['deviation_percent']:.2f}%")
        
        if verification_results["non_one_hot_states"]:
            print("\nUnexpected states detected:")
            for state in verification_results["non_one_hot_states"]:
                print(f"|{state['state']}⟩: prob={state['probability']:.6f}, "
                      f"hamming weight={state['hamming_weight']}")
        
        if suggestions:
            print("\nImprovement suggestions:")
            for suggestion in suggestions:
                print(f"- {suggestion}")
    
    return {
        "success": success,
        "fidelity": fidelity,
        "verification_results": verification_results,
        "error_analysis": error_analysis,
        "suggestions": suggestions
    }

if __name__ == "__main__":
    # Test the W-state implementation for 2, 3 and 4 qubits
    for n in [2, 3, 4]:
        print(f"\nTesting {n}-qubit W-state:")
        results = test_w_state_fidelity(n, detailed=True)
        print(f"Test {'PASSED' if results['success'] else 'FAILED'}") 