#!/usr/bin/env python3

"""
Test script for the text-to-image generation functionality.

This script demonstrates how to use the QuantumTextToImage class 
to generate images from text descriptions.

Usage:
    python test_text_to_image.py
"""

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import logging
import time

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import text-to-image functionality
from experimental.quantum_diffusion.text_to_image import QuantumTextToImage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_text_to_image(output_dir: str = "text_to_image_test_results", 
                      image_size: int = 16,
                      num_samples: int = 2,
                      custom_prompts: list = None):
    """
    Test the text-to-image generation functionality.
    
    Args:
        output_dir: Directory to save the results
        image_size: Size of generated images
        num_samples: Number of samples to generate for each prompt
        custom_prompts: Custom prompts to use, if None uses default prompts
    """
    logger.info(f"Testing text-to-image generation with image size {image_size}")
    
    # Create text-to-image generator
    t2i = QuantumTextToImage(image_size=image_size, embedding_size=16)
    
    # Use default prompts if custom prompts not provided
    if custom_prompts is None:
        prompts = [
            "Quantum computer with entangled qubits",
            "Quantum superposition state",
            "Quantum algorithm visualization",
            "Quantum wave function collapse"
        ]
    else:
        prompts = custom_prompts
    
    # Generate images for each prompt
    for i, prompt in enumerate(prompts):
        logger.info(f"Generating {num_samples} images for prompt: '{prompt}'")
        
        # Record start time
        start_time = time.time()
        
        # Generate images
        images = t2i.generate_image(prompt, num_samples=num_samples)
        
        # Record generation time
        generation_time = time.time() - start_time
        logger.info(f"Generated {num_samples} images in {generation_time:.2f} seconds")
        
        # Save images
        image_paths = t2i.save_generated_images(images, prompt, output_dir)
        
        logger.info(f"Saved images to: {', '.join(image_paths)}")
    
    logger.info(f"Text-to-image generation test completed")

def main():
    parser = argparse.ArgumentParser(description="Test text-to-image generation")
    parser.add_argument("--output", type=str, default="text_to_image_test_results", 
                        help="Directory to save test results")
    parser.add_argument("--size", type=int, default=16, 
                        help="Size of generated images (square)")
    parser.add_argument("--samples", type=int, default=2, 
                        help="Number of samples to generate for each prompt")
    parser.add_argument("--prompts", type=str, nargs="+", 
                        help="Custom prompts to use (optional)")
    args = parser.parse_args()
    
    test_text_to_image(args.output, args.size, args.samples, args.prompts)

if __name__ == "__main__":
    main() 