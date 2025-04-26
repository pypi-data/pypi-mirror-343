"""
Risk Visualization Component for Quantum Financial Analysis

This module provides advanced visualization tools for quantum risk assessments,
offering interactive and informative visual representations of risk data.

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
import matplotlib.dates as mdates
from typing import Dict, List, Tuple, Optional, Union, Any
import logging
from datetime import datetime
from matplotlib import colors
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RiskVisualization:
    """
    Advanced visualization components for quantum risk assessments, 
    focusing on factor contribution, temporal patterns, and comparative analysis.
    
    Key capabilities:
    - Interactive risk factor dashboards
    - Historical risk evolution visualization
    - Quantum vs. classical comparison charts
    - Risk distribution heatmaps
    """
    
    def __init__(self, output_dir: str = 'risk_visualization_results'):
        """
        Initialize the RiskVisualization component
        
        Args:
            output_dir: Directory where visualization outputs will be saved
        """
        self.output_dir = output_dir
        self.visualization_paths = {}
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Initialized RiskVisualization with output directory: {output_dir}")
    
    def create_risk_distribution_heatmap(self,
                                       risk_data: Dict[str, Any],
                                       output_file: Optional[str] = None) -> str:
        """
        Creates a heatmap visualization of risk distributions across factors.
        
        Args:
            risk_data: Risk assessment data containing risk factors
            output_file: Optional file path to save the visualization
            
        Returns:
            Path to the saved visualization file
        """
        # Extract risk factors and their scores
        risk_factors = risk_data.get('risk_factors', {})
        if not risk_factors:
            logger.warning("No risk factors found in risk data")
            return ""
        
        # Create a matrix of risk distributions
        factor_names = list(risk_factors.keys())
        factor_scores = [risk_factors[f].get('risk_score', 0) for f in factor_names]
        
        # Create readable labels
        readable_names = [name.replace('_', ' ').title() for name in factor_names]
        
        # Get overall risk
        overall_risk = risk_data.get('overall_risk', 0.0)
        symbol = risk_data.get('symbol', 'unknown')
        
        # Create figure
        plt.figure(figsize=(10, 8))
        ax = plt.gca()
        
        # Define risk level colors
        cmap = matplotlib.colormaps['RdYlGn_r']  # Red-Yellow-Green reversed (red is high risk)
        
        # Create horizontal bar chart with color gradient based on risk level
        y_pos = np.arange(len(readable_names))
        bars = ax.barh(y_pos, factor_scores, align='center')
        
        # Color bars based on risk score
        for i, bar in enumerate(bars):
            bar.set_color(cmap(factor_scores[i]/100))
        
        # Add a reference line for overall risk
        ax.axvline(x=overall_risk, color='blue', linestyle='--', 
                  alpha=0.7, label=f'Overall Risk ({overall_risk:.1f}%)')
        
        # Add risk zones (color bands)
        risk_zones = [
            (0, 20, 'Very Low', 'green'),
            (20, 40, 'Low', 'yellowgreen'),
            (40, 60, 'Moderate', 'yellow'),
            (60, 80, 'High', 'orange'),
            (80, 100, 'Very High', 'red')
        ]
        
        # Add zone labels at the top
        for min_val, max_val, label, color in risk_zones:
            ax.axvspan(min_val, max_val, alpha=0.1, color=color)
            mid_point = (min_val + max_val) / 2
            ax.text(mid_point, len(readable_names) + 0.2, label, 
                   ha='center', va='bottom', color=color, fontweight='bold')
        
        # Add score labels to the end of each bar
        for i, score in enumerate(factor_scores):
            ax.text(score + 1, i, f'{score:.1f}%', va='center')
        
        # Set chart title and labels
        ax.set_title(f'{symbol} Risk Factor Distribution', fontsize=14)
        ax.set_xlabel('Risk Score (%)', fontsize=12)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(readable_names)
        ax.set_xlim(0, 105)  # Allow space for labels
        
        # Add grid
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Add legend
        ax.legend()
        
        # Determine output file path if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, 
                f'{symbol}_risk_distribution_{timestamp}.png'
            )
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Created risk distribution heatmap: {output_file}")
        return output_file
    
    def create_risk_correlation_network(self,
                                      risk_data: Dict[str, Any],
                                      correlation_matrix: Optional[np.ndarray] = None,
                                      output_file: Optional[str] = None) -> str:
        """
        Creates a network visualization showing correlations between risk factors.
        
        Args:
            risk_data: Risk assessment data containing risk factors
            correlation_matrix: Optional correlation matrix between factors
            output_file: Optional file path to save the visualization
            
        Returns:
            Path to the saved visualization file
        """
        try:
            import networkx as nx
        except ImportError:
            logger.error("NetworkX library is required for correlation network visualization")
            return ""
        
        # Extract risk factors
        risk_factors = risk_data.get('risk_factors', {})
        if not risk_factors:
            logger.warning("No risk factors found in risk data")
            return ""
        
        factor_names = list(risk_factors.keys())
        readable_names = [name.replace('_', ' ').title() for name in factor_names]
        factor_scores = [risk_factors[f].get('risk_score', 0) for f in factor_names]
        
        # If correlation matrix not provided, create a dummy one based on scores
        if correlation_matrix is None:
            n_factors = len(factor_names)
            correlation_matrix = np.zeros((n_factors, n_factors))
            
            # Create some meaningful correlations based on risk scores
            for i in range(n_factors):
                for j in range(n_factors):
                    if i == j:
                        correlation_matrix[i, j] = 1.0
                    else:
                        # Create correlation based on how close the risk scores are
                        score_diff = abs(factor_scores[i] - factor_scores[j]) / 100
                        correlation_matrix[i, j] = max(0, 1 - score_diff)
        
        # Create graph
        G = nx.Graph()
        
        # Add nodes with risk scores as attributes
        for i, name in enumerate(readable_names):
            G.add_node(name, risk_score=factor_scores[i])
        
        # Add edges with correlations as weights
        for i in range(len(readable_names)):
            for j in range(i+1, len(readable_names)):  # Only add each edge once
                # Only add edges with meaningful correlations
                if correlation_matrix[i, j] >= 0.2:
                    G.add_edge(
                        readable_names[i], 
                        readable_names[j], 
                        weight=correlation_matrix[i, j]
                    )
        
        # Create figure and axes - a simpler approach avoiding constrained_layout issues
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Get positions using spring layout
        pos = nx.spring_layout(G, seed=42)
        
        # Define color map for nodes based on risk score
        cmap = matplotlib.colormaps['RdYlGn_r']
        node_colors = [cmap(G.nodes[node]['risk_score']/100) for node in G.nodes()]
        
        # Define node sizes based on risk score
        node_sizes = [300 + (G.nodes[node]['risk_score'] * 5) for node in G.nodes()]
        
        # Get edge weights for line thickness
        edge_weights = [G[u][v]['weight'] * 3 for u, v in G.edges()]
        
        # Draw the graph
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray')
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # Add title
        symbol = risk_data.get('symbol', 'unknown')
        plt.title(f'{symbol} Risk Factor Correlation Network', fontsize=16)
        
        # Remove axis
        plt.axis('off')
        
        # Add a colorbar - using a simpler approach
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=colors.Normalize(0, 100))
        sm.set_array([])
        
        # Create a colorbar in its own axis space - standard approach
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        cbar = plt.colorbar(sm, cax=cax)
        cbar.set_label('Risk Level')
        
        # Determine output file path if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, 
                f'{symbol}_risk_network_{timestamp}.png'
            )
        
        # Save figure without tight_layout - adjusted to prevent warnings
        plt.subplots_adjust(right=0.85)  # Make room for colorbar
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Created risk correlation network: {output_file}")
        return output_file
    
    def create_multi_asset_comparison(self,
                                    risk_data_list: List[Dict[str, Any]],
                                    factors_to_include: Optional[List[str]] = None,
                                    output_file: Optional[str] = None) -> str:
        """
        Creates a comparison chart for multiple assets, showing risk profiles side by side.
        
        Args:
            risk_data_list: List of risk assessment data for different assets
            factors_to_include: Optional list of specific factors to include
            output_file: Optional file path to save the visualization
            
        Returns:
            Path to the saved visualization file
        """
        if not risk_data_list:
            logger.warning("No risk data provided for multi-asset comparison")
            return ""
        
        # Extract symbols and prepare data
        symbols = []
        overall_risks = []
        factor_data = {}
        
        for risk_data in risk_data_list:
            symbol = risk_data.get('symbol', 'unknown')
            symbols.append(symbol)
            overall_risks.append(risk_data.get('overall_risk', 0))
            
            # Extract factor data
            risk_factors = risk_data.get('risk_factors', {})
            for factor, data in risk_factors.items():
                if factors_to_include and factor not in factors_to_include:
                    continue
                
                if factor not in factor_data:
                    factor_data[factor] = []
                
                factor_data[factor].append(data.get('risk_score', 0))
        
        # Ensure all factors have data for all symbols
        for factor in factor_data:
            if len(factor_data[factor]) < len(symbols):
                # Fill missing values with zeros
                factor_data[factor].extend([0] * (len(symbols) - len(factor_data[factor])))
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[1, 2])
        
        # Plot overall risk comparison in first subplot
        x = np.arange(len(symbols))
        bars = ax1.bar(x, overall_risks, width=0.6, alpha=0.7)
        
        # Color bars based on risk level
        cmap = matplotlib.colormaps['RdYlGn_r']
        for i, bar in enumerate(bars):
            bar.set_color(cmap(overall_risks[i]/100))
        
        # Add risk score labels
        for i, v in enumerate(overall_risks):
            ax1.text(i, v + 2, f'{v:.1f}%', ha='center')
        
        # Add risk zones
        for min_val, max_val, label, color in [
            (0, 20, 'Very Low', 'green'),
            (20, 40, 'Low', 'yellowgreen'),
            (40, 60, 'Moderate', 'yellow'),
            (60, 80, 'High', 'orange'),
            (80, 100, 'Very High', 'red')
        ]:
            ax1.axhspan(min_val, max_val, alpha=0.1, color=color)
        
        # Configure first subplot
        ax1.set_title('Overall Risk Comparison', fontsize=14)
        ax1.set_xticks(x)
        ax1.set_xticklabels(symbols)
        ax1.set_ylabel('Overall Risk (%)')
        ax1.set_ylim(0, 105)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Plot factor comparison in second subplot
        # Convert factor data to DataFrame for easier plotting
        factor_df = pd.DataFrame(factor_data, index=symbols)
        
        # Create readable factor names
        readable_factors = [f.replace('_', ' ').title() for f in factor_df.columns]
        
        # Plot grouped bar chart
        factor_df.plot(kind='bar', ax=ax2, width=0.8, colormap='viridis')
        
        # Configure second subplot
        ax2.set_title('Risk Factor Comparison', fontsize=14)
        ax2.set_xticklabels(symbols, rotation=0)
        ax2.set_ylabel('Risk Score (%)')
        ax2.set_ylim(0, 105)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.legend(readable_factors, loc='upper right')
        
        # Determine output file path if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, 
                f'multi_asset_comparison_{timestamp}.png'
            )
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Created multi-asset comparison chart: {output_file}")
        return output_file
    
    def create_risk_dashboard(self,
                            risk_data: Dict[str, Any],
                            historical_data: Optional[List[Dict[str, Any]]] = None,
                            market_events: Optional[List[Dict[str, Any]]] = None,
                            output_file: Optional[str] = None) -> str:
        """
        Creates a comprehensive dashboard combining multiple visualizations.
        
        Args:
            risk_data: Current risk assessment data
            historical_data: Optional historical risk assessments
            market_events: Optional market events to highlight
            output_file: Optional file path to save the visualization
            
        Returns:
            Path to the saved dashboard file
        """
        symbol = risk_data.get('symbol', 'unknown')
        overall_risk = risk_data.get('overall_risk', 0.0)
        
        # Create figure with multiple subplots
        fig = plt.figure(figsize=(15, 12))
        
        # Define grid layout
        gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.5])
        
        # Risk gauge (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        self._create_risk_gauge(ax1, overall_risk, symbol)
        
        # Risk factor distribution (top right)
        ax2 = fig.add_subplot(gs[0, 1])
        self._create_factor_distribution(ax2, risk_data)
        
        # Historical evolution (bottom)
        ax3 = fig.add_subplot(gs[1, :])
        if historical_data:
            self._create_historical_evolution(ax3, historical_data, market_events)
        else:
            ax3.text(0.5, 0.5, 'No historical data available', 
                    ha='center', va='center', fontsize=14)
            ax3.axis('off')
        
        # Add dashboard title
        fig.suptitle(f'{symbol} Risk Assessment Dashboard', fontsize=16, y=0.98)
        
        # Add timestamp
        timestamp = risk_data.get('timestamp', datetime.now().isoformat())
        try:
            dt = pd.to_datetime(timestamp)
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            time_str = str(timestamp)
            
        fig.text(0.5, 0.01, f'Generated: {time_str}', ha='center', fontsize=10)
        
        # Add quantum advantage indicator if available
        if 'quantum_advantage' in risk_data:
            advantage = risk_data.get('quantum_advantage', {})
            advantage_value = advantage.get('value', 0.0)
            if advantage_value > 0:
                fig.text(0.01, 0.01, 
                        f'Quantum Advantage: {advantage_value:.2f}', 
                        fontsize=10, color='blue')
        
        # Determine output file path if not provided
        if not output_file:
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, 
                f'{symbol}_risk_dashboard_{timestamp_str}.png'
            )
        
        # Save figure
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust for title and footer
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Created risk dashboard: {output_file}")
        return output_file
    
    def _create_risk_gauge(self, ax, risk_value, symbol):
        """Helper method to create a risk gauge visualization"""
        import matplotlib.patches as patches
        
        # Create gauge
        gauge_colors = [
            (0, 0.2, 'green'),
            (0.2, 0.4, 'yellowgreen'),
            (0.4, 0.6, 'yellow'),
            (0.6, 0.8, 'orange'),
            (0.8, 1.0, 'red')
        ]
        
        # Draw gauge background
        for i, (start, end, color) in enumerate(gauge_colors):
            angle_start = np.pi * (0.75 + start * 1.5)
            angle_end = np.pi * (0.75 + end * 1.5)
            
            # Create wedge
            wedge = patches.Wedge(
                center=(0.5, 0.5),
                r=0.4,
                theta1=np.degrees(angle_start),
                theta2=np.degrees(angle_end),
                facecolor=color,
                alpha=0.7,
                width=0.2
            )
            ax.add_patch(wedge)
        
        # Add risk level labels
        risk_labels = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
        angles = np.linspace(np.pi * 0.75, np.pi * 2.25, len(risk_labels) + 1)[:-1]
        radius = 0.45
        
        for angle, label in zip(angles, risk_labels):
            x = 0.5 + radius * np.cos(angle)
            y = 0.5 + radius * np.sin(angle)
            ax.text(x, y, label, ha='center', va='center', fontsize=8, 
                   rotation=np.degrees(angle) - 90)
        
        # Convert risk value to angle
        risk_norm = risk_value / 100.0
        angle = np.pi * (0.75 + risk_norm * 1.5)
        
        # Draw needle
        needle_x = 0.5 + 0.35 * np.cos(angle)
        needle_y = 0.5 + 0.35 * np.sin(angle)
        ax.plot([0.5, needle_x], [0.5, needle_y], 'k-', linewidth=2)
        
        # Add central circle
        central_circle = patches.Circle((0.5, 0.5), 0.03, facecolor='black')
        ax.add_patch(central_circle)
        
        # Add risk value text
        ax.text(0.5, 0.25, f'{risk_value:.1f}%', ha='center', va='center', 
               fontsize=16, fontweight='bold')
        
        # Set title and remove axis
        ax.set_title(f'{symbol} Risk Level', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    def _create_factor_distribution(self, ax, risk_data):
        """Helper method to create a factor distribution visualization"""
        # Extract risk factors
        risk_factors = risk_data.get('risk_factors', {})
        if not risk_factors:
            ax.text(0.5, 0.5, 'No risk factor data available', 
                   ha='center', va='center', fontsize=14)
            ax.axis('off')
            return
        
        # Create readable labels and sort by risk score
        items = [(k.replace('_', ' ').title(), v.get('risk_score', 0)) 
                for k, v in risk_factors.items()]
        items.sort(key=lambda x: x[1], reverse=True)
        
        factor_names = [item[0] for item in items]
        factor_scores = [item[1] for item in items]
        
        # Create horizontal bars
        y_pos = np.arange(len(factor_names))
        cmap = matplotlib.colormaps['RdYlGn_r']
        
        bars = ax.barh(y_pos, factor_scores, align='center')
        
        # Color bars based on risk score
        for i, bar in enumerate(bars):
            bar.set_color(cmap(factor_scores[i]/100))
            
        # Add labels
        for i, score in enumerate(factor_scores):
            ax.text(score + 1, i, f'{score:.1f}%', va='center')
        
        # Set labels and title
        ax.set_yticks(y_pos)
        ax.set_yticklabels(factor_names)
        ax.invert_yaxis()  # Labels read top-to-bottom
        ax.set_xlabel('Risk Score (%)')
        ax.set_title('Risk Factor Distribution', fontsize=14)
        ax.set_xlim(0, 105)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    def _create_historical_evolution(self, ax, historical_data, market_events=None):
        """Helper method to create a historical evolution visualization"""
        if not historical_data:
            ax.text(0.5, 0.5, 'No historical data available', 
                   ha='center', va='center', fontsize=14)
            ax.axis('off')
            return
        
        # Extract timestamps and risk scores
        timestamps = []
        risk_scores = []
        symbol = historical_data[0].get('symbol', 'unknown')
        
        for risk_data in historical_data:
            timestamp_str = risk_data.get('timestamp', '')
            if timestamp_str:
                try:
                    timestamp = pd.to_datetime(timestamp_str)
                    timestamps.append(timestamp)
                    risk_scores.append(risk_data.get('overall_risk', 0.0))
                except (ValueError, TypeError):
                    pass
        
        if not timestamps:
            ax.text(0.5, 0.5, 'No valid timestamps in historical data', 
                   ha='center', va='center', fontsize=14)
            ax.axis('off')
            return
        
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
                        pass
            
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
        ax.set_xlabel('Date')
        ax.set_ylabel('Risk Score (%)')
        ax.set_ylim(0, 100)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Format date axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator()) 