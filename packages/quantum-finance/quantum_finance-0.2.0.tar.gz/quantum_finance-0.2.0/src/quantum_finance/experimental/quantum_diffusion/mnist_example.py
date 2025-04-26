#!/usr/bin/env python3

"""
MNIST Example for Quantum Diffusion Models

This script demonstrates using the Q-Dense quantum diffusion model with the MNIST dataset.
It serves as a proof of concept for quantum diffusion models in image generation.

The script:
1. Loads and preprocesses MNIST data
2. Creates a simplified Q-Dense model
3. Trains the model on a small subset of MNIST data
4. Generates and visualizes samples

Note: This is a minimal example for demonstration purposes. Training a full model
would require more computational resources and time.
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from sklearn.preprocessing import MinMaxScaler
import os
import sys
import logging
from datetime import datetime
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the QDenseDiffusion model
from experimental.quantum_diffusion.qdense_model import QDenseDiffusion

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def preprocess_mnist(downsample_size=(8, 8), num_samples=100):
    """
    Load and preprocess MNIST dataset.
    
    Args:
        downsample_size (tuple): Target size for downsampled images
        num_samples (int): Number of samples to use
        
    Returns:
        np.ndarray: Preprocessed MNIST data
    """
    logger.info(f"Loading MNIST dataset and preprocessing {num_samples} samples")
    
    # Load MNIST dataset
    (x_train, _), (_, _) = mnist.load_data()
    
    # Take a subset for faster processing
    x_subset = x_train[:num_samples]
    
    # Downsample images to reduce computation requirements
    x_downsampled = []
    for img in x_subset:
        # Simple downsampling by averaging blocks
        h_ratio = img.shape[0] // downsample_size[0]
        w_ratio = img.shape[1] // downsample_size[1]
        
        downsampled = np.zeros(downsample_size)
        for i in range(downsample_size[0]):
            for j in range(downsample_size[1]):
                downsampled[i, j] = np.mean(
                    img[i*h_ratio:(i+1)*h_ratio, j*w_ratio:(j+1)*w_ratio]
                )
        
        x_downsampled.append(downsampled)
    
    # Convert to numpy array
    x_downsampled = np.array(x_downsampled)
    
    # Normalize to [0, 1]
    scaler = MinMaxScaler()
    x_downsampled = np.array([
        scaler.fit_transform(img) for img in x_downsampled
    ])
    
    logger.info(f"Preprocessed {len(x_downsampled)} MNIST images to size {downsample_size}")
    
    return x_downsampled

def visualize_original_vs_noisy(original_images, noisy_images, sample_indices=[0, 1, 2], save_path=None):
    """
    Visualize original images vs. noisy versions.
    
    Args:
        original_images (np.ndarray): Original images
        noisy_images (np.ndarray): Noisy versions
        sample_indices (list): Indices of samples to visualize
        save_path (str): Path to save visualization (if None, display instead)
    """
    num_samples = len(sample_indices)
    fig, axes = plt.subplots(2, num_samples, figsize=(num_samples*3, 6))
    
    for i, idx in enumerate(sample_indices):
        # Original image
        axes[0, i].imshow(original_images[idx], cmap='gray')
        axes[0, i].set_title(f"Original {idx}")
        axes[0, i].axis('off')
        
        # Noisy image
        axes[1, i].imshow(noisy_images[idx], cmap='gray')
        axes[1, i].set_title(f"Noisy {idx}")
        axes[1, i].axis('off')
    
    plt.suptitle("Original vs. Noisy MNIST Images")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def save_samples(samples, dir_name="mnist_samples"):
    """
    Save generated samples to disk.
    
    Args:
        samples (np.ndarray): Samples to save
        dir_name (str): Directory to save samples in
    """
    # Create directory if it doesn't exist
    os.makedirs(dir_name, exist_ok=True)
    
    # Save individual samples
    for i, sample in enumerate(samples):
        plt.figure(figsize=(3, 3))
        plt.imshow(sample, cmap='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(dir_name, f"sample_{i}.png"))
        plt.close()
    
    # Save a grid of all samples
    rows = int(np.ceil(len(samples) / 5))
    cols = min(5, len(samples))
    
    plt.figure(figsize=(cols*2, rows*2))
    for i, sample in enumerate(samples):
        if i < rows*cols:
            plt.subplot(rows, cols, i+1)
            plt.imshow(sample, cmap='gray')
            plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(dir_name, "all_samples.png"))
    plt.close()
    
    logger.info(f"Saved {len(samples)} samples to {dir_name}")

def run_mnist_example():
    """
    Run the MNIST example with Q-Dense diffusion model.
    """
    # Set parameters for a manageable example
    DOWNSAMPLE_SIZE = (8, 8)
    NUM_SAMPLES = 10  # Small number for proof of concept
    NUM_QUBITS = 4    # Simplified for faster execution
    NUM_LAYERS = 5    # Simplified for faster execution
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = f"mnist_results_{timestamp}"
    os.makedirs(results_dir, exist_ok=True)
    
    # Step 1: Load and preprocess MNIST data
    mnist_data = preprocess_mnist(downsample_size=DOWNSAMPLE_SIZE, num_samples=NUM_SAMPLES)
    
    # Step 2: Create a Q-Dense model
    logger.info(f"Creating Q-Dense model with {NUM_QUBITS} qubits and {NUM_LAYERS} layers")
    model = QDenseDiffusion(num_qubits=NUM_QUBITS, num_layers=NUM_LAYERS, shots=1000)
    
    # Step 3: Demonstrate forward diffusion
    logger.info("Demonstrating forward diffusion")
    noisy_images = []
    for i in range(NUM_SAMPLES):
        noisy_image, _ = model.forward_diffusion(mnist_data[i], t=500)
        noisy_images.append(noisy_image)
    
    # Visualize original vs. noisy
    visualize_original_vs_noisy(
        mnist_data, 
        np.array(noisy_images), 
        sample_indices=range(min(3, NUM_SAMPLES)),
        save_path=os.path.join(results_dir, "original_vs_noisy.png")
    )
    
    # Step 4: Train on a very small subset (this is just a demonstration)
    # Note: In practice, this would require much more training
    logger.info("Training Q-Dense model on MNIST subset (simplified demonstration)")
    
    # Use just 5 examples for this demo
    num_train = min(5, NUM_SAMPLES)
    train_subset = mnist_data[:num_train]
    
    # Very brief training (just to demonstrate the process)
    loss_history = model.train(
        train_subset, 
        epochs=2,           # Very small for demo
        batch_size=2,       # Small batch size
        learning_rate=0.01  # Learning rate
    )
    
    # Plot training loss
    plt.figure(figsize=(8, 5))
    plt.plot(loss_history)
    plt.title("Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, "training_loss.png"))
    plt.close()
    
    # Step 5: Generate and visualize samples
    logger.info("Generating samples from trained model")
    
    # Generate a few samples (with reduced timesteps for speed)
    num_gen_samples = 4
    generated_samples = model.generate_samples(
        num_samples=num_gen_samples,
        shape=DOWNSAMPLE_SIZE,
        timesteps=50  # Reduced for demonstration
    )
    
    # Save samples
    save_samples(generated_samples, dir_name=os.path.join(results_dir, "generated_samples"))
    
    # Visualize samples
    model.visualize_samples(
        generated_samples, 
        title="Generated MNIST Samples", 
        save_path=os.path.join(results_dir, "generated_samples.png")
    )
    
    # Save model parameters
    model.save_model(os.path.join(results_dir, "model_params.npy"))
    
    logger.info(f"Example completed. Results saved to {results_dir}")
    logger.info("Note: This is a simplified proof of concept. A full implementation would require more extensive training and larger models.")

if __name__ == "__main__":
    run_mnist_example() 