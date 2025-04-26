#!/usr/bin/env python3

"""
Visualize the generated images from text-to-image generation.

This script creates a grid visualization of all the generated images
from the text-to-image generation process.

Usage:
    python visualize_results.py --dir text_to_image_test_results
"""

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import logging
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def visualize_images(image_dir: str, output_file: str = None) -> None:
    """
    Create a grid visualization of all images in the directory.
    
    Args:
        image_dir: Directory containing the images
        output_file: Path to save the visualization, if None uses image_dir/grid.png
    """
    if not os.path.exists(image_dir) or not os.path.isdir(image_dir):
        logger.error(f"Image directory does not exist: {image_dir}")
        return
    
    if output_file is None:
        output_file = os.path.join(image_dir, "grid_visualization.png")
    
    # Find all image files
    image_extensions = ['.png', '.jpg', '.jpeg']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob(os.path.join(image_dir, f"*{ext}")))
    
    if not image_files:
        logger.warning(f"No image files found in {image_dir}")
        return
    
    logger.info(f"Found {len(image_files)} images in {image_dir}")
    
    # Sort images by name
    image_files.sort()
    
    # Load images
    images = []
    titles = []
    
    for img_file in image_files:
        try:
            # Skip grid visualizations
            if "grid" in os.path.basename(img_file) or "display" in os.path.basename(img_file):
                continue
                
            # Load image
            img = plt.imread(img_file)
            images.append(img)
            
            # Extract title from filename
            filename = os.path.basename(img_file)
            # Remove timestamp and extension
            parts = filename.split('_')
            if len(parts) > 2:
                # Skip timestamp (first part)
                title = ' '.join(parts[1:-1])  # Skip the last part (index)
            else:
                title = filename
                
            # Clean up title
            title = title.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
            titles.append(title)
            
        except Exception as e:
            logger.error(f"Error loading {img_file}: {str(e)}")
    
    if not images:
        logger.warning("No valid images loaded")
        return
    
    # Create grid
    n_images = len(images)
    cols = min(4, n_images)
    rows = (n_images + cols - 1) // cols
    
    plt.figure(figsize=(4*cols, 4*rows))
    
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(rows, cols, i+1)
        plt.imshow(img)
        plt.title(title)
        plt.axis('off')
    
    plt.suptitle("Generated Images from Text Prompts", fontsize=16)
    plt.tight_layout()
    
    # Save visualization
    plt.savefig(output_file)
    plt.close()
    
    logger.info(f"Saved grid visualization to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Visualize generated images")
    parser.add_argument("--dir", type=str, required=True, help="Directory containing images")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    args = parser.parse_args()
    
    visualize_images(args.dir, args.output)

if __name__ == "__main__":
    main() 