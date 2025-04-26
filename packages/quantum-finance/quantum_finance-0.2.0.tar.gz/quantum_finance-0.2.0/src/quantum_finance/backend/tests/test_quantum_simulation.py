import logging
import unittest
import torch

from quantum_finance.backend.quantum_hybrid_engine import QuantumHybridEngine


class TestQuantumSimulation(unittest.TestCase):
    def setUp(self):
        # Setup logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('TestQuantumSimulation')
        self.engine = QuantumHybridEngine()

    def test_run_hybrid_simulation(self):
        # Dummy input for simulation; using a torch tensor with shape (1, 16) as expected by QuantumTransformer (n_qubits=4 leads to 4*4=16)
        test_input = torch.randn(1, 16)
        try:
            result = self.engine.run_hybrid_simulation(test_input, 'grovers')
            self.logger.info(f"Quantum simulation result: {result}")
            # Assert that the result is not None
            self.assertIsNotNone(result, "Simulation result should not be None")
        except Exception as e:
            self.fail(f"Quantum simulation raised an exception: {e}")


if __name__ == '__main__':
    unittest.main() 