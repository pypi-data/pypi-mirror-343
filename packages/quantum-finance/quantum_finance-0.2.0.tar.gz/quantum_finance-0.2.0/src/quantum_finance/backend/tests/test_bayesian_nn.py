import logging
import unittest
import numpy as np

from quantum_finance.backend.quantum_hybrid_engine import QuantumHybridEngine


class TestBayesianNN(unittest.TestCase):
    def setUp(self):
        # Setup logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('TestBayesianNN')
        self.engine = QuantumHybridEngine()

    def test_bayesian_nn_update(self):
        # Create dummy data for Bayesian NN update
        X = np.random.rand(10, 5)  # 10 samples, 5 features each
        y = np.random.rand(10)     # 10 dummy target values
        try:
            # Attempt to update the Bayesian NN with dummy data
            self.engine.bayesian_nn.update(X, y)
            self.logger.info("Bayesian NN update successful with dummy data.")
        except Exception as e:
            self.fail(f"Bayesian NN update raised an exception: {e}")


if __name__ == '__main__':
    unittest.main() 