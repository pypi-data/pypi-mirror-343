import unittest
import numpy as np
from pathlib import Path
import shutil
import time
import matplotlib.pyplot as plt
from quantum_finance.backend.visualization import create_visualizer, MetaOptimizerVisualizer


class TestMetaOptimizerVisualizer(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path("test_visualization_output")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            
        self.visualizer = create_visualizer(
            update_interval=0.1,  # Short interval for testing
            save_dir=str(self.test_dir),
            max_points=5  # Small number for testing
        )
        
        # Create sample metrics
        self.sample_metrics = {
            'loss_values': [1.0, 0.8, 0.6],
            'update_norms': [0.1, 0.08, 0.06],
            'param_norms': [1.0, 1.1, 1.2],
            'dampening_values': [0.1, 0.095, 0.09]
        }
        
    def tearDown(self):
        """Clean up test environment."""
        plt.close('all')  # Close all figures
        self.visualizer.close()
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            
    def test_initialization(self):
        """Test that the visualizer initializes correctly."""
        self.assertTrue(self.test_dir.exists())
        self.assertEqual(self.visualizer.max_points, 5)
        self.assertEqual(self.visualizer.update_interval, 0.1)
        
        # Check that all required metrics are initialized
        expected_metrics = {
            'loss_values', 'update_norms', 'param_norms',
            'dampening_values', 'learning_rates', 'gradient_norms'
        }
        self.assertEqual(
            set(self.visualizer.metrics_history.keys()),
            expected_metrics
        )
        
    def test_update_metrics(self):
        """Test that metrics are updated correctly."""
        # Update with initial metrics
        self.visualizer.update_metrics(
            metrics=self.sample_metrics,
            current_lr=0.001,
            current_grad_norm=0.1
        )
        
        # Check that metrics were stored
        for key, values in self.sample_metrics.items():
            self.assertEqual(
                self.visualizer.metrics_history[key][-1],
                values[-1]
            )
            
        # Check learning rate and gradient norm
        self.assertEqual(self.visualizer.metrics_history['learning_rates'][-1], 0.001)
        self.assertEqual(self.visualizer.metrics_history['gradient_norms'][-1], 0.1)
        
    def test_max_points_limit(self):
        """Test that the number of stored points is limited correctly."""
        # Create more points than max_points
        many_points = list(range(10))  # More than max_points=5
        
        # Update multiple times
        for point in many_points:
            metrics = {
                'loss_values': [float(point)],
                'update_norms': [float(point)],
                'param_norms': [float(point)],
                'dampening_values': [float(point)]
            }
            self.visualizer.update_metrics(metrics)
            
        # Check that only max_points are stored
        for key in self.sample_metrics.keys():
            self.assertLessEqual(
                len(self.visualizer.metrics_history[key]),
                self.visualizer.max_points
            )
            
    def test_plot_saving(self):
        """Test that plots are saved correctly."""
        # Update metrics multiple times to ensure plot saving
        for i in range(3):  # Update multiple times
            metrics = {
                'loss_values': [1.0 - i * 0.1],
                'update_norms': [0.1 - i * 0.01],
                'param_norms': [1.0 + i * 0.1],
                'dampening_values': [0.1 - i * 0.005]
            }
            self.visualizer.update_metrics(
                metrics=metrics,
                current_lr=0.001,
                current_grad_norm=0.1
            )
            # Force a plot refresh
            self.visualizer.refresh_plots()
            # Ensure plot is saved
            self.visualizer.save_current_plot()
            # Wait a bit to ensure file is written
            time.sleep(0.2)
        
        # Check that plot files exist
        plot_files = list(self.test_dir.glob("*.png"))
        self.assertGreater(len(plot_files), 0, "No plot files were saved")
        
        # Verify file properties
        for plot_file in plot_files:
            self.assertTrue(plot_file.exists(), f"Plot file {plot_file} does not exist")
            self.assertGreater(plot_file.stat().st_size, 0, f"Plot file {plot_file} is empty")
        
    def test_error_handling(self):
        """Test that the visualizer handles errors gracefully."""
        # Test with empty metrics
        try:
            self.visualizer.update_metrics({})
        except Exception as e:
            self.fail(f"update_metrics failed with empty metrics: {str(e)}")
            
        # Test with None values
        try:
            self.visualizer.update_metrics(
                self.sample_metrics,
                current_lr=None,
                current_grad_norm=None
            )
        except Exception as e:
            self.fail(f"update_metrics failed with None values: {str(e)}")
            
    def test_notebook_detection(self):
        """Test notebook detection functionality."""
        # Should return False in unittest environment
        self.assertFalse(self.visualizer._check_if_notebook())


if __name__ == '__main__':
    unittest.main() 