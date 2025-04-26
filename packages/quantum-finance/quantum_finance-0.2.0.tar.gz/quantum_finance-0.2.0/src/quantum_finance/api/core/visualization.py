#!/usr/bin/env python3

"""
Visualization Tools for Quantum-Classical Comparison

This module provides visualization tools for comparing quantum and classical approaches
to financial analysis, making the quantum advantage visually explainable.

Author: Quantum-AI Team
"""

import os
import sys
import logging
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Union, Any, Literal
from datetime import datetime
import io
import base64

# Add project root to path to ensure imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComparisonVisualizer:
    """
    Generates visualizations for quantum-classical comparisons.
    
    This class creates various visualizations to explain the differences between
    quantum and classical approaches to financial analysis, highlighting the
    quantum advantage in an interpretable way.
    
    NOTE (2024-07-26):
    Seaborn only accepts the following styles: 'white', 'dark', 'whitegrid', 'darkgrid', 'ticks'.
    Using any other value (e.g., 'default', 'dark_background') will cause a ValueError.
    The default theme is now set to 'whitegrid' for compatibility and clarity.
    If you want a dark background, use 'darkgrid'.
    """
    
    def __init__(self, theme: Literal['white', 'dark', 'whitegrid', 'darkgrid', 'ticks'] = 'whitegrid', figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize the visualizer.
        
        Args:
            theme: The Seaborn style to use (default: 'whitegrid').
                   Valid options: Literal['white', 'dark', 'whitegrid', 'darkgrid', 'ticks']
            figsize: Default figure size for visualizations
        """
        self.theme = theme
        self.figsize = figsize
        self._setup_style()
        
        logger.info(f"Initialized ComparisonVisualizer with theme '{theme}'")
    
    def _setup_style(self):
        """Set up the visualization style."""
        # Use a valid matplotlib style for plt.style.use if desired, but keep it simple for now
        # plt.style.use(self.theme)  # Commented out to avoid confusion with Seaborn
        
        # Define custom colors for quantum and classical
        self.quantum_color = '#00CCFF'  # Bright cyan for quantum
        self.classical_color = '#FF9500'  # Orange for classical
        self.difference_color = '#FF00CC'  # Magenta for differences
        
        # Set up seaborn with a valid style
        valid_styles = ['white', 'dark', 'whitegrid', 'darkgrid', 'ticks']
        if self.theme not in valid_styles:
            raise ValueError(f"Invalid Seaborn style: {self.theme}. Must be one of {valid_styles}.")
        sns.set_style(self.theme)  # type: ignore[arg-type]
    
    def create_prediction_comparison(self, 
                                    quantum_results: Dict[str, Any], 
                                    classical_results: Dict[str, Any],
                                    title: str = "Quantum vs Classical Prediction Comparison") -> str:
        """
        Generate side-by-side prediction comparison charts.
        
        Args:
            quantum_results: Results from quantum analysis
            classical_results: Results from classical analysis
            title: Title for the visualization
            
        Returns:
            Base64 encoded PNG image of the visualization
        """
        logger.info("Creating prediction comparison visualization")
        
        # TODO: Implement visualization logic
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Placeholder for actual implementation
        ax.text(0.5, 0.5, "Prediction Comparison Visualization\n(Implementation pending)", 
                ha='center', va='center', fontsize=16)
        
        plt.title(title)
        plt.tight_layout()
        
        # Convert to base64 for return
        return self._fig_to_base64(fig)
        
    def create_confidence_interval_plot(self, 
                                      quantum_results: Dict[str, Any], 
                                      classical_results: Dict[str, Any],
                                      title: str = "Confidence Interval Comparison") -> str:
        """
        Generate confidence interval comparison plot.
        
        Args:
            quantum_results: Results from quantum analysis
            classical_results: Results from classical analysis
            title: Title for the visualization
            
        Returns:
            Base64 encoded PNG image of the visualization
        """
        logger.info("Creating confidence interval visualization")
        
        # TODO: Implement visualization logic
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Placeholder for actual implementation
        ax.text(0.5, 0.5, "Confidence Interval Visualization\n(Implementation pending)", 
                ha='center', va='center', fontsize=16)
        
        plt.title(title)
        plt.tight_layout()
        
        # Convert to base64 for return
        return self._fig_to_base64(fig)
        
    def create_divergence_heatmap(self, 
                                comparison_data: Dict[str, Any],
                                title: str = "Quantum-Classical Divergence Heatmap") -> str:
        """
        Create heatmap highlighting differences between quantum and classical approaches.
        
        Args:
            comparison_data: Data containing comparison metrics
            title: Title for the visualization
            
        Returns:
            Base64 encoded PNG image of the visualization
        """
        logger.info("Creating divergence heatmap visualization")
        
        # TODO: Implement visualization logic
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Placeholder for actual implementation
        ax.text(0.5, 0.5, "Divergence Heatmap Visualization\n(Implementation pending)", 
                ha='center', va='center', fontsize=16)
        
        plt.title(title)
        plt.tight_layout()
        
        # Convert to base64 for return
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 encoded string."""
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        img_buf.seek(0)
        img_str = base64.b64encode(img_buf.read()).decode('utf-8')
        plt.close(fig)
        return img_str

# For testing purposes
if __name__ == "__main__":
    print("Comparison Visualizer module")
    print("This module provides visualization tools for quantum-classical comparisons.") 