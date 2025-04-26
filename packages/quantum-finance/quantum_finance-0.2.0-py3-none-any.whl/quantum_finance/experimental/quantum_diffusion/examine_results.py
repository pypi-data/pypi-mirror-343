#!/usr/bin/env python3

"""
Simple script to examine and display the existing generated images in a results directory

Usage:
    python examine_results.py --dir quick_test_results_20250308_133521
"""

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import json
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def examine_and_display_results(results_dir: str, output_dir: str = None) -> None:
    """
    Examine and display the results in the given directory.
    
    Args:
        results_dir: Directory containing the results
        output_dir: Directory to save the displayed results, if None uses results_dir
    """
    if not os.path.exists(results_dir) or not os.path.isdir(results_dir):
        logger.error(f"Results directory does not exist: {results_dir}")
        return
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(results_dir), "examination_results")
    
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Examining results in: {results_dir}")
    logger.info(f"Saving examination results to: {output_dir}")
    
    # Look for images in the results directory
    image_extensions = ['.png', '.jpg', '.jpeg']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob(os.path.join(results_dir, f"*{ext}")))
    
    # Also look for markdown or text summary files
    summary_files = glob(os.path.join(results_dir, "*.md")) + glob(os.path.join(results_dir, "*.txt"))
    
    if not image_files and not summary_files:
        logger.warning(f"No image or summary files found in {results_dir}")
        return
    
    # Print summary files content
    for summary_file in summary_files:
        try:
            with open(summary_file, 'r') as f:
                content = f.read()
                
            logger.info(f"Content of {os.path.basename(summary_file)}:")
            print("\n" + "="*80)
            print(content)
            print("="*80 + "\n")
            
            # Save to output directory
            with open(os.path.join(output_dir, os.path.basename(summary_file)), 'w') as f:
                f.write(content)
                
        except Exception as e:
            logger.error(f"Error reading {summary_file}: {str(e)}")
    
    # Display and save images
    for img_file in image_files:
        try:
            # Get image name
            img_name = os.path.basename(img_file)
            logger.info(f"Displaying {img_name}")
            
            # Read and display image
            img = plt.imread(img_file)
            
            plt.figure(figsize=(10, 8))
            plt.imshow(img)
            plt.title(img_name.replace('_', ' ').replace('.png', '').replace('.jpg', '').replace('.jpeg', ''))
            plt.axis('off')
            plt.tight_layout()
            
            # Save to output directory
            output_path = os.path.join(output_dir, f"display_{img_name}")
            plt.savefig(output_path)
            plt.close()
            
            logger.info(f"Saved display to {output_path}")
            
        except Exception as e:
            logger.error(f"Error displaying {img_file}: {str(e)}")
    
    logger.info(f"Examination complete. Results saved to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Examine and display results")
    parser.add_argument("--dir", type=str, required=True, help="Directory containing results to examine")
    parser.add_argument("--output", type=str, default=None, help="Directory to save examination results")
    args = parser.parse_args()
    
    examine_and_display_results(args.dir, args.output)

if __name__ == "__main__":
    main() 