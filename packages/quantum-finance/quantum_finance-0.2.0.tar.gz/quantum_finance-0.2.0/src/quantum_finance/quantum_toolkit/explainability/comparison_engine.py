"""
Quantum Explainability Interface - Comparison Engine

This module provides tools for comparing quantum and classical prediction approaches,
helping to explain when and why quantum methods provide advantages for financial
risk assessment.

The comparison engine integrates with existing quantum risk models to provide:
1. Side-by-side visualization of quantum vs. classical predictions
2. Confidence interval analysis
3. Divergence metrics to highlight where quantum methods differ most
4. Interactive data for dashboard display

Author: Quantum-AI Team
"""

import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Union, Any
from datetime import datetime
import os
import json
from matplotlib.ticker import MaxNLocator
from matplotlib.transforms import Bbox
import seaborn as sns

# Import quantum risk components
from ..error_correction import ErrorMitigationFactory
from quantum_finance.data import CryptoDataFetcher

# Project-specific modules for core functionality
from quantum_finance.quantum_bayesian_risk import QuantumBayesianRiskNetwork
from quantum_finance.quantum_risk.analyzer import QuantumEnhancedCryptoRiskAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComparisonResult:
    """
    Represents the result of a comparison between quantum and classical approaches.

    Stores key metrics and data points from the comparative analysis.
    """
    def __init__(self, 
                 symbol: str, 
                 timestamp: datetime,
                 quantum_results: Any, 
                 classical_results: Any, 
                 comparison_metrics: Dict[str, Any],
                 divergence_metrics: Dict[str, float],
                 confidence_intervals: Dict[str, Any],
                 visualization_files: Dict[str, str]):
        """
        Initialize the ComparisonResult.

        Args:
            symbol: Asset symbol (e.g., 'BTC').
            timestamp: Timestamp of the analysis.
            quantum_results: Results from the quantum model.
            classical_results: Results from the classical model.
            comparison_metrics: Metrics comparing the two approaches (e.g., differences).
            divergence_metrics: Metrics quantifying the divergence between distributions (e.g., KL divergence).
            confidence_intervals: Confidence interval data for both quantum and classical results.
            visualization_files: Paths to generated visualization files.
        """
        self.symbol = symbol
        self.timestamp = timestamp
        self.quantum_results = quantum_results
        self.classical_results = classical_results
        self.comparison_metrics = comparison_metrics
        self.divergence_metrics = divergence_metrics
        self.confidence_intervals = confidence_intervals
        self.visualization_files = visualization_files

    def __repr__(self):
        return (
            f"ComparisonResult(symbol='{self.symbol}', timestamp='{self.timestamp}', " 
            f"metrics_keys={list(self.comparison_metrics.keys())})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the result object to a dictionary."""
        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "quantum_results": self.quantum_results, # Consider how to best serialize this
            "classical_results": self.classical_results, # Consider how to best serialize this
            "comparison_metrics": self.comparison_metrics,
            "divergence_metrics": self.divergence_metrics,
            "confidence_intervals": self.confidence_intervals,
            "visualization_files": self.visualization_files
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComparisonResult':
        """Create a ComparisonResult instance from a dictionary."""
        return cls(
            symbol=data["symbol"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            quantum_results=data["quantum_results"],
            classical_results=data["classical_results"],
            comparison_metrics=data["comparison_metrics"],
            divergence_metrics=data["divergence_metrics"],
            confidence_intervals=data["confidence_intervals"],
            visualization_files=data["visualization_files"]
        )


class ComparisonEngine:
    """
    Provides tools for comparing quantum and classical prediction approaches.
    
    This class integrates with existing quantum risk models to provide detailed
    comparisons, visualizations, and metrics that help explain when and why
    quantum methods provide advantages.
    """
    
    def __init__(self, output_dir: str = "comparison_results"):
        """
        Initialize the comparison engine.
        
        Args:
            output_dir: Directory to store comparison results and visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.comparison_results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"Initialized ComparisonEngine with output directory: {output_dir}")
    
    def run_comparative_analysis(self, 
                               symbol: str,
                               risk_network: QuantumBayesianRiskNetwork,
                               initial_probabilities: List[float],
                               output_prefix: Optional[str] = None) -> Dict[str, Any]:
        """
        Run both quantum and classical analysis and store detailed comparison metrics.
        
        Args:
            symbol: Asset symbol (e.g., 'BTC', 'ETH')
            risk_network: Initialized quantum Bayesian risk network
            initial_probabilities: Initial risk probabilities
            output_prefix: Optional prefix for output files
            
        Returns:
            Dictionary with comparative analysis results
        """
        logger.info(f"Running comparative analysis for {symbol}")
        
        # Generate unique prefix for this analysis
        prefix = output_prefix or f"{symbol}_{self.timestamp}"
        
        # Run quantum vs classical comparison with detailed metrics
        comparison_metrics = self._run_detailed_comparison(
            risk_network, 
            initial_probabilities, 
            prefix
        )
        
        # Calculate divergence metrics
        divergence_metrics = self._calculate_divergence_metrics(
            comparison_metrics["quantum_probabilities"],
            comparison_metrics["classical_probabilities"]
        )
        
        # Generate confidence intervals
        confidence_intervals = self._generate_confidence_intervals(
            risk_network,
            initial_probabilities
        )
        
        # Create comprehensive visualizations
        self._create_detailed_visualizations(
            risk_network.risk_factor_names,
            comparison_metrics,
            confidence_intervals,
            divergence_metrics,
            prefix
        )
        
        # Combine all results
        analysis_results = {
            "symbol": symbol,
            "timestamp": self.timestamp,
            "comparison_metrics": comparison_metrics,
            "divergence_metrics": divergence_metrics,
            "confidence_intervals": confidence_intervals,
            "visualization_files": {
                "comparison_chart": f"{prefix}_quantum_classical_comparison.png",
                "confidence_intervals": f"{prefix}_confidence_intervals.png",
                "divergence_heatmap": f"{prefix}_divergence_heatmap.png",
                "advantage_metrics": f"{prefix}_quantum_advantage_metrics.png"
            }
        }
        
        # Save results to JSON for later use
        results_file = os.path.join(self.output_dir, f"{prefix}_comparison_results.json")
        with open(results_file, "w") as f:
            json.dump(analysis_results, f, indent=2)
        
        # Store in instance for reference
        self.comparison_results[symbol] = analysis_results
        
        logger.info(f"Comparative analysis complete for {symbol}")
        return analysis_results
    
    def _run_detailed_comparison(self, 
                              risk_network: QuantumBayesianRiskNetwork,
                              initial_probabilities: List[float],
                              prefix: str) -> Dict[str, Any]:
        """
        Run detailed comparison between quantum and classical approaches.
        
        Args:
            risk_network: Quantum Bayesian risk network
            initial_probabilities: Initial probabilities
            prefix: Output file prefix
            
        Returns:
            Comparison metrics
        """
        # Define output file
        output_file = os.path.join(self.output_dir, f"{prefix}_quantum_classical_comparison.png")
        
        # Run comparison using existing method in risk network
        comparison = risk_network.compare_classical_quantum(
            initial_probabilities,
            output_file=output_file
        )
        
        # Add additional metrics
        comparison["relative_difference"] = [
            (q - c) / max(c, 0.001) 
            for q, c in zip(comparison["quantum_probabilities"], comparison["classical_probabilities"])
        ]
        
        # Calculate aggregate metrics
        comparison["mean_absolute_difference"] = np.mean(np.abs(comparison["difference"]))
        comparison["max_absolute_difference"] = np.max(np.abs(comparison["difference"]))
        comparison["mean_relative_difference"] = np.mean(np.abs(comparison["relative_difference"]))
        
        return comparison
    
    def _calculate_divergence_metrics(self, 
                                   quantum_probs: List[float], 
                                   classical_probs: List[float]) -> Dict[str, float]:
        """
        Calculate advanced divergence metrics between quantum and classical probabilities.
        
        Args:
            quantum_probs: Quantum probabilities
            classical_probs: Classical probabilities
            
        Returns:
            Dictionary with divergence metrics
        """
        # Convert to numpy arrays
        q_probs = np.array(quantum_probs)
        c_probs = np.array(classical_probs)
        
        # Calculate KL divergence (with small epsilon to avoid division by zero)
        epsilon = 1e-10
        q_probs_safe = np.clip(q_probs, epsilon, 1.0 - epsilon)
        c_probs_safe = np.clip(c_probs, epsilon, 1.0 - epsilon)
        
        # KL(P||Q) = sum_i P(i) * log(P(i)/Q(i))
        kl_qc = np.sum(q_probs_safe * np.log(q_probs_safe / c_probs_safe))
        kl_cq = np.sum(c_probs_safe * np.log(c_probs_safe / q_probs_safe))
        
        # Jensen-Shannon divergence (symmetric)
        m_probs = 0.5 * (q_probs_safe + c_probs_safe)
        js_divergence = 0.5 * (
            np.sum(q_probs_safe * np.log(q_probs_safe / m_probs)) +
            np.sum(c_probs_safe * np.log(c_probs_safe / m_probs))
        )
        
        # Total variation distance
        tv_distance = 0.5 * np.sum(np.abs(q_probs - c_probs))
        
        # Hellinger distance
        hellinger = np.sqrt(0.5 * np.sum((np.sqrt(q_probs) - np.sqrt(c_probs))**2))
        
        return {
            "kl_divergence_qc": float(kl_qc),
            "kl_divergence_cq": float(kl_cq),
            "jensen_shannon_divergence": float(js_divergence),
            "total_variation_distance": float(tv_distance),
            "hellinger_distance": float(hellinger)
        }
    
    def _generate_confidence_intervals(self,
                                    risk_network: QuantumBayesianRiskNetwork,
                                    initial_probabilities: List[float],
                                    num_samples: int = 100) -> Dict[str, Any]:
        """
        Generate confidence intervals for quantum and classical predictions.
        
        Args:
            risk_network: Quantum Bayesian risk network
            initial_probabilities: Initial probabilities
            num_samples: Number of samples for bootstrap
            
        Returns:
            Dictionary with confidence intervals
        """
        # Prepare result containers
        quantum_samples = []
        classical_samples = []
        
        # Run bootstrap sampling
        for _ in range(num_samples):
            # Add small perturbations to initial probabilities
            perturbed_probs = [
                min(1.0, max(0.0, p + np.random.normal(0, 0.02))) 
                for p in initial_probabilities
            ]
            
            # Run quantum analysis with perturbed inputs
            # Use lower shot count for efficiency
            quantum_result = risk_network.propagate_risk(perturbed_probs, shots=1000)
            quantum_samples.append(quantum_result["updated_probabilities"])
            
            # Simple classical Bayesian propagation (similar to compare_classical_quantum)
            classical_result = perturbed_probs.copy()
            for (cause, effect), circuit in risk_network.conditional_circuits.items():
                # Extract strength from circuit
                strength = 0.0
                for instruction in circuit.data:
                    if instruction.operation.name == 'cry':
                        angle = instruction.operation.params[0]
                        strength = angle / np.pi
                        break
                
                # Update probability
                influence = strength * perturbed_probs[cause]
                classical_result[effect] = min(
                    1.0, 
                    classical_result[effect] + influence * (1 - classical_result[effect])
                )
            
            classical_samples.append(classical_result)
        
        # Convert to numpy array for easier analysis
        quantum_array = np.array(quantum_samples)
        classical_array = np.array(classical_samples)
        
        # Calculate confidence intervals (95%)
        quantum_means = np.mean(quantum_array, axis=0)
        quantum_lower = np.percentile(quantum_array, 2.5, axis=0)
        quantum_upper = np.percentile(quantum_array, 97.5, axis=0)
        
        classical_means = np.mean(classical_array, axis=0)
        classical_lower = np.percentile(classical_array, 2.5, axis=0)
        classical_upper = np.percentile(classical_array, 97.5, axis=0)
        
        return {
            "quantum": {
                "means": quantum_means.tolist(),
                "lower_bounds": quantum_lower.tolist(),
                "upper_bounds": quantum_upper.tolist()
            },
            "classical": {
                "means": classical_means.tolist(),
                "lower_bounds": classical_lower.tolist(),
                "upper_bounds": classical_upper.tolist()
            },
            "overlap_percentage": self._calculate_confidence_overlap(
                quantum_lower, quantum_upper,
                classical_lower, classical_upper
            )
        }
    
    def _calculate_confidence_overlap(self,
                                   q_lower: np.ndarray,
                                   q_upper: np.ndarray,
                                   c_lower: np.ndarray,
                                   c_upper: np.ndarray) -> List[float]:
        """
        Calculate percentage overlap between confidence intervals.
        
        Args:
            q_lower: Quantum lower bounds
            q_upper: Quantum upper bounds
            c_lower: Classical lower bounds
            c_upper: Classical upper bounds
            
        Returns:
            List of overlap percentages for each risk factor
        """
        overlap_percentage = []
        
        for i in range(len(q_lower)):
            # Calculate overlap
            overlap_start = max(q_lower[i], c_lower[i])
            overlap_end = min(q_upper[i], c_upper[i])
            
            if overlap_start > overlap_end:
                # No overlap
                overlap_percentage.append(0.0)
            else:
                # Calculate overlap percentage relative to the union of both intervals
                union_length = max(q_upper[i], c_upper[i]) - min(q_lower[i], c_lower[i])
                overlap_length = overlap_end - overlap_start
                overlap_percentage.append(
                    (overlap_length / union_length) * 100 if union_length > 0 else 100.0
                )
        
        return overlap_percentage
    
    def _create_detailed_visualizations(self,
                                     risk_factor_names: List[str],
                                     comparison_metrics: Dict[str, Any],
                                     confidence_intervals: Dict[str, Any],
                                     divergence_metrics: Dict[str, float],
                                     prefix: str) -> None:
        """
        Create detailed visualizations for comparison results.
        
        Args:
            risk_factor_names: Names of risk factors
            comparison_metrics: Comparison metrics dictionary
            confidence_intervals: Confidence intervals dictionary
            divergence_metrics: Divergence metrics dictionary
            prefix: Output file prefix
        """
        # 1. Create confidence interval visualization
        self._create_confidence_interval_plot(
            risk_factor_names,
            confidence_intervals,
            os.path.join(self.output_dir, f"{prefix}_confidence_intervals.png")
        )
        
        # 2. Create divergence heatmap
        self._create_divergence_heatmap(
            risk_factor_names,
            comparison_metrics,
            os.path.join(self.output_dir, f"{prefix}_divergence_heatmap.png")
        )
        
        # 3. Create quantum advantage metrics visualization
        self._create_advantage_metrics_visualization(
            divergence_metrics,
            comparison_metrics,
            os.path.join(self.output_dir, f"{prefix}_quantum_advantage_metrics.png")
        )
    
    def _create_confidence_interval_plot(self,
                                      risk_factor_names: List[str],
                                      confidence_intervals: Dict[str, Any],
                                      output_file: str) -> None:
        """
        Create confidence interval plot showing quantum and classical predictions.
        
        Args:
            risk_factor_names: Names of risk factors
            confidence_intervals: Confidence interval data
            output_file: Output file path
        """
        plt.figure(figsize=(12, 8))
        
        # X positions for the bars
        x = np.arange(len(risk_factor_names))
        width = 0.35
        
        # Extract data
        q_means = confidence_intervals["quantum"]["means"]
        q_err_lower = np.array(q_means) - np.array(confidence_intervals["quantum"]["lower_bounds"])
        q_err_upper = np.array(confidence_intervals["quantum"]["upper_bounds"]) - np.array(q_means)
        
        c_means = confidence_intervals["classical"]["means"]
        c_err_lower = np.array(c_means) - np.array(confidence_intervals["classical"]["lower_bounds"])
        c_err_upper = np.array(confidence_intervals["classical"]["upper_bounds"]) - np.array(c_means)
        
        # Create the bar plots with error bars
        plt.bar(x - width/2, q_means, width, label='Quantum', color='royalblue', alpha=0.7)
        plt.bar(x + width/2, c_means, width, label='Classical', color='firebrick', alpha=0.7)
        
        # Add error bars
        plt.errorbar(
            x - width/2, q_means, 
            yerr=[q_err_lower, q_err_upper], 
            fmt='none', ecolor='black', capsize=5
        )
        plt.errorbar(
            x + width/2, c_means, 
            yerr=[c_err_lower, c_err_upper], 
            fmt='none', ecolor='black', capsize=5
        )
        
        # Add overlap percentage text
        for i, overlap in enumerate(confidence_intervals["overlap_percentage"]):
            plt.text(i, max(q_means[i], c_means[i]) + 0.1, 
                    f"Overlap: {overlap:.1f}%", 
                    ha='center', va='center', fontsize=8)
        
        # Configure the plot
        plt.xlabel('Risk Factors')
        plt.ylabel('Probability')
        plt.title('Quantum vs Classical Risk Assessment with 95% Confidence Intervals')
        plt.xticks(x, risk_factor_names, rotation=45, ha='right')
        plt.ylim(0, 1.1)
        plt.legend()
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
    
    def _create_divergence_heatmap(self,
                                risk_factor_names: List[str],
                                comparison_metrics: Dict[str, Any],
                                output_file: str) -> None:
        """
        Create a heatmap showing divergence between quantum and classical predictions.
        
        Args:
            risk_factor_names: Names of risk factors
            comparison_metrics: Comparison metrics
            output_file: Output file path
        """
        plt.figure(figsize=(12, 8))
        
        # Create data for the heatmap
        data = pd.DataFrame({
            'Risk Factor': risk_factor_names,
            'Absolute Difference': comparison_metrics["difference"],
            'Relative Difference (%)': [d * 100 for d in comparison_metrics["relative_difference"]]
        }).set_index('Risk Factor')
        
        # Create heatmap
        im = plt.imshow(data.T, cmap='coolwarm')
        
        # Configure labels
        plt.yticks(np.arange(len(data.columns)), data.columns)
        plt.xticks(np.arange(len(data.index)), data.index, rotation=45, ha='right')
        
        # Add colorbar
        cbar = plt.colorbar(im)
        cbar.set_label('Difference')
        
        # Add text annotations with actual values
        for i in range(len(data.columns)):
            for j in range(len(data.index)):
                text = plt.text(j, i, f"{data.iloc[j, i]:.2f}", 
                               ha="center", va="center", color="black")
        
        plt.title('Quantum vs Classical Divergence by Risk Factor')
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
    
    def _create_advantage_metrics_visualization(self,
                                             divergence_metrics: Dict[str, float],
                                             comparison_metrics: Dict[str, Any],
                                             output_file: str) -> None:
        """
        Create visualization showing quantum advantage metrics.
        
        Args:
            divergence_metrics: Dict of divergence metrics
            comparison_metrics: Comparison metrics
            output_file: Output file path
        """
        plt.figure(figsize=(14, 8))
        
        # Create a table-like visualization for the metrics
        metrics = {
            'KL Divergence (Q→C)': divergence_metrics["kl_divergence_qc"],
            'KL Divergence (C→Q)': divergence_metrics["kl_divergence_cq"],
            'Jensen-Shannon Divergence': divergence_metrics["jensen_shannon_divergence"],
            'Total Variation Distance': divergence_metrics["total_variation_distance"],
            'Hellinger Distance': divergence_metrics["hellinger_distance"],
            'Mean Absolute Difference': comparison_metrics["mean_absolute_difference"],
            'Max Absolute Difference': comparison_metrics["max_absolute_difference"],
            'Mean Relative Difference': comparison_metrics["mean_relative_difference"]
        }
        
        # Create bar chart
        plt.bar(metrics.keys(), metrics.values(), color='mediumseagreen')
        
        # Add value labels
        for i, (key, value) in enumerate(metrics.items()):
            plt.text(i, value + 0.01, f"{value:.4f}", ha='center')
        
        # Configure the plot
        plt.title('Quantum Advantage Metrics')
        plt.ylabel('Value')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Add a supplementary table with interpretation
        table_data = [
            ['Metric', 'Interpretation'],
            ['KL Divergence', 'Information gain from quantum model'],
            ['JS Divergence', 'Symmetric measure of model difference'],
            ['TV Distance', 'Maximum probability difference'],
            ['Hellinger', 'Difference in probability distributions'],
            ['Mean Abs Diff', 'Average absolute difference in risk estimates'],
            ['Max Abs Diff', 'Largest risk estimate difference']
        ]
        
        table = plt.table(
            cellText=table_data,
            loc='bottom',
            cellLoc='center',
            bbox=Bbox.from_bounds(0, -0.5, 1, 0.3)
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        
        # Save the plot
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()


# Example usage
if __name__ == "__main__":
    # Create a simple example
    from quantum_finance.quantum_bayesian_risk import QuantumBayesianRiskNetwork
    
    # Initialize the risk network
    network = QuantumBayesianRiskNetwork(num_risk_factors=5)
    
    # Add some relationships
    network.add_conditional_relationship(0, 1, 0.7)
    network.add_conditional_relationship(1, 2, 0.6)
    network.add_conditional_relationship(2, 3, 0.5)
    network.add_conditional_relationship(3, 4, 0.8)
    network.add_conditional_relationship(0, 4, 0.4)
    
    # Create some example initial probabilities
    initial_probs = [0.2, 0.3, 0.4, 0.3, 0.5]
    
    # Create comparison engine
    engine = ComparisonEngine(output_dir="example_output")
    
    # Run analysis
    result = engine.run_comparative_analysis(
        symbol="BTC",
        risk_network=network,
        initial_probabilities=initial_probs
    )
    
    print("Analysis complete")
    print(f"Results saved to {engine.output_dir}") 