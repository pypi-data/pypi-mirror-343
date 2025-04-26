#!/usr/bin/env python3

"""
Quick Test Script for MNIST Quantum Diffusion 

This script runs a very small test of the quantum diffusion model on MNIST data
to validate that the implementation works correctly.

It uses minimal resources to allow for quick testing.
"""

import os
import sys
import logging
import numpy as np
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the QDenseDiffusion model
from experimental.quantum_diffusion.qdense_model import QDenseDiffusion

def create_test_data():
    """Create simple test data for validation."""
    # Create a 2x2 checkerboard pattern expanded to 8x8
    pattern = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            if (i // 4 + j // 4) % 2 == 0:
                pattern[i, j] = 1.0
    
    # Create 2 different patterns
    pattern2 = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            if ((i // 2) % 2) == ((j // 2) % 2):
                pattern2[i, j] = 1.0
    
    # Create a dataset of these patterns
    data = np.stack([pattern, pattern2])
    logger.info(f"Created test dataset with shape {data.shape}")
    
    return data

def run_test():
    """Run a quick test of the QDenseDiffusion model."""
    # Configuration
    NUM_QUBITS = 3  # Small number for quick test
    NUM_LAYERS = 2  # Minimal layers
    SHOTS = 500     # Reduced shots
    
    # Create test data
    test_data = create_test_data()
    
    # Create directory for results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = f"quick_test_results_{timestamp}"
    os.makedirs(results_dir, exist_ok=True)
    
    # Save test data images
    import matplotlib.pyplot as plt
    for i, img in enumerate(test_data):
        plt.figure(figsize=(3, 3))
        plt.imshow(img, cmap='gray')
        plt.title(f"Test Pattern {i+1}")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, f"test_pattern_{i+1}.png"))
        plt.close()
    
    # Initialize model
    logger.info(f"Initializing Q-Dense model with {NUM_QUBITS} qubits and {NUM_LAYERS} layers")
    model = QDenseDiffusion(
        num_qubits=NUM_QUBITS, 
        num_layers=NUM_LAYERS,
        shots=SHOTS
    )
    
    # Test forward diffusion
    logger.info("Testing forward diffusion...")
    noisy_image, _ = model.forward_diffusion(test_data[0], t=500)
    
    plt.figure(figsize=(6, 3))
    plt.subplot(1, 2, 1)
    plt.imshow(test_data[0], cmap='gray')
    plt.title("Original")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(noisy_image, cmap='gray')
    plt.title("Noisy (t=500)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "forward_diffusion_test.png"))
    plt.close()
    
    # Test training for a single step
    logger.info("Testing training step...")
    loss = model.train_step(test_data, learning_rate=0.01)
    logger.info(f"Training step loss: {loss:.6f}")
    
    # Test sampling with minimal steps
    logger.info("Testing sampling (with 10 diffusion steps)...")
    sample = model.sample(shape=(8, 8), timesteps=10)
    
    plt.figure(figsize=(3, 3))
    plt.imshow(sample, cmap='gray')
    plt.title("Generated Sample")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "generated_sample.png"))
    plt.close()
    
    # Test quantum denoising step
    logger.info("Testing quantum denoising step...")
    predicted_noise = model.quantum_denoising_step(noisy_image, t=500)
    
    plt.figure(figsize=(6, 3))
    plt.subplot(1, 2, 1)
    plt.imshow(noisy_image, cmap='gray')
    plt.title("Noisy Image")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(predicted_noise, cmap='gray')
    plt.title("Predicted Noise")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "denoising_test.png"))
    plt.close()
    
    # Test visualization function
    logger.info("Testing visualization...")
    samples = model.generate_samples(num_samples=2, shape=(8, 8), timesteps=10)
    model.visualize_samples(
        samples, 
        title="Test Samples", 
        save_path=os.path.join(results_dir, "test_visualization.png")
    )
    
    # Test saving and loading model parameters
    logger.info("Testing model save/load...")
    model_path = os.path.join(results_dir, "test_model.npy")
    model.save_model(model_path)
    model.load_model(model_path)
    
    logger.info(f"All tests completed successfully! Results saved to {results_dir}")
    logger.info("This quick test validates the basic functionality of the QDenseDiffusion model.")
    logger.info("For full benchmarking, run the mnist_example_enhanced.py script.")

if __name__ == "__main__":
    run_test() 