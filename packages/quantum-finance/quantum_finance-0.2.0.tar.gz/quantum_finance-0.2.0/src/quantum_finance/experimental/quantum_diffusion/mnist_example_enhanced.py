#!/usr/bin/env python3

"""
Enhanced MNIST Example for Quantum Diffusion Models

This script provides a comprehensive demonstration of quantum diffusion models
compared to classical approaches, using the MNIST dataset.

Key enhancements:
1. Classical diffusion model baseline for comparison
2. Advanced visualizations of the training process and generated samples
3. Comprehensive benchmarking metrics
4. Integration with project benchmarking infrastructure
5. Configurable parameters via command-line arguments

Usage:
    python -m experimental.quantum_diffusion.mnist_example_enhanced [--options]
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Reshape, Flatten, Input
from sklearn.preprocessing import MinMaxScaler
import argparse
import os
import sys
import logging
import time
from datetime import datetime
from tqdm import tqdm
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the QDenseDiffusion model
from experimental.quantum_diffusion.qdense_model import QDenseDiffusion

# Project imports
try:
    from quantum_ai_utils import standardize_quantum_input
    from benchmark_results.benchmark_utils import save_benchmark_results
except ImportError:
    # Define simple versions if project utilities are not available
    def standardize_quantum_input(data):
        """Simple standardization function."""
        return (data - np.min(data)) / (np.max(data) - np.min(data) + 1e-8)
    
    def save_benchmark_results(results, benchmark_name):
        """Simple benchmark saving function."""
        os.makedirs('benchmark_results', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'benchmark_results/{benchmark_name}_{timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Benchmark results saved to {filename}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClassicalDiffusionModel:
    """
    A simple classical diffusion model for comparison.
    
    This is a simplified implementation using a basic neural network
    to demonstrate the diffusion process for comparison with the quantum approach.
    """
    
    def __init__(self, input_shape=(8, 8), latent_dim=16):
        """
        Initialize the classical diffusion model.
        
        Args:
            input_shape (tuple): Shape of input images
            latent_dim (int): Dimension of latent space
        """
        self.input_shape = input_shape
        self.latent_dim = latent_dim
        self.flat_dim = np.prod(input_shape)
        
        # Diffusion process parameters
        self.beta_schedule = np.linspace(0.0001, 0.02, 1000)
        self.timesteps = len(self.beta_schedule)
        
        # Build the model
        self._build_model()
        
        logger.info(f"Initialized Classical Diffusion Model with input shape {input_shape}")
    
    def _build_model(self):
        """Build the neural network model for denoising."""
        # Inputs: noisy image and timestep
        image_input = Input(shape=self.input_shape)
        time_input = Input(shape=(1,))
        
        # Flatten the image
        x = Flatten()(image_input)
        
        # Concat with time embedding
        time_embedding = Dense(32, activation='swish')(time_input)
        time_embedding = Dense(self.flat_dim, activation='swish')(time_embedding)
        x = tf.keras.layers.Concatenate()([x, time_embedding])
        
        # Dense layers
        x = Dense(128, activation='swish')(x)
        x = Dense(128, activation='swish')(x)
        x = Dense(self.flat_dim, activation=None)(x)
        
        # Reshape back to image
        output = Reshape(self.input_shape)(x)
        
        # Create model
        self.model = Model([image_input, time_input], output)
        self.model.compile(optimizer='adam', loss='mse')
        
        # Print model summary
        self.model.summary()
    
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
    
    def train_step(self, batch_data):
        """
        Perform a single training step.
        
        Args:
            batch_data (np.ndarray): Batch of training data
            
        Returns:
            float: Loss value
        """
        total_loss = 0
        batch_size = len(batch_data)
        
        # Prepare inputs and targets
        noisy_images = []
        timesteps = []
        target_noise = []
        
        for image in batch_data:
            # Sample a random timestep
            t = np.random.randint(0, self.timesteps)
            
            # Apply forward diffusion to get noisy image and true noise
            x_t, epsilon = self.forward_diffusion(image, t)
            
            # Store inputs and targets
            noisy_images.append(x_t)
            timesteps.append([t / self.timesteps])  # Normalize timestep
            target_noise.append(epsilon)
        
        # Convert to numpy arrays
        noisy_images = np.array(noisy_images)
        timesteps = np.array(timesteps)
        target_noise = np.array(target_noise)
        
        # Train the model to predict the noise
        loss = self.model.train_on_batch(
            [noisy_images, timesteps],
            target_noise
        )
        
        return loss
    
    def train(self, train_data, epochs=10, batch_size=32):
        """
        Train the classical diffusion model.
        
        Args:
            train_data (np.ndarray): Training data
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
            
        Returns:
            list: Training loss history
        """
        logger.info(f"Training Classical Diffusion model for {epochs} epochs")
        
        loss_history = []
        
        # Ensure batch_size is not larger than the dataset
        batch_size = min(batch_size, len(train_data))
        
        # Ensure we have at least one batch
        num_batches = max(1, len(train_data) // batch_size)
        
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
                batch_loss = self.train_step(batch)
                epoch_loss += batch_loss
            
            avg_epoch_loss = epoch_loss / num_batches
            loss_history.append(avg_epoch_loss)
            
            logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {avg_epoch_loss:.6f}")
        
        return loss_history
    
    def predict_noise(self, x_t, t):
        """
        Predict noise at timestep t for noisy image x_t.
        
        Args:
            x_t (np.ndarray): Noisy image
            t (int): Timestep
            
        Returns:
            np.ndarray: Predicted noise
        """
        # Prepare input
        if len(x_t.shape) == 2:
            x_t = np.expand_dims(x_t, 0)  # Add batch dimension
        
        t_input = np.array([[t / self.timesteps]])  # Normalize timestep
        
        # Predict noise
        predicted_noise = self.model.predict([x_t, t_input], verbose=0)
        
        return predicted_noise[0]  # Remove batch dimension
    
    def sample(self, shape=(8, 8), timesteps=None):
        """
        Generate a sample by iteratively denoising from pure noise.
        
        Args:
            shape (tuple): Shape of the output image
            timesteps (int): Number of diffusion steps
            
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
            
            # Predict noise
            predicted_noise = self.predict_noise(x, t)
            
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
    
    def generate_samples(self, num_samples=1, shape=None, timesteps=None):
        """
        Generate multiple samples.
        
        Args:
            num_samples (int): Number of samples to generate
            shape (tuple): Shape of each sample
            timesteps (int): Number of diffusion steps
            
        Returns:
            np.ndarray: Generated samples with shape (num_samples, *shape)
        """
        if shape is None:
            shape = self.input_shape
            
        samples = []
        for i in tqdm(range(num_samples), desc="Generating samples"):
            sample = self.sample(shape, timesteps)
            samples.append(sample)
        
        return np.array(samples)

def preprocess_mnist(downsample_size=(8, 8), num_samples=100):
    """
    Load and preprocess MNIST dataset.
    
    Args:
        downsample_size (tuple): Target size for downsampled images
        num_samples (int): Number of samples to use
        
    Returns:
        tuple: (train_data, test_data) - Preprocessed MNIST data
    """
    logger.info(f"Loading MNIST dataset and preprocessing {num_samples} samples")
    
    # Load MNIST dataset
    (x_train, _), (x_test, _) = mnist.load_data()
    
    # Take a subset for faster processing
    x_train_subset = x_train[:num_samples]
    x_test_subset = x_test[:min(num_samples // 10, len(x_test))]
    
    # Downsample images
    x_train_downsampled = downsample_images(x_train_subset, downsample_size)
    x_test_downsampled = downsample_images(x_test_subset, downsample_size)
    
    logger.info(f"Preprocessed {len(x_train_downsampled)} train and {len(x_test_downsampled)} test MNIST images")
    
    return x_train_downsampled, x_test_downsampled

def downsample_images(images, target_size):
    """
    Downsample a batch of images to the target size.
    
    Args:
        images (np.ndarray): Images to downsample
        target_size (tuple): Target size for downsampled images
        
    Returns:
        np.ndarray: Downsampled images
    """
    downsampled = []
    for img in images:
        # Simple downsampling by averaging blocks
        h_ratio = img.shape[0] // target_size[0]
        w_ratio = img.shape[1] // target_size[1]
        
        result = np.zeros(target_size)
        for i in range(target_size[0]):
            for j in range(target_size[1]):
                result[i, j] = np.mean(
                    img[i*h_ratio:(i+1)*h_ratio, j*w_ratio:(j+1)*w_ratio]
                )
        
        # Normalize to [0, 1]
        result = result / 255.0
        downsampled.append(result)
    
    return np.array(downsampled)

def compute_metrics(original_images, generated_images):
    """
    Compute quality metrics between original and generated images.
    
    Args:
        original_images (np.ndarray): Original images
        generated_images (np.ndarray): Generated images
        
    Returns:
        dict: Dictionary of metrics
    """
    from skimage.metrics import structural_similarity as ssim
    from skimage.metrics import peak_signal_noise_ratio as psnr
    
    # If original_images is empty, return default metrics
    if len(original_images) == 0:
        return {
            'mse': 1.0,
            'psnr': 0.0,
            'ssim': 0.0
        }
    
    # Make sure we have the same number of images to compare
    num_compare = min(len(original_images), len(generated_images))
    original = original_images[:num_compare]
    generated = generated_images[:num_compare]
    
    # Calculate MSE
    mse = np.mean((original - generated) ** 2)
    
    # Calculate PSNR
    psnr_value = psnr(original, generated, data_range=1.0)
    
    # Calculate SSIM
    ssim_values = []
    for i in range(num_compare):
        ssim_values.append(
            ssim(original[i], generated[i], data_range=1.0)
        )
    ssim_value = np.mean(ssim_values)
    
    # Create metrics dictionary
    metrics = {
        'mse': float(mse),
        'psnr': float(psnr_value),
        'ssim': float(ssim_value)
    }
    
    return metrics

def visualize_samples_comparison(quantum_samples, classical_samples, original_samples=None, save_path=None):
    """
    Visualize and compare samples from quantum and classical models.
    
    Args:
        quantum_samples (np.ndarray): Samples from quantum model
        classical_samples (np.ndarray): Samples from classical model
        original_samples (np.ndarray): Original samples for comparison
        save_path (str): Path to save visualization
    """
    num_quantum = len(quantum_samples)
    num_classical = len(classical_samples)
    num_samples = min(num_quantum, num_classical)
    
    if original_samples is not None:
        num_rows = 3
        fig_title = "Comparison: Original vs. Quantum vs. Classical"
    else:
        num_rows = 2
        fig_title = "Comparison: Quantum vs. Classical Diffusion"
    
    fig, axes = plt.subplots(num_rows, num_samples, figsize=(num_samples*2, num_rows*2))
    
    for i in range(num_samples):
        # Original sample (if provided)
        if original_samples is not None:
            if num_samples == 1:
                axes[0].imshow(original_samples[i], cmap='gray')
                axes[0].set_title(f"Original")
                axes[0].axis('off')
            else:
                axes[0, i].imshow(original_samples[i], cmap='gray')
                axes[0, i].set_title(f"Original {i+1}")
                axes[0, i].axis('off')
        
        # Quantum sample
        if num_samples == 1:
            row_idx = 0 if original_samples is None else 1
            axes[row_idx].imshow(quantum_samples[i], cmap='gray')
            axes[row_idx].set_title(f"Quantum")
            axes[row_idx].axis('off')
        else:
            row_idx = 0 if original_samples is None else 1
            axes[row_idx, i].imshow(quantum_samples[i], cmap='gray')
            axes[row_idx, i].set_title(f"Quantum {i+1}")
            axes[row_idx, i].axis('off')
        
        # Classical sample
        if num_samples == 1:
            row_idx = 1 if original_samples is None else 2
            axes[row_idx].imshow(classical_samples[i], cmap='gray')
            axes[row_idx].set_title(f"Classical")
            axes[row_idx].axis('off')
        else:
            row_idx = 1 if original_samples is None else 2
            axes[row_idx, i].imshow(classical_samples[i], cmap='gray')
            axes[row_idx, i].set_title(f"Classical {i+1}")
            axes[row_idx, i].axis('off')
    
    plt.suptitle(fig_title)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def visualize_training_comparison(quantum_loss, classical_loss, save_path=None):
    """
    Visualize training loss comparison between quantum and classical models.
    
    Args:
        quantum_loss (list): Training loss history of quantum model
        classical_loss (list): Training loss history of classical model
        save_path (str): Path to save visualization
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(quantum_loss, label='Quantum Diffusion', marker='o')
    plt.plot(classical_loss, label='Classical Diffusion', marker='x')
    
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def run_benchmark(train_data, test_data, quantum_params, classical_params, sample_params, results_dir):
    """
    Run benchmarking comparing quantum and classical diffusion models.
    
    Args:
        train_data (np.ndarray): Training data
        test_data (np.ndarray): Test data
        quantum_params (dict): Parameters for quantum model
        classical_params (dict): Parameters for classical model
        sample_params (dict): Parameters for sampling
        results_dir (str): Directory to save results
        
    Returns:
        dict: Benchmark results
    """
    input_shape = train_data[0].shape
    
    # Use train_data as a fallback if test_data is empty
    comparison_data = test_data if len(test_data) > 0 else train_data
    
    # Initialize models
    logger.info("Initializing models...")
    quantum_model = QDenseDiffusion(
        num_qubits=quantum_params['num_qubits'],
        num_layers=quantum_params['num_layers'],
        shots=quantum_params['shots']
    )
    
    classical_model = ClassicalDiffusionModel(
        input_shape=input_shape,
        latent_dim=classical_params['latent_dim']
    )
    
    # Training time measurement
    logger.info("Training quantum model...")
    quantum_start_time = time.time()
    quantum_loss = quantum_model.train(
        train_data[:quantum_params['train_samples']],
        epochs=quantum_params['epochs'],
        batch_size=quantum_params['batch_size'],
        learning_rate=quantum_params['learning_rate']
    )
    quantum_train_time = time.time() - quantum_start_time
    
    logger.info("Training classical model...")
    classical_start_time = time.time()
    classical_loss = classical_model.train(
        train_data[:classical_params['train_samples']],
        epochs=classical_params['epochs'],
        batch_size=classical_params['batch_size']
    )
    classical_train_time = time.time() - classical_start_time
    
    # Visualize training comparison
    visualize_training_comparison(
        quantum_loss, 
        classical_loss,
        save_path=os.path.join(results_dir, "training_loss_comparison.png")
    )
    
    # Sampling time measurement
    logger.info("Generating samples from quantum model...")
    quantum_gen_start_time = time.time()
    quantum_samples = quantum_model.generate_samples(
        num_samples=sample_params['num_samples'],
        shape=input_shape,
        timesteps=sample_params['timesteps']
    )
    quantum_gen_time = time.time() - quantum_gen_start_time
    
    logger.info("Generating samples from classical model...")
    classical_gen_start_time = time.time()
    classical_samples = classical_model.generate_samples(
        num_samples=sample_params['num_samples'],
        shape=input_shape,
        timesteps=sample_params['timesteps']
    )
    classical_gen_time = time.time() - classical_gen_start_time
    
    # Compute quality metrics
    quantum_metrics = compute_metrics(comparison_data, quantum_samples)
    classical_metrics = compute_metrics(comparison_data, classical_samples)
    
    # Visualize sample comparison
    visualize_samples_comparison(
        quantum_samples,
        classical_samples,
        original_samples=comparison_data[:sample_params['num_samples']] if len(comparison_data) > 0 else None,
        save_path=os.path.join(results_dir, "sample_comparison.png")
    )
    
    # Compile benchmark results
    benchmark_results = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'quantum_model': {
            'type': 'QDenseDiffusion',
            'parameters': quantum_params,
            'training_time': quantum_train_time,
            'generation_time': quantum_gen_time,
            'metrics': quantum_metrics,
            'loss_history': [float(loss) for loss in quantum_loss]
        },
        'classical_model': {
            'type': 'ClassicalDiffusionModel',
            'parameters': classical_params,
            'training_time': classical_train_time,
            'generation_time': classical_gen_time,
            'metrics': classical_metrics,
            'loss_history': [float(loss) for loss in classical_loss]
        },
        'sample_parameters': sample_params,
        'data_info': {
            'dataset': 'MNIST',
            'shape': list(input_shape),
            'train_samples': len(train_data),
            'test_samples': len(test_data)
        }
    }
    
    # Save detailed benchmark results
    with open(os.path.join(results_dir, "benchmark_details.json"), "w") as f:
        json.dump(benchmark_results, f, indent=2)
    
    # Create summary
    summary = {
        'quantum_train_time': quantum_train_time,
        'classical_train_time': classical_train_time,
        'quantum_gen_time': quantum_gen_time,
        'classical_gen_time': classical_gen_time,
        'quantum_metrics': quantum_metrics,
        'classical_metrics': classical_metrics,
        'parameter_efficiency': {
            'quantum_params': quantum_model.total_params,
            'classical_params': classical_model.model.count_params()
        }
    }
    
    logger.info("Benchmark Summary:")
    logger.info(f"Quantum Training Time: {quantum_train_time:.2f}s")
    logger.info(f"Classical Training Time: {classical_train_time:.2f}s")
    logger.info(f"Quantum Generation Time: {quantum_gen_time:.2f}s")
    logger.info(f"Classical Generation Time: {classical_gen_time:.2f}s")
    logger.info(f"Quantum Parameters: {quantum_model.total_params}")
    logger.info(f"Classical Parameters: {classical_model.model.count_params()}")
    logger.info(f"Quantum Metrics: {quantum_metrics}")
    logger.info(f"Classical Metrics: {classical_metrics}")
    
    # Save benchmark results using project infrastructure (if available)
    try:
        save_benchmark_results(benchmark_results, "quantum_diffusion_mnist")
    except Exception as e:
        logger.warning(f"Could not save using project infrastructure: {e}")
    
    return benchmark_results

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run enhanced MNIST example for quantum diffusion models')
    
    # Data parameters
    parser.add_argument('--num-samples', type=int, default=100, 
                        help='Number of MNIST samples to use')
    parser.add_argument('--image-size', type=int, default=8,
                        help='Size of downsampled MNIST images (square)')
    
    # Quantum model parameters
    parser.add_argument('--qubits', type=int, default=4,
                        help='Number of qubits for quantum model')
    parser.add_argument('--layers', type=int, default=5, 
                        help='Number of layers for quantum model')
    parser.add_argument('--shots', type=int, default=1000,
                        help='Number of measurement shots per circuit execution')
    parser.add_argument('--q-epochs', type=int, default=3,
                        help='Number of training epochs for quantum model')
    parser.add_argument('--q-batch-size', type=int, default=2,
                        help='Batch size for quantum model training')
    parser.add_argument('--q-lr', type=float, default=0.01,
                        help='Learning rate for quantum model')
    parser.add_argument('--q-train-samples', type=int, default=10,
                        help='Number of samples to train quantum model on')
    
    # Classical model parameters
    parser.add_argument('--latent-dim', type=int, default=16,
                        help='Latent dimension for classical model')
    parser.add_argument('--c-epochs', type=int, default=10,
                        help='Number of training epochs for classical model')
    parser.add_argument('--c-batch-size', type=int, default=16,
                        help='Batch size for classical model training')
    parser.add_argument('--c-train-samples', type=int, default=100,
                        help='Number of samples to train classical model on')
    
    # Sampling parameters
    parser.add_argument('--gen-samples', type=int, default=4,
                        help='Number of samples to generate')
    parser.add_argument('--gen-steps', type=int, default=50,
                        help='Number of diffusion steps for generation')
    
    # Output parameters
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Directory to save results (default: timestamped directory)')
    
    return parser.parse_args()

def main():
    """Main function to run the enhanced MNIST example."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up output directory
    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"mnist_diffusion_results_{timestamp}"
    else:
        output_dir = args.output_dir
    
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Results will be saved to {output_dir}")
    
    # Preprocess MNIST data
    train_data, test_data = preprocess_mnist(
        downsample_size=(args.image_size, args.image_size),
        num_samples=args.num_samples
    )
    
    # Prepare parameters for benchmark
    quantum_params = {
        'num_qubits': args.qubits,
        'num_layers': args.layers,
        'shots': args.shots,
        'epochs': args.q_epochs,
        'batch_size': args.q_batch_size,
        'learning_rate': args.q_lr,
        'train_samples': args.q_train_samples
    }
    
    classical_params = {
        'latent_dim': args.latent_dim,
        'epochs': args.c_epochs,
        'batch_size': args.c_batch_size,
        'train_samples': args.c_train_samples
    }
    
    sample_params = {
        'num_samples': args.gen_samples,
        'timesteps': args.gen_steps
    }
    
    # Save parameters
    with open(os.path.join(output_dir, "parameters.json"), "w") as f:
        json.dump({
            'quantum_params': quantum_params,
            'classical_params': classical_params,
            'sample_params': sample_params,
            'data_params': {
                'num_samples': args.num_samples,
                'image_size': args.image_size
            }
        }, f, indent=2)
    
    # Run benchmark
    logger.info("Starting benchmark...")
    benchmark_results = run_benchmark(
        train_data, 
        test_data, 
        quantum_params, 
        classical_params, 
        sample_params,
        output_dir
    )
    
    # Create summary report
    summary_path = os.path.join(output_dir, "summary.md")
    with open(summary_path, "w") as f:
        f.write("# Quantum vs Classical Diffusion Models Benchmark\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Dataset\n")
        f.write(f"- MNIST (downsampled to {args.image_size}x{args.image_size})\n")
        f.write(f"- {len(train_data)} training samples, {len(test_data)} test samples\n\n")
        
        f.write("## Parameter Efficiency\n")
        f.write(f"- Quantum Model: {benchmark_results['quantum_model']['parameters']['num_qubits']} qubits, ")
        f.write(f"{benchmark_results['quantum_model']['parameters']['num_layers']} layers, ")
        f.write(f"**{quantum_params['num_qubits'] * quantum_params['num_layers'] * 3} parameters**\n")
        f.write(f"- Classical Model: {classical_params['latent_dim']} latent dimension, ")
        f.write(f"**{benchmark_results['classical_model']['parameters']['train_samples']} parameters**\n\n")
        
        f.write("## Performance Metrics\n")
        f.write("### Training Time\n")
        f.write(f"- Quantum: {benchmark_results['quantum_model']['training_time']:.2f} seconds\n")
        f.write(f"- Classical: {benchmark_results['classical_model']['training_time']:.2f} seconds\n\n")
        
        f.write("### Generation Time\n")
        f.write(f"- Quantum: {benchmark_results['quantum_model']['generation_time']:.2f} seconds\n")
        f.write(f"- Classical: {benchmark_results['classical_model']['generation_time']:.2f} seconds\n\n")
        
        f.write("### Quality Metrics\n")
        f.write("| Metric | Quantum | Classical |\n")
        f.write("|--------|---------|------------|\n")
        f.write(f"| MSE    | {benchmark_results['quantum_model']['metrics']['mse']:.4f} | {benchmark_results['classical_model']['metrics']['mse']:.4f} |\n")
        f.write(f"| PSNR   | {benchmark_results['quantum_model']['metrics']['psnr']:.4f} | {benchmark_results['classical_model']['metrics']['psnr']:.4f} |\n")
        f.write(f"| SSIM   | {benchmark_results['quantum_model']['metrics']['ssim']:.4f} | {benchmark_results['classical_model']['metrics']['ssim']:.4f} |\n\n")
        
        f.write("## Visualizations\n")
        f.write("- Sample comparison: [sample_comparison.png](sample_comparison.png)\n")
        f.write("- Training loss comparison: [training_loss_comparison.png](training_loss_comparison.png)\n\n")
        
        f.write("## Conclusions\n")
        
        # Determine which model performed better
        q_metrics = benchmark_results['quantum_model']['metrics']
        c_metrics = benchmark_results['classical_model']['metrics']
        
        if q_metrics['ssim'] > c_metrics['ssim'] and q_metrics['psnr'] > c_metrics['psnr']:
            f.write("The quantum diffusion model achieved superior image quality metrics (SSIM, PSNR) ")
            f.write("compared to the classical model. This suggests quantum advantage in generating ")
            f.write("high-quality samples with fewer parameters.\n\n")
        elif c_metrics['ssim'] > q_metrics['ssim'] and c_metrics['psnr'] > q_metrics['psnr']:
            f.write("The classical diffusion model achieved superior image quality metrics (SSIM, PSNR) ")
            f.write("compared to the quantum model. This suggests that our quantum implementation ")
            f.write("needs further optimization or more qubits/layers to match classical performance.\n\n")
        else:
            f.write("Both models showed comparable performance in different metrics, ")
            f.write("suggesting that our quantum implementation is competitive with ")
            f.write("classical approaches for this simplified MNIST task.\n\n")
        
        # Parameter efficiency
        q_params = quantum_params['num_qubits'] * quantum_params['num_layers'] * 3
        c_params = 43456  # Hardcoded for now based on model summary
        
        if q_params < c_params:
            f.write(f"The quantum model used significantly fewer parameters ({q_params} vs {c_params}), ")
            f.write("demonstrating the parameter efficiency advantage described in quantum diffusion research.\n")
        else:
            f.write("For this small-scale example, the parameter efficiency advantage of quantum diffusion ")
            f.write("was not demonstrated. Larger scale experiments with more qubits may be needed.\n")
    
    logger.info(f"Summary report saved to {summary_path}")
    logger.info(f"All benchmark results saved to {output_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 