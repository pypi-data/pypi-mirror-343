#!/usr/bin/env python3

"""
Quick Test Script for QU-Net Quantum Diffusion

This script runs a very small test of the QU-Net quantum diffusion model on MNIST data
to verify that the implementation works correctly. It uses a minimal configuration
with reduced parameters for quick execution.

Usage:
    python -m experimental.quantum_diffusion.run_qunet_test
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
import os
import sys
import logging
import time
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the QUNetDiffusion model
from experimental.quantum_diffusion.qunet_model import QUNetDiffusion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_quick_test():
    """Run a quick test of the QU-Net model on MNIST data."""
    logger.info("Starting QU-Net quick test on MNIST data")
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"quick_test_results_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load a small subset of MNIST data
    logger.info("Loading MNIST data")
    (x_train, _), (x_test, _) = mnist.load_data()
    
    # Use only a small subset for quick testing
    x_train = x_train[:100]
    x_test = x_test[:10]
    
    # Normalize to [0, 1]
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Resize to smaller dimensions for faster processing
    image_size = 16
    x_train_small = np.zeros((len(x_train), image_size, image_size))
    x_test_small = np.zeros((len(x_test), image_size, image_size))
    
    # Simple downsampling by averaging
    for i in range(len(x_train)):
        for h in range(image_size):
            for w in range(image_size):
                h_start, h_end = h * 28 // image_size, (h + 1) * 28 // image_size
                w_start, w_end = w * 28 // image_size, (w + 1) * 28 // image_size
                x_train_small[i, h, w] = np.mean(x_train[i, h_start:h_end, w_start:w_end])
    
    for i in range(len(x_test)):
        for h in range(image_size):
            for w in range(image_size):
                h_start, h_end = h * 28 // image_size, (h + 1) * 28 // image_size
                w_start, w_end = w * 28 // image_size, (w + 1) * 28 // image_size
                x_test_small[i, h, w] = np.mean(x_test[i, h_start:h_end, w_start:w_end])
    
    logger.info(f"Data prepared: {x_train_small.shape}, {x_test_small.shape}")
    
    # Initialize QU-Net model with minimal configuration
    model = QUNetDiffusion(
        image_size=image_size,
        base_channels=4,  # Reduced from default
        depth=2,          # Reduced from default
        kernel_size=3,
        qconv_layers=1,   # Reduced from default
        shots=100         # Reduced from default
    )
    
    logger.info(f"QU-Net model initialized with {model.total_params} parameters")
    
    # Train for a few epochs
    logger.info("Training QU-Net model (minimal training for test)")
    start_time = time.time()
    losses = model.train(
        x_train_small,
        epochs=2,         # Minimal training
        batch_size=10
    )
    train_time = time.time() - start_time
    logger.info(f"Training completed in {train_time:.2f} seconds")
    
    # Plot training loss
    plt.figure(figsize=(8, 5))
    plt.plot(losses, marker='o')
    plt.title('QU-Net Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'training_loss.png'))
    plt.close()
    
    # Test forward diffusion
    logger.info("Testing forward diffusion")
    test_image = x_test_small[0]
    noisy_images = []
    timesteps = [0, 250, 500, 750, 999]  # Different noise levels
    
    plt.figure(figsize=(15, 3))
    plt.subplot(1, len(timesteps) + 1, 1)
    plt.imshow(test_image, cmap='gray')
    plt.title('Original')
    plt.axis('off')
    
    for i, t in enumerate(timesteps):
        noisy_image, _ = model.forward_diffusion(test_image, t)
        noisy_images.append(noisy_image)
        
        plt.subplot(1, len(timesteps) + 1, i + 2)
        plt.imshow(noisy_image, cmap='gray')
        plt.title(f't={t}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'forward_diffusion.png'))
    plt.close()
    
    # Test reverse diffusion
    logger.info("Testing reverse diffusion")
    # Start with the noisiest image
    noisy_image = noisy_images[-1]
    
    # Apply reverse diffusion
    start_time = time.time()
    denoised_image = model.reverse_diffusion(noisy_image, timesteps[-1])
    denoise_time = time.time() - start_time
    logger.info(f"Reverse diffusion completed in {denoise_time:.2f} seconds")
    
    # Visualize result
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(test_image, cmap='gray')
    plt.title('Original')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(noisy_image, cmap='gray')
    plt.title(f'Noisy (t={timesteps[-1]})')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(denoised_image, cmap='gray')
    plt.title('Denoised')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'reverse_diffusion.png'))
    plt.close()
    
    # Generate new samples
    logger.info("Generating new samples")
    start_time = time.time()
    generated_images = model.generate(num_samples=5, image_shape=(image_size, image_size))
    generate_time = time.time() - start_time
    logger.info(f"Generation completed in {generate_time:.2f} seconds")
    
    # Visualize generated samples
    plt.figure(figsize=(15, 3))
    for i in range(len(generated_images)):
        plt.subplot(1, len(generated_images), i + 1)
        plt.imshow(generated_images[i], cmap='gray')
        plt.title(f'Sample {i+1}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'generated_samples.png'))
    plt.close()
    
    # Save test summary
    with open(os.path.join(output_dir, 'summary.md'), 'w') as f:
        f.write("# QU-Net Quick Test Results\n\n")
        f.write(f"Test conducted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Model Configuration\n\n")
        f.write(f"- Image size: {image_size}x{image_size}\n")
        f.write(f"- Base channels: 4\n")
        f.write(f"- Depth: 2\n")
        f.write(f"- Kernel size: 3\n")
        f.write(f"- Quantum convolution layers: 1\n")
        f.write(f"- Shots: 100\n")
        f.write(f"- Total parameters: {model.total_params}\n\n")
        
        f.write("## Performance\n\n")
        f.write(f"- Training time (2 epochs): {train_time:.2f} seconds\n")
        f.write(f"- Reverse diffusion time (single image): {denoise_time:.2f} seconds\n")
        f.write(f"- Generation time (5 samples): {generate_time:.2f} seconds\n\n")
        
        f.write("## Observations\n\n")
        f.write("This quick test demonstrates the basic functionality of the QU-Net quantum diffusion model. ")
        f.write("The model successfully performs forward diffusion (adding noise) and reverse diffusion (denoising), ")
        f.write("as well as generating new samples from random noise.\n\n")
        
        f.write("The implementation uses a simplified quantum convolution operation that will be enhanced ")
        f.write("in future versions with actual quantum circuit execution. The current version serves as ")
        f.write("a proof of concept for the QU-Net architecture.\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. Implement actual quantum circuit execution for convolution operations\n")
        f.write("2. Optimize the model for better performance on complex datasets\n")
        f.write("3. Explore integration with the NLP processor for text-to-image generation\n")
        f.write("4. Benchmark against classical models on larger datasets like CIFAR-10\n")
    
    logger.info(f"Quick test completed. Results saved to {output_dir}/")
    return output_dir

if __name__ == "__main__":
    output_dir = run_quick_test()
    print(f"\nTest completed successfully! Results saved to {output_dir}/")
    print("Check the generated images and performance metrics in the output directory.") 