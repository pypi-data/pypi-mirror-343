"""
Quantum feed-forward network implementation using quantum circuits.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Tuple, Optional
from quantum_finance.backend.quantum_wrapper import quantum_wrapper
from quantum_finance.utils.analog_linear import AnalogLinear  # type: ignore

class QuantumFeedForward(nn.Module):
    """
    A feed-forward network that uses quantum circuits for computation.
    
    Args:
        d_model (int): Input dimension
        n_qubits (int): Number of qubits to use
        n_layers (int): Number of quantum circuit layers
    """
    def __init__(self, d_model: int, n_qubits: int, n_layers: int = 2) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        
        # Input projection to match quantum circuit size (analog fallback)
        self.input_proj = AnalogLinear(d_model, 2**n_qubits, dtype=torch.float32)
        
        # Output projection back to model dimension (analog fallback)
        self.output_proj = AnalogLinear(2**n_qubits, d_model, dtype=torch.float32)
        
        # Learnable parameters for quantum gates
        self.rotation_params = nn.Parameter(torch.randn(n_layers, n_qubits, 3, dtype=torch.float32))  # 3 for Rx, Ry, Rz
        self.entangle_params = nn.Parameter(torch.randn(n_layers, n_qubits - 1, dtype=torch.float32))
        
        # Layer normalization
        self.norm = nn.LayerNorm(d_model, dtype=torch.float32)
        
        # Number of parameters for external access
        self.n_parameters = n_layers * (3 * n_qubits + (n_qubits - 1))
        
        # Default entanglement pairs
        self._setup_default_entanglement()
    
    def _setup_default_entanglement(self) -> None:
        """Setup default nearest-neighbor entanglement pattern."""
        self.entangle_pairs = [(i, i+1) for i in range(self.n_qubits - 1)]
    
    def set_entanglement(self, pairs: List[Tuple[int, int]]) -> None:
        """
        Update the entanglement pattern.
        
        Args:
            pairs: List of qubit pairs to entangle
        """
        for i, j in pairs:
            if not (0 <= i < self.n_qubits and 0 <= j < self.n_qubits):
                raise ValueError(f"Invalid qubit indices: ({i}, {j})")
        self.entangle_pairs = pairs
    
    def _prepare_quantum_circuit(self, x: torch.Tensor) -> dict:
        """
        Prepare quantum circuit specification from input tensor.
        
        Args:
            x: Input tensor
        Returns:
            Circuit specification dictionary
        """
        # Normalize input to valid quantum state
        state_vector = F.normalize(x, p=2, dim=-1)
        
        # Prepare circuit specification
        circuit_spec = {
            'n_qubits': self.n_qubits,
            'input_state': state_vector.detach().cpu().numpy(),
            'gates': []
        }
        
        # Add parametrized gates for each layer
        for layer in range(self.n_layers):
            # Single-qubit rotations
            for qubit in range(self.n_qubits):
                rx, ry, rz = self.rotation_params[layer, qubit]
                circuit_spec['gates'].extend([
                    ('rx', qubit, rx.detach().item()),
                    ('ry', qubit, ry.detach().item()),
                    ('rz', qubit, rz.detach().item())
                ])
            
            # Two-qubit entangling gates
            for i, (q1, q2) in enumerate(self.entangle_pairs):
                if i < len(self.entangle_params[layer]):
                    angle = self.entangle_params[layer, i]
                    circuit_spec['gates'].append(('cz', q1, q2, angle.detach().item()))
        
        return circuit_spec
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the quantum feed-forward network.
        
        Args:
            x: Input tensor of shape (..., d_model)
            
        Returns:
            Output tensor of shape (..., d_model)
        """
        # Store original shape and flatten batch dimensions
        orig_shape = x.shape[:-1]
        x_flat = x.view(-1, self.d_model)
        
        # Project to quantum dimension
        x_quantum = self.input_proj(x_flat)
        
        # Process each input state through quantum circuit
        quantum_outputs = []
        for single_input in x_quantum:
            # Prepare and simulate quantum circuit
            circuit_spec = self._prepare_quantum_circuit(single_input)
            quantum_output = quantum_wrapper.simulate_circuit(circuit_spec)
            
            # Convert complex numpy array to torch tensor
            quantum_output = torch.from_numpy(quantum_output).to(x.device)
            # Take absolute values squared (probabilities) to get real numbers
            quantum_output = torch.abs(quantum_output) ** 2
            # Convert to same dtype as input
            quantum_output = quantum_output.to(dtype=x.dtype)
            quantum_outputs.append(quantum_output)
        
        # Stack outputs
        quantum_output = torch.stack(quantum_outputs)
        
        # Project back to model dimension
        output = self.output_proj(quantum_output)
        
        # Reshape to original dimensions
        output = output.view(*orig_shape, self.d_model)
        
        # Apply layer normalization
        return self.norm(output)
    
    def update_parameters(self, params: List[float]) -> None:
        """
        Update quantum circuit parameters from external optimization.
        
        Args:
            params: List of new parameter values
        """
        if len(params) != self.n_parameters:
            raise ValueError(f"Expected {self.n_parameters} parameters, got {len(params)}")
        
        # Reshape parameters into rotation and entanglement parameters
        n_rotation_params = self.n_layers * self.n_qubits * 3
        rotation_params = torch.tensor(params[:n_rotation_params]).view(
            self.n_layers, self.n_qubits, 3)
        entangle_params = torch.tensor(params[n_rotation_params:]).view(
            self.n_layers, self.n_qubits - 1)
        
        # Update parameters
        with torch.no_grad():
            self.rotation_params.copy_(rotation_params)
            self.entangle_params.copy_(entangle_params) 