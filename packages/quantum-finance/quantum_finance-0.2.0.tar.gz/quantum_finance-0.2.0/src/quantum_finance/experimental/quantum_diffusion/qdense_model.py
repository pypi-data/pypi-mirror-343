#!/usr/bin/env python3

"""
Q-Dense: Quantum Diffusion Model Implementation

This module implements the Q-Dense architecture for quantum diffusion models,
as described in the research on quantum denoising diffusion. It provides tools
for creating, training, and evaluating a quantum diffusion model using Qiskit.

Key components:
1. Quantum circuit creation with parameterized rotation gates
2. Amplitude embedding for input data
3. Forward and reverse diffusion processes
4. Training and evaluation utilities

Usage:
    from experimental.quantum_diffusion.qdense_model import QDenseDiffusion
    model = QDenseDiffusion(num_qubits=7, num_layers=47)
    model.train(train_data, epochs=10)
    generated_images = model.generate(num_samples=5)

Note:
    This is an experimental implementation focused on:
    - Proof of concept for quantum diffusion
    - Benchmarking against classical approaches
    - Parameter efficiency evaluation
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Quantum imports
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import ZZFeatureMap, QuantumVolume
from qiskit.circuit import Parameter, ParameterVector
from qiskit.visualization import plot_histogram
from qiskit_aer.primitives import Sampler

# Project imports
from quantum_ai_utils import standardize_quantum_input, run_parameter_sweep
from quantum_ai_interface import QuantumMeasurementResult, CircuitMetadata

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QDenseDiffusion:
    """
    Q-Dense Quantum Diffusion Model implementation.
    
    Uses a parameterized quantum circuit with ZZFeatureMap for data embedding
    and implements the diffusion process using quantum circuits.
    """
    
    def __init__(self, num_qubits=7, num_layers=47, shots=1000):
        """
        Initialize the Q-Dense Diffusion model.
        
        Args:
            num_qubits (int): Number of qubits in the circuit
            num_layers (int): Number of parameterized layers
            shots (int): Number of measurement shots per circuit execution
        """
        self.num_qubits = num_qubits
        self.num_layers = num_layers
        self.shots = shots
        
        # Calculate total number of parameters
        self.params_per_layer = 3 * num_qubits  # 3 rotation gates per qubit
        self.total_params = num_layers * self.params_per_layer
        
        # Initialize parameters randomly
        self.params = np.random.random(self.total_params) * np.pi * 2 - np.pi
        
        # Diffusion process parameters
        self.beta_schedule = np.linspace(0.0001, 0.02, 1000)  # Noise schedule
        self.timesteps = len(self.beta_schedule)
        
        logger.info(f"Initialized Q-Dense Diffusion with {num_qubits} qubits, "
                   f"{num_layers} layers, and {self.total_params} parameters")
    
    def _create_circuit(self):
        """
        Create the parameterized Q-Dense quantum circuit.
        
        Returns:
            tuple: (QuantumCircuit, parameter dictionary)
        """
        # Create quantum circuit
        qc = QuantumCircuit(self.num_qubits)
        
        # Create parameters for the circuit
        params = ParameterVector('θ', self.total_params)
        param_binding_dict = {}
        
        # Input embedding (ZZ Feature Map for amplitude embedding)
        feature_map = ZZFeatureMap(feature_dimension=self.num_qubits)
        qc.compose(feature_map, inplace=True)
        
        # Add variational layers
        param_idx = 0
        for l in range(self.num_layers):
            # Rotation gates
            for q in range(self.num_qubits):
                qc.rx(params[param_idx], q)
                param_binding_dict[params[param_idx]] = self.params[param_idx]
                param_idx += 1
                
                qc.ry(params[param_idx], q)
                param_binding_dict[params[param_idx]] = self.params[param_idx]
                param_idx += 1
                
                qc.rz(params[param_idx], q)
                param_binding_dict[params[param_idx]] = self.params[param_idx]
                param_idx += 1
            
            # Entanglement
            for q in range(self.num_qubits-1):
                qc.cx(q, q+1)
            qc.cx(self.num_qubits-1, 0)  # Close the loop
        
        # Add measurements
        qc.measure_all()
        
        return qc, param_binding_dict
    
    def update_parameters(self, new_params):
        """
        Update the model parameters.
        
        Args:
            new_params (np.ndarray): New parameter values
        """
        assert len(new_params) == self.total_params, "Parameter count mismatch"
        self.params = new_params
    
    def embed_data(self, image_data):
        """
        Embed classical image data into quantum states.
        
        Args:
            image_data (np.ndarray): Image data to embed
            
        Returns:
            list: Embedded data ready for circuit input
        """
        # Flatten and normalize the image
        flattened = image_data.flatten()
        
        # Create our own normalization function if project's is not compatible
        try:
            normalized = standardize_quantum_input(flattened, target_shape=2**self.num_qubits)
        except (TypeError, ValueError):
            # Fallback to a simple normalization
            normalized = (flattened - np.min(flattened)) / (np.max(flattened) - np.min(flattened) + 1e-8)
        
        # If data dimension is larger than number of qubits, downsample
        if len(normalized) > 2**self.num_qubits:
            logger.warning(f"Input dimension {len(normalized)} is larger than circuit capacity "
                          f"({2**self.num_qubits}). Downsampling data.")
            # Simple downsampling by averaging
            samples_per_bin = len(normalized) // (2**self.num_qubits)
            embedded = []
            for i in range(2**self.num_qubits):
                start_idx = i * samples_per_bin
                end_idx = min((i+1) * samples_per_bin, len(normalized))
                if start_idx < end_idx:
                    embedded.append(np.mean(normalized[start_idx:end_idx]))
                else:
                    embedded.append(0.0)
        else:
            # Pad with zeros if needed
            embedded = np.pad(normalized, (0, 2**self.num_qubits - len(normalized)))
        
        return embedded
    
    def forward_diffusion(self, x_0, t):
        """
        Apply forward diffusion process for t steps.
        
        Args:
            x_0 (np.ndarray): Initial clean data
            t (int): Number of diffusion steps
            
        Returns:
            tuple: (noisy data x_t, noise added)
        """
        # Calculate cumulative variance schedule
        alpha = 1 - self.beta_schedule
        alpha_bar = np.cumprod(alpha)
        
        # Get the alpha at time t
        alpha_t = alpha_bar[t]
        
        # Sample noise
        epsilon = np.random.randn(*x_0.shape)
        
        # Add noise according to diffusion schedule
        x_t = np.sqrt(alpha_t) * x_0 + np.sqrt(1 - alpha_t) * epsilon
        
        return x_t, epsilon
    
    def quantum_denoising_step(self, x_t, t):
        """
        Apply quantum circuit to predict noise at timestep t.
        
        Args:
            x_t (np.ndarray): Noisy data at timestep t
            t (int): Current timestep
            
        Returns:
            np.ndarray: Predicted noise
        """
        # Embed the noisy data for quantum circuit
        embedded_data = self.embed_data(x_t)
        
        # Create a parameterized circuit as before
        qc = QuantumCircuit(self.num_qubits, self.num_qubits)
        params = ParameterVector('θ', self.total_params)
        param_idx = 0
        for l in range(self.num_layers):
            for q in range(self.num_qubits):
                qc.rx(params[param_idx], q)
                param_idx += 1
                qc.ry(params[param_idx], q)
                param_idx += 1
                qc.rz(params[param_idx], q)
                param_idx += 1
            for q in range(self.num_qubits-1):
                qc.cx(q, q+1)
            qc.cx(self.num_qubits-1, 0)
        qc.measure(range(self.num_qubits), range(self.num_qubits))
        
        # Prepare parameter values as a list (order matches params)
        param_values = [self.params]
        
        # Use run_parameter_sweep utility for execution (local AerSimulator by default)
        # Extensive inline notes: This ensures production-ready, robust execution and logging.
        from qiskit_aer import AerSimulator
        backend = AerSimulator()
        sweep_results = run_parameter_sweep(
            qc,
            param_values,
            backend_or_service=backend,
            shots=self.shots,
            use_runtime_sampler=False,
            log_prefix="[QDenseDiffusion.quantum_denoising_step] "
        )
        # Extract the first result (since we only run one parameter set)
        quasi_dists = sweep_results[0]
        
        # Convert bit strings and process
        binary_values = []
        probabilities = []
        for bitstring, prob in quasi_dists.items():
            binary_values.append(int(bitstring, 2) if isinstance(bitstring, str) else bitstring)
            probabilities.append(prob)
        if binary_values:
            binary_values = np.array(binary_values)
            probabilities = np.array(probabilities)
            expected_binary = np.sum(binary_values * probabilities)
            max_value = 2**self.num_qubits - 1
            normalized_value = expected_binary / max_value if max_value > 0 else 0.5
        else:
            normalized_value = 0.5
        predicted_noise = (normalized_value * 2 - 1) * np.ones_like(x_t)
        return predicted_noise
    
    def sample(self, shape=(8, 8), timesteps=None):
        """
        Generate a sample by iteratively denoising from pure noise.
        
        Args:
            shape (tuple): Shape of the output image
            timesteps (int): Number of diffusion steps (default: use all)
            
        Returns:
            np.ndarray: Generated sample
        """
        if timesteps is None:
            timesteps = self.timesteps
        
        # Start from pure noise
        x = np.random.randn(*shape)
        
        # Iteratively denoise
        for t in tqdm(range(timesteps-1, -1, -1), desc="Sampling"):
            # Get alpha values for current timestep
            alpha = 1 - self.beta_schedule
            alpha_bar = np.cumprod(alpha)
            
            alpha_t = alpha_bar[t]
            alpha_t_prev = alpha_bar[t-1] if t > 0 else 1.0
            
            # Denoising step
            predicted_noise = self.quantum_denoising_step(x, t)
            
            # Update sample using the predicted noise
            beta_t = self.beta_schedule[t]
            
            # No noise for the last step
            if t > 0:
                noise = np.random.randn(*shape)
            else:
                noise = 0
            
            # Compute the denoised sample
            x = (1 / np.sqrt(alpha[t])) * (
                x - (beta_t / np.sqrt(1 - alpha_bar[t])) * predicted_noise
            ) + np.sqrt(beta_t) * noise
        
        return x
    
    def train_step(self, batch_data, learning_rate=0.01):
        """
        Perform a single training step.
        
        Args:
            batch_data (np.ndarray): Batch of training data
            learning_rate (float): Learning rate for parameter updates
            
        Returns:
            float: Loss value
        """
        # This is a simplified training approach 
        # (A full implementation would involve more sophisticated optimization)
        
        total_loss = 0
        grad_accumulation = np.zeros_like(self.params)
        
        for image in batch_data:
            # Sample a random timestep
            t = np.random.randint(0, self.timesteps)
            
            # Apply forward diffusion to get noisy image and true noise
            x_t, true_noise = self.forward_diffusion(image, t)
            
            # Predict noise using quantum circuit
            predicted_noise = self.quantum_denoising_step(x_t, t)
            
            # Calculate loss (MSE between true and predicted noise)
            # Ensure both are numpy arrays
            true_noise = np.asarray(true_noise)
            predicted_noise = np.asarray(predicted_noise)
            loss = np.mean((true_noise - predicted_noise) ** 2)
            total_loss += loss
            
            # Compute approximate gradients using finite differences
            for i in range(self.total_params):
                delta = 0.01
                perturbed_params = self.params.copy()
                perturbed_params[i] += delta
                original_params = self.params.copy()
                self.params = perturbed_params
                predicted_noise_perturbed = self.quantum_denoising_step(x_t, t)
                predicted_noise_perturbed = np.asarray(predicted_noise_perturbed)
                perturbed_loss = np.mean((true_noise - predicted_noise_perturbed) ** 2)
                grad = (perturbed_loss - loss) / delta
                grad_accumulation[i] += grad
                self.params = original_params
            
        # Update parameters using accumulated gradients
        avg_grad = grad_accumulation / len(batch_data)
        self.params -= learning_rate * avg_grad
        
        avg_loss = total_loss / len(batch_data)
        return avg_loss
    
    def train(self, train_data, epochs=10, batch_size=4, learning_rate=0.01):
        """
        Train the quantum diffusion model.
        
        Args:
            train_data (np.ndarray): Training data
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
            learning_rate (float): Learning rate for parameter updates
            
        Returns:
            list: Training loss history
        """
        logger.info(f"Training Q-Dense Diffusion model for {epochs} epochs")
        
        loss_history = []
        num_batches = len(train_data) // batch_size
        
        for epoch in range(epochs):
            epoch_loss = 0
            
            # Shuffle data
            indices = np.random.permutation(len(train_data))
            shuffled_data = train_data[indices]
            
            for batch_idx in tqdm(range(num_batches), desc=f"Epoch {epoch+1}/{epochs}"):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, len(train_data))
                batch = shuffled_data[start_idx:end_idx]
                
                # Perform training step
                batch_loss = self.train_step(batch, learning_rate)
                epoch_loss += batch_loss
            
            avg_epoch_loss = epoch_loss / num_batches
            loss_history.append(avg_epoch_loss)
            
            logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {avg_epoch_loss:.6f}")
        
        return loss_history
    
    def generate_samples(self, num_samples=1, shape=(8, 8), timesteps=None):
        """
        Generate multiple samples.
        
        Args:
            num_samples (int): Number of samples to generate
            shape (tuple): Shape of each sample
            timesteps (int): Number of diffusion steps
            
        Returns:
            np.ndarray: Generated samples with shape (num_samples, *shape)
        """
        samples = []
        for i in tqdm(range(num_samples), desc="Generating samples"):
            sample = self.sample(shape, timesteps)
            samples.append(sample)
        
        return np.array(samples)
    
    def visualize_samples(self, samples, title="Generated Samples", save_path=None):
        """
        Visualize generated samples.
        
        Args:
            samples (np.ndarray): Samples to visualize
            title (str): Plot title
            save_path (str): Path to save the figure (if None, display instead)
        """
        n = len(samples)
        fig, axes = plt.subplots(1, n, figsize=(n*3, 3))
        
        if n == 1:
            axes = [axes]
            
        for i, ax in enumerate(axes):
            ax.imshow(samples[i], cmap='gray')
            ax.set_title(f"Sample {i+1}")
            ax.axis('off')
        
        plt.suptitle(title)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    def save_model(self, filepath):
        """
        Save the model parameters.
        
        Args:
            filepath (str): Path to save the parameters
        """
        np.save(filepath, self.params)
        logger.info(f"Model parameters saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load model parameters.
        
        Args:
            filepath (str): Path to load parameters from
        """
        self.params = np.load(filepath)
        assert len(self.params) == self.total_params, "Parameter count mismatch in loaded model"
        logger.info(f"Model parameters loaded from {filepath}")

# Simple test function for the model
def test_model():
    """
    Test the Q-Dense diffusion model with a simple example.
    """
    # Create a simplified 4-qubit model for testing
    model = QDenseDiffusion(num_qubits=4, num_layers=10, shots=1000)
    print(f"Created test model with {model.total_params} parameters")
    
    # Generate a simple 8x8 test image (checkerboard pattern)
    test_image = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                test_image[i, j] = 1
    
    # Test forward diffusion
    noisy_image, noise = model.forward_diffusion(test_image, t=100)
    print("Forward diffusion test:", "✓" if isinstance(noisy_image, np.ndarray) and noisy_image.shape == test_image.shape else "✗")
    
    # Test quantum denoising step (now uses run_parameter_sweep)
    predicted_noise = model.quantum_denoising_step(noisy_image, t=100)
    print("Quantum denoising test:", "✓" if isinstance(predicted_noise, np.ndarray) and predicted_noise.shape == test_image.shape else "✗")
    print("Predicted noise (sample):", predicted_noise.ravel()[:5])
    
    # Test sampling (generate a small sample for quick testing)
    sample = model.sample(shape=(4, 4), timesteps=10)
    print("Sampling test:", "✓" if isinstance(sample, np.ndarray) and sample.shape == (4, 4) else "✗")
    
    print("Basic functionality tests completed.")

if __name__ == "__main__":
    # Run the test
    test_model() 