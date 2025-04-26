import unittest
import numpy as np
import torch
from quantum_finance.backend.meta_optimizer import LSTMMetaOptimizer


class TestLSTMMetaOptimizer(unittest.TestCase):
    def setUp(self):
        """Initialize the optimizer with test configuration."""
        self.input_dim = 1
        self.hidden_dim = 10
        self.output_dim = 1
        self.n_history = 5
        
        self.optimizer = LSTMMetaOptimizer(
            input_dim=self.input_dim,
            hidden_dim=self.hidden_dim,
            output_dim=self.output_dim,
            n_history=self.n_history
        )
        # Create a dummy history of 15 parameters
        self.dummy_history = np.array([0.1] * 15)
        # Create a sequence of loss values
        self.loss_sequence = [1.0, 0.8, 0.6, 0.5, 0.45, 0.4]

    def test_initialization(self):
        """Test that the optimizer is initialized with correct parameters."""
        self.assertEqual(self.optimizer.input_dim, self.input_dim)
        self.assertEqual(self.optimizer.hidden_dim, self.hidden_dim)
        self.assertEqual(self.optimizer.output_dim, self.output_dim)
        self.assertEqual(self.optimizer.n_history, self.n_history)
        self.assertEqual(len(self.optimizer.loss_history), 0)
        self.assertEqual(len(self.optimizer.update_history), 0)
        self.assertEqual(len(self.optimizer.param_norm_history), 0)

    def test_output_shape(self):
        """Test that the optimizer produces correctly shaped outputs."""
        updated_params = self.optimizer.optimize(self.dummy_history)
        self.assertEqual(updated_params.shape, self.dummy_history.shape)

    def test_values_updated(self):
        """Test that the optimizer actually updates parameter values."""
        updated_params = self.optimizer.optimize(self.dummy_history)
        self.assertFalse(np.allclose(updated_params, self.dummy_history), 
                        "Parameters were not updated.")

    def test_output_type(self):
        """Test that the optimizer produces numpy arrays."""
        updated_params = self.optimizer.optimize(self.dummy_history)
        self.assertIsInstance(updated_params, np.ndarray)

    def test_adaptive_dampening(self):
        """Test that adaptive dampening responds to loss trends."""
        # Initial dampening value
        initial_dampening = self.optimizer.adaptive_dampening
        
        # Simulate improving loss trend
        for loss in self.loss_sequence:
            self.optimizer.optimize(self.dummy_history, current_loss=loss)
        
        # Check that dampening was reduced for improving loss
        self.assertLess(self.optimizer.adaptive_dampening, initial_dampening,
                       "Dampening should decrease with improving loss")
        
        # Simulate worsening loss trend
        for loss in reversed(self.loss_sequence):
            self.optimizer.optimize(self.dummy_history, current_loss=loss)
        
        # Check that dampening was increased for worsening loss
        self.assertGreater(self.optimizer.adaptive_dampening, initial_dampening,
                          "Dampening should increase with worsening loss")

    def test_performance_metrics(self):
        """Test that performance metrics are properly tracked."""
        # Run a few optimization steps
        for loss in self.loss_sequence:
            self.optimizer.optimize(self.dummy_history, current_loss=loss)
        
        metrics = self.optimizer.get_performance_metrics()
        
        # Check that all metric types are present
        self.assertIn('update_norms', metrics)
        self.assertIn('param_norms', metrics)
        self.assertIn('dampening_values', metrics)
        self.assertIn('loss_values', metrics)
        
        # Check that metrics have been recorded
        self.assertEqual(len(metrics['loss_values']), len(self.loss_sequence))
        
        # Test metric reset
        self.optimizer.reset_metrics()
        empty_metrics = self.optimizer.get_performance_metrics()
        for values in empty_metrics.values():
            self.assertEqual(len(values), 0)

    def test_nan_handling(self):
        """Test that the optimizer handles NaN values gracefully."""
        # Create parameters with NaN
        nan_params = np.array([np.nan] * 15)
        
        # Optimize should return original parameters when given NaN
        result = self.optimizer.optimize(nan_params)
        self.assertTrue(np.array_equal(result, nan_params))
        
        # Check that a warning was logged
        # Note: In a real implementation, you might want to use a mock logger
        # and verify that the warning was actually logged

    def test_parameter_bounds(self):
        """Test that parameter updates respect bounds."""
        # Create extreme parameter values
        large_params = np.array([1e6] * 15)
        small_params = np.array([1e-6] * 15)
        
        # Test large parameters
        updated_large = self.optimizer.optimize(large_params)
        self.assertTrue(np.all(np.abs(updated_large) <= large_params * 2))
        
        # Test small parameters
        updated_small = self.optimizer.optimize(small_params)
        self.assertTrue(np.all(np.abs(updated_small) >= small_params / 2))

    def test_forward_pass(self):
        """Test the forward pass of the LSTM network."""
        batch_size = 2
        seq_length = 3
        
        # Create input tensor
        x = torch.randn(batch_size, seq_length, self.input_dim)
        
        # Run forward pass
        with torch.no_grad():
            output = self.optimizer.forward(x)
        
        # Check output shape
        expected_shape = (batch_size, seq_length, self.output_dim)
        self.assertEqual(output.shape, expected_shape)
        
        # Check that output values are finite
        self.assertTrue(torch.all(torch.isfinite(output)))


if __name__ == '__main__':
    unittest.main() 