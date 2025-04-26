#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quantum Financial Benchmark Framework

This module provides a comprehensive framework for benchmarking quantum financial algorithms,
measuring performance metrics for both classical and quantum implementations, and generating
standardized reports following project guidelines.

Author: Quantum Financial System Team
Date: March 11, 2025
"""

# --- SHOWCASE BENCHMARK SCRIPT ---
# This script (quantum_financial_benchmark.py) is the recommended entry point for publication-quality, production-ready benchmarking.
# All algorithms must use real data/APIs (no mocks or placeholders). Plug in your actual quantum/classical/hybrid algorithms.
# See docs/benchmarking_showcase.md for usage instructions and requirements.
# --------------------------------

import os
import json
import time
import logging
import argparse
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

# Import quantum modules
try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    from qiskit.visualization import plot_histogram
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    logging.warning("Qiskit not available, some benchmarks will be skipped")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quantum_financial_benchmark")

# Constants
DEFAULT_OUTPUT_DIR = "benchmark_results"
DEFAULT_REPORT_DIR = "benchmark_reports"
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

class SystemInfoCollector:
    """Collects and reports system hardware and software information."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Collect system information for benchmark documentation."""
        system_info = {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        # Add CPU information if available
        try:
            import psutil
            system_info["cpu_count_physical"] = psutil.cpu_count(logical=False)
            system_info["cpu_count_logical"] = psutil.cpu_count(logical=True)
            system_info["memory_total_gb"] = round(psutil.virtual_memory().total / (1024**3), 2)
        except ImportError:
            system_info["cpu_count_physical"] = os.cpu_count()
            system_info["cpu_count_logical"] = os.cpu_count()
        
        # Add Qiskit version if available
        if QISKIT_AVAILABLE:
            try:
                import qiskit
                system_info["qiskit_version"] = qiskit.__version__
            except (ImportError, AttributeError):
                system_info["qiskit_version"] = "Unknown"
        
        return system_info


class BenchmarkMetricsCollector:
    """Collects and records benchmark metrics."""
    
    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR):
        """Initialize the benchmark metrics collector.
        
        Args:
            output_dir: Directory to store benchmark results
        """
        self.output_dir = os.path.join(output_dir, f"run_{datetime.now().strftime(TIMESTAMP_FORMAT)}")
        os.makedirs(self.output_dir, exist_ok=True)
        self.metrics = {}
        self.system_info = SystemInfoCollector.get_system_info()
        
    def start_timer(self) -> float:
        """Start a timer for benchmarking.
        
        Returns:
            Current time in seconds
        """
        return time.time()
    
    def stop_timer(self, start_time: float) -> float:
        """Stop the timer and return elapsed time.
        
        Args:
            start_time: Time when the timer was started
            
        Returns:
            Elapsed time in seconds
        """
        return time.time() - start_time
    
    def record_metric(self, category: str, metric_name: str, value: Union[float, int, List, Dict]) -> None:
        """Record a benchmark metric.
        
        Args:
            category: Category of the metric (e.g., 'circuit_execution', 'memory_usage')
            metric_name: Name of the metric
            value: Value of the metric
        """
        if category not in self.metrics:
            self.metrics[category] = {}
        
        self.metrics[category][metric_name] = value
        
    def record_quantum_metrics(self, circuit: 'QuantumCircuit', execution_time: float) -> None:
        """Record quantum-specific metrics for a circuit.
        
        Args:
            circuit: Quantum circuit that was executed
            execution_time: Time taken to execute the circuit
        """
        if not QISKIT_AVAILABLE:
            logger.warning("Qiskit not available, skipping quantum metrics")
            return
        
        quantum_metrics = {
            "num_qubits": circuit.num_qubits,
            "depth": circuit.depth(),
            "gate_counts": circuit.count_ops(),
            "execution_time": execution_time
        }
        
        # Transpile the circuit to get more accurate gate counts
        try:
            backend = AerSimulator()
            transpiled = transpile(circuit, backend)
            quantum_metrics["transpiled_depth"] = transpiled.depth()
            quantum_metrics["transpiled_gate_counts"] = transpiled.count_ops()
        except Exception as e:
            logger.error(f"Error transpiling circuit: {e}")
        
        self.record_metric("quantum_metrics", f"circuit_{circuit.num_qubits}q", quantum_metrics)
    
    def save_results(self, filename_prefix: str = "benchmark") -> str:
        """Save benchmark results to a JSON file.
        
        Args:
            filename_prefix: Prefix for the output filename
            
        Returns:
            Path to the saved file
        """
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        full_results = {
            "system_info": self.system_info,
            "metrics": self.metrics,
            "timestamp": timestamp
        }
        
        output_file = os.path.join(self.output_dir, f"{filename_prefix}_{timestamp}.json")
        with open(output_file, 'w') as f:
            json.dump(full_results, f, indent=2)
        
        logger.info(f"Benchmark results saved to {output_file}")
        return output_file
    
    def compare_with_previous(self, previous_results_file: str) -> Dict[str, Any]:
        """Compare current results with previous benchmark results.
        
        Args:
            previous_results_file: Path to previous benchmark results
            
        Returns:
            Dictionary with comparison metrics
        """
        try:
            with open(previous_results_file, 'r') as f:
                previous_results = json.load(f)
            
            comparison = {"timestamp": datetime.now().strftime(TIMESTAMP_FORMAT)}
            
            # Compare metrics
            for category in self.metrics:
                if category in previous_results["metrics"]:
                    comparison[category] = {}
                    for metric_name in self.metrics[category]:
                        if metric_name in previous_results["metrics"][category]:
                            current = self.metrics[category][metric_name]
                            previous = previous_results["metrics"][category][metric_name]
                            
                            # Handle different types of metrics
                            if isinstance(current, (int, float)) and isinstance(previous, (int, float)):
                                change = ((current - previous) / previous) * 100
                                comparison[category][metric_name] = {
                                    "current": current,
                                    "previous": previous,
                                    "change_percent": round(change, 2)
                                }
            
            return comparison
        except Exception as e:
            logger.error(f"Error comparing with previous results: {e}")
            return {"error": str(e)}


class QuantumFinancialBenchmark:
    """Main benchmark class for quantum financial algorithms."""
    
    def __init__(self, 
                 output_dir: str = DEFAULT_OUTPUT_DIR,
                 report_dir: str = DEFAULT_REPORT_DIR):
        """Initialize the quantum financial benchmark.
        
        Args:
            output_dir: Directory to store benchmark results
            report_dir: Directory to store benchmark reports
        """
        self.metrics = BenchmarkMetricsCollector(output_dir)
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
        
        # Store historical benchmarks
        self.history_file = os.path.join(output_dir, "benchmark_history.json")
        self.load_benchmark_history()
    
    def load_benchmark_history(self) -> None:
        """Load benchmark history from file or initialize if not exists."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Could not decode {self.history_file}, initializing new history")
                self.history = {"benchmarks": []}
        else:
            self.history = {"benchmarks": []}
    
    def update_benchmark_history(self, result_file: str) -> None:
        """Update benchmark history with a new benchmark result.
        
        Args:
            result_file: Path to benchmark result file
        """
        try:
            with open(result_file, 'r') as f:
                result = json.load(f)
            
            # Add summary to history
            entry = {
                "timestamp": result["timestamp"],
                "file": result_file,
                "system": result["system_info"],
            }
            
            # Add summary metrics
            entry["summary"] = {}
            for category, metrics in result["metrics"].items():
                entry["summary"][category] = {
                    "metric_count": len(metrics),
                    "metric_names": list(metrics.keys())
                }
            
            self.history["benchmarks"].append(entry)
            
            # Save updated history
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
                
            logger.info(f"Benchmark history updated with {result_file}")
        except Exception as e:
            logger.error(f"Error updating benchmark history: {e}")
    
    def benchmark_classical_algorithm(self, 
                                     algorithm_func, 
                                     input_data: Any, 
                                     name: str, 
                                     iterations: int = 5) -> Dict[str, float]:
        """Benchmark a classical financial algorithm.
        
        Args:
            algorithm_func: Function implementing the algorithm to benchmark
            input_data: Input data for the algorithm
            name: Name of the algorithm
            iterations: Number of iterations to run
            
        Returns:
            Dictionary with benchmark results
        """
        logger.info(f"Benchmarking classical algorithm: {name}")
        
        # Track memory usage if psutil is available
        try:
            import psutil
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        except ImportError:
            initial_memory = None
        
        # Run warm-up iteration
        algorithm_func(input_data)
        
        # Run benchmark iterations
        execution_times = []
        for i in range(iterations):
            start_time = self.metrics.start_timer()
            result = algorithm_func(input_data)
            execution_time = self.metrics.stop_timer(start_time)
            execution_times.append(execution_time)
            logger.debug(f"Iteration {i+1}/{iterations}: {execution_time:.4f} seconds")
        
        # Calculate statistics
        mean_time = np.mean(execution_times)
        std_dev = np.std(execution_times)
        min_time = np.min(execution_times)
        max_time = np.max(execution_times)
        
        # Record memory usage if available
        if initial_memory is not None:
            final_memory = process.memory_info().rss / (1024 * 1024)  # MB
            memory_diff = final_memory - initial_memory
            self.metrics.record_metric("memory_usage", f"{name}_memory_mb", memory_diff)
        
        # Record metrics
        benchmark_result = {
            "mean_time": mean_time,
            "std_dev": std_dev,
            "min_time": min_time,
            "max_time": max_time,
            "iterations": iterations
        }
        
        self.metrics.record_metric("classical_performance", name, benchmark_result)
        logger.info(f"Classical algorithm {name} benchmark complete: {mean_time:.4f} sec (±{std_dev:.4f})")
        
        return benchmark_result
    
    def benchmark_quantum_algorithm(self, 
                                   circuit_generator_func, 
                                   input_data: Any,
                                   name: str,
                                   shots: int = 1024,
                                   iterations: int = 3) -> Dict[str, Any]:
        """Benchmark a quantum financial algorithm.
        
        Args:
            circuit_generator_func: Function that generates a quantum circuit
            input_data: Input data for the algorithm
            name: Name of the algorithm
            shots: Number of shots for the quantum simulation
            iterations: Number of iterations to run
            
        Returns:
            Dictionary with benchmark results
        """
        if not QISKIT_AVAILABLE:
            logger.error("Qiskit not available, cannot benchmark quantum algorithm")
            return {"error": "Qiskit not available"}
        
        logger.info(f"Benchmarking quantum algorithm: {name} with {shots} shots")
        
        # Track memory usage if psutil is available
        try:
            import psutil
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        except ImportError:
            initial_memory = None
        
        # Initialize Aer simulator
        simulator = AerSimulator()
        
        # Benchmark circuit generation
        start_time = self.metrics.start_timer()
        circuit = circuit_generator_func(input_data)
        circuit_generation_time = self.metrics.stop_timer(start_time)
        
        self.metrics.record_metric("quantum_circuit_generation", name, {
            "generation_time": circuit_generation_time,
            "num_qubits": circuit.num_qubits,
            "depth": circuit.depth()
        })
        
        # Benchmark transpilation
        start_time = self.metrics.start_timer()
        transpiled_circuit = transpile(circuit, simulator)
        transpilation_time = self.metrics.stop_timer(start_time)
        
        self.metrics.record_metric("quantum_transpilation", name, {
            "transpilation_time": transpilation_time,
            "depth_before": circuit.depth(),
            "depth_after": transpiled_circuit.depth(),
            "gates_before": circuit.count_ops(),
            "gates_after": transpiled_circuit.count_ops()
        })
        
        # Run benchmark iterations for simulation
        execution_times = []
        for i in range(iterations):
            start_time = self.metrics.start_timer()
            job = simulator.run(transpiled_circuit, shots=shots)
            result = job.result()
            execution_time = self.metrics.stop_timer(start_time)
            execution_times.append(execution_time)
            logger.debug(f"Iteration {i+1}/{iterations}: {execution_time:.4f} seconds")
        
        # Calculate statistics
        mean_time = np.mean(execution_times)
        std_dev = np.std(execution_times)
        min_time = np.min(execution_times)
        max_time = np.max(execution_times)
        
        # Record memory usage if available
        if initial_memory is not None:
            final_memory = process.memory_info().rss / (1024 * 1024)  # MB
            memory_diff = final_memory - initial_memory
            self.metrics.record_metric("memory_usage", f"{name}_memory_mb", memory_diff)
        
        # Record quantum metrics
        self.metrics.record_quantum_metrics(circuit, mean_time)
        
        # Record simulation metrics
        benchmark_result = {
            "mean_time": mean_time,
            "std_dev": std_dev,
            "min_time": min_time,
            "max_time": max_time,
            "iterations": iterations,
            "shots": shots,
            "circuit_generation_time": circuit_generation_time,
            "transpilation_time": transpilation_time
        }
        
        self.metrics.record_metric("quantum_performance", name, benchmark_result)
        logger.info(f"Quantum algorithm {name} benchmark complete: {mean_time:.4f} sec (±{std_dev:.4f})")
        
        return benchmark_result
    
    def benchmark_hybrid_algorithm(self,
                                  classical_func,
                                  quantum_circuit_generator_func,
                                  input_data: Any,
                                  name: str,
                                  shots: int = 1024,
                                  iterations: int = 3) -> Dict[str, Any]:
        """Benchmark a hybrid classical-quantum financial algorithm.
        
        Args:
            classical_func: Classical processing function
            quantum_circuit_generator_func: Function that generates a quantum circuit
            input_data: Input data for the algorithm
            name: Name of the algorithm
            shots: Number of shots for the quantum simulation
            iterations: Number of iterations to run
            
        Returns:
            Dictionary with benchmark results
        """
        logger.info(f"Benchmarking hybrid algorithm: {name}")
        
        # Benchmark classical part
        classical_start = self.metrics.start_timer()
        classical_result = classical_func(input_data)
        classical_time = self.metrics.stop_timer(classical_start)
        
        # Benchmark quantum part if available
        if QISKIT_AVAILABLE:
            quantum_result = self.benchmark_quantum_algorithm(
                quantum_circuit_generator_func,
                classical_result,  # Use classical result as input to quantum part
                f"{name}_quantum",
                shots,
                iterations
            )
            quantum_time = quantum_result["mean_time"]
        else:
            quantum_time = 0
            quantum_result = {"error": "Qiskit not available"}
        
        # Record hybrid metrics
        total_time = classical_time + quantum_time
        hybrid_result = {
            "total_time": total_time,
            "classical_time": classical_time,
            "quantum_time": quantum_time,
            "classical_percentage": (classical_time / total_time) * 100 if total_time > 0 else 0,
            "quantum_percentage": (quantum_time / total_time) * 100 if total_time > 0 else 0,
            "iterations": iterations
        }
        
        self.metrics.record_metric("hybrid_performance", name, hybrid_result)
        logger.info(f"Hybrid algorithm {name} benchmark complete: {total_time:.4f} sec "
                   f"(Classical: {classical_time:.4f} sec, Quantum: {quantum_time:.4f} sec)")
        
        return hybrid_result
    
    def generate_visualizations(self, output_file: str) -> List[str]:
        """Generate visualizations from benchmark results.
        
        Args:
            output_file: Path to benchmark results file
            
        Returns:
            List of paths to generated visualization files
        """
        with open(output_file, 'r') as f:
            results = json.load(f)
        
        visualization_files = []
        timestamp = results["timestamp"]
        
        # Create output directory for visualizations
        vis_dir = os.path.join(os.path.dirname(output_file), "visualizations")
        os.makedirs(vis_dir, exist_ok=True)
        
        # Generate performance comparison visualization if we have both classical and quantum metrics
        if "classical_performance" in results["metrics"] and "quantum_performance" in results["metrics"]:
            classical_data = results["metrics"]["classical_performance"]
            quantum_data = results["metrics"]["quantum_performance"]
            
            # Extract algorithm names and execution times
            names = []
            classical_times = []
            quantum_times = []
            
            for name, data in classical_data.items():
                quantum_name = f"{name}_quantum"
                if quantum_name in quantum_data:
                    names.append(name)
                    classical_times.append(data["mean_time"])
                    quantum_times.append(quantum_data[quantum_name]["mean_time"])
            
            if names:
                plt.figure(figsize=(12, 8))
                x = np.arange(len(names))
                width = 0.35
                
                plt.bar(x - width/2, classical_times, width, label='Classical Implementation')
                plt.bar(x + width/2, quantum_times, width, label='Quantum Implementation')
                
                plt.xlabel('Algorithm')
                plt.ylabel('Execution Time (seconds)')
                plt.title('Classical vs Quantum Performance Comparison')
                plt.xticks(x, names, rotation=45, ha='right')
                plt.legend()
                plt.tight_layout()
                
                vis_file = os.path.join(vis_dir, f"classical_vs_quantum_{timestamp}.png")
                plt.savefig(vis_file)
                plt.close()
                visualization_files.append(vis_file)
                logger.info(f"Created classical vs quantum comparison visualization: {vis_file}")
        
        # Generate quantum circuit metrics visualization
        if "quantum_metrics" in results["metrics"]:
            quantum_metrics = results["metrics"]["quantum_metrics"]
            
            qubits = []
            depths = []
            exec_times = []
            
            for name, data in quantum_metrics.items():
                if name.startswith("circuit_") and "q" in name:
                    qubits.append(int(name.split("_")[1].replace("q", "")))
                    depths.append(data["depth"])
                    exec_times.append(data["execution_time"])
            
            if qubits:
                fig, ax1 = plt.subplots(figsize=(12, 8))
                
                color = 'tab:blue'
                ax1.set_xlabel('Number of Qubits')
                ax1.set_ylabel('Circuit Depth', color=color)
                ax1.plot(qubits, depths, 'o-', color=color)
                ax1.tick_params(axis='y', labelcolor=color)
                
                ax2 = ax1.twinx()
                color = 'tab:red'
                ax2.set_ylabel('Execution Time (seconds)', color=color)
                ax2.plot(qubits, exec_times, 's-', color=color)
                ax2.tick_params(axis='y', labelcolor=color)
                
                plt.title('Quantum Circuit Complexity vs Execution Time')
                fig.tight_layout()
                
                vis_file = os.path.join(vis_dir, f"quantum_scaling_{timestamp}.png")
                plt.savefig(vis_file)
                plt.close()
                visualization_files.append(vis_file)
                logger.info(f"Created quantum scaling visualization: {vis_file}")
        
        return visualization_files
    
    def generate_report(self, 
                       benchmark_file: str, 
                       visualizations: List[str],
                       compare_with: Optional[str] = None) -> str:
        """Generate a comprehensive benchmark report.
        
        Args:
            benchmark_file: Path to benchmark results file
            visualizations: List of paths to visualization files
            compare_with: Path to previous benchmark results file for comparison
            
        Returns:
            Path to the generated report
        """
        with open(benchmark_file, 'r') as f:
            results = json.load(f)
        
        timestamp = results["timestamp"]
        system_info = results["system_info"]
        
        # Load comparison data if provided
        comparison = None
        if compare_with and os.path.exists(compare_with):
            comparison = self.metrics.compare_with_previous(compare_with)
        
        # Create report
        report_lines = [
            "# Quantum Financial System Benchmark Report",
            "",
            f"## Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## System Information",
            f"- Platform: {system_info['platform']}",
            f"- Processor: {system_info['processor']}",
            f"- CPU Count: {system_info['cpu_count_logical']} logical, {system_info['cpu_count_physical']} physical",
            f"- Memory: {system_info.get('memory_total_gb', 'Unknown')} GB",
            f"- Python Version: {system_info['python_version']}",
        ]
        
        if "qiskit_version" in system_info:
            report_lines.append(f"- Qiskit Version: {system_info['qiskit_version']}")
        
        report_lines.extend(["", "## Performance Metrics", ""])
        
        # Add classical algorithm metrics
        if "classical_performance" in results["metrics"]:
            report_lines.append("### Classical Algorithms")
            for name, data in results["metrics"]["classical_performance"].items():
                report_lines.append(f"- **{name}**:")
                report_lines.append(f"  - Execution Time: {data['mean_time']:.4f} seconds (±{data['std_dev']:.4f})")
                if "memory_usage" in results["metrics"] and f"{name}_memory_mb" in results["metrics"]["memory_usage"]:
                    memory = results["metrics"]["memory_usage"][f"{name}_memory_mb"]
                    report_lines.append(f"  - Memory Usage: {memory:.2f} MB")
            report_lines.append("")
        
        # Add quantum algorithm metrics
        if "quantum_performance" in results["metrics"]:
            report_lines.append("### Quantum Algorithms")
            for name, data in results["metrics"]["quantum_performance"].items():
                report_lines.append(f"- **{name}**:")
                report_lines.append(f"  - Execution Time: {data['mean_time']:.4f} seconds (±{data['std_dev']:.4f})")
                report_lines.append(f"  - Circuit Generation Time: {data['circuit_generation_time']:.4f} seconds")
                report_lines.append(f"  - Transpilation Time: {data['transpilation_time']:.4f} seconds")
                if "memory_usage" in results["metrics"] and f"{name}_memory_mb" in results["metrics"]["memory_usage"]:
                    memory = results["metrics"]["memory_usage"][f"{name}_memory_mb"]
                    report_lines.append(f"  - Memory Usage: {memory:.2f} MB")
            report_lines.append("")
        
        # Add hybrid algorithm metrics
        if "hybrid_performance" in results["metrics"]:
            report_lines.append("### Hybrid Algorithms")
            for name, data in results["metrics"]["hybrid_performance"].items():
                report_lines.append(f"- **{name}**:")
                report_lines.append(f"  - Total Execution Time: {data['total_time']:.4f} seconds")
                report_lines.append(f"  - Classical Time: {data['classical_time']:.4f} seconds ({data['classical_percentage']:.1f}%)")
                report_lines.append(f"  - Quantum Time: {data['quantum_time']:.4f} seconds ({data['quantum_percentage']:.1f}%)")
            report_lines.append("")
        
        # Add circuit metrics
        if "quantum_metrics" in results["metrics"]:
            report_lines.append("### Quantum Circuit Metrics")
            for name, data in results["metrics"]["quantum_metrics"].items():
                report_lines.append(f"- **{name}**:")
                report_lines.append(f"  - Qubits: {data['num_qubits']}")
                report_lines.append(f"  - Depth: {data['depth']}")
                report_lines.append(f"  - Gate Counts: {data['gate_counts']}")
                if "transpiled_depth" in data:
                    report_lines.append(f"  - Transpiled Depth: {data['transpiled_depth']}")
                    report_lines.append(f"  - Transpiled Gate Counts: {data['transpiled_gate_counts']}")
            report_lines.append("")
        
        # Add comparison metrics if available
        if comparison and "error" not in comparison:
            report_lines.extend(["## Performance Comparison with Previous Benchmark", ""])
            
            for category, metrics in comparison.items():
                if category not in ["timestamp", "error"]:
                    report_lines.append(f"### {category.replace('_', ' ').title()}")
                    for metric_name, data in metrics.items():
                        report_lines.append(f"- **{metric_name}**:")
                        report_lines.append(f"  - Current: {data['current']:.4f}")
                        report_lines.append(f"  - Previous: {data['previous']:.4f}")
                        change = data['change_percent']
                        direction = "improvement" if change < 0 else "regression"
                        report_lines.append(f"  - Change: {abs(change):.2f}% {direction}")
                    report_lines.append("")
        
        # Add visualizations
        if visualizations:
            report_lines.extend(["## Visualizations", ""])
            for i, vis_file in enumerate(visualizations):
                rel_path = os.path.relpath(vis_file, self.report_dir)
                report_lines.append(f"### Visualization {i+1}")
                report_lines.append(f"![{os.path.basename(vis_file)}]({rel_path})")
                report_lines.append("")
        
        # Add recommendations section
        report_lines.extend([
            "## Recommendations",
            "",
            "Based on the benchmark results, consider the following recommendations:",
            "",
        ])
        
        # Add automatic recommendations based on results
        recommendations = []
        
        # Look for slow quantum algorithms
        if "quantum_performance" in results["metrics"] and "classical_performance" in results["metrics"]:
            for q_name, q_data in results["metrics"]["quantum_performance"].items():
                c_name = q_name.replace("_quantum", "")
                if c_name in results["metrics"]["classical_performance"]:
                    c_data = results["metrics"]["classical_performance"][c_name]
                    ratio = q_data["mean_time"] / c_data["mean_time"]
                    if ratio > 5:
                        recommendations.append(
                            f"Optimize the quantum implementation of {c_name} which is {ratio:.1f}x slower than its classical counterpart."
                        )
        
        # Look for high transpilation overhead
        if "quantum_transpilation" in results["metrics"]:
            for name, data in results["metrics"]["quantum_transpilation"].items():
                if data["transpilation_time"] > 0.5:  # Arbitrary threshold
                    recommendations.append(
                        f"Consider optimizing the transpilation process for {name} which takes {data['transpilation_time']:.4f} seconds."
                    )
        
        # Add general recommendations if no specific ones were found
        if not recommendations:
            recommendations = [
                "Continue regular benchmarking to track performance changes over time.",
                "Consider implementing more quantum financial algorithms to compare with classical counterparts.",
                "Explore optimized transpilation options for the quantum circuits to reduce execution time.",
                "Monitor memory usage for large-scale simulations to prevent performance issues."
            ]
        
        # Add recommendations to report
        for i, rec in enumerate(recommendations):
            report_lines.append(f"{i+1}. {rec}")
        
        report_lines.extend([
            "",
            "## Next Steps",
            "",
            "- Update the benchmark suite with additional quantum financial algorithms",
            "- Implement performance regression testing in CI/CD pipeline",
            "- Compare containerized versus native performance",
            "- Extend benchmarks to include real quantum hardware when available",
            "",
            f"This report was automatically generated from benchmark data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        ])
        
        # Save report
        report_file = os.path.join(self.report_dir, f"quantum_financial_benchmark_{timestamp}.md")
        with open(report_file, 'w') as f:
            f.write("\n".join(report_lines))
        
        logger.info(f"Benchmark report generated: {report_file}")
        return report_file


def main():
    """Main function to run benchmarks from command line."""
    parser = argparse.ArgumentParser(description="Quantum Financial Benchmark Framework")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Directory to store benchmark results")
    parser.add_argument("--report-dir", default=DEFAULT_REPORT_DIR, help="Directory to store benchmark reports")
    parser.add_argument("--compare-with", help="Previous benchmark file to compare with")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info("Starting Quantum Financial Benchmark")
    
    # Initialize benchmark framework
    benchmark = QuantumFinancialBenchmark(args.output_dir, args.report_dir)
    
    # Sample benchmark functions - these would be replaced with actual implementations
    def sample_classical_algorithm(data):
        # Simulate a classical financial calculation
        time.sleep(0.1)  # Simulating computation
        return data * 2
    
    def sample_quantum_circuit_generator(data):
        # Create a simple quantum circuit based on input data
        if not QISKIT_AVAILABLE:
            return None
        
        num_qubits = 4
        circuit = QuantumCircuit(num_qubits)
        
        # Apply gates based on data
        for i in range(num_qubits):
            circuit.h(i)
        
        for i in range(num_qubits-1):
            circuit.cx(i, i+1)
        
        # Measure all qubits
        circuit.measure_all()
        
        return circuit
    
    # Run benchmarks
    sample_data = 42
    benchmark.benchmark_classical_algorithm(sample_classical_algorithm, sample_data, "sample_financial_calculation")
    
    if QISKIT_AVAILABLE:
        benchmark.benchmark_quantum_algorithm(sample_quantum_circuit_generator, sample_data, "quantum_calculation")
        benchmark.benchmark_hybrid_algorithm(
            sample_classical_algorithm,
            sample_quantum_circuit_generator,
            sample_data,
            "hybrid_financial_calculation"
        )
    
    # Save results
    result_file = benchmark.metrics.save_results("quantum_financial_benchmark")
    
    # Update benchmark history
    benchmark.update_benchmark_history(result_file)
    
    # Generate visualizations
    visualizations = benchmark.generate_visualizations(result_file)
    
    # Generate report
    report_file = benchmark.generate_report(result_file, visualizations, args.compare_with)
    
    logger.info(f"Benchmark complete. Report available at: {report_file}")


if __name__ == "__main__":
    main() 