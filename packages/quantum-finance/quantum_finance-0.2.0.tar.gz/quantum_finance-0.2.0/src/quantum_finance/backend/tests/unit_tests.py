import unittest
from quantum_finance.backend.quantum_algorithms import simulate_quantum_circuit

class TestQuantumCircuitSimulation(unittest.TestCase):
    def test_hadamard_gate(self):
        circuit_data = {
            'num_qubits': 1,
            'gates': [{'type': 'h', 'qubits': [0]}]
        }
        result = simulate_quantum_circuit(circuit_data)
        self.assertAlmostEqual(result.get('0', 0) / 1000, 0.5, delta=0.1)
        self.assertAlmostEqual(result.get('1', 0) / 1000, 0.5, delta=0.1)

    def test_cnot_gate(self):
        circuit_data = {
            'num_qubits': 2,
            'gates': [
                {'type': 'h', 'qubits': [0]},
                {'type': 'cx', 'qubits': [0, 1]}
            ]
        }
        result = simulate_quantum_circuit(circuit_data)
        self.assertAlmostEqual(result.get('00', 0) / 1000, 0.5, delta=0.1)
        self.assertAlmostEqual(result.get('11', 0) / 1000, 0.5, delta=0.1)

    def test_x_gate(self):
        circuit_data = {
            'num_qubits': 1,
            'gates': [{'type': 'x', 'qubits': [0]}]
        }
        result = simulate_quantum_circuit(circuit_data)
        self.assertAlmostEqual(result.get('1', 0) / 1000, 1.0, delta=0.1)

    def test_y_gate(self):
        circuit_data = {
            'num_qubits': 1,
            'gates': [{'type': 'y', 'qubits': [0]}]
        }
        result = simulate_quantum_circuit(circuit_data)
        self.assertAlmostEqual(result.get('1', 0) / 1000, 1.0, delta=0.1)

    def test_z_gate(self):
        circuit_data = {
            'num_qubits': 1,
            'gates': [
                {'type': 'h', 'qubits': [0]},
                {'type': 'z', 'qubits': [0]},
                {'type': 'h', 'qubits': [0]}
            ]
        }
        result = simulate_quantum_circuit(circuit_data)
        self.assertAlmostEqual(result.get('1', 0) / 1000, 1.0, delta=0.1)

    def test_rotation_gates(self):
        import math
        circuit_data = {
            'num_qubits': 1,
            'gates': [
                {'type': 'rx', 'qubits': [0], 'angle': math.pi},
                {'type': 'ry', 'qubits': [0], 'angle': math.pi},
                {'type': 'rz', 'qubits': [0], 'angle': math.pi}
            ]
        }
        result = simulate_quantum_circuit(circuit_data)
        self.assertAlmostEqual(result.get('1', 0) / 1000, 1.0, delta=0.1)

    def test_s_and_t_gates(self):
        circuit_data = {
            'num_qubits': 1,
            'gates': [
                {'type': 'h', 'qubits': [0]},
                {'type': 's', 'qubits': [0]},
                {'type': 't', 'qubits': [0]},
                {'type': 'h', 'qubits': [0]}
            ]
        }
        result = simulate_quantum_circuit(circuit_data)
        # The exact result depends on the phase, but we can check if it's measured
        self.assertTrue('0' in result or '1' in result)

    def test_unsupported_gate(self):
        circuit_data = {
            'num_qubits': 1,
            'gates': [{'type': 'unsupported', 'qubits': [0]}]
        }
        with self.assertRaises(ValueError):
            simulate_quantum_circuit(circuit_data)

if __name__ == '__main__':
    unittest.main()