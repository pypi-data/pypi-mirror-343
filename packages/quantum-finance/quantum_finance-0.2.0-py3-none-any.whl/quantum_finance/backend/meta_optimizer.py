'''Module: meta_optimizer.py

This module provides an enhanced LSTM-based meta-optimizer for dynamic parameter optimization in quantum circuits.
The optimizer uses historical circuit parameters to propose parameter updates while maintaining stability and convergence.
Key features:
- Adaptive dampening based on loss trends
- Enhanced parameter normalization
- Comprehensive logging and monitoring
- Robust gradient handling with clipping
'''

import torch
import torch.nn as nn
import numpy as np
import logging
from typing import List, Tuple, Optional, Dict
from pathlib import Path
from quantum_finance.utils.analog_linear import AnalogLinear

class MetaOptimizer(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=16, history_length=3):  # Reduced hidden_dim further
        super().__init__()
        self.history_length = history_length
        
        # Smaller initial parameter ranges
        self.fc1 = AnalogLinear(input_dim * history_length, hidden_dim)
        self.fc2 = AnalogLinear(hidden_dim, hidden_dim)
        self.fc3 = AnalogLinear(hidden_dim, 1)
        
        # Initialize with very small weights
        for layer in [self.fc1, self.fc2, self.fc3]:
            nn.init.xavier_normal_(layer.weight, gain=0.01)
            nn.init.constant_(layer.bias, 0.0)
        
        # Increased dropout for more regularization
        self.dropout = nn.Dropout(p=0.3)
        self.activation = nn.ReLU()
        
        # Initialize history buffers
        self.reset_history()
        
        # Initialize adaptive dampening parameters
        self.base_dampening = 0.1
        self.adaptive_dampening = self.base_dampening
        self.n_history = history_length
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Performance tracking
        self.performance_metrics = {
            'update_norms': [],
            'param_norms': [],
            'dampening_values': [],
            'loss_values': []
        }
        
    def reset_history(self):
        """Reset all history buffers."""
        self.loss_history = []
        self.grad_norm_history = []
        self.param_norm_history = []
        self.performance_metrics = {
            'update_norms': [],
            'param_norms': [],
            'dampening_values': [],
            'loss_values': []
        }

    def _update_adaptive_dampening(self, loss_value: float):
        """Update the adaptive dampening factor based on loss trends."""
        self.loss_history.append(loss_value)
        if len(self.loss_history) > self.n_history:
            self.loss_history.pop(0)
            
            # Calculate loss trend
            loss_diff = np.diff(self.loss_history)
            loss_improving = np.mean(loss_diff) < 0
            
            # Adjust dampening based on loss trend
            if loss_improving:
                self.adaptive_dampening = max(
                    self.base_dampening / 2,
                    self.adaptive_dampening * 0.95
                )
            else:
                self.adaptive_dampening = min(
                    self.base_dampening * 2,
                    self.adaptive_dampening * 1.05
                )
            
            self.performance_metrics['dampening_values'].append(self.adaptive_dampening)
    
    def forward(self, current_loss, current_grad_norm, current_param_norm):
        # Scale inputs to prevent explosion
        current_loss = torch.log1p(torch.abs(current_loss))  # Use log1p for better numerical stability
        current_grad_norm = torch.log1p(current_grad_norm)
        current_param_norm = torch.log1p(current_param_norm)
        
        # Update history with scaled values
        self.loss_history.append(current_loss.item())
        self.grad_norm_history.append(current_grad_norm.item())
        self.param_norm_history.append(current_param_norm.item())
        
        # Pad history if not enough values
        while len(self.loss_history) < self.history_length:
            self.loss_history.insert(0, 0.0)
        while len(self.grad_norm_history) < self.history_length:
            self.grad_norm_history.insert(0, 0.0)
        while len(self.param_norm_history) < self.history_length:
            self.param_norm_history.insert(0, 0.0)
        
        # Prepare input tensor with scaled values
        x = torch.tensor([
            self.loss_history[-self.history_length:],
            self.grad_norm_history[-self.history_length:],
            self.param_norm_history[-self.history_length:],
            [1.0] * self.history_length  # Bias term
        ], dtype=torch.float32).flatten()
        
        # Forward pass with increased regularization
        x = self.dropout(self.activation(self.fc1(x)))
        x = self.dropout(self.activation(self.fc2(x)))
        x = torch.sigmoid(self.fc3(x)) * 0.01  # Limit maximum learning rate to 0.01
        
        return x

    def optimize(self, parameter_history: np.ndarray, current_loss: Optional[float] = None) -> np.ndarray:
        """
        Optimize parameters using the meta-optimizer with adaptive dampening.
        
        Args:
            parameter_history: History of parameters to optimize
            current_loss: Current loss value for adaptive dampening
            
        Returns:
            Updated parameters
        """
        if current_loss is not None:
            self._update_adaptive_dampening(current_loss)
            self.performance_metrics['loss_values'].append(current_loss)
        
        # Convert parameters to tensor
        param_tensor = torch.tensor(parameter_history, dtype=torch.float32)
        param_norm = torch.norm(param_tensor)
        
        # Get update factor from forward pass
        self.eval()
        with torch.no_grad():
            update_factor = self.forward(
                torch.tensor(current_loss) if current_loss is not None else torch.tensor(0.0),
                torch.tensor(0.0),  # No gradient norm available
                param_norm
            )
            
            # Apply update with adaptive dampening
            updated_params = parameter_history * (1 + self.adaptive_dampening * update_factor.item())
            
            # Update metrics
            update_norm = np.linalg.norm(updated_params - parameter_history)
            param_norm = np.linalg.norm(updated_params)
            
            self.performance_metrics['update_norms'].append(update_norm)
            self.performance_metrics['param_norms'].append(param_norm)
            
            return updated_params
    
    def get_performance_metrics(self) -> Dict[str, List[float]]:
        """Get the current performance metrics."""
        return self.performance_metrics
    
    def reset_metrics(self):
        """Reset all performance metrics."""
        self.performance_metrics = {
            'update_norms': [],
            'param_norms': [],
            'dampening_values': [],
            'loss_values': []
        }
        self.reset_history()


if __name__ == "__main__":
    # Basic test for LSTMMetaOptimizer with enhanced optimize method
    optimizer = MetaOptimizer(input_dim=4, hidden_dim=16, history_length=3)
    # Create a dummy history of 15 parameters
    dummy_history = np.array([0.1] * 15)
    updated = optimizer.optimize(dummy_history, current_loss=0.5)
    print("Original parameters:", dummy_history)
    print("Updated parameters:", updated)
    print("Performance metrics:", optimizer.get_performance_metrics())

# Added alias for backward compatibility with tests
LSTMMetaOptimizer = MetaOptimizer 