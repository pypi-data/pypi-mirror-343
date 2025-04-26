#!/usr/bin/env python3

"""
Verification and Benchmarking Script for QU-Net

This script performs the following tasks:
1. Examines generated images in the output directory
2. Visualizes the forward diffusion process (adding noise)
3. Visualizes the reverse diffusion process (denoising)
4. Assesses the quality of generated samples
5. Benchmarks performance between simulated and actual quantum computation

Usage:
    python verify_and_benchmark.py --output_dir quick_test_results_20250308_133521
"""

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import time
import json
from typing import Dict, List, Tuple, Optional, Union
import logging

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import QU-Net model and text-to-image functionality
from experimental.quantum_diffusion.qunet_model import QUNetDiffusion, QuantumConvolution
from experimental.quantum_diffusion.text_to_image import QuantumTextToImage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def examine_output_directory(output_dir: str) -> Dict[str, str]:
    """
    Examine the output directory and return paths to key files.
    
    Args:
        output_dir: Path to the output directory
        
    Returns:
        Dictionary mapping file types to file paths
    """
    logger.info(f"Examining output directory: {output_dir}")
    
    # Check if directory exists
    if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        logger.error(f"Output directory does not exist: {output_dir}")
        return {}
    
    # Check for key files
    file_mapping = {
        'summary': None,
        'forward_diffusion': None,
        'reverse_diffusion': None,
        'generated_samples': None,
        'training_loss': None
    }
    
    # Find files by pattern matching
    for file_type in file_mapping:
        matching_files = glob(os.path.join(output_dir, f"{file_type}*"))
        if matching_files:
            file_mapping[file_type] = matching_files[0]
    
    # Log found files
    for file_type, file_path in file_mapping.items():
        if file_path:
            logger.info(f"Found {file_type} file: {file_path}")
        else:
            logger.warning(f"Could not find {file_type} file")
    
    return file_mapping


def visualize_forward_diffusion(model: QUNetDiffusion, output_dir: str) -> str:
    """
    Visualize the forward diffusion process (adding noise).
    
    Args:
        model: QUNetDiffusion model
        output_dir: Directory to save the visualization
        
    Returns:
        Path to the saved visualization
    """
    logger.info("Visualizing forward diffusion process")
    
    # Create a sample image (Gaussian blob)
    image_size = model.image_size
    x, y = np.meshgrid(
        np.linspace(-1, 1, image_size),
        np.linspace(-1, 1, image_size)
    )
    sigma = 0.3
    sample_image = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # Apply forward diffusion at different timesteps
    timesteps = [0, 100, 200, 400, 600, 800, 999]
    diffused_images = []
    
    for t in timesteps:
        noisy_image = model.forward_diffusion(sample_image, t)
        # Handle tuple return type if present
        if isinstance(noisy_image, tuple):
            noisy_image = noisy_image[0]  # Extract the first element from the tuple
        
        # Ensure noisy_image has the correct shape (height, width)
        if hasattr(noisy_image, 'shape') and len(noisy_image.shape) > 2:
            noisy_image = noisy_image[0]  # Take the first image if multiple returned
        
        diffused_images.append(noisy_image)
    
    # Create visualization
    plt.figure(figsize=(15, 5))
    for i, (t, img) in enumerate(zip(timesteps, diffused_images)):
        plt.subplot(1, len(timesteps), i + 1)
        plt.imshow(img, cmap='gray')
        plt.title(f"t={t}")
        plt.axis('off')
    
    plt.suptitle("Forward Diffusion Process (Adding Noise)")
    plt.tight_layout()
    
    # Save visualization
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "forward_diffusion_visualization.png")
    plt.savefig(output_path)
    plt.close()
    
    logger.info(f"Saved forward diffusion visualization to {output_path}")
    return output_path


def visualize_reverse_diffusion(model: QUNetDiffusion, output_dir: str) -> str:
    """
    Visualize the reverse diffusion process (denoising).
    
    Args:
        model: QUNetDiffusion model
        output_dir: Directory to save the visualization
        
    Returns:
        Path to the saved visualization
    """
    logger.info("Visualizing reverse diffusion process")
    
    # Start with random noise
    image_size = model.image_size
    np.random.seed(42)  # For reproducibility
    noisy_image = np.random.randn(image_size, image_size)
    
    # Apply reverse diffusion
    timesteps = list(range(980, -1, -140))  # [980, 840, 700, 560, 420, 280, 140, 0]
    denoised_images = []
    
    # Add the initial noisy image
    denoised_images.append(noisy_image)
    
    # Current x_t
    x_t = noisy_image
    
    # Apply reverse diffusion steps
    for t in timesteps[:-1]:  # Skip the last timestep (0) for the loop
        x_t = model.reverse_diffusion(x_t, t)
        
        # Handle tuple return type if present
        if isinstance(x_t, tuple):
            x_t = x_t[0]  # Extract the first element from the tuple
            
        # Ensure correct shape
        if hasattr(x_t, 'shape') and len(x_t.shape) > 2:
            x_t = x_t[0]  # Take the first image if multiple returned
            
        denoised_images.append(x_t)
    
    # Create visualization
    plt.figure(figsize=(16, 6))
    titles = ["Initial Noise"] + [f"t={t}" for t in timesteps[:-1]]
    
    for i, (title, img) in enumerate(zip(titles, denoised_images)):
        plt.subplot(1, len(denoised_images), i + 1)
        
        # Normalize for visualization
        if np.min(img) < 0 or np.max(img) > 1:
            display_img = (img - np.min(img)) / (np.max(img) - np.min(img))
        else:
            display_img = img
            
        plt.imshow(display_img, cmap='gray')
        plt.title(title)
        plt.axis('off')
    
    plt.suptitle("Reverse Diffusion Process (Denoising)")
    plt.tight_layout()
    
    # Save visualization
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "reverse_diffusion_visualization.png")
    plt.savefig(output_path)
    plt.close()
    
    logger.info(f"Saved reverse diffusion visualization to {output_path}")
    return output_path


def generate_and_assess_samples(model: QUNetDiffusion, num_samples: int, output_dir: str) -> str:
    """
    Generate samples and assess their quality.
    
    Args:
        model: QUNetDiffusion model
        num_samples: Number of samples to generate
        output_dir: Directory to save the results
        
    Returns:
        Path to the saved visualization
    """
    logger.info(f"Generating and assessing {num_samples} samples")
    
    # Generate samples
    start_time = time.time()
    samples = model.generate(num_samples=num_samples, image_shape=(model.image_size, model.image_size))
    generation_time = time.time() - start_time
    
    logger.info(f"Generated {num_samples} samples in {generation_time:.2f} seconds")
    
    # Handle tuple return type if present
    if isinstance(samples, tuple):
        samples = samples[0]  # Extract the first element from the tuple
    
    # Ensure samples has the right shape
    if hasattr(samples, 'shape'):
        if len(samples.shape) < 3:
            # If only one sample with shape (height, width)
            samples = samples.reshape(1, samples.shape[0], samples.shape[1])
        elif len(samples.shape) > 3:
            # If extra dimensions
            samples = samples.reshape(samples.shape[0], samples.shape[1], samples.shape[2])
    else:
        # If samples is not a numpy array, try to convert it
        try:
            samples = np.array(samples)
            if len(samples.shape) < 3:
                samples = samples.reshape(1, samples.shape[0], samples.shape[1])
        except:
            logger.error("Could not convert samples to a numpy array with the right shape")
            return ""
    
    # Calculate quality metrics
    metrics = {
        'mean_value': float(np.mean(samples)),
        'std_dev': float(np.std(samples)),
        'min_value': float(np.min(samples)),
        'max_value': float(np.max(samples)),
        'generation_time': generation_time,
        'generation_time_per_sample': generation_time / num_samples
    }
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    for i, sample in enumerate(samples):
        plt.subplot(2, (num_samples + 1) // 2, i + 1)
        
        # Normalize for visualization
        if np.min(sample) < 0 or np.max(sample) > 1:
            display_img = (sample - np.min(sample)) / (np.max(sample) - np.min(sample))
        else:
            display_img = sample
            
        plt.imshow(display_img, cmap='gray')
        plt.title(f"Sample {i+1}")
        plt.axis('off')
    
    plt.suptitle(f"Generated Samples (Generation time: {generation_time:.2f}s)")
    plt.tight_layout()
    
    # Save visualization
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "generated_samples_assessment.png")
    plt.savefig(output_path)
    plt.close()
    
    # Save metrics
    metrics_path = os.path.join(output_dir, "sample_quality_metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logger.info(f"Saved sample quality assessment to {output_path}")
    logger.info(f"Saved sample quality metrics to {metrics_path}")
    
    return output_path


def benchmark_quantum_computation(model: QUNetDiffusion, output_dir: str) -> str:
    """
    Benchmark the performance difference between simulation and actual quantum computation.
    
    Args:
        model: QUNetDiffusion model
        output_dir: Directory to save the results
        
    Returns:
        Path to the saved benchmark results
    """
    logger.info("Benchmarking quantum computation vs. simulation")
    
    # Run the benchmark
    benchmark_results = model.benchmark_quantum_convolution(num_runs=5)
    
    # Extract data for plotting
    sim_times = benchmark_results['simulation']['times']
    quantum_times = benchmark_results['quantum']['times']
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    
    # Plot timing comparison
    plt.subplot(2, 1, 1)
    plt.bar([1], [np.mean(sim_times)], width=0.4, label='Simulation', alpha=0.7)
    plt.bar([1.5], [np.mean(quantum_times)], width=0.4, label='Quantum', alpha=0.7)
    plt.errorbar([1], [np.mean(sim_times)], yerr=[np.std(sim_times)], fmt='o', color='blue')
    plt.errorbar([1.5], [np.mean(quantum_times)], yerr=[np.std(quantum_times)], fmt='o', color='orange')
    plt.xticks([1, 1.5], ['Simulation', 'Quantum'])
    plt.ylabel('Time (seconds)')
    plt.title('Execution Time Comparison')
    plt.legend()
    
    # Plot individual run times
    plt.subplot(2, 1, 2)
    plt.plot(range(1, len(sim_times) + 1), sim_times, 'o-', label='Simulation')
    plt.plot(range(1, len(quantum_times) + 1), quantum_times, 'o-', label='Quantum')
    plt.xlabel('Run Number')
    plt.ylabel('Time (seconds)')
    plt.title('Execution Time per Run')
    plt.legend()
    
    plt.suptitle('Quantum Computation vs. Simulation Benchmark')
    plt.tight_layout()
    
    # Save visualization
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "quantum_benchmark_results.png")
    plt.savefig(output_path)
    plt.close()
    
    # Save raw benchmark data
    benchmark_path = os.path.join(output_dir, "quantum_benchmark_data.json")
    with open(benchmark_path, 'w') as f:
        # Convert numpy arrays to lists for JSON serialization
        serializable_results = {
            'simulation': {
                'avg_time': float(benchmark_results['simulation']['avg_time']),
                'times': [float(t) for t in benchmark_results['simulation']['times']],
                'std_dev': float(benchmark_results['simulation']['std_dev'])
            },
            'quantum': {
                'avg_time': float(benchmark_results['quantum']['avg_time']),
                'times': [float(t) for t in benchmark_results['quantum']['times']],
                'std_dev': float(benchmark_results['quantum']['std_dev'])
            },
            'comparison': {
                'speedup_factor': float(benchmark_results['comparison']['speedup_factor']),
                'time_difference': float(benchmark_results['comparison']['time_difference']),
                'result_correlation': float(benchmark_results['comparison']['result_correlation'])
            }
        }
        json.dump(serializable_results, f, indent=2)
    
    logger.info(f"Saved benchmark results to {output_path}")
    logger.info(f"Saved benchmark data to {benchmark_path}")
    
    return output_path


def demonstrate_text_to_image(output_dir: str) -> str:
    """
    Demonstrate text-to-image generation with the NLP processor integration.
    
    Args:
        output_dir: Directory to save the results
        
    Returns:
        Path to the saved visualization
    """
    logger.info("Demonstrating text-to-image generation")
    
    # Create text-to-image generator
    t2i = QuantumTextToImage(image_size=16, embedding_size=16)
    
    # Generate images for different text prompts
    prompts = [
        "Quantum computer",
        "Entangled qubits",
        "Quantum superposition",
        "Wave function collapse"
    ]
    
    all_images = []
    for prompt in prompts:
        logger.info(f"Generating image for prompt: '{prompt}'")
        images = t2i.generate_image(prompt, num_samples=1)
        
        # Handle tuple return type if present
        if isinstance(images, tuple):
            images = images[0]  # Extract the first element from the tuple
            
        # Ensure correct shape
        if hasattr(images, 'shape'):
            if len(images.shape) > 3:
                images = images.reshape(images.shape[0], images.shape[1], images.shape[2])
            elif len(images.shape) < 3 and len(images.shape) > 0:
                images = images.reshape(1, images.shape[0], images.shape[1])
        else:
            # If images is not a numpy array, try to convert it
            try:
                images = np.array(images)
                if len(images.shape) < 3:
                    images = images.reshape(1, images.shape[0], images.shape[1])
            except:
                logger.error(f"Could not convert images for prompt '{prompt}' to a numpy array")
                continue
                
        all_images.append((prompt, images[0]))
    
    # Create visualization
    plt.figure(figsize=(12, 10))
    for i, (prompt, img) in enumerate(all_images):
        plt.subplot(2, 2, i + 1)
        
        # Normalize for visualization
        if np.min(img) < 0 or np.max(img) > 1:
            display_img = (img - np.min(img)) / (np.max(img) - np.min(img))
        else:
            display_img = img
            
        plt.imshow(display_img, cmap='gray')
        plt.title(f'"{prompt}"')
        plt.axis('off')
    
    plt.suptitle("Text-to-Image Generation Examples")
    plt.tight_layout()
    
    # Save visualization
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "text_to_image_examples.png")
    plt.savefig(output_path)
    plt.close()
    
    logger.info(f"Saved text-to-image examples to {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Verify and benchmark QU-Net implementation")
    parser.add_argument("--output_dir", type=str, required=False, 
                        default="quantum_diffusion_verification",
                        help="Directory to save verification results")
    parser.add_argument("--examine_dir", type=str, required=False,
                        help="Directory containing existing results to examine")
    parser.add_argument("--image_size", type=int, default=16,
                        help="Size of images for generation (square)")
    parser.add_argument("--num_samples", type=int, default=4,
                        help="Number of samples to generate for quality assessment")
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Examine existing results if specified
    if args.examine_dir:
        file_mapping = examine_output_directory(args.examine_dir)
        
        # Display images if found
        for file_type, file_path in file_mapping.items():
            if file_path and file_path.endswith(('.png', '.jpg', '.jpeg')):
                plt.figure(figsize=(10, 8))
                img = plt.imread(file_path)
                plt.imshow(img)
                plt.title(f"{file_type.replace('_', ' ').title()}")
                plt.axis('off')
                plt.tight_layout()
                plt.savefig(os.path.join(args.output_dir, f"existing_{file_type}.png"))
                plt.close()
    
    # Initialize QU-Net model
    logger.info(f"Initializing QUNetDiffusion with image size {args.image_size}")
    model = QUNetDiffusion(
        image_size=args.image_size,
        base_channels=4,
        depth=2,
        kernel_size=3,
        qconv_layers=2,
        shots=1000
    )
    
    # Perform verification and benchmarking
    visualize_forward_diffusion(model, args.output_dir)
    visualize_reverse_diffusion(model, args.output_dir)
    generate_and_assess_samples(model, args.num_samples, args.output_dir)
    benchmark_quantum_computation(model, args.output_dir)
    demonstrate_text_to_image(args.output_dir)
    
    logger.info(f"Verification and benchmarking completed. Results saved to {args.output_dir}")


if __name__ == "__main__":
    main() 