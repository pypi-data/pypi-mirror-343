from quantum_finance.backend.quantum_algorithms import GroversAlgorithm, ShorWrapper
from quantum_finance.backend.ml_framework import BayesianNN
from quantum_finance.backend.quantum_transformer import QuantumTransformer
import numpy as np

class QuantumHybridEngine:
    def __init__(self):
        self.quantum_algs = {
            'grovers': GroversAlgorithm(),
            'shors': ShorWrapper()
        }
        self.bayesian_nn = BayesianNN()
        self.quantum_transformer = QuantumTransformer(64, 4, 2, 4)

    def run_hybrid_simulation(self, input_data, simulation_type):
        quantum_results = self._run_quantum_simulation(input_data, simulation_type)
        classical_results = self._run_classical_simulation(input_data)
        return self._combine_results(quantum_results, classical_results)

    def _run_quantum_simulation(self, input_data, simulation_type):
        if simulation_type in self.quantum_algs:
            return self.quantum_algs[simulation_type].run(input_data)
        else:
            raise ValueError(f"Unsupported quantum simulation type: {simulation_type}")

    def _run_classical_simulation(self, input_data):
        bayesian_output = self.bayesian_nn.predict(input_data)
        transformer_output = self.quantum_transformer.forward(input_data)

        # Detach transformer output if it's a torch tensor that requires grad
        if hasattr(transformer_output, 'detach'):
            transformer_output = transformer_output.detach().numpy()

        # If bayesian_output is None, replace with zeros of the same shape as transformer_output
        if bayesian_output is None:
            bayesian_output = np.zeros(transformer_output.shape)
        else:
            bayesian_output = np.array(bayesian_output)

        return np.mean([bayesian_output, transformer_output], axis=0)

    def _combine_results(self, quantum_results, classical_results):
        # Convert quantum_results to a numeric numpy array if not already numeric;
        # if quantum_results is not numeric (e.g., a string), default to zeros with the same shape as classical_results
        if not (isinstance(quantum_results, np.ndarray) and np.issubdtype(quantum_results.dtype, np.number)):
            quantum_results = np.zeros_like(classical_results)
        return 0.6 * quantum_results + 0.4 * classical_results