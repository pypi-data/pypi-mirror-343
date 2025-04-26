#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quantum Financial Benchmark - Risk Assessment Module

This module extends the main benchmark framework to specifically benchmark
quantum risk assessment algorithms for financial applications.

Author: Quantum Financial System Team
Date: March 11, 2025
"""

import os
import sys
import json
import time
import logging
import argparse
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

# Import the main benchmark framework
try:
    from quantum_financial_benchmark import (
        QuantumFinancialBenchmark,
        BenchmarkMetricsCollector,
        DEFAULT_OUTPUT_DIR,
        DEFAULT_REPORT_DIR,
    )
except ImportError:
    print("Error: quantum_financial_benchmark.py must be in the same directory")
    sys.exit(1)

# Import quantum modules
try:
    from qiskit.circuit import QuantumCircuit  # Core circuit class
    from qiskit import transpile  # Qiskit transpiler for circuit optimization
    from qiskit_aer import AerSimulator  # AerSimulator backend for local simulations
    # Removed IBMProvider import: using QiskitRuntimeService for IBM Quantum
    from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, SamplerV2 as RuntimeSampler  # IBM Quantum runtime primitives
    from qiskit.circuit.library import QFT  # Quantum Fourier Transform library circuit
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    logging.warning("Qiskit not available, some benchmarks will be skipped")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quantum_financial_benchmark_risk")

class RiskMetricsCollector(BenchmarkMetricsCollector):
    """Extends the benchmark metrics collector with risk-specific metrics."""
    
    def record_risk_metrics(self, risk_score: float, confidence: float, 
                          circuit_complexity: int, execution_time: float) -> None:
        """Record risk assessment specific metrics.
        
        Args:
            risk_score: Calculated risk score
            confidence: Confidence level of the risk score
            circuit_complexity: Complexity measure of the quantum circuit
            execution_time: Time taken to execute the risk assessment
        """
        risk_metrics = {
            "risk_score": risk_score,
            "confidence": confidence,
            "circuit_complexity": circuit_complexity,
            "execution_time": execution_time
        }
        
        self.record_metric("risk_assessment", f"risk_assessment_{datetime.now().strftime('%H%M%S')}", risk_metrics)


class QuantumRiskBenchmark(QuantumFinancialBenchmark):
    """Extends the main benchmark class with risk assessment specific algorithms."""
    
    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR, report_dir: str = DEFAULT_REPORT_DIR):
        """Initialize the quantum risk benchmark.
        
        Args:
            output_dir: Directory to store benchmark results
            report_dir: Directory to store benchmark reports
        """
        super().__init__(output_dir, report_dir)
        
        # Replace the metrics collector with our extended version
        self.metrics = RiskMetricsCollector(output_dir)
        
    def benchmark_var_calculation(self, 
                                price_data: List[float],
                                confidence_level: float = 0.95,
                                iterations: int = 3) -> Dict[str, Any]:
        """Benchmark Value at Risk (VaR) calculation using quantum algorithms.
        
        Args:
            price_data: Historical price data
            confidence_level: Confidence level for VaR calculation
            iterations: Number of iterations to run
            
        Returns:
            Dictionary with benchmark results
        """
        if not QISKIT_AVAILABLE:
            logger.error("Qiskit not available, cannot benchmark quantum VaR")
            return {"error": "Qiskit not available"}
        
        logger.info(f"Benchmarking quantum VaR calculation with {len(price_data)} data points")
        
        # Classical VaR calculation for comparison
        classical_var = self._calculate_classical_var(price_data, confidence_level)
        self.metrics.record_metric("classical_risk", "var_calculation", {
            "var": classical_var,
            "confidence_level": confidence_level,
            "data_points": len(price_data)
        })
        
        # Quantum VaR calculation
        # Run benchmark iterations
        execution_times = []
        var_results = []
        circuit_complexities = []
        
        for i in range(iterations):
            start_time = self.metrics.start_timer()
            var_value, circuit = self._calculate_quantum_var(price_data, confidence_level)
            execution_time = self.metrics.stop_timer(start_time)
            
            execution_times.append(execution_time)
            var_results.append(var_value)
            circuit_complexities.append(circuit.depth())
            
            logger.debug(f"Iteration {i+1}/{iterations}: VaR={var_value:.4f}, Time={execution_time:.4f}s")
        
        # Calculate statistics
        mean_time = np.mean(execution_times)
        mean_var = np.mean(var_results)
        mean_complexity = np.mean(circuit_complexities)
        
        # Record metrics
        self.metrics.record_risk_metrics(
            risk_score=float(mean_var),
            confidence=float(confidence_level),
            circuit_complexity=int(mean_complexity),
            execution_time=float(mean_time)
        )
        
        benchmark_result = {
            "mean_time": mean_time,
            "mean_var": mean_var,
            "circuit_complexity": mean_complexity,
            "classical_var": classical_var,
            "quantum_var_difference": mean_var - classical_var,
            "data_points": len(price_data),
            "iterations": iterations
        }
        
        self.metrics.record_metric("quantum_risk", "var_calculation", benchmark_result)
        logger.info(f"Quantum VaR benchmark complete: {mean_var:.4f} (±{np.std(var_results):.4f})")
        
        return benchmark_result
    
    def benchmark_portfolio_optimization(self,
                                       returns: List[float],
                                       covariance_matrix: List[List[float]],
                                       iterations: int = 3) -> Dict[str, Any]:
        """Benchmark quantum portfolio optimization algorithm.
        
        Args:
            returns: Expected returns for assets
            covariance_matrix: Covariance matrix of asset returns
            iterations: Number of iterations to run
            
        Returns:
            Dictionary with benchmark results
        """
        if not QISKIT_AVAILABLE:
            logger.error("Qiskit not available, cannot benchmark quantum portfolio optimization")
            return {"error": "Qiskit not available"}
        
        logger.info(f"Benchmarking quantum portfolio optimization with {len(returns)} assets")
        
        # Classical portfolio optimization for comparison
        classical_weights, classical_risk = self._calculate_classical_portfolio(returns, covariance_matrix)
        self.metrics.record_metric("classical_risk", "portfolio_optimization", {
            "weights": classical_weights,
            "risk": classical_risk,
            "assets": len(returns)
        })
        
        # Quantum portfolio optimization
        # Run benchmark iterations
        execution_times = []
        quantum_weights_list = []
        quantum_risk_list = []
        circuit_complexities = []
        
        for i in range(iterations):
            start_time = self.metrics.start_timer()
            quantum_weights, quantum_risk, circuit = self._calculate_quantum_portfolio(returns, covariance_matrix)
            execution_time = self.metrics.stop_timer(start_time)
            
            execution_times.append(execution_time)
            quantum_weights_list.append(quantum_weights)
            quantum_risk_list.append(quantum_risk)
            circuit_complexities.append(circuit.depth())
            
            logger.debug(f"Iteration {i+1}/{iterations}: Risk={quantum_risk:.4f}, Time={execution_time:.4f}s")
        
        # Calculate statistics
        mean_time = np.mean(execution_times)
        mean_risk = np.mean(quantum_risk_list)
        mean_complexity = np.mean(circuit_complexities)
        
        # Record metrics
        self.metrics.record_risk_metrics(
            risk_score=float(mean_risk),
            confidence=float(0.95),  # Default confidence level
            circuit_complexity=int(mean_complexity),
            execution_time=float(mean_time)
        )
        
        benchmark_result = {
            "mean_time": mean_time,
            "mean_risk": mean_risk,
            "circuit_complexity": mean_complexity,
            "classical_risk": classical_risk,
            "risk_difference": mean_risk - classical_risk,
            "assets": len(returns),
            "iterations": iterations
        }
        
        self.metrics.record_metric("quantum_risk", "portfolio_optimization", benchmark_result)
        logger.info(f"Quantum portfolio optimization benchmark complete: Risk={mean_risk:.4f}")
        
        return benchmark_result
    
    def _calculate_classical_var(self, price_data: List[float], confidence_level: float) -> float:
        """Calculate VaR using classical methods.
        
        Args:
            price_data: Historical price data
            confidence_level: Confidence level for VaR calculation
            
        Returns:
            Classical VaR value
        """
        returns = np.diff(price_data) / price_data[:-1]
        var = np.percentile(returns, 100 * (1 - confidence_level))
        return float(-var * price_data[-1])
    
    def _calculate_quantum_var(self, price_data: List[float], confidence_level: float) -> Tuple[float, QuantumCircuit]:
        """Calculate VaR using a quantum algorithm.
        
        This is a simplified implementation for benchmarking purposes.
        
        Args:
            price_data: Historical price data
            confidence_level: Confidence level for VaR calculation
            
        Returns:
            Tuple of (quantum VaR value, quantum circuit used)
        """
        # For this example, we'll create a simple quantum circuit that approximates VaR
        # In a real implementation, this would use amplitude estimation or other quantum algorithms
        
        returns = np.diff(price_data) / price_data[:-1]
        
        # Create a quantum circuit based on the size of returns data
        num_qubits = max(3, int(np.log2(len(returns))) + 1)
        circuit = QuantumCircuit(num_qubits)
        
        # Apply gates based on returns data and confidence level
        for i in range(num_qubits):
            circuit.h(i)
        
        # Encode some data properties into rotation angles
        for i in range(num_qubits):
            # Use statistical properties of returns to set rotation angles
            angle = np.pi * np.percentile(returns, i * 100 / num_qubits) / np.max(np.abs(returns))
            circuit.rz(angle, i)
        
        # Add some entanglement
        for i in range(num_qubits - 1):
            circuit.cx(i, i + 1)
        
        # Add a QFT to help with distribution representation
        qft = QFT(num_qubits)
        circuit.compose(qft, inplace=True)
        
        # Simulate the circuit
        simulator = AerSimulator()
        transpiled_circuit = transpile(circuit, simulator)
        job = simulator.run(transpiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        
        # Calculate VaR from the quantum state (simplified)
        # In a real algorithm, we would use proper amplitude estimation
        sorted_counts = sorted(counts.items(), key=lambda x: int(x[0], 2))
        cumulative_prob = 0
        var_index = 0
        
        for bitstring, count in sorted_counts:
            prob = count / 1024
            cumulative_prob += prob
            if cumulative_prob >= confidence_level:
                var_index = int(bitstring, 2)
                break
        
        # Scale the var_index to the price range
        min_return = np.min(returns)
        max_return = np.max(returns)
        var_return = min_return + (var_index / (2**num_qubits - 1)) * (max_return - min_return)
        
        # Apply a small random factor to simulate quantum advantage/difference
        quantum_factor = 1.0 + 0.05 * (np.random.random() - 0.5)
        var_value = float(-var_return * price_data[-1] * quantum_factor)
        
        return var_value, circuit
    
    def _calculate_classical_portfolio(self, returns: List[float], 
                                      covariance_matrix: List[List[float]]) -> Tuple[List[float], float]:
        """Calculate optimal portfolio weights using classical methods.
        
        Args:
            returns: Expected returns for assets
            covariance_matrix: Covariance matrix of asset returns
            
        Returns:
            Tuple of (optimal weights, portfolio risk)
        """
        # Simple equal weighting for demonstration
        n_assets = len(returns)
        weights = [1.0 / n_assets] * n_assets
        
        # Calculate portfolio risk
        cov_matrix = np.array(covariance_matrix)
        weights_array = np.array(weights)
        portfolio_risk = np.sqrt(weights_array.T @ cov_matrix @ weights_array)
        
        return weights, float(portfolio_risk)
    
    def _calculate_quantum_portfolio(self, returns: List[float],
                                   covariance_matrix: List[List[float]]) -> Tuple[List[float], float, QuantumCircuit]:
        """Calculate optimal portfolio weights using a quantum algorithm.
        
        This is a simplified implementation for benchmarking purposes.
        
        Args:
            returns: Expected returns for assets
            covariance_matrix: Covariance matrix of asset returns
            
        Returns:
            Tuple of (optimal weights, portfolio risk, quantum circuit used)
        """
        n_assets = len(returns)
        
        # Create a quantum circuit for portfolio optimization
        # In a real implementation, this would use QAOA or VQE
        num_qubits = max(3, n_assets)
        circuit = QuantumCircuit(num_qubits)
        
        # Apply gates based on returns and covariance data
        for i in range(num_qubits):
            circuit.h(i)
        
        # Encode returns data
        for i in range(min(n_assets, num_qubits)):
            # Normalize returns to use as rotation angles
            angle = np.pi * returns[i] / max(abs(min(returns)), abs(max(returns)))
            circuit.ry(angle, i)
        
        # Encode covariance using entangling gates
        for i in range(min(n_assets, num_qubits)):
            for j in range(i+1, min(n_assets, num_qubits)):
                if i < len(covariance_matrix) and j < len(covariance_matrix[i]):
                    # Use covariance to control interaction strength
                    angle = np.pi * covariance_matrix[i][j] / max([max(row) for row in covariance_matrix])
                    circuit.crz(angle, i, j)
        
        # Add some mixing with parameterized gates
        for i in range(num_qubits):
            circuit.rx(np.pi / 4, i)
        
        # Simulate the circuit
        simulator = AerSimulator()
        transpiled_circuit = transpile(circuit, simulator)
        job = simulator.run(transpiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        
        # Extract weights from the quantum state (simplified)
        # In reality, this would use a proper quantum algorithm like QAOA
        weights = [0] * n_assets
        total_count = sum(counts.values())
        
        # Process measurement outcomes
        for bitstring, count in counts.items():
            for i in range(min(n_assets, len(bitstring))):
                if bitstring[-(i+1)] == '1':  # Check if the corresponding bit is 1
                    weights[i] += count / total_count
        
        # Normalize weights
        if sum(weights) > 0:
            weights = [w / sum(weights) for w in weights]
        else:
            weights = [1.0 / n_assets] * n_assets
        
        # Calculate portfolio risk with these weights
        cov_matrix = np.array(covariance_matrix)
        weights_array = np.array(weights)
        portfolio_risk = np.sqrt(weights_array.T @ cov_matrix @ weights_array)
        
        # Apply a small random factor to simulate quantum advantage/difference
        quantum_factor = 1.0 + 0.05 * (np.random.random() - 0.5)
        portfolio_risk *= quantum_factor
        
        return weights, float(portfolio_risk), circuit
    
    def generate_risk_visualizations(self, output_file: str) -> List[str]:
        """Generate risk-specific visualizations from benchmark results.
        
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
        
        # Generate risk assessment visualization if data is available
        if "risk_assessment" in results["metrics"]:
            risk_data = results["metrics"]["risk_assessment"]
            
            # Extract metrics
            timestamps: List[str] = []
            risk_scores: List[float] = []
            confidence_levels: List[float] = []
            circuit_complexities: List[int] = []
            
            for name, data in risk_data.items():
                timestamps.append(name.split('_')[-1])  # Extract timestamp part
                risk_scores.append(float(data["risk_score"]))  # Ensure float type
                confidence_levels.append(float(data["confidence"]))  # Ensure float type
                circuit_complexities.append(int(data["circuit_complexity"]))  # Ensure int type
            
            # Sort by timestamp
            sorted_indices = sorted(range(len(timestamps)), key=lambda i: timestamps[i])
            risk_scores = [risk_scores[i] for i in sorted_indices]
            confidence_levels = [confidence_levels[i] for i in sorted_indices]
            circuit_complexities = [circuit_complexities[i] for i in sorted_indices]
            
            # Create risk score vs circuit complexity visualization
            plt.figure(figsize=(12, 8))
            
            plt.subplot(2, 1, 1)
            plt.plot(range(len(risk_scores)), risk_scores, 'o-', color='red', label='Risk Score')
            plt.ylabel('Risk Score')
            plt.title('Quantum Risk Assessment Results')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            
            plt.subplot(2, 1, 2)
            plt.plot(range(len(circuit_complexities)), circuit_complexities, 's-', color='blue', label='Circuit Complexity')
            plt.plot(range(len(confidence_levels)), [c*max(circuit_complexities) for c in confidence_levels], 
                   'd-', color='green', label='Confidence (scaled)')
            plt.xlabel('Assessment Run')
            plt.ylabel('Complexity / Confidence')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            
            plt.tight_layout()
            
            vis_file = os.path.join(vis_dir, f"risk_assessment_{timestamp}.png")
            plt.savefig(vis_file)
            plt.close()
            visualization_files.append(vis_file)
            logger.info(f"Created risk assessment visualization: {vis_file}")
        
        # Generate VaR comparison visualization if data is available
        if "classical_risk" in results["metrics"] and "quantum_risk" in results["metrics"]:
            if "var_calculation" in results["metrics"]["classical_risk"] and "var_calculation" in results["metrics"]["quantum_risk"]:
                classical_var = results["metrics"]["classical_risk"]["var_calculation"]["var"]
                quantum_var = results["metrics"]["quantum_risk"]["var_calculation"]["mean_var"]
                
                plt.figure(figsize=(10, 6))
                plt.bar(["Classical VaR", "Quantum VaR"], [classical_var, quantum_var], color=['blue', 'purple'])
                plt.ylabel('Value at Risk (VaR)')
                plt.title('Classical vs Quantum VaR Calculation')
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                
                # Add percent difference annotation
                pct_diff = ((quantum_var - classical_var) / classical_var) * 100
                plt.annotate(f'{pct_diff:.2f}% difference', 
                            xy=(1, quantum_var), 
                            xytext=(0.75, max(classical_var, quantum_var) * 1.1),
                            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))
                
                plt.tight_layout()
                
                vis_file = os.path.join(vis_dir, f"var_comparison_{timestamp}.png")
                plt.savefig(vis_file)
                plt.close()
                visualization_files.append(vis_file)
                logger.info(f"Created VaR comparison visualization: {vis_file}")
        
        return visualization_files


def generate_sample_data(num_assets: int = 5, data_points: int = 100) -> Tuple[List[float], List[List[float]], List[float]]:
    """Generate sample financial data for benchmarking.
    
    Args:
        num_assets: Number of assets in the portfolio
        data_points: Number of historical price data points
        
    Returns:
        Tuple of (returns, covariance matrix, price data)
    """
    # Generate random returns for assets
    returns: List[float] = [0.05 + 0.1 * np.random.random() for _ in range(num_assets)]
    
    # Generate random correlation matrix (ensuring it's symmetric and positive definite)
    corr_matrix = np.random.random((num_assets, num_assets))
    corr_matrix = 0.5 * (corr_matrix + corr_matrix.T)  # Make symmetric
    corr_matrix = corr_matrix + num_assets * np.eye(num_assets)  # Ensure positive definite
    
    # Convert to correlation matrix (diagonal = 1)
    d = np.sqrt(np.diag(corr_matrix))
    corr_matrix = corr_matrix / np.outer(d, d)
    
    # Generate random volatilities
    vols = [0.1 + 0.2 * np.random.random() for _ in range(num_assets)]
    
    # Convert correlation to covariance matrix
    cov_matrix: List[List[float]] = []
    for i in range(num_assets):
        row = []
        for j in range(num_assets):
            row.append(corr_matrix[i][j] * vols[i] * vols[j])
        cov_matrix.append(row)
    
    # Generate sample price data
    start_price: float = 100.0  # Starting price as float to ensure price_data is list of floats
    price_data: List[float] = [start_price]
    
    for _ in range(data_points - 1):
        return_val = 0.0005 + 0.001 * np.random.randn()  # Daily return with some randomness
        new_price = price_data[-1] * (1 + return_val)
        price_data.append(new_price)
    
    return returns, cov_matrix, price_data


def main():
    """Main function to run quantum risk benchmarks."""
    parser = argparse.ArgumentParser(description="Quantum Financial Risk Benchmark Framework")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Directory to store benchmark results")
    parser.add_argument("--report-dir", default=DEFAULT_REPORT_DIR, help="Directory to store benchmark reports")
    parser.add_argument("--assets", type=int, default=5, help="Number of assets for portfolio optimization")
    parser.add_argument("--data-points", type=int, default=100, help="Number of price data points")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info("Starting Quantum Financial Risk Benchmark")
    
    # Generate sample data
    returns, cov_matrix, price_data = generate_sample_data(args.assets, args.data_points)
    
    # Initialize benchmark framework
    benchmark = QuantumRiskBenchmark(args.output_dir, args.report_dir)
    
    # Run benchmarks
    benchmark.benchmark_var_calculation(price_data)
    benchmark.benchmark_portfolio_optimization(returns, cov_matrix)
    
    # Save results
    result_file = benchmark.metrics.save_results("quantum_financial_benchmark_risk")
    
    # Update benchmark history
    benchmark.update_benchmark_history(result_file)
    
    # Generate visualizations
    risk_visualizations = benchmark.generate_risk_visualizations(result_file)
    all_visualizations = benchmark.generate_visualizations(result_file)
    all_visualizations.extend(risk_visualizations)
    
    # Generate report
    report_file = benchmark.generate_report(result_file, all_visualizations)
    
    logger.info(f"Risk benchmark complete. Report available at: {report_file}")


if __name__ == "__main__":
    main() 