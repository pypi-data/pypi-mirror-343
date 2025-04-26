import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Tuple, Callable, Optional
from pathlib import Path

# Import necessary components using full package paths
from quantum_finance.backend.quantum_wrapper import quantum_wrapper
from quantum_finance.backend.attention import MultiHeadAttention
from quantum_finance.backend.quantum_feedforward import QuantumFeedForward
from quantum_finance.backend.quantum_memory import QuantumMemristor
from quantum_finance.dynamic_circuit import dynamic_entanglement, ring_topology  # Import dynamic circuit functions
from quantum_finance.utils.analog_linear import AnalogLinear  # type: ignore

"""
Quantum Transformer Module

This module implements a novel quantum-enhanced transformer architecture that combines 
quantum computing concepts with the transformer neural network model. It leverages quantum
principles to improve the attention mechanism, feature extraction, and processing capabilities
of traditional transformers.

Key components:
- Quantum attention mechanisms for improved context understanding
- Quantum-inspired embedding transformations
- Hybrid classical-quantum processing pipelines
- Variational quantum circuits for feature extraction

The module provides both simulation-based implementations for classical computers
and interfaces for execution on actual quantum hardware when available.
"""

# Helper function to ensure the input state vector is full (i.e. of length 2**n_qubits).
# If the provided state vector is shorter, it is extended by tensoring with the |0> state.

def ensure_full_state(state: np.ndarray, n_qubits: int) -> np.ndarray:
    """Ensure that the state vector is of length 2**n_qubits. If not, extend it by tensoring with |0> states."""
    expected_dim = 2 ** n_qubits
    if state.size == expected_dim:
        return state
    elif state.size < expected_dim:
        # Calculate how many times to tensor with |0>, where |0> is represented as [1, 0]
        r = int(np.log2(expected_dim) - np.log2(state.size))
        extension = np.array([1, 0], dtype=state.dtype)
        for i in range(1, r):
            extension = np.kron(extension, np.array([1, 0], dtype=state.dtype))
        new_state = np.kron(state, extension)
        return new_state
    else:
        # If state is longer than expected, assume it's already full
        return state

class PositionalEncoding(nn.Module):
    """
    Implements standard sinusoidal positional encoding.
    
    Args:
        d_model (int): Dimension of the model (embedding size).
        max_len (int): Maximum expected sequence length.
    """
    def __init__(self, d_model: int, max_len: int = 5000) -> None:
        super().__init__()
        position = torch.arange(max_len).unsqueeze(1).float()  # (max_len, 1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(np.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)  # (max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x (Tensor): Shape (seq_len, batch_size, d_model)
        Returns:
            Tensor: x with positional encoding added.
        """
        return x + self.pe[:x.size(0)]

class QuantumTransformerLayer(nn.Module):
    """
    A transformer layer that integrates classical multi-head attention with quantum-inspired components.
    Avoids in-place operations for better gradient computation.
    
    Args:
        d_model (int): Embedding dimension.
        n_heads (int): Number of attention heads.
        n_qubits (int): Number of qubits used in the quantum components.
        memory_size (int): Size of the quantum memory state.
        circuit_topology (Optional[Callable[[int], List[Tuple[int, int]]]]): 
            A function that, given n_qubits, returns a list of qubit pairs to entangle.
    """
    def __init__(self, 
                 d_model: int, 
                 n_heads: int, 
                 n_qubits: int,
                 memory_size: Optional[int] = None,
                 circuit_topology: Optional[Callable[[int], List[Tuple[int, int]]]] = None) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_qubits = n_qubits
        self.memory_size = memory_size or d_model
        
        # Multi-head attention component
        self.mha = MultiHeadAttention(d_model, n_heads)
        
        # Quantum feed-forward network
        self.quantum_ffn = QuantumFeedForward(d_model, n_qubits)
        
        # Quantum memory component
        self.quantum_memory = QuantumMemristor(
            state_size=self.memory_size,
            n_qubits=n_qubits,
            learning_rate=0.01,
            decay_rate=0.999
        )
        
        # Optional dynamic entanglement configuration, defaulting to dynamic topology generation if not provided
        if circuit_topology is None:
            # Using a lambda to capture self.gradient_stats and defer call to dynamic_topology_generator
            self.circuit_topology = lambda n: globals()['dynamic_topology_generator'](n, self.gradient_stats)
        else:
            self.circuit_topology = circuit_topology
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        
        # Projection layers for memory integration
        self.memory_in_proj = AnalogLinear(d_model, self.memory_size)
        self.memory_out_proj = AnalogLinear(self.memory_size, d_model)
        
        # Gradient accumulation for dynamic topology
        self.register_buffer('gradient_stats', torch.zeros(n_qubits, n_qubits))
        
        # Initialize default entanglement configuration
        self.entanglement_config = ring_topology(n_qubits)
        
    def update_topology(self, gradient_stats: torch.Tensor) -> None:
        """
        Update the circuit topology based on gradient statistics.
        Avoids in-place operations.
        
        Args:
            gradient_stats: Tensor containing gradient information
        """
        # Create new tensor for gradient stats update
        self.gradient_stats = 0.9 * self.gradient_stats.clone() + 0.1 * gradient_stats
        if self.circuit_topology is not None:
            entangle_pairs = self.circuit_topology(self.n_qubits)
            self.quantum_ffn.set_entanglement(entangle_pairs)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Process input through the transformer layer.
        Avoids in-place operations for better gradient computation.
        
        Args:
            x (Tensor): Input tensor of shape (seq_len, batch_size, d_model)
            
        Returns:
            Tensor: Processed tensor of same shape as input
        """
        # Store original input for residual connections
        identity = x.clone()
        
        # BEGIN: Dynamic Circuit Reconfiguration Integration
        if hasattr(self, 'gradient_norms') and isinstance(self.gradient_norms, list):
            self.entanglement_config = dynamic_entanglement(self.n_qubits, self.gradient_norms)
        else:
            self.entanglement_config = ring_topology(self.n_qubits)
        
        # Multi-head attention with residual connection and normalization
        attn_out, _ = self.mha(x, x, x)  # Unpack the tuple, ignoring attention weights
        x = self.norm1(identity + attn_out)  # Using + instead of += for safety
        
        # Process through quantum memory (avoiding in-place operations)
        memory_in = self.memory_in_proj(x.clone())  # Clone to avoid in-place modifications
        memory_out = self.quantum_memory(memory_in)
        memory_projected = self.memory_out_proj(memory_out)
        x = self.norm2(x + memory_projected)  # Using + instead of += for safety
        
        # Update entanglement if dynamic topology is enabled
        if self.training and self.circuit_topology is not None:
            with torch.no_grad():
                # Clone gradient stats to avoid in-place modification
                grad_stats = self.gradient_stats.clone()
                self.update_topology(grad_stats)
        
        # Apply quantum feed-forward network (avoiding in-place operations)
        qfn_out = self.quantum_ffn(x.clone())  # Clone to avoid in-place modifications
        x = self.norm3(x + qfn_out)  # Using + instead of += for safety
        
        return x
    
    def reset_memory(self) -> None:
        """Reset the quantum memory state"""
        self.quantum_memory.reset_state()
    
    @property
    def memory_state(self) -> dict:
        """Get the current memory state"""
        return self.quantum_memory.get_state_dict()

class QuantumTransformer(nn.Module):
    """
    QuantumTransformer model that cascades multiple QuantumTransformerLayers.
    
    Args:
        d_model (int): Embedding dimension.
        n_heads (int): Number of attention heads.
        n_layers (int): Number of transformer layers.
        n_qubits (int): Number of qubits for quantum components.
        memory_size (Optional[int]): Size of quantum memory state.
        use_positional_encoding (bool): Whether to add positional encoding to inputs.
        input_dim (Optional[int]): Dimension of the input. If not provided, defaults to 2**n_qubits.
    """
    def __init__(self, 
                 d_model: int, 
                 n_heads: int, 
                 n_layers: int, 
                 n_qubits: int,
                 memory_size: Optional[int] = None,
                 use_positional_encoding: bool = True,
                 input_dim: Optional[int] = None) -> None:
        super().__init__()
        self.use_positional_encoding = use_positional_encoding
        if self.use_positional_encoding:
            self.pos_encoder = PositionalEncoding(d_model)
        
        # Create transformer layers with quantum memory
        self.layers = nn.ModuleList([
            QuantumTransformerLayer(
                d_model=d_model,
                n_heads=n_heads,
                n_qubits=n_qubits,
                memory_size=memory_size
            )
            for _ in range(n_layers)
        ])
        
        # Initialize optimizer for quantum circuit parameters
        self.optimizer = None
        
        # Set input_dim to user-specified value or default to 2**n_qubits
        self.input_dim = input_dim if input_dim is not None else 2**n_qubits
        self.d_model = d_model
        
        # Updated input projection: maps from input_dim to d_model
        self.input_proj = AnalogLinear(self.input_dim, d_model)  # Analog fallback for input projection
        # Output projection: maps d_model to quantum state space dimension (2**n_qubits)
        self.output_proj = AnalogLinear(d_model, 2**n_qubits)  # Analog fallback for output projection
        
        # Added latent projection to ensure training output has dimension d_model in case layers reduce dimension
        self.latent_proj = AnalogLinear(2**n_qubits, d_model)  # Analog fallback for latent projection

    def forward(self, x: torch.Tensor, task: str = "train") -> torch.Tensor:
        """
        Process input through the transformer.
        
        Args:
            x (Tensor): Input tensor of shape (batch_size, d_model) or (batch_size, input_dim) or with added sequence dimension.
            task (str): Specifies the task mode.
                        'train' returns latent representation of shape (batch, d_model).
                        'predict' returns the latent representation with tanh activation of shape (batch, d_model) and with values in (-1, 1).
                        
        Returns:
            Tensor: Processed output tensor according to specified task.
        """
        original_dim = x.dim()
        # Handle 2D input: shape (batch, features)
        if x.dim() == 2:
            if x.shape[-1] == self.input_dim:
                x = self.input_proj(x)  # project from input_dim to d_model
            elif x.shape[-1] == self.d_model:
                pass  # input already in d_model space
            else:
                raise ValueError(f"Unexpected input feature size: {x.shape[-1]}. Expected either {self.input_dim} or {self.d_model}.")
            # Add sequence dimension
            x = x.unsqueeze(0)  # shape becomes (1, batch, d_model)
        elif x.dim() == 3:
            if x.shape[-1] == self.input_dim:
                seq_len, batch, _ = x.shape
                x = x.reshape(seq_len * batch, -1)
                x = self.input_proj(x)
                x = x.reshape(seq_len, batch, -1)
            elif x.shape[-1] == self.d_model:
                pass
            else:
                raise ValueError(f"Unexpected input feature size: {x.shape[-1]}. Expected either {self.input_dim} or {self.d_model}.")
        else:
            raise ValueError("Input tensor must be 2D or 3D")

        # Add positional encoding if enabled; pos_encoder expects shape (seq_len, batch, d_model)
        if self.use_positional_encoding:
            x = self.pos_encoder(x)

        # Process through all transformer layers
        for layer in self.layers:
            x = layer(x)

        latent = x

        # If the latent representation does not have the expected d_model size, project it back
        if latent.shape[-1] != self.d_model:
            latent = self.latent_proj(latent)

        # If original input was 2D, remove the added sequence dimension
        if original_dim == 2:
            latent = latent.squeeze(0)  # shape becomes (batch, d_model)

        if task == "predict":
            out = self.output_proj(latent)
            out = torch.tanh(out)
            return out

        # For training, return the latent representation
        return latent
    
    def reset_memory(self) -> None:
        """Reset memory states in all layers"""
        for layer in self.layers:
            layer.reset_memory()
    
    def get_memory_states(self) -> List[dict]:
        """Get memory states from all layers"""
        return [layer.memory_state for layer in self.layers]
    
    def optimize_circuit_parameters(self, 
                                 objective_function: Callable[[nn.Module], float],
                                 circuit_parameters: List[float]) -> Tuple[List[float], float]:
        """
        Optimize quantum circuit parameters using quantum-inspired optimization.
        
        Args:
            objective_function: Function that accepts the model and returns a scalar loss
            circuit_parameters: Initial parameters for quantum circuits
            
        Returns:
            Tuple[List[float], float]: (Best parameters, best objective value)
        """
        try:
            from quantum_finance.backend.quantum_algorithms import QuantumInspiredOptimizer
            
            if self.optimizer is None:
                self.optimizer = QuantumInspiredOptimizer(
                    n_particles=50,
                    n_dimensions=len(circuit_parameters)
                )
            
            def wrapped_objective(params: List[float]) -> float:
                self._update_circuit_parameters(params)
                return objective_function(self)
            
            best_params, best_value = self.optimizer.quantum_inspired_pso(wrapped_objective)
            self._update_circuit_parameters(best_params)
            best_value = float(best_value)  # Ensure best_value is a Python float
            return best_params, best_value
            
        except ImportError:
            print("QuantumInspiredOptimizer not available. Using default parameters.")
            return circuit_parameters, float('inf')
    
    def _update_circuit_parameters(self, params: List[float]) -> None:
        """Update quantum circuit parameters across all layers"""
        param_idx = 0
        for layer in self.layers:
            n_params = layer.quantum_ffn.n_parameters
            layer_params = params[param_idx:param_idx + n_params]
            layer.quantum_ffn.update_parameters(layer_params)
            param_idx += n_params
    
    def _get_circuit_parameters(self) -> List[float]:
        """Extract current circuit parameters from all layers' quantum_ffn modules."""
        params = []
        for layer in self.layers:
            try:
                # Attempt to extract circuit_params attribute
                params.extend(layer.quantum_ffn.circuit_params)
            except AttributeError:
                # Fallback: assume n_parameters exists and fill with zeros
                params.extend([0.0] * layer.quantum_ffn.n_parameters)
        return params
    
    def fine_tune(self, X, y):
        """Dummy fine-tune method for QuantumTransformer. Currently a no-op."""
        pass

def load_and_preprocess_data(circuit_data: List[dict]) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Loads circuit data and computes corresponding outputs via the quantum wrapper.
    
    Args:
        circuit_data (List[dict]): Each dictionary must contain 'input_state' and additional keys.
    Returns:
        Tuple[Tensor, Tensor]: Stacked input states and corresponding output states.
    """
    input_states = []
    output_states = []
    for circuit in circuit_data:
        if 'input_state' not in circuit:
            raise KeyError("Each circuit entry must have an 'input_state' key.")
        # Ensure the input state is full (i.e., has length 2**n_qubits)
        raw_state = np.array(circuit['input_state'], dtype=np.float32)
        full_state = ensure_full_state(raw_state, circuit['n_qubits'])
        input_state = torch.tensor(full_state, dtype=torch.float32)
        input_states.append(input_state)
        output_state = quantum_wrapper.simulate_circuit(circuit)
        output_states.append(torch.tensor(output_state, dtype=torch.float32))
    return torch.stack(input_states), torch.stack(output_states)

def train_quantum_transformer(model: QuantumTransformer, 
                              train_data: List[dict], 
                              num_epochs: int = 100, 
                              learning_rate: float = 0.001) -> QuantumTransformer:
    """
    Train the QuantumTransformer model using a mean squared error loss.
    
    Args:
        model (QuantumTransformer): The model instance.
        train_data (List[dict]): Training data containing circuit definitions.
        num_epochs (int): Number of epochs.
        learning_rate (float): Learning rate for the optimizer.
    Returns:
        QuantumTransformer: The trained model.
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()
    
    input_tensor, target_tensor = load_and_preprocess_data(train_data)
    device = next(model.parameters()).device
    input_tensor = input_tensor.to(device)
    target_tensor = target_tensor.to(device)
    
    # Create a projection layer to match model output dimensions to target dimensions
    output_dim = target_tensor.shape[-1]
    projection = nn.Linear(model.d_model, output_dim).to(device)
    
    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        output = model(input_tensor)
        # Project the output to match target dimensions
        projected_output = projection(output)
        loss = criterion(projected_output, target_tensor)
        loss.backward()

        # Optionally integrate meta-learning update for circuit parameters every 10 epochs
        if epoch % 10 == 0:
            try:
                from quantum_finance.backend.meta_learning import meta_optimizer
                # Extract current circuit parameters using the new helper method
                circuit_params = model._get_circuit_parameters()
                # Get updated parameters from meta_optimizer
                updated_params = meta_optimizer(circuit_params)
                # Update the model's circuit parameters with the updated values
                model._update_circuit_parameters(updated_params)
                print(f"Meta-learning update at epoch {epoch}: circuit parameters updated to {updated_params}.")
            except Exception as e:
                print(f"Meta-learning update skipped due to error: {e}")

        optimizer.step()
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")
    
    return model

def predict_quantum_state(model: QuantumTransformer, input_state: np.ndarray) -> np.ndarray:
    """
    Generate a latent prediction from the QuantumTransformer model.
    
    Args:
        model (QuantumTransformer): The trained model.
        input_state (np.ndarray): Input state as a NumPy array.
    Returns:
        np.ndarray: Latent representation of shape (d_model,) with values in (-1, 1) after tanh activation.
    """
    model.eval()
    with torch.no_grad():
        full_state = ensure_full_state(np.array(input_state, dtype=np.float32), model.layers[0].n_qubits)
        input_tensor = torch.tensor(full_state, dtype=torch.float32).unsqueeze(0)
        input_tensor = input_tensor.to(next(model.parameters()).device)
        # Get the latent representation instead of the predict output
        output = model(input_tensor, task="train")
        # Apply tanh to constrain values between -1 and 1
        output = torch.tanh(output)
    return output.squeeze().cpu().numpy()

def train_and_use_quantum_transformer(quantum_circuit_data: List[dict]) -> QuantumTransformer:
    """
    High-level routine: initialize, train, and test the QuantumTransformer.
    
    Args:
        quantum_circuit_data (List[dict]): List of circuit data dictionaries.
    Returns:
        QuantumTransformer: The trained model.
    """
    # Define model hyperparameters
    d_model = 64
    n_heads = 4
    num_layers = 2
    n_qubits = quantum_circuit_data[0]['n_qubits']
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = QuantumTransformer(d_model, n_heads, num_layers, n_qubits).to(device)
    
    # Train the model
    trained_model = train_quantum_transformer(model, quantum_circuit_data)
    
    # Test prediction with a sample circuit
    test_circuit = {'input_state': [1, 0, 0, 0], 'gates': ['H', 'CNOT'], 'n_qubits': 2}
    test_input = np.array(test_circuit['input_state'])
    predicted_state = predict_quantum_state(trained_model, test_input)
    
    print(f"Predicted quantum state: {predicted_state}")
    print(f"Quantum backend info: {quantum_wrapper.backend_info}")
    
    return trained_model

# Insertion: dynamic_topology_generator function for dynamic circuit enhancement

def dynamic_topology_generator(n_qubits: int, gradient_stats: torch.Tensor) -> List[Tuple[int, int]]:
    """Generate dynamic entanglement patterns based on gradient statistics.
    This function converts the gradient_stats tensor into per-qubit norms and then uses
    dynamic_entanglement from the dynamic_circuit module to determine the entanglement configuration.
    
    Args:
        n_qubits (int): Number of qubits in the system.
        gradient_stats (torch.Tensor): A tensor of shape (n_qubits, n_qubits) representing gradient metrics.
        
    Returns:
        List[Tuple[int, int]]: A list of qubit index pairs representing entanglement connections.
    """
    from dynamic_circuit import dynamic_entanglement  # Import the dynamic entanglement function
    # Compute per-qubit gradient norms (L2 norm for each row of the gradient stats matrix)
    gradient_norms = torch.norm(gradient_stats, dim=1).tolist()
    return dynamic_entanglement(n_qubits, gradient_norms)

if __name__ == "__main__":
    # Example usage with sample circuit data
    sample_data = [
        {'input_state': [1, 0, 0, 0], 'gates': ['H', 'CNOT'], 'n_qubits': 2},
        {'input_state': [0, 1, 0, 0], 'gates': ['X', 'H', 'CNOT'], 'n_qubits': 2},
    ]
    trained_model = train_and_use_quantum_transformer(sample_data)
    print(f"Final quantum backend status: {quantum_wrapper.backend_info}")