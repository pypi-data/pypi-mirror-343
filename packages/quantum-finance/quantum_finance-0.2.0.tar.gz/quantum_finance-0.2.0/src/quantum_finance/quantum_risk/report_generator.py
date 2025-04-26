#!/usr/bin/env python3

"""
Report Generator for Quantum Risk Assessment

This module generates markdown reports for quantum-enhanced risk analysis results,
providing detailed analysis and visualizations of quantum vs classical risk assessment.

Author: Quantum-AI Team
"""

import os
from datetime import datetime
from typing import Dict, Any, List
import markdown

# Internal relative imports
from quantum_finance.quantum_risk.utils.logging_util import setup_logger

logger = setup_logger(__name__)

class ReportGenerator:
    """
    Report generator for quantum-enhanced risk analysis results.
    """
    
    @staticmethod
    def generate_markdown_report(results: Dict[str, Any]) -> str:
        """
        Generate a markdown report of the quantum-enhanced risk analysis.
        
        Args:
            results: Results from quantum risk analysis
            
        Returns:
            Markdown formatted report file path
        """
        symbol = results['symbol']
        timestamp = results['timestamp']
        report_file = f"{symbol}_quantum_risk_report_{timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write(f"# Quantum-Enhanced Risk Assessment for {symbol}\n\n")
            f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write(f"Current {symbol} price: ${results['current_price']:.2f}\n\n")
            
            # Create a summary table
            f.write("| Risk Metric | Classical | Quantum-Enhanced | Difference |\n")
            f.write("|-------------|-----------|------------------|------------|\n")
            
            for metric in ['overall_risk', 'liquidity_risk', 'volatility_risk', 'market_depth_risk']:
                classical = results['classical_risk'][metric]
                quantum = results['quantum_enhanced_risk'][metric]
                diff = results['risk_differences'][metric]
                
                # Determine if risk increased or decreased with quantum model
                impact = "↑" if diff > 0 else "↓"
                
                f.write(f"| {metric.replace('_', ' ').title()} | {classical:.2f}% | {quantum:.2f}% | {impact} {abs(diff):.2f}% |\n")
            
            f.write("\n## Market Microstructure Metrics\n\n")
            f.write(f"- **Bid-Ask Spread:** {results['market_metrics']['bid_ask_spread']*100:.4f}%\n")
            f.write(f"- **Daily Volatility:** {results['market_metrics']['volatility']*100:.2f}%\n")
            f.write(f"- **Order Book Depth:** {results['market_metrics']['normalized_depth']*100:.2f}% of reference\n")
            f.write(f"- **Order Book Imbalance:** {results['market_metrics']['imbalance']*100:.2f}%\n")
            f.write(f"- **Price Impact (10 {symbol}):** {results['market_metrics']['price_impact']*100:.4f}%\n")
            f.write(f"- **Trading Volume:** {results['market_metrics']['normalized_volume']*100:.2f}% of reference\n\n")
            
            f.write("## Quantum Analysis Visualizations\n\n")
            
            # Add visualization images if files exist
            for name, file in results['visualizations'].items():
                if os.path.exists(file):
                    f.write(f"### {name.replace('_', ' ').title()}\n\n")
                    f.write(f"![{name}]({file})\n\n")
            
            f.write("## Methodology\n\n")
            f.write("This analysis uses quantum computing techniques to enhance cryptocurrency risk assessment:\n\n")
            f.write("1. **Quantum Bayesian Network:** Models dependencies between risk factors using quantum entanglement and interference\n")
            f.write("2. **Quantum Market Encoding:** Represents market microstructure data as quantum states\n")
            f.write("3. **Uncertainty Propagation:** Uses quantum principles for more accurate risk propagation\n")
            f.write("4. **Classical Comparison:** Compares quantum results with classical calculation methods\n\n")
            
            f.write("## Interpretation\n\n")
            
            # Generate simple interpretation based on results
            overall_diff = results['risk_differences']['overall_risk']
            
            if abs(overall_diff) < 1.0:
                f.write("The quantum model shows similar overall risk assessment to the classical model, ")
                f.write("suggesting that in the current market conditions, quantum uncertainty considerations ")
                f.write("do not significantly alter the risk profile.\n\n")
            elif overall_diff > 0:
                f.write("The quantum model indicates **higher overall risk** than the classical model. ")
                f.write("This suggests that quantum uncertainty propagation is capturing potential risks ")
                f.write("that classical models may underestimate in the current market conditions.\n\n")
                f.write("Recommendations: Consider more conservative positions and increased hedging.\n\n")
            else:
                f.write("The quantum model indicates **lower overall risk** than the classical model. ")
                f.write("This suggests that classical models may be overestimating certain risks ")
                f.write("due to inadequate modeling of the correlations between market factors.\n\n")
                f.write("Recommendations: Current market conditions may present opportunities for strategic positions.\n\n")
        
        logger.info(f"Report generated: {report_file}")
        return report_file
    
    @staticmethod
    def generate_summary(results: Dict[str, Any]) -> List[str]:
        """
        Generate a summary of analysis results in a format suitable for terminal output.
        
        Args:
            results: Results from quantum risk analysis
            
        Returns:
            List of summary strings
        """
        summary = []
        summary.append(f"- Current price: ${results['current_price']:.2f}")
        summary.append(f"- Classical overall risk: {results['classical_risk']['overall_risk']:.2f}%")
        summary.append(f"- Quantum-enhanced overall risk: {results['quantum_enhanced_risk']['overall_risk']:.2f}%")
        
        diff = results['risk_differences']['overall_risk']
        summary.append(f"- Risk difference: {'+' if diff > 0 else ''}{diff:.2f}%")
        
        summary.append("\nVisualization files generated:")
        for name, file in results['visualizations'].items():
            summary.append(f"- {name}: {file}")
            
        return summary 