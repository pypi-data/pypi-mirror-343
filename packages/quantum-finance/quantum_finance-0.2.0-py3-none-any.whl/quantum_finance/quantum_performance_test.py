# NOTE: Imports updated after major refactor (March 2025)
# - quantum.circuits -> quantum_finance.quantum_toolkit.circuits
# - quantum_benchmark -> quantum_finance.quantum_benchmark
# - quantum_visualization -> quantum_finance.quantum_visualization
# This ensures compatibility with the new codebase structure and maintains benchmark integrity.
import time
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from quantum_finance.quantum_toolkit.circuits import (
    create_bell_state,
    create_ghz_state,
    create_w_state,
    create_quantum_fourier_transform,
    create_random_circuit,
    run_circuit_simulation
)
from quantum_finance.quantum_benchmark import run_circuit_simulation as benchmark_simulation
from quantum_finance.quantum_visualization import create_performance_report
import os

def measure_execution_time(func, *args, **kwargs):
    """Measure execution time of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def benchmark_circuit(circuit_name, circuit_func, *args, shots=1000, repetitions=5):
    """Run benchmarks for a specific circuit multiple times."""
    times = []
    results = []
    
    print(f"\nBenchmarking {circuit_name}:")
    print("-" * 50)
    
    # NOTE: Use 'benchmark_simulation' (from quantum_benchmark.py) instead of 'run_circuit_simulation' (from quantum_toolkit.circuits)
    # because only the former returns a result object with 'metadata' and 'gate_counts' attributes.
    for i in range(repetitions):
        circuit = circuit_func(*args)
        # Decompose W state circuits to avoid custom gate errors in Qiskit Aer
        if circuit_name.lower().startswith('w state'):
            # Decompose recursively to ensure all custom gates are expanded
            circuit = circuit.decompose(reps=10)
            # Notation: This is required because Qiskit Aer does not recognize custom gates (e.g., from recursive W state construction)
        result, execution_time = benchmark_simulation(circuit)
        times.append(execution_time)
        results.append(result)
        
        print(f"Run {i+1}: {execution_time:.4f} seconds")
        print(f"Circuit depth: {result.metadata.circuit_depth}")
        print(f"Gate counts: {result.metadata.gate_counts}")
    
    avg_time = np.mean(times)
    std_time = np.std(times)
    
    print(f"\nAverage execution time: {avg_time:.4f} ± {std_time:.4f} seconds")
    return avg_time, std_time, results

def run_performance_tests(output_dir="performance_reports"):
    """Run comprehensive performance tests on quantum circuits."""
    print("Starting Quantum Circuit Performance Tests")
    print("=" * 80)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Test parameters
    qubit_ranges = [2, 4, 8, 12]  # Different numbers of qubits to test
    shots = 1000  # Number of shots per circuit
    repetitions = 5  # Number of times to repeat each test
    
    results = {}
    
    # 1. Bell State Tests
    print("\nTesting Bell State Circuit")
    results['bell_state'] = benchmark_circuit(
        "Bell State",
        create_bell_state
    )
    
    # 2. GHZ State Tests
    print("\nTesting GHZ State Circuit")
    for n_qubits in qubit_ranges:
        results[f'ghz_state_{n_qubits}'] = benchmark_circuit(
            f"GHZ State ({n_qubits} qubits)",
            create_ghz_state,
            n_qubits
        )
    
    # 3. W State Tests
    print("\nTesting W State Circuit")
    for n_qubits in qubit_ranges[:2]:  # W states are more complex, test with fewer qubits
        results[f'w_state_{n_qubits}'] = benchmark_circuit(
            f"W State ({n_qubits} qubits)",
            create_w_state,
            n_qubits
        )
    
    # 4. QFT Tests
    print("\nTesting Quantum Fourier Transform")
    for n_qubits in qubit_ranges:
        results[f'qft_{n_qubits}'] = benchmark_circuit(
            f"QFT ({n_qubits} qubits)",
            create_quantum_fourier_transform,
            n_qubits
        )
    
    # 5. Random Circuit Tests
    print("\nTesting Random Circuits")
    depths = [3, 5, 10]
    for n_qubits in qubit_ranges[:2]:
        for depth in depths:
            results[f'random_{n_qubits}q_{depth}d'] = benchmark_circuit(
                f"Random Circuit ({n_qubits} qubits, depth {depth})",
                create_random_circuit,
                n_qubits,
                depth
            )
    
    # Generate summary report
    print("\nPerformance Test Summary")
    print("=" * 80)
    print(f"{'Circuit Type':<30} {'Avg Time (s)':<15} {'Std Dev (s)':<15}")
    print("-" * 80)
    
    for circuit_name, (avg_time, std_time, _) in results.items():
        print(f"{circuit_name:<30} {avg_time:<15.4f} {std_time:<15.4f}")
    
    # Generate comprehensive report with visualizations
    report_path = create_performance_report(results, output_dir)
    print(f"\nDetailed performance report generated at: {report_path}")

if __name__ == "__main__":
    run_performance_tests() 