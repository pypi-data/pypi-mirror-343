"""
Real-time visualization module for monitoring meta-optimizer performance metrics.
This module provides interactive plotting capabilities to track training progress
and meta-optimizer behavior during quantum circuit optimization.

Features:
- Real-time metric visualization
- Interactive plot updates
- Multi-metric comparison
- Automatic plot saving
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import Dict, List, Optional
import logging
from pathlib import Path
import time
from IPython.display import clear_output

class MetaOptimizerVisualizer:
    def __init__(self, 
                 update_interval: float = 1.0,
                 save_dir: str = "visualization_output",
                 max_points: int = 100):
        """
        Initialize the visualizer for meta-optimizer metrics.
        
        Args:
            update_interval: Time between plot updates in seconds
            save_dir: Directory to save plot images
            max_points: Maximum number of points to show in plots
        """
        self.update_interval = update_interval
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True, parents=True)
        self.max_points = max_points
        
        # Setup plotting
        plt.ion()  # Enable interactive mode
        self.fig = plt.figure(figsize=(15, 10))
        self.setup_plots()
        
        # Initialize metric storage
        self.metrics_history = {
            'loss_values': [],
            'update_norms': [],
            'param_norms': [],
            'dampening_values': [],
            'learning_rates': [],
            'gradient_norms': []
        }
        
        self.last_update = time.time()
        self.is_notebook = self._check_if_notebook()
        
    def _check_if_notebook(self) -> bool:
        """Check if code is running in Jupyter notebook."""
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True
            return False
        except NameError:
            return False
        
    def setup_plots(self):
        """Initialize the subplot layout."""
        # Loss plot
        self.ax1 = self.fig.add_subplot(231)
        self.ax1.set_title('Loss History')
        self.ax1.set_xlabel('Step')
        self.ax1.set_ylabel('Loss')
        self.ax1.grid(True)
        
        # Parameter norm plot
        self.ax2 = self.fig.add_subplot(232)
        self.ax2.set_title('Parameter Norm')
        self.ax2.set_xlabel('Step')
        self.ax2.set_ylabel('Norm')
        self.ax2.grid(True)
        
        # Update norm plot
        self.ax3 = self.fig.add_subplot(233)
        self.ax3.set_title('Update Norm')
        self.ax3.set_xlabel('Step')
        self.ax3.set_ylabel('Norm')
        self.ax3.grid(True)
        
        # Dampening plot
        self.ax4 = self.fig.add_subplot(234)
        self.ax4.set_title('Adaptive Dampening')
        self.ax4.set_xlabel('Step')
        self.ax4.set_ylabel('Dampening Factor')
        self.ax4.grid(True)
        
        # Learning rate plot
        self.ax5 = self.fig.add_subplot(235)
        self.ax5.set_title('Learning Rate')
        self.ax5.set_xlabel('Step')
        self.ax5.set_ylabel('Learning Rate')
        self.ax5.grid(True)
        
        # Gradient norm plot
        self.ax6 = self.fig.add_subplot(236)
        self.ax6.set_title('Gradient Norm')
        self.ax6.set_xlabel('Step')
        self.ax6.set_ylabel('Norm')
        self.ax6.grid(True)
        
        plt.tight_layout()
        
    def update_metrics(self, 
                      metrics: Dict[str, List[float]], 
                      current_lr: Optional[float] = None,
                      current_grad_norm: Optional[float] = None):
        """
        Update stored metrics and refresh plots if enough time has passed.
        
        Args:
            metrics: Dictionary of current meta-optimizer metrics
            current_lr: Current learning rate
            current_grad_norm: Current gradient norm
        """
        # Update stored metrics
        for key, values in metrics.items():
            if values:
                self.metrics_history[key].append(values[-1])
                if len(self.metrics_history[key]) > self.max_points:
                    self.metrics_history[key] = self.metrics_history[key][-self.max_points:]
        
        if current_lr is not None:
            self.metrics_history['learning_rates'].append(current_lr)
            if len(self.metrics_history['learning_rates']) > self.max_points:
                self.metrics_history['learning_rates'] = self.metrics_history['learning_rates'][-self.max_points:]
                
        if current_grad_norm is not None:
            self.metrics_history['gradient_norms'].append(current_grad_norm)
            if len(self.metrics_history['gradient_norms']) > self.max_points:
                self.metrics_history['gradient_norms'] = self.metrics_history['gradient_norms'][-self.max_points:]
        
        # Check if it's time to update plots
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.refresh_plots()
            self.last_update = current_time
            
    def refresh_plots(self):
        """Update all plot contents."""
        # Clear previous plots
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6]:
            ax.clear()
            ax.grid(True)
        
        # Update loss plot
        if self.metrics_history['loss_values']:
            self.ax1.plot(self.metrics_history['loss_values'], 'b-')
            self.ax1.set_title('Loss History')
            self.ax1.set_yscale('log')
        
        # Update parameter norm plot
        if self.metrics_history['param_norms']:
            self.ax2.plot(self.metrics_history['param_norms'], 'g-')
            self.ax2.set_title('Parameter Norm')
        
        # Update update norm plot
        if self.metrics_history['update_norms']:
            self.ax3.plot(self.metrics_history['update_norms'], 'r-')
            self.ax3.set_title('Update Norm')
            self.ax3.set_yscale('log')
        
        # Update dampening plot
        if self.metrics_history['dampening_values']:
            self.ax4.plot(self.metrics_history['dampening_values'], 'm-')
            self.ax4.set_title('Adaptive Dampening')
        
        # Update learning rate plot
        if self.metrics_history['learning_rates']:
            self.ax5.plot(self.metrics_history['learning_rates'], 'c-')
            self.ax5.set_title('Learning Rate')
            self.ax5.set_yscale('log')
        
        # Update gradient norm plot
        if self.metrics_history['gradient_norms']:
            self.ax6.plot(self.metrics_history['gradient_norms'], 'y-')
            self.ax6.set_title('Gradient Norm')
            self.ax6.set_yscale('log')
        
        plt.tight_layout()
        
        # Handle display based on environment
        if self.is_notebook:
            clear_output(wait=True)
            plt.show()
        else:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        
        # Save current plot
        self.save_current_plot()
        
    def save_current_plot(self):
        """Save the current plot state."""
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = self.save_dir / f"training_metrics_{timestamp}.png"
            
            # Ensure the directory exists
            self.save_dir.mkdir(parents=True, exist_ok=True)
            
            # Save with high quality
            self.fig.savefig(
                save_path,
                dpi=300,
                bbox_inches='tight',
                pad_inches=0.1,
                facecolor='white',
                edgecolor='none'
            )
            
            logging.info(f"Plot saved to: {save_path}")
            
        except Exception as e:
            logging.error(f"Error saving plot: {str(e)}")
        
    def close(self):
        """Clean up resources."""
        plt.close(self.fig)
        plt.ioff()  # Disable interactive mode


def create_visualizer(update_interval: float = 1.0,
                     save_dir: str = "visualization_output",
                     max_points: int = 100) -> MetaOptimizerVisualizer:
    """
    Factory function to create and return a MetaOptimizerVisualizer instance.
    
    Args:
        update_interval: Time between plot updates in seconds
        save_dir: Directory to save plot images
        max_points: Maximum number of points to show in plots
        
    Returns:
        MetaOptimizerVisualizer: Configured visualizer instance
    """
    return MetaOptimizerVisualizer(
        update_interval=update_interval,
        save_dir=save_dir,
        max_points=max_points
    ) 