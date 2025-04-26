#!/usr/bin/env python3

"""
Comprehensive Quantum Simulation Benchmark Script

This script runs a series of benchmarks on various quantum simulation components
and provides a comprehensive report comparing current performance with historical data.
"""

import time
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from quantum_finance.dynamic_circuit_refactoring_optimized import DynamicCircuitRefactor
from qiskit.circuit import QuantumCircuit  # Core circuit class
from qiskit import transpile  # Qiskit transpiler for circuit optimization
from qiskit_aer import AerSimulator  # Aer simulator backend
import sys
import argparse  # Added for command-line argument support
from quantum_finance.quantum_ai_interface import QuantumMeasurementResult, CircuitMetadata, UncertaintyMetrics
from dataclasses import dataclass
from typing import Dict, Any
from matplotlib.animation import FuncAnimation
from quantum_finance.data import CryptoDataFetcher

# Add memory profiling imports
try:
    from memory_profiler import memory_usage
    import tracemalloc
    MEMORY_PROFILING_AVAILABLE = True
except ImportError:
    MEMORY_PROFILING_AVAILABLE = False
    print("Warning: memory_profiler not available. Install with 'pip install memory-profiler' for memory profiling.")

# Add the site-packages to path to ensure we use the installed qiskit_aer, not the local one
site_packages = [p for p in sys.path if 'site-packages' in p]
if site_packages:
    sys.path = site_packages + [p for p in sys.path if p not in site_packages]

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BENCHMARK_ITERATIONS = 100
QUBIT_SIZES = [2, 4, 8, 16]
HISTORICAL_RESULTS_FILE = 'benchmark_results.json'

# Try to import visualization libraries, but continue if they're not available
try:
    import numpy as np
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    print("Warning: Matplotlib and/or NumPy not available. Charts will not be generated.")
    VISUALIZATION_AVAILABLE = False

# Create a directory for memory profiles if needed
MEMORY_PROFILE_DIR = "benchmark_results/memory_profiles"
os.makedirs(MEMORY_PROFILE_DIR, exist_ok=True)

def create_circuit(num_qubits, depth=3):
    """Create a test quantum circuit with the specified number of qubits and depth."""
    circuit = QuantumCircuit(num_qubits)
    
    # Add a layer of Hadamard gates
    for i in range(num_qubits):
        circuit.h(i)
    
    # Add depth layers of entangling operations
    for d in range(depth):
        # Add CX gates between adjacent qubits
        for i in range(0, num_qubits-1, 2):
            circuit.cx(i, i+1)
        
        # Add another layer of Hadamards
        for i in range(num_qubits):
            circuit.h(i)
        
        # Add CX gates between other pairs of qubits
        for i in range(1, num_qubits-1, 2):
            circuit.cx(i, i+1)
    
    # Add measurement operations
    circuit.measure_all()
    
    return circuit

def run_circuit_simulation(circuit):
    """Run a quantum circuit simulation and time the execution."""
    # Create a simulator
    simulator = AerSimulator()
    
    # Start timing
    start_time = time.time()
    
    # Run the simulation
    job = simulator.run(circuit, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)
    
    # End timing
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Create circuit metadata
    gate_counts = {}
    for instruction, _, _ in circuit.data:
        gate_name = instruction.name
        if gate_name in gate_counts:
            gate_counts[gate_name] += 1
        else:
            gate_counts[gate_name] = 1
    
    metadata = CircuitMetadata(
        num_qubits=circuit.num_qubits,
        circuit_depth=circuit.depth(),
        gate_counts=gate_counts,
        simulation_method='aer_simulator'
    )
    
    # Create uncertainty metrics based on shot noise
    shots = 1000
    shot_noise = 1.0 / np.sqrt(shots)
    uncertainty = UncertaintyMetrics(
        shot_noise=shot_noise,
        standard_error=shot_noise,
        confidence_interval=(0.0, 2*shot_noise),
        total_uncertainty=shot_noise
    )
    
    # Create and return the measurement result
    measurement_result = QuantumMeasurementResult(
        counts=counts,
        metadata=metadata,
        uncertainty=uncertainty,
        shots=shots
    )
    
    return measurement_result, execution_time

def run_circuit_refactoring(circuit):
    """Run a circuit refactoring operation and time the execution."""
    start_time = time.time()
    
    # Perform circuit refactoring (using transpile as a refactoring operation)
    refactored_circuit = transpile(circuit, basis_gates=['u1', 'u2', 'u3', 'cx'], optimization_level=3)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return execution_time

def run_dynamic_circuit_generation(qubits):
    """Run dynamic circuit generation benchmark."""
    start_time = time.time()
    circuit = DynamicCircuitRefactor().generate_dynamic_circuit(qubits)
    end_time = time.time()
    return end_time - start_time  # Return timing instead of circuit

def benchmark_circuit_generation(refactor, iterations=100):
    """Benchmark the dynamic circuit generation."""
    start = time.perf_counter()
    for _ in range(iterations):
        circuit = refactor.generate_dynamic_circuit()
    end = time.perf_counter()
    duration = end - start
    avg_time = duration/iterations
    logger.info(f"Generated {iterations} circuits in {duration:.4f} seconds, average = {avg_time:.6f} sec/circuit.")
    return avg_time

def benchmark_circuit_refactoring(refactor, iterations=100):
    """Benchmark the dynamic circuit refactoring (transpile) function."""
    # Generate a static circuit to refactor
    circuit = refactor.generate_dynamic_circuit()
    start = time.perf_counter()
    for _ in range(iterations):
        _ = refactor.refactor_circuit(circuit)
    end = time.perf_counter()
    duration = end - start
    avg_time = duration/iterations
    logger.info(f"Refactored circuit {iterations} times in {duration:.4f} seconds, average = {avg_time:.6f} sec/refactor.")
    return avg_time

def benchmark_circuit_simulation(qubits, depth=3, iterations=100):
    """Benchmark circuit simulation performance."""
    logger.info(f"Benchmarking circuit simulation with {qubits} qubits...")
    
    # Function to create test circuit
    def create_test_circuit(num_qubits, depth):
        qc = QuantumCircuit(num_qubits)
        # Add some gates
        for _ in range(depth):
            for i in range(num_qubits):
                qc.h(i)
            for i in range(num_qubits-1):
                qc.cx(i, i+1)
        qc.measure_all()  # Add measurement for proper simulation
        return qc
    
    # Run the benchmark
    total_time = 0
    circuit = create_test_circuit(qubits, depth)
    measurement_results = []  # Store measurement results for analysis
    
    for i in range(iterations):
        measurement_result, execution_time = run_circuit_simulation(circuit)
        total_time += execution_time
        measurement_results.append(measurement_result)
        
        if i % 10 == 0:  # Log progress every 10 iterations
            logger.info(f"  Completed {i}/{iterations} iterations")
    
    avg_time = total_time / iterations
    logger.info(f"  Average simulation time: {avg_time:.6f} seconds")
    
    # Use the quantum_ai_interface for analysis
    # Calculate measurement entropy across all results as an example
    entropies = [result.entropy() for result in measurement_results]
    avg_entropy = sum(entropies) / len(entropies)
    logger.info(f"  Average measurement entropy: {avg_entropy:.4f}")
    
    # Return the results in a JSON-serializable format
    results_summary = {}
    if measurement_results:
        sample_result = measurement_results[0]
        results_summary = {
            'counts': sample_result.counts,
            'metadata': sample_result.metadata.to_dict(),
            'uncertainty': sample_result.uncertainty.to_dict()
        }
    
    return {
        'operation': 'circuit_simulation',
        'qubits': qubits,
        'depth': depth,
        'iterations': iterations,
        'average_time': avg_time,
        'average_entropy': avg_entropy,
        'results_summary': results_summary
    }

def benchmark_all():
    """Run all benchmarks and collect results."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "machine_info": {
            "processor": os.uname().machine,
            "system": os.uname().sysname,
            "release": os.uname().release,
        },
        "dynamic_circuit": {},
        "circuit_simulation": {}
    }
    
    # Dynamic circuit benchmarks for different qubit counts
    for qubits in QUBIT_SIZES[:3]:  # Limit to 8 qubits to avoid excessive time
        logger.info(f"\n=== Benchmarking {qubits}-qubit Dynamic Circuit ===")
        refactor = DynamicCircuitRefactor(num_qubits=qubits)
        
        # Generation benchmark
        gen_time = benchmark_circuit_generation(refactor, BENCHMARK_ITERATIONS)
        results["dynamic_circuit"][f"{qubits}_qubits_generation"] = gen_time
        
        # Refactoring benchmark
        refactor_time = benchmark_circuit_refactoring(refactor, BENCHMARK_ITERATIONS)
        results["dynamic_circuit"][f"{qubits}_qubits_refactoring"] = refactor_time
    
    # Circuit simulation benchmarks
    for qubits in QUBIT_SIZES:
        logger.info(f"\n=== Benchmarking {qubits}-qubit Circuit Simulation ===")
        sim_time = benchmark_circuit_simulation(qubits, depth=3, iterations=BENCHMARK_ITERATIONS)
        results["circuit_simulation"][f"{qubits}_qubits"] = sim_time
    
    return results

def load_historical_results():
    """Load historical benchmark results if available."""
    if os.path.exists(HISTORICAL_RESULTS_FILE):
        try:
            with open(HISTORICAL_RESULTS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading historical results: {e}")
            return {}
    return {}

def save_results(results):
    """Save benchmark results."""
    # Load existing results if available
    historical = load_historical_results()
    
    # Add new results
    if "benchmarks" not in historical:
        historical["benchmarks"] = []
    
    historical["benchmarks"].append(results)
    
    # Save updated results
    with open(HISTORICAL_RESULTS_FILE, 'w') as f:
        json.dump(historical, f, indent=2)
    
    logger.info(f"Results saved to {HISTORICAL_RESULTS_FILE}")

def generate_comparison_report(current_results, historical_results):
    """Generate a report comparing current benchmark results with historical data."""
    report = []
    report.append("# Quantum Benchmark Report\n")
    
    # Add timestamp to the report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report.append(f"Timestamp: {timestamp}\n")
    
    # Add current results to the report
    report.append("## Current Results\n")
    
    # Process results based on how they were generated
    if isinstance(current_results, dict):
        # Check if results are directly formatted as execution times
        if all(isinstance(current_results[k], (int, float)) for k in current_results if k != 'memory'):
            # Results from a single operation with simple time values
            report.append("| Operation | Time (seconds) |")
            report.append("|-----------|----------------|")
            for op, time in current_results.items():
                if op != 'memory':  # Skip memory data in the timing table
                    report.append(f"| {op} | {time:.6f} |")
            
            # Add memory information if available
            if 'memory' in current_results:
                report.append("\n### Memory Usage\n")
                report.append("| Metric | Value |")
                report.append("|--------|-------|")
                report.append(f"| Peak Memory | {current_results['memory']['peak_mb']:.2f} MB |")
                report.append(f"| Average Memory | {current_results['memory']['avg_mb']:.2f} MB |")
        else:
            # Results from multiple operations or complex benchmarks
            report.append("| Operation | Details | Value |")
            report.append("|-----------|---------|-------|")
            
            for op, results in current_results.items():
                if op == 'timestamp' or op == 'memory':
                    continue  # Skip these special keys
                
                if isinstance(results, dict):
                    # Check if this is our new format with detailed metrics
                    if 'average_time' in results:
                        report.append(f"| {op} | Average Time | {results['average_time']:.6f} s |")
                        
                        if 'average_entropy' in results:
                            report.append(f"| {op} | Average Entropy | {float(results['average_entropy']):.4f} |")
                            
                        if 'qubits' in results:
                            report.append(f"| {op} | Qubits | {results['qubits']} |")
                            
                        if 'depth' in results:
                            report.append(f"| {op} | Circuit Depth | {results['depth']} |")
                    else:
                        # Older format with direct time values by qubit size
                        for size, time_value in results.items():
                            if size != 'memory' and not isinstance(time_value, dict):  
                                report.append(f"| {op} | {size} | {time_value:.6f} s |")
            
            # Add memory information if available
            has_memory = any('memory' in results for op, results in current_results.items() if op != 'timestamp')
            if has_memory:
                report.append("\n### Memory Usage\n")
                report.append("| Operation | Metric | Value |")
                report.append("|-----------|--------|-------|")
                for op, results in current_results.items():
                    if op != 'timestamp' and 'memory' in results:
                        mem_data = results['memory']
                        report.append(f"| {op} | Peak Memory | {mem_data['peak_mb']:.2f} MB |")
                        report.append(f"| {op} | Average Memory | {mem_data['avg_mb']:.2f} MB |")
    
    # Add comparison with historical data if available
    if historical_results:
        report.append("\n## Historical Comparison\n")
        report.append("| Metric | Current Value | Historical Best | Difference |")
        report.append("|--------|---------------|----------------|------------|")
        
        # We'll just compare the average time for now
        if 'circuit_simulation' in current_results:
            curr_result = current_results['circuit_simulation']
            
            # Handle the new result format
            if isinstance(curr_result, dict) and 'average_time' in curr_result:
                current_time = curr_result['average_time']
                
                # Find historical best if available
                historical_times = []
                
                for benchmark in historical_results.get('benchmarks', []):
                    if 'circuit_simulation' in benchmark:
                        if isinstance(benchmark['circuit_simulation'], dict) and 'average_time' in benchmark['circuit_simulation']:
                            historical_times.append(benchmark['circuit_simulation']['average_time'])
                        elif isinstance(benchmark['circuit_simulation'], (int, float)):
                            historical_times.append(benchmark['circuit_simulation'])
                
                if historical_times:
                    historical_best = min(historical_times)
                    diff_pct = (current_time - historical_best) / historical_best * 100
                    indicator = "🔴" if diff_pct > 5 else "🟢" if diff_pct < -5 else "🟡"
                    report.append(f"| Circuit Simulation Time | {current_time:.6f}s | {historical_best:.6f}s | {indicator} {diff_pct:.1f}% |")
                else:
                    report.append(f"| Circuit Simulation Time | {current_time:.6f}s | N/A | N/A |")
    
    # Join report lines and return as a string
    return "\n".join(report)

def plot_performance_trend(historical_results):
    """Generate performance trend plots based on historical data.
    
    This function handles missing data points in the historical results by:
    1. Tracking valid indices of data points for each metric separately
    2. Only plotting data points that exist (skipping benchmarks with missing data)
    3. Ensuring x and y arrays have matching dimensions before plotting
    4. Using separate tracking for different types of benchmarks (dynamic_circuit vs circuit_simulation)
    
    This approach ensures the visualization remains robust even when benchmark runs contain
    inconsistent or incomplete data, which is common in long-running benchmark processes.
    """
    if not historical_results or "benchmarks" not in historical_results or len(historical_results["benchmarks"]) < 2:
        logger.info("Insufficient historical data for trend analysis")
        return
    
    benchmarks = historical_results["benchmarks"]
    timestamps = [b.get("timestamp", "Unknown") for b in benchmarks]
    
    # Convert timestamps to datetime objects and then to simpler strings
    dates = []
    for ts in timestamps:
        try:
            dt = datetime.fromisoformat(ts)
            dates.append(dt.strftime("%m-%d %H:%M"))
        except:
            dates.append("Unknown")
    
    # Plot dynamic circuit performance
    plt.figure(figsize=(12, 8))
    
    # Extract data for dynamic circuit generation (4 qubits)
    key = "4_qubits_generation"
    values = []
    valid_indices = []  # Track indices of valid data points
    
    # Loop through benchmarks and collect only valid data points
    # This helps handle missing data by skipping benchmarks that don't have the required data
    for i, b in enumerate(benchmarks):
        if "dynamic_circuit" in b and key in b["dynamic_circuit"]:
            values.append(b["dynamic_circuit"][key])
            valid_indices.append(i)
    
    if values:
        # Use only the valid dates that correspond to our values
        # This ensures x and y arrays have matching dimensions for plotting
        valid_dates = [dates[i] for i in valid_indices]
        
        # Make sure we have at least 2 data points for plotting
        if len(valid_dates) >= 2 and len(values) >= 2:
            # Take at most the last 10 data points to avoid overcrowding
            plot_dates = valid_dates[-10:]
            plot_values = values[-10:]
            
            plt.subplot(2, 1, 1)
            plt.plot(plot_dates, plot_values, 'o-', label=f"Dynamic Circuit Generation (4 qubits)")
            plt.title("Dynamic Circuit Generation Performance Trend")
            plt.xlabel("Date")
            plt.ylabel("Average Time (seconds)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
        else:
            logger.info(f"Not enough data points for Dynamic Circuit Generation trend plot")
    
    # Extract data for circuit simulation (4 and 8 qubits)
    plt.subplot(2, 1, 2)
    has_data = False
    
    # Handle each qubit size separately to ensure proper data collection
    # when one size might be missing from some benchmark runs
    for qubits in [4, 8]:
        key = f"{qubits}_qubits"
        values = []
        valid_indices = []
        
        # Again, collect only valid data points for this specific metric
        for i, b in enumerate(benchmarks):
            if "circuit_simulation" in b and key in b["circuit_simulation"]:
                values.append(b["circuit_simulation"][key])
                valid_indices.append(i)
        
        if values and len(values) >= 2:
            # Use only the valid dates that correspond to our values
            # This ensures dimension matching between x and y arrays
            valid_dates = [dates[i] for i in valid_indices]
            
            # Take at most the last 10 data points
            plot_dates = valid_dates[-10:]
            plot_values = values[-10:]
            
            plt.plot(plot_dates, plot_values, 'o-', label=f"Circuit Simulation ({qubits} qubits)")
            has_data = True
        else:
            logger.info(f"Not enough data points for Circuit Simulation ({qubits} qubits) trend plot")
    
    if has_data:
        plt.title("Circuit Simulation Performance Trend")
        plt.xlabel("Date")
        plt.ylabel("Average Time (seconds)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
    else:
        logger.info("No data available for Circuit Simulation trend plot")
    
    plt.tight_layout()
    
    # Create the output directory if it doesn't exist
    output_dir = "benchmark_results/visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the plot with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"quantum_performance_trend_{timestamp}.png")
    plt.savefig(output_file)
    logger.info(f"Performance trend plot saved as {output_file}")

def profile_memory_usage(func, *args, **kwargs):
    """Profile memory usage of a function."""
    if not MEMORY_PROFILING_AVAILABLE:
        logger.warning("Memory profiling is not available. Install memory_profiler package.")
        return func(*args, **kwargs), None
    
    # Start tracemalloc for detailed memory allocation tracking
    tracemalloc.start()
    
    # Run the function with memory profiling by casting proc to Any
    proc: Any = (func, args, kwargs)  # type: ignore[var-annotated]
    mem_usage, result = memory_usage(
        proc,
        retval=True,
        max_usage=True
    )
    
    # Get peak memory allocation information
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    memory_info = {
        "peak_mb": peak / (1024 * 1024),  # Convert to MB
        "samples": mem_usage,
        "min_mb": min(mem_usage),
        "max_mb": max(mem_usage),
        "avg_mb": sum(mem_usage) / len(mem_usage)
    }
    
    return result, memory_info

def run_specific_benchmark(operation, qubits, repetitions, profile_memory=False):
    """Run a specific benchmark operation with the given parameters."""
    logger.info(f"Running {operation} benchmark with {qubits} qubits ({repetitions} repetitions)")
    
    # Create a circuit for the benchmark
    circuit = create_circuit(qubits)
    
    # Create a timestamp for this benchmark
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {}
    memory_profile = None
    
    if operation == 'circuit_simulation':
        if profile_memory:
            result, memory_profile = profile_memory_usage(
                benchmark_circuit_simulation, 
                qubits, 
                depth=3, 
                iterations=repetitions
            )
            # The result is already a properly formatted dictionary
            results[operation] = result
        else:
            # Call the benchmark function that returns a properly formatted dictionary
            results[operation] = benchmark_circuit_simulation(
                qubits, 
                depth=3, 
                iterations=repetitions
            )
    
    elif operation == 'circuit_refactoring':
        if profile_memory:
            result, memory_profile = profile_memory_usage(run_circuit_refactoring, circuit)
            execution_time = result
        else:
            execution_time = run_circuit_refactoring(circuit)
        results[operation] = execution_time
        
    elif operation == 'dynamic_circuit_generation':
        if profile_memory:
            result, memory_profile = profile_memory_usage(run_dynamic_circuit_generation, qubits)
            execution_time = result
        else:
            execution_time = run_dynamic_circuit_generation(qubits)
        results[operation] = execution_time
    
    elif operation == 'all':
        # Run all benchmarks
        for op in ['circuit_simulation', 'circuit_refactoring', 'dynamic_circuit_generation']:
            results[op] = run_specific_benchmark(op, qubits, repetitions, profile_memory)
    
    # Save memory profile if generated
    if memory_profile and operation != 'all':
        memory_profile_file = os.path.join(
            MEMORY_PROFILE_DIR, 
            f"memory_profile_{operation}_{qubits}qubits_{timestamp}.json"
        )
        with open(memory_profile_file, 'w') as f:
            json.dump(memory_profile, f, indent=2)
        logger.info(f"Memory profile saved to {memory_profile_file}")
        
        # Add memory information to results
        if isinstance(results, dict):
            results["memory"] = {
                "peak_mb": memory_profile["peak_mb"],
                "avg_mb": memory_profile["avg_mb"]
            }
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run quantum benchmarks")
    parser.add_argument("--operations", type=str, default="all", 
                        help="Operations to benchmark (comma-separated or 'all')")
    parser.add_argument("--qubit-count", type=int, default=8, 
                        help="Number of qubits to use for benchmarks")
    parser.add_argument("--repetitions", type=int, default=10, 
                        help="Number of repetitions for each benchmark")
    parser.add_argument("--scaling", action="store_true", 
                        help="Run scaling benchmarks across multiple qubit sizes")
    parser.add_argument("--memory-profile", action="store_true",
                       help="Enable memory profiling during benchmarks")
    parser.add_argument("--output-dir", type=str, default="benchmark_results", 
                        help="Directory to save benchmark results")
    
    args = parser.parse_args()
    
    # Check for memory profiling capability
    if args.memory_profile and not MEMORY_PROFILING_AVAILABLE:
        logger.error("Memory profiling requested but memory_profiler is not installed.")
        logger.error("Please install it with: pip install memory-profiler")
        sys.exit(1)
    
    # Run the specified benchmarks
    if args.operations.lower() == "all":
        operations = ["circuit_simulation", "circuit_refactoring", "dynamic_circuit_generation"]
    else:
        operations = [op.strip() for op in args.operations.split(",")]
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Check if scaling benchmark was requested
    if args.scaling:
        # Load config if available
        config_file = "benchmark_config.json"
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
                if "qubit_sizes" in config:
                    qubit_sizes = config["qubit_sizes"]
                else:
                    qubit_sizes = [4, 8, 16]
        else:
            qubit_sizes = [4, 8, 16]
            
        # Run benchmarks for multiple qubit sizes
        scaling_results = {}
        for op in operations:
            scaling_results[op] = {}
            for qsize in qubit_sizes:
                logger.info(f"Running scaling benchmark: {op} with {qsize} qubits")
                result = run_specific_benchmark(op, qsize, args.repetitions, args.memory_profile)
                if op != "all":
                    scaling_results[op][qsize] = result[op]
                    if args.memory_profile and "memory" in result:
                        if "memory" not in scaling_results[op]:
                            scaling_results[op]["memory"] = {}
                        scaling_results[op]["memory"][qsize] = result["memory"]
        
        # Save scaling results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"{args.output_dir}/scaling/native_{timestamp}.json"
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
        
        with open(result_file, "w") as f:
            json.dump(scaling_results, f, indent=2)
        logger.info(f"Scaling benchmark results saved to {result_file}")
    else:
        # Run standard benchmarks
        for op in operations:
            result = run_specific_benchmark(op, args.qubit_count, args.repetitions, args.memory_profile)
            logger.info(f"Benchmark results for {op}: {result}")
            
            # Save the result
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = f"{args.output_dir}/benchmark_results_{timestamp}.json"
            
            # Make sure we have results to save
            if op != "all":
                results_to_save = {op: result[op]}
                if args.memory_profile and "memory" in result:
                    results_to_save["memory"] = result["memory"]
            else:
                results_to_save = result
                
            with open(result_file, "w") as f:
                json.dump(results_to_save, f, indent=2)
            logger.info(f"Benchmark results saved to {result_file}")
        
        # Generate report
        report = generate_comparison_report(result, load_historical_results())
        print(report)
        
        # Save report to file
        with open("quantum_benchmark_report.txt", "w") as f:
            f.write(report)
        logger.info("Benchmark report saved to quantum_benchmark_report.txt")
        
        # Generate performance trend plot
        if VISUALIZATION_AVAILABLE:
            plot_performance_trend(load_historical_results())
        
        logger.info("Benchmark completed successfully!") 