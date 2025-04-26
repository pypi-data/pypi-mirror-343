#!/usr/bin/env python3
"""
W-State Verification Test Script

This script tests and verifies the correctness of W-state implementations
across different qubit counts. It checks both the updated standard implementation
and the new recursive implementation for compatibility and correctness.
"""

import os
import sys
import numpy as np
from typing import Tuple, Dict, List

# Add parent directory to path to allow imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Try importing from both implementations
try:
    # Import the new dedicated W-state module
    from quantum.circuits.w_state import create_w_state_circuit, verify_w_state
    HAS_W_STATE_MODULE = True
    print("✅ Found dedicated W-state module")
except ImportError:
    HAS_W_STATE_MODULE = False
    print("❌ Dedicated W-state module not found")

try:
    # Import from standard circuits
    from quantum.circuits.standard import create_w_state as create_w_state_standard
    HAS_STANDARD_IMPL = True
    print("✅ Found standard W-state implementation")
except ImportError:
    HAS_STANDARD_IMPL = False
    print("❌ Standard W-state implementation not found")

try:
    # Import from base circuits
    from quantum.circuits.base import create_w_state as create_w_state_base
    HAS_BASE_IMPL = True
    print("✅ Found base W-state implementation")
except ImportError:
    HAS_BASE_IMPL = False
    print("❌ Base W-state implementation not found")

try:
    # Import necessary Qiskit components
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector, state_fidelity
    HAS_QISKIT = True
    print("✅ Qiskit successfully imported")
except ImportError:
    HAS_QISKIT = False
    print("❌ Qiskit not found - install with 'pip install qiskit'")


def create_theoretical_w_state(num_qubits: int) -> np.ndarray:
    """
    Creates a theoretical W-state statevector for comparison.
    
    Args:
        num_qubits (int): Number of qubits
        
    Returns:
        np.ndarray: Theoretical W-state statevector
    """
    state = np.zeros(2**num_qubits, dtype=complex)
    
    # Set equal amplitude for each one-hot state
    amplitude = 1.0 / np.sqrt(num_qubits)
    
    # Add amplitude to each state with exactly one qubit in |1⟩
    for i in range(num_qubits):
        idx = 2**i  # Binary index with only the i-th bit set
        state[idx] = amplitude
        
    return state


def verify_circuit_statevector(circuit: QuantumCircuit, num_qubits: int) -> Tuple[float, bool]:
    """
    Verifies the statevector produced by a quantum circuit.
    
    Args:
        circuit (QuantumCircuit): Circuit to verify
        num_qubits (int): Number of qubits
        
    Returns:
        Tuple[float, bool]: (fidelity, passed_test)
    """
    if not HAS_QISKIT:
        print("Qiskit required for verification")
        return (0.0, False)
    
    # Get the statevector from the circuit
    sv = Statevector.from_instruction(circuit)
    
    # Create theoretical W-state statevector
    theoretical_sv = create_theoretical_w_state(num_qubits)
    
    # Calculate fidelity
    fidelity = state_fidelity(sv.data, theoretical_sv)
    
    # Check if fidelity exceeds threshold
    passed = fidelity > 0.99  # 99% fidelity threshold
    
    # Print the most significant states for debugging
    probabilities = np.abs(sv.data) ** 2
    print(f"\nState distribution for {num_qubits}-qubit circuit:")
    
    for i, prob in enumerate(probabilities):
        if prob > 0.001:  # Only show states with significant probability
            binary = format(i, f"0{num_qubits}b")
            print(f"|{binary}⟩: {prob:.6f}")
    
    print(f"Fidelity with theoretical W-state: {fidelity:.6f}")
    
    return (fidelity, passed)


def test_implementation(create_func, name: str, qubit_range: List[int] = [2, 3, 4]) -> Dict[int, Tuple[float, bool]]:
    """
    Tests a W-state implementation across multiple qubit counts.
    
    Args:
        create_func: Function that creates W-state circuit
        name: Name of the implementation being tested
        qubit_range: Range of qubit counts to test
        
    Returns:
        Dict[int, Tuple[float, bool]]: Results for each qubit count
    """
    print(f"\n{'='*60}")
    print(f"Testing W-state implementation: {name}")
    print(f"{'='*60}")
    
    results = {}
    
    for n in qubit_range:
        try:
            print(f"\nTesting {n}-qubit W-state:")
            
            # Create circuit
            circuit = create_func(n)
            
            # Verify the circuit
            fidelity, passed = verify_circuit_statevector(circuit, n)
            
            results[n] = (fidelity, passed)
            print(f"Test {'PASSED' if passed else 'FAILED'}")
            
        except Exception as e:
            print(f"Error testing {n}-qubit W-state: {str(e)}")
            results[n] = (0.0, False)
    
    return results


def main():
    """Main test function to verify all W-state implementations."""
    if not HAS_QISKIT:
        print("Qiskit is required for verification. Please install it with 'pip install qiskit'")
        return
    
    implementations = []
    
    # Test the dedicated W-state module if available
    if HAS_W_STATE_MODULE:
        implementations.append((create_w_state_circuit, "Dedicated Recursive Implementation"))
    
    # Test the standard implementation if available
    if HAS_STANDARD_IMPL:
        implementations.append((lambda n: create_w_state_standard(n), "Standard Implementation"))
    
    # Test the base implementation if available
    if HAS_BASE_IMPL:
        implementations.append((lambda n: create_w_state_base(n, False), "Base Implementation"))
    
    # Run tests for each implementation
    all_results = {}
    for impl_func, impl_name in implementations:
        results = test_implementation(impl_func, impl_name)
        all_results[impl_name] = results
    
    # Show summary of results
    print("\n\n" + "="*60)
    print("W-STATE IMPLEMENTATION SUMMARY")
    print("="*60)
    
    for impl_name, results in all_results.items():
        print(f"\n{impl_name}:")
        for n_qubits, (fidelity, passed) in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {n_qubits}-qubit W-state: Fidelity {fidelity:.6f} - {status}")
    
    print("\nRecommendation:")
    
    # Check if dedicated recursive implementation worked for all cases
    if "Dedicated Recursive Implementation" in all_results:
        recursive_results = all_results["Dedicated Recursive Implementation"]
        all_passed = all(passed for _, passed in recursive_results.values())
        
        if all_passed:
            print("The dedicated recursive W-state implementation works correctly for all tested qubit counts.")
            print("This is the recommended implementation moving forward.")
        else:
            print("The recursive implementation still has issues. Review the detailed output above.")


if __name__ == "__main__":
    main() 