"""
Risk Explainer for Quantum Financial Analysis

This module provides tools for explaining the outputs of quantum risk assessment models,
breaking down factors that contribute to risk scores and comparing quantum vs classical approaches.

Note on Matplotlib API compatibility:
- This module uses modern Matplotlib API (2.5+) with matplotlib.colormaps[] syntax
- The older cm.get_cmap() method is deprecated and has been replaced

Note on Qiskit deprecation warnings:
- Some Qiskit-related deprecation warnings may appear from the Qiskit library itself
- These include DAGCircuit.duration and DAGCircuit.unit which are deprecated in Qiskit 1.3.0
- These will be removed in Qiskit 2.0.0 and should be addressed in future updates

Author: Quantum-AI Team
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # Still imported for backward compatibility
from typing import Dict, List, Tuple, Optional, Union, Any
import logging
from datetime import datetime
from matplotlib import colors
import matplotlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RiskExplainer:
    """
    Quantum risk assessment explainability framework that breaks down
    contributions from different market factors and provides visualizations
    and natural language explanations.
    
    Key capabilities:
    - Factor contribution analysis (what factors drive the risk)
    - Natural language explanations of risk assessments
    - Comparative analysis (quantum vs classical methods)
    - Visualization of risk factors and temporal patterns
    """
    
    def __init__(self, output_dir: str = 'explainability_results'):
        """
        Initialize the RiskExplainer
        
        Args:
            output_dir: Directory where explanation outputs will be saved
        """
        self.output_dir = output_dir
        self.factor_contributions = {}
        self.explanation_cache = {}
        self.visualization_paths = {}
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Initialized RiskExplainer with output directory: {output_dir}")
    
    def analyze_factor_contributions(self, 
                                     risk_assessment: Dict[str, Any], 
                                     market_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Analyzes how each market factor contributes to the overall risk assessment.
        
        Args:
            risk_assessment: Output from a quantum risk assessment model
            market_data: Market data used for the risk assessment
            
        Returns:
            Dict mapping factors to their contribution percentages
        """
        # Extract risk factors and their probabilities
        risk_factors = risk_assessment.get('risk_factors', {})
        if not risk_factors:
            logger.warning("No risk factors found in risk assessment")
            return {}
            
        # Extract overall risk score
        overall_risk = risk_assessment.get('overall_risk', 0.0)
        
        # Calculate factor contributions through sensitivity analysis
        contributions = {}
        total_contribution = 0.0
        
        # Process each risk factor
        for factor_name, factor_data in risk_factors.items():
            # Extract factor-specific risk
            factor_risk = factor_data.get('risk_score', 0.0)
            
            # Calculate relative importance based on correlation with overall risk
            # and the factor's own risk score
            factor_weight = factor_data.get('weight', 1.0)
            raw_contribution = factor_risk * factor_weight
            
            # Store for normalization
            contributions[factor_name] = raw_contribution
            total_contribution += raw_contribution
        
        # Normalize contributions to percentages
        normalized_contributions = {}
        if total_contribution > 0:
            for factor, contribution in contributions.items():
                normalized_contributions[factor] = (contribution / total_contribution) * 100
        
        # Cache the results
        assessment_id = risk_assessment.get('id', 'unknown')
        self.factor_contributions[assessment_id] = normalized_contributions
        
        logger.info(f"Analyzed factor contributions for assessment {assessment_id}")
        return normalized_contributions
    
    def generate_natural_language_explanation(self, 
                                             risk_assessment: Dict[str, Any],
                                             factor_contributions: Optional[Dict[str, float]] = None) -> str:
        """
        Generates human-readable explanation of risk assessment results.
        
        Args:
            risk_assessment: Output from a quantum risk assessment model
            factor_contributions: Optional pre-calculated factor contributions
            
        Returns:
            String containing natural language explanation
        """
        # Get asset symbol and overall risk
        symbol = risk_assessment.get('symbol', 'unknown')
        overall_risk = risk_assessment.get('overall_risk', 0.0)
        
        # Get factor contributions if not provided
        if not factor_contributions:
            assessment_id = risk_assessment.get('id', 'unknown')
            factor_contributions = self.factor_contributions.get(assessment_id, {})
            if not factor_contributions and 'market_data' in risk_assessment:
                factor_contributions = self.analyze_factor_contributions(
                    risk_assessment, 
                    risk_assessment.get('market_data', {})
                )
        
        # Define risk levels and their explanations
        risk_levels = {
            'very_low': (0, 20, 'very low risk'),
            'low': (20, 40, 'low risk'),
            'moderate': (40, 60, 'moderate risk'),
            'high': (60, 80, 'high risk'),
            'very_high': (80, 100, 'very high risk')
        }
        
        # Determine risk level
        risk_level_name = 'unknown'
        risk_level_text = 'unknown risk'
        for name, (min_val, max_val, text) in risk_levels.items():
            if min_val <= overall_risk < max_val:
                risk_level_name = name
                risk_level_text = text
                break
        
        # Start building the explanation
        explanation = [
            f"Based on quantum analysis, {symbol} currently shows {risk_level_text} "
            f"with an overall risk score of {overall_risk:.1f}%."
        ]
        
        # Add factor contribution information if available
        if factor_contributions:
            # Sort factors by contribution (descending)
            sorted_factors = sorted(
                factor_contributions.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            # Add top factors to explanation
            top_factors = sorted_factors[:3]
            if top_factors:
                explanation.append("The primary risk factors are:")
                for factor_name, contribution in top_factors:
                    # Format factor name for readability
                    readable_name = factor_name.replace('_', ' ').title()
                    explanation.append(f"- {readable_name}: {contribution:.1f}% contribution")
            
            # Mention protective factors (lowest risk contributors)
            if len(sorted_factors) > 3:
                bottom_factors = sorted_factors[-2:]
                explanation.append("Factors showing lower risk levels include:")
                for factor_name, contribution in bottom_factors:
                    readable_name = factor_name.replace('_', ' ').title()
                    explanation.append(f"- {readable_name}: {contribution:.1f}% contribution")
        
        # Add quantum-specific insights if available
        if 'quantum_advantage' in risk_assessment:
            advantage = risk_assessment.get('quantum_advantage', {})
            advantage_metric = advantage.get('value', 0.0)
            if advantage_metric > 0.05:  # Only mention if there's a meaningful advantage
                explanation.append(
                    f"This assessment shows a quantum advantage of {advantage_metric:.2f}, "
                    f"indicating that quantum analysis provides significantly different insights "
                    f"compared to classical methods in this market context."
                )
        
        # Cache explanation
        assessment_id = risk_assessment.get('id', 'unknown')
        self.explanation_cache[assessment_id] = '\n'.join(explanation)
        
        return '\n'.join(explanation)
    
    def create_factor_contribution_chart(self, 
                                        factor_contributions: Dict[str, float], 
                                        title: str = 'Risk Factor Contributions',
                                        output_file: Optional[str] = None) -> str:
        """
        Creates visualization showing relative contributions of different market factors to risk assessment.
        
        Args:
            factor_contributions: Dictionary mapping factors to their contribution percentages
            title: Chart title
            output_file: Optional file path to save the visualization
            
        Returns:
            Path to the saved visualization file
        """
        if not factor_contributions:
            logger.warning("No factor contributions provided for visualization")
            return ""
        
        # Sort factors by contribution (descending)
        sorted_items = sorted(factor_contributions.items(), key=lambda x: x[1], reverse=True)
        factor_names = [item[0].replace('_', ' ').title() for item in sorted_items]
        contribution_values = [item[1] for item in sorted_items]
        
        # Create the figure
        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        
        # Use viridis colormap for the bars
        colors = matplotlib.colormaps['viridis'](np.linspace(0.1, 0.9, len(factor_names)))
        bars = ax.barh(factor_names, contribution_values, color=colors)
        
        # Add percentage labels to bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{width:.1f}%', va='center')
        
        # Set chart title and labels
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Contribution to Risk (%)', fontsize=12)
        ax.set_ylabel('Risk Factors', fontsize=12)
        
        # Adjust grid
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Determine output file path if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_dir, f'risk_factors_{timestamp}.png')
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Created factor contribution chart: {output_file}")
        return output_file
    
    def quantum_vs_classical_comparison(self, 
                                      quantum_risk: Dict[str, Any], 
                                      classical_risk: Dict[str, Any],
                                      output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Compares quantum and classical risk assessments to highlight where
        quantum advantages are most significant.
        
        Args:
            quantum_risk: Quantum risk assessment results
            classical_risk: Classical risk assessment results
            output_file: Optional file path to save the visualization
            
        Returns:
            Dictionary containing comparison metrics and visualization path
        """
        # Extract risk factors from both assessments
        q_factors = quantum_risk.get('risk_factors', {})
        c_factors = classical_risk.get('risk_factors', {})
        
        if not q_factors or not c_factors:
            logger.warning("Missing risk factors in quantum or classical assessment")
            return {'error': 'Insufficient data for comparison'}
        
        # Find common factors
        common_factors = set(q_factors.keys()).intersection(set(c_factors.keys()))
        
        if not common_factors:
            logger.warning("No common risk factors found between assessments")
            return {'error': 'No common risk factors found'}
        
        # Extract risk scores for common factors
        factors = list(common_factors)
        q_scores = [q_factors[f].get('risk_score', 0) for f in factors]
        c_scores = [c_factors[f].get('risk_score', 0) for f in factors]
        
        # Calculate differences and divergence
        differences = [q - c for q, c in zip(q_scores, c_scores)]
        abs_differences = [abs(diff) for diff in differences]
        
        # Calculate overall metrics
        mean_abs_diff = sum(abs_differences) / len(abs_differences)
        max_diff_factor = factors[abs_differences.index(max(abs_differences))]
        
        # Create the visualization
        plt.figure(figsize=(12, 8))
        ax = plt.gca()
        
        # Prepare x-axis positions
        x = np.arange(len(factors))
        width = 0.35
        
        # Create grouped bar chart
        ax.bar(x - width/2, q_scores, width, label='Quantum Assessment', color='blue', alpha=0.7)
        ax.bar(x + width/2, c_scores, width, label='Classical Assessment', color='green', alpha=0.7)
        
        # Add labels and formatting
        factor_labels = [f.replace('_', ' ').title() for f in factors]
        ax.set_xticks(x)
        ax.set_xticklabels(factor_labels, rotation=45, ha='right')
        ax.set_ylabel('Risk Score (%)', fontsize=12)
        ax.set_title('Quantum vs Classical Risk Assessment Comparison', fontsize=14)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add a secondary axis for differences
        ax2 = ax.twinx()
        ax2.plot(x, differences, 'ro-', label='Difference (Q-C)')
        ax2.set_ylabel('Difference (percentage points)', color='red', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.legend(loc='upper right')
        
        # Determine output file path if not provided
        if not output_file:
            symbol = quantum_risk.get('symbol', 'unknown')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, 
                f'{symbol}_quantum_classical_comparison_{timestamp}.png'
            )
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Prepare results
        results = {
            'comparison_metrics': {
                'mean_absolute_difference': mean_abs_diff,
                'max_difference_factor': max_diff_factor,
                'max_difference_value': max(abs_differences),
                'quantum_advantage_score': mean_abs_diff / (sum(q_scores) / len(q_scores)) if sum(q_scores) > 0 else 0
            },
            'visualization_path': output_file
        }
        
        logger.info(f"Created quantum vs classical comparison: {output_file}")
        return results
    
    def create_temporal_risk_evolution(self,
                                     historical_risk_data: List[Dict[str, Any]],
                                     market_events: Optional[List[Dict[str, Any]]] = None,
                                     output_file: Optional[str] = None) -> str:
        """
        Visualizes how risk assessment has evolved over time, with key market events highlighted.
        
        Args:
            historical_risk_data: List of historical risk assessments ordered by time
            market_events: Optional list of market events to highlight on the chart
            output_file: Optional file path to save the visualization
            
        Returns:
            Path to the saved visualization file
        """
        if not historical_risk_data:
            logger.warning("No historical risk data provided for temporal visualization")
            return ""
        
        # Extract timestamps and risk scores
        timestamps = []
        risk_scores = []
        symbol = historical_risk_data[0].get('symbol', 'unknown')
        
        for risk_data in historical_risk_data:
            timestamp_str = risk_data.get('timestamp', '')
            if timestamp_str:
                try:
                    timestamp = pd.to_datetime(timestamp_str)
                    timestamps.append(timestamp)
                    risk_scores.append(risk_data.get('overall_risk', 0.0))
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse timestamp: {timestamp_str}")
        
        if not timestamps:
            logger.warning("No valid timestamps found in historical data")
            return ""
        
        # Create figure
        plt.figure(figsize=(12, 6))
        ax = plt.gca()
        
        # Plot risk evolution
        ax.plot(timestamps, risk_scores, 'b-', linewidth=2)
        ax.fill_between(timestamps, 0, risk_scores, alpha=0.2, color='blue')
        
        # Add risk level bands
        risk_levels = [
            (0, 20, 'Very Low', 'green'),
            (20, 40, 'Low', 'yellowgreen'),
            (40, 60, 'Moderate', 'yellow'),
            (60, 80, 'High', 'orange'),
            (80, 100, 'Very High', 'red')
        ]
        
        # Add color bands for risk levels
        for min_val, max_val, label, color in risk_levels:
            ax.axhspan(min_val, max_val, alpha=0.1, color=color)
            ax.text(timestamps[0], (min_val + max_val) / 2, label, 
                   verticalalignment='center', color=color, alpha=0.8)
        
        # Add market events if provided
        if market_events:
            event_times = []
            event_labels = []
            
            for event in market_events:
                event_time_str = event.get('timestamp', '')
                if event_time_str:
                    try:
                        event_time = pd.to_datetime(event_time_str)
                        event_times.append(event_time)
                        event_labels.append(event.get('description', ''))
                    except (ValueError, TypeError):
                        logger.warning(f"Could not parse event timestamp: {event_time_str}")
            
            if event_times:
                # Find corresponding risk scores for events
                event_scores = []
                for event_time in event_times:
                    idx = 0
                    for i, t in enumerate(timestamps):
                        if abs((t - event_time).total_seconds()) < abs((timestamps[idx] - event_time).total_seconds()):
                            idx = i
                    event_scores.append(risk_scores[idx])
                
                # Plot events
                ax.scatter(event_times, event_scores, color='red', s=80, zorder=5)
                
                # Add event labels
                for i, (time, score, label) in enumerate(zip(event_times, event_scores, event_labels)):
                    # Alternate above/below positioning to avoid overlap
                    vert_pos = 'bottom' if i % 2 == 0 else 'top'
                    vert_offset = 5 if i % 2 == 0 else -5
                    
                    ax.annotate(
                        label, 
                        xy=(time, score),
                        xytext=(0, vert_offset),
                        textcoords='offset points',
                        ha='center',
                        va=vert_pos,
                        fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7)
                    )
        
        # Format the chart
        ax.set_title(f'{symbol} Risk Evolution Over Time', fontsize=14)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Risk Score (%)', fontsize=12)
        ax.set_ylim(0, 100)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Format date axis
        plt.gcf().autofmt_xdate()
        
        # Determine output file path if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, 
                f'{symbol}_risk_evolution_{timestamp}.png'
            )
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Created temporal risk evolution chart: {output_file}")
        return output_file
    
    def save_explanation(self, 
                        risk_assessment: Dict[str, Any], 
                        explanation: str,
                        visualization_paths: Optional[Dict[str, str]] = None) -> str:
        """
        Saves the complete explanation with visualizations to a markdown file.
        
        Args:
            risk_assessment: Risk assessment data
            explanation: Natural language explanation
            visualization_paths: Dictionary of visualization paths
            
        Returns:
            Path to the saved explanation file
        """
        symbol = risk_assessment.get('symbol', 'unknown')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine output file path
        output_file = os.path.join(
            self.output_dir, 
            f'{symbol}_risk_explanation_{timestamp}.md'
        )
        
        # Prepare content
        content = [
            f"# {symbol} Risk Assessment Explanation",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Risk Summary",
            explanation,
            "",
        ]
        
        # Add visualization references if provided
        if visualization_paths:
            content.append("## Visualizations")
            
            for viz_type, viz_path in visualization_paths.items():
                if os.path.exists(viz_path):
                    # Get relative path for markdown
                    rel_path = os.path.relpath(viz_path, os.path.dirname(output_file))
                    title = viz_type.replace('_', ' ').title()
                    content.append(f"### {title}")
                    content.append(f"![]({rel_path})")
                    content.append("")
        
        # Add metadata section
        content.append("## Metadata")
        content.append("```json")
        metadata = {
            "symbol": symbol,
            "timestamp": risk_assessment.get('timestamp', timestamp),
            "overall_risk": risk_assessment.get('overall_risk', 0.0),
            "risk_factors": list(risk_assessment.get('risk_factors', {}).keys()),
            "model_version": risk_assessment.get('model_version', 'unknown')
        }
        content.append(json.dumps(metadata, indent=2))
        content.append("```")
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(content))
        
        logger.info(f"Saved complete explanation to: {output_file}")
        return output_file 