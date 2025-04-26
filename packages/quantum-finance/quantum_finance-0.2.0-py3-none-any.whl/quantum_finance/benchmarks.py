import time
import json
import os
import datetime
from dynamic_circuit_refactoring import DynamicCircuitRefactor

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BENCHMARK_ITERATIONS = 100
QUBIT_SIZES = [2, 4, 8]
HISTORICAL_RESULTS_FILE = 'benchmark_results.json'


def benchmark_generate(refactor, iterations=100):
    """Benchmark the dynamic circuit generation."""
    start = time.perf_counter()
    for _ in range(iterations):
        circuit = refactor.generate_dynamic_circuit()
    end = time.perf_counter()
    duration = end - start
    avg_time = duration/iterations
    logger.info(f"Generated {iterations} circuits in {duration:.4f} seconds, average = {avg_time:.6f} sec/circuit.")
    return avg_time


def benchmark_refactor(refactor, iterations=100):
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


def benchmark_all():
    """Run all benchmarks and collect results."""
    results = {
        "timestamp": datetime.datetime.now().isoformat(),
        "machine_info": {
            "processor": os.uname().machine,
            "system": os.uname().sysname,
            "release": os.uname().release,
        },
        "dynamic_circuit": {}
    }
    
    # Dynamic circuit benchmarks for different qubit counts
    for qubits in QUBIT_SIZES:
        logger.info(f"\n=== Benchmarking {qubits}-qubit Dynamic Circuit ===")
        refactor = DynamicCircuitRefactor(num_qubits=qubits)
        
        # Generation benchmark
        gen_time = benchmark_generate(refactor, BENCHMARK_ITERATIONS)
        results["dynamic_circuit"][f"{qubits}_qubits_generation"] = gen_time
        
        # Refactoring benchmark
        refactor_time = benchmark_refactor(refactor, BENCHMARK_ITERATIONS)
        results["dynamic_circuit"][f"{qubits}_qubits_refactoring"] = refactor_time
    
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
    # Create a new results entry
    new_entry = {
        "timestamp": results["timestamp"],
        "machine_info": results["machine_info"],
        "dynamic_circuit": results["dynamic_circuit"]
    }
    
    # Try to append to existing results
    try:
        with open(HISTORICAL_RESULTS_FILE, 'r') as f:
            historical = json.load(f)
            
        if "benchmarks" not in historical:
            historical["benchmarks"] = []
            
        historical["benchmarks"].append(new_entry)
    except (FileNotFoundError, json.JSONDecodeError):
        # Create new file if it doesn't exist or is corrupted
        historical = {
            "benchmarks": [new_entry]
        }
    
    # Save updated results
    with open(HISTORICAL_RESULTS_FILE, 'w') as f:
        json.dump(historical, f, indent=2)
    
    logger.info(f"Results saved to {HISTORICAL_RESULTS_FILE}")


def generate_comparison_report(current_results, historical_results):
    """Generate a comparison report between current and historical results."""
    report = []
    report.append("\n" + "="*80)
    report.append("QUANTUM SIMULATION PERFORMANCE BENCHMARK REPORT")
    report.append("="*80)
    
    # Format current results
    report.append("\nCURRENT BENCHMARK RESULTS:")
    report.append(f"Timestamp: {current_results['timestamp']}")
    report.append(f"System: {current_results['machine_info']['system']} {current_results['machine_info']['release']} ({current_results['machine_info']['processor']})")
    
    # Dynamic circuit results
    report.append("\nDynamic Circuit Performance:")
    for key, value in current_results['dynamic_circuit'].items():
        report.append(f"  {key}: {value:.6f} seconds")
    
    # Historical comparison if available
    if historical_results and "benchmarks" in historical_results and len(historical_results["benchmarks"]) > 1:
        report.append("\n" + "-"*80)
        report.append("COMPARISON WITH PREVIOUS BENCHMARKS:")
        
        # Get previous benchmark results (excluding the current one)
        prev_results = historical_results["benchmarks"][-2]
        
        # Compare dynamic circuit performance
        report.append("\nDynamic Circuit Performance Changes:")
        for key in current_results['dynamic_circuit']:
            if key in prev_results.get('dynamic_circuit', {}):
                current = current_results['dynamic_circuit'][key]
                previous = prev_results['dynamic_circuit'][key]
                change_pct = ((current - previous) / previous) * 100
                improvement = "improvement" if change_pct < 0 else "slowdown"
                report.append(f"  {key}: {abs(change_pct):.2f}% {improvement} " + 
                             f"({previous:.6f}s → {current:.6f}s)")
    
    report.append("\n" + "="*80)
    
    return "\n".join(report)


if __name__ == "__main__":
    logger.info("Starting quantum simulation benchmarks...")
    
    # Run all benchmarks
    current_results = benchmark_all()
    
    # Load historical results
    historical_results = load_historical_results()
    
    # Save current results
    save_results(current_results)
    
    # Generate comparison report
    report = generate_comparison_report(current_results, historical_results)
    print(report)
    
    # Save report to file
    with open("quantum_benchmark_report.txt", "w") as f:
        f.write(report)
    logger.info("Benchmark report saved to quantum_benchmark_report.txt")
    
    logger.info("Benchmark completed successfully!") 