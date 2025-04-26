"""
Quantum Explainability Integration Layer

This module provides the connection between the Explainability Interface
and the existing Quantum Risk Analysis components, making it easy to
incorporate explainability into existing workflows.

Author: Quantum-AI Team
"""

import logging
import os
from typing import Dict, List, Optional, Any, Union
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Import core components
from .comparison_engine import ComparisonEngine as ce
from quantum_finance.quantum_bayesian_risk import QuantumBayesianRiskNetwork
from quantum_finance.quantum_enhanced_crypto_risk import QuantumEnhancedCryptoRisk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExplainabilityIntegrator:
    """
    Integrates explainability capabilities with existing quantum risk models.
    
    This class acts as a bridge between the existing quantum risk analysis tools
    and the new explainability interface, making it easy to add powerful
    visualization and explanation capabilities to existing workflows.
    """
    
    def __init__(self, output_dir: str = "explainability_results"):
        """
        Initialize the integrator.
        
        Args:
            output_dir: Directory to store explainability results
        """
        self.output_dir = output_dir
        self.comparison_engine = ce(output_dir=output_dir)
        logger.info(f"Initialized ExplainabilityIntegrator with output directory: {output_dir}")
    
    def enhance_crypto_risk_analysis(self, 
                                   risk_analyzer,
                                   symbol: str,
                                   include_explainability: bool = True) -> Dict[str, Any]:
        """
        Enhance cryptocurrency risk analysis with explainability.
        
        This method integrates with the QuantumEnhancedCryptoRiskAnalyzer to add
        explainability features to the standard risk analysis.
        
        Args:
            risk_analyzer: QuantumEnhancedCryptoRiskAnalyzer instance
            symbol: Asset symbol (e.g., 'BTC', 'ETH')
            include_explainability: Whether to include explainability data
            
        Returns:
            Enhanced risk analysis results with explainability data
        """
        logger.info(f"Enhancing risk analysis for {symbol} with explainability")
        start_time = time.time()
        
        # Run standard risk analysis
        risk_results = risk_analyzer.analyze_with_quantum(symbol)
        
        # If explainability is disabled or analysis failed, return standard results
        if not include_explainability or "error" in risk_results:
            return risk_results
        
        # Extract quantum network and initial probabilities from risk analyzer
        try:
            risk_network = risk_analyzer.quantum_bayesian_network
            
            # Get initial probabilities (may need to be extracted from the results)
            if "initial_probabilities" in risk_results:
                initial_probabilities = risk_results["initial_probabilities"]
            else:
                # Build from risk metrics (approximate)
                initial_probabilities = [
                    risk_results.get("classical_risk", {}).get("imbalance", 0.5),
                    risk_results.get("classical_risk", {}).get("volatility", 0.5),
                    risk_results.get("classical_risk", {}).get("market_depth_risk", 50) / 100,
                    risk_results.get("classical_risk", {}).get("liquidity_risk", 50) / 100,
                    risk_results.get("classical_risk", {}).get("overall_risk", 50) / 100
                ]
            
            # Generate unique prefix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_prefix = f"{symbol}_explainable_{timestamp}"
            
            # Run comparative analysis with explainability
            explainability_results = self.comparison_engine.run_comparative_analysis(
                symbol=symbol,
                risk_network=risk_network,
                initial_probabilities=initial_probabilities,
                output_prefix=output_prefix
            )
            
            # Add explainability results to standard results
            risk_results["explainability"] = {
                "quantum_advantage_metrics": explainability_results["divergence_metrics"],
                "confidence_intervals": explainability_results["confidence_intervals"],
                "visualization_files": explainability_results["visualization_files"]
            }
            
            logger.info(f"Added explainability data to risk analysis for {symbol}")
            risk_results["explainability"]["execution_time"] = time.time() - start_time
            
            return risk_results
        
        except Exception as e:
            logger.error(f"Failed to add explainability to risk analysis: {str(e)}")
            # Still return the original risk results even if explainability failed
            risk_results["explainability_error"] = str(e)
            return risk_results
    
    def enhance_batch_risk_assessment(self,
                                    batch_assessment,
                                    asset_id: str,
                                    risk_network: QuantumBayesianRiskNetwork,
                                    initial_probabilities: List[float]) -> Dict[str, Any]:
        """
        Enhance batch risk assessment with explainability.
        
        This method integrates with the BatchRiskAssessment class to add
        explainability features to batch risk assessment.
        
        Args:
            batch_assessment: BatchRiskAssessment instance
            asset_id: Asset identifier
            risk_network: Quantum Bayesian risk network for the asset
            initial_probabilities: Initial risk probabilities
            
        Returns:
            Enhanced batch assessment results with explainability data
        """
        logger.info(f"Enhancing batch risk assessment for {asset_id} with explainability")
        
        # Generate unique prefix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_prefix = f"{asset_id}_batch_{timestamp}"
        
        # Run comparative analysis with explainability
        explainability_results = self.comparison_engine.run_comparative_analysis(
            symbol=asset_id,
            risk_network=risk_network,
            initial_probabilities=initial_probabilities,
            output_prefix=output_prefix
        )
        
        # Create enhanced assessment result
        enhanced_result = {
            "asset_id": asset_id,
            "timestamp": timestamp,
            "explainability": {
                "quantum_advantage_metrics": explainability_results["divergence_metrics"],
                "confidence_intervals": explainability_results["confidence_intervals"],
                "visualization_files": explainability_results["visualization_files"]
            }
        }
        
        logger.info(f"Generated explainability data for batch assessment of {asset_id}")
        return enhanced_result
    
    def create_comparative_dashboard(self, 
                                  symbol: str,
                                  comparison_results: Dict[str, Any],
                                  output_dir: Optional[str] = None) -> str:
        """
        Create an HTML dashboard summarizing comparative results.
        
        Args:
            symbol: Asset symbol
            comparison_results: Results from comparative analysis
            output_dir: Optional directory to store dashboard
            
        Returns:
            Path to the generated dashboard HTML file
        """
        # Use the provided output directory or default
        out_dir = output_dir or self.output_dir
        os.makedirs(out_dir, exist_ok=True)
        
        # Generate dashboard filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dashboard_file = os.path.join(out_dir, f"{symbol}_dashboard_{timestamp}.html")
        
        # Build HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Quantum vs Classical Analysis: {symbol}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .dashboard {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; 
                          text-align: center; margin-bottom: 20px; }}
                .section {{ background-color: #f5f5f5; padding: 15px; margin-bottom: 20px;
                           border-radius: 5px; }}
                .metrics {{ display: flex; flex-wrap: wrap; justify-content: space-around; }}
                .metric-card {{ background-color: white; padding: 15px; margin: 10px;
                              border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                              min-width: 200px; }}
                .visualization {{ margin: 20px 0; text-align: center; }}
                .visualization img {{ max-width: 100%; border: 1px solid #ddd; 
                                   border-radius: 5px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #2c3e50; color: white; }}
                .footer {{ text-align: center; margin-top: 30px; font-size: 0.8em; 
                         color: #777; }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>Quantum vs Classical Analysis Dashboard</h1>
                    <h2>{symbol} - {timestamp}</h2>
                </div>
                
                <div class="section">
                    <h2>Key Quantum Advantage Metrics</h2>
                    <div class="metrics">
        """
        
        # Add metrics
        metrics = comparison_results.get("divergence_metrics", {})
        for metric_name, value in metrics.items():
            html_content += f"""
                        <div class="metric-card">
                            <h3>{metric_name.replace('_', ' ').title()}</h3>
                            <p class="value">{value:.4f}</p>
                        </div>
            """
        
        # Add visualizations
        vis_files = comparison_results.get("visualization_files", {})
        html_content += """
                    </div>
                </div>
                
                <div class="section">
                    <h2>Visualizations</h2>
        """
        
        for vis_name, vis_file in vis_files.items():
            title = vis_name.replace('_', ' ').title()
            rel_path = os.path.relpath(os.path.join(self.output_dir, vis_file), out_dir)
            html_content += f"""
                    <div class="visualization">
                        <h3>{title}</h3>
                        <img src="{rel_path}" alt="{title}">
                    </div>
            """
        
        # Add confidence intervals
        html_content += """
                </div>
                
                <div class="section">
                    <h2>Confidence Intervals</h2>
                    <table>
                        <tr>
                            <th>Risk Factor</th>
                            <th>Quantum Mean</th>
                            <th>Quantum Range</th>
                            <th>Classical Mean</th>
                            <th>Classical Range</th>
                            <th>Overlap %</th>
                        </tr>
        """
        
        conf_intervals = comparison_results.get("confidence_intervals", {})
        q_means = conf_intervals.get("quantum", {}).get("means", [])
        q_lower = conf_intervals.get("quantum", {}).get("lower_bounds", [])
        q_upper = conf_intervals.get("quantum", {}).get("upper_bounds", [])
        
        c_means = conf_intervals.get("classical", {}).get("means", [])
        c_lower = conf_intervals.get("classical", {}).get("lower_bounds", [])
        c_upper = conf_intervals.get("classical", {}).get("upper_bounds", [])
        
        overlaps = conf_intervals.get("overlap_percentage", [])
        
        # Get risk factor names from visualization files if available
        vis_file = vis_files.get("comparison_chart", "")
        risk_factor_names = ["Factor " + str(i+1) for i in range(len(q_means))]
        
        for i, factor in enumerate(risk_factor_names):
            if i < len(q_means):
                html_content += f"""
                        <tr>
                            <td>{factor}</td>
                            <td>{q_means[i]:.3f}</td>
                            <td>{q_lower[i]:.3f} - {q_upper[i]:.3f}</td>
                            <td>{c_means[i]:.3f}</td>
                            <td>{c_lower[i]:.3f} - {c_upper[i]:.3f}</td>
                            <td>{overlaps[i]:.1f}%</td>
                        </tr>
                """
        
        # Close HTML
        html_content += """
                    </table>
                </div>
                
                <div class="footer">
                    <p>Generated by Quantum Explainability Interface</p>
                    <p>© Quantum-AI Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write to file
        with open(dashboard_file, "w") as f:
            f.write(html_content)
        
        logger.info(f"Created comparative dashboard at {dashboard_file}")
        return dashboard_file


# Example usage
if __name__ == "__main__":
    try:
        # Import crypto risk analyzer for example - rely on top-level import now
        # from quantum_enhanced_crypto_risk import QuantumEnhancedCryptoRiskAnalyzer # Removed local import

        # Create risk analyzer
        # Ensure QuantumEnhancedCryptoRisk is available from top-level import and use correct name
        risk_analyzer = QuantumEnhancedCryptoRisk() # Corrected class name usage

        # Create explainability integrator
        integrator = ExplainabilityIntegrator(output_dir="example_explainability")
        
        # Run enhanced analysis for Bitcoin
        symbol = "BTC"
        enhanced_results = integrator.enhance_crypto_risk_analysis(
            risk_analyzer=risk_analyzer,
            symbol=symbol
        )
        
        # Create dashboard
        dashboard_path = integrator.create_comparative_dashboard(
            symbol=symbol,
            comparison_results=enhanced_results.get("explainability", {})
        )
        
        print(f"Enhanced analysis complete for {symbol}")
        print(f"Dashboard created at: {dashboard_path}")
        
    except ImportError as e:
        print(f"Could not import required modules: {str(e)}")
        print("This example requires the QuantumEnhancedCryptoRisk class.") # Updated message

        # Create a simple example with just the comparison engine
        # Rely on top-level import now
        # from quantum_finance.quantum_bayesian_risk import QuantumBayesianRiskNetwork # Removed local import

        # Initialize the risk network
        # Ensure QuantumBayesianRiskNetwork is available from top-level import
        network = QuantumBayesianRiskNetwork(num_risk_factors=5)

        # Add some relationships
        network.add_conditional_relationship(0, 1, 0.7)
        network.add_conditional_relationship(1, 2, 0.6)
        network.add_conditional_relationship(2, 3, 0.5)
        network.add_conditional_relationship(3, 4, 0.8)
        
        # Create integrator
        integrator = ExplainabilityIntegrator(output_dir="example_explainability")
        
        # Use comparison engine directly
        results = integrator.comparison_engine.run_comparative_analysis(
            symbol="EXAMPLE",
            risk_network=network,
            initial_probabilities=[0.2, 0.3, 0.4, 0.3, 0.5]
        )
        
        # Create dashboard with direct results
        dashboard_path = integrator.create_comparative_dashboard(
            symbol="EXAMPLE",
            comparison_results=results
        )
        
        print("Example analysis complete")
        print(f"Dashboard created at: {dashboard_path}")

    # Run direct usage example - Remove redundant import block
    # from quantum_finance.quantum_bayesian_risk import QuantumBayesianRiskNetwork # Corrected Import # Removed redundant block

    # # Initialize the risk network # Removed redundant block
    # network = QuantumBayesianRiskNetwork(num_risk_factors=5) # Removed redundant block
    # # ... rest of the redundant example code ... # Removed redundant block 