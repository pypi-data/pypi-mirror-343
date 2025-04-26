import unittest
import numpy as np
import torch
from quantum_finance.backend.ml_framework import MLFramework, preprocess_data
import os
import tempfile

class TestMLFramework(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.ml_framework = MLFramework()
        # Create sample data for testing
        self.X = np.random.rand(100, 10)  # 100 samples, 10 features
        self.y = np.random.randint(0, 2, 100)  # Binary labels

    def test_initialization(self):
        """Test if MLFramework initializes correctly."""
        self.assertIsNone(self.ml_framework.model)
        self.assertIsNone(self.ml_framework.scaler)
        self.assertEqual(len(self.ml_framework.feedback_data), 0)
        self.assertEqual(len(self.ml_framework.history), 0)
        self.assertEqual(len(self.ml_framework.quantum_features), 0)
        self.assertIsInstance(self.ml_framework.transformer_config, dict)

    def test_preprocess_data(self):
        """Test data preprocessing functionality."""
        X_scaled, scaler = preprocess_data(self.X)
        self.assertIsNotNone(X_scaled)
        self.assertIsNotNone(scaler)
        self.assertEqual(X_scaled.shape, self.X.shape)

    def test_train_model(self):
        """Test model training functionality."""
        model = self.ml_framework.train_model(self.X, self.y)
        self.assertIsNotNone(model)
        self.assertIsNotNone(self.ml_framework.scaler)

    def test_predict(self):
        """Test prediction functionality."""
        # First train the model
        self.ml_framework.train_model(self.X, self.y)
        # Make predictions
        predictions = self.ml_framework.predict(self.X)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), len(self.X))

    def test_update_model_with_feedback(self):
        """Test model update with feedback."""
        prediction = np.random.rand(10)  # Random prediction
        self.ml_framework.update_model_with_feedback(prediction, True)
        self.assertEqual(len(self.ml_framework.feedback_data), 1)

    def test_compute_quantum_features(self):
        """Test quantum feature computation."""
        features = self.ml_framework.compute_quantum_features(self.X)
        self.assertIsNotNone(features)
        self.assertIn('persistence_homology', features)
        self.assertIn('quantum_kernel', features)

    def test_quantum_kernel(self):
        """Test quantum kernel computation."""
        kernel_matrix = self.ml_framework._quantum_kernel(self.X[:5])  # Test with small subset
        self.assertIsNotNone(kernel_matrix)
        self.assertEqual(kernel_matrix.shape, (5, 5))

    def test_optimize_hyperparameters(self):
        """Test hyperparameter optimization."""
        best_params = self.ml_framework.optimize_hyperparameters(self.X, self.y)
        self.assertIsNotNone(best_params)
        self.assertIn('hidden_layer_sizes', best_params)
        self.assertIn('activation', best_params)
        self.assertIn('learning_rate', best_params)
        self.assertIn('max_iter', best_params)

    def test_integrate_quantum_transformer(self):
        """Test quantum transformer integration."""
        input_dim = 10
        self.ml_framework.integrate_quantum_transformer(input_dim)
        self.assertTrue(hasattr(self.ml_framework, 'transformer'))

    def test_train_hybrid_model(self):
        """Test hybrid model training."""
        self.ml_framework.integrate_quantum_transformer(self.X.shape[1])
        self.ml_framework.train_hybrid_model(self.X, self.y, epochs=2)
        self.assertIsNotNone(self.ml_framework.model)

    def test_hybrid_predict(self):
        """Test hybrid prediction functionality."""
        self.ml_framework.integrate_quantum_transformer(self.X.shape[1])
        self.ml_framework.train_hybrid_model(self.X, self.y, epochs=2)
        predictions = self.ml_framework.hybrid_predict(self.X)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), len(self.X))

    def test_save_and_load_hybrid_model(self):
        """Test saving and loading of hybrid model."""
        # Train the model first
        self.ml_framework.integrate_quantum_transformer(self.X.shape[1])
        self.ml_framework.train_hybrid_model(self.X, self.y, epochs=2)
        
        # Create temporary directory for test
        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = os.path.join(tmpdir, 'test_model')
            
            # Save the model
            self.ml_framework.save_hybrid_model(model_path)
            
            # Create new instance and load the model
            new_framework = MLFramework()
            new_framework.load_hybrid_model(model_path)
            
            # Verify the loaded model works
            predictions = new_framework.hybrid_predict(self.X)
            self.assertIsNotNone(predictions)
            self.assertEqual(len(predictions), len(self.X))

if __name__ == '__main__':
    unittest.main() 