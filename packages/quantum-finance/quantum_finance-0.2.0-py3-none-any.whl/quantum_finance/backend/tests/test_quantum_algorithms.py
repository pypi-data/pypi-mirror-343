"""
Module: test_quantum_algorithms.py
Description: Contains unit tests for the quantum algorithm implementations in the platform.
Note: Inline documentation and type annotations have been added per project deployment updates.
"""

import unittest
from quantum_finance.backend.qio_module import QuantumInspiredOptimizer
from quantum_finance.backend.quantum_algorithms import (
    QuantumCircuitSimulator, 
    grovers_algorithm, 
    simulate_quantum_circuit, 
    QuantumCircuit, 
    shor_factorization,
    run_grover  # Add this instead of grover_search
)
import numpy as np
from qiskit import execute
from qiskit_aer import AerSimulator

class TestQuantumAlgorithms(unittest.TestCase):
    def test_qio(self):
        def fitness_func(x):
            return -np.sum((x - 0.5)**2)

        qio = QuantumInspiredOptimizer(problem_size=5)
        best_solution = qio.optimize(fitness_func, generations=50)
        
        self.assertEqual(len(best_solution), 5)
        self.assertTrue(all(0 <= x <= 1 for x in best_solution))
        self.assertGreater(fitness_func(best_solution), -1)  # Assuming reasonable convergence

    def test_quantum_circuit_simulator(self):
        simulator = QuantumCircuitSimulator(2)
        simulator.apply_gate('H', 0)
        simulator.apply_controlled_gate('CX', 0, 1)
        simulator.measure()
        results = simulator.run(shots=1000)
        
        self.assertIn('00', results)
        self.assertIn('11', results)
        self.assertTrue(abs(results['00'] - results['11']) < 100)  # Roughly equal probabilities

    def test_grovers_algorithm(self):
        def oracle(circuit):
            circuit.z(0)
            circuit.z(1)

        grover_circuit = grovers_algorithm(2, oracle)
        backend = AerSimulator()
        job = execute(grover_circuit, backend, shots=1000)
        result = job.result()
        counts = result.get_counts()
        
        self.assertIn('11', counts)
        self.assertTrue(counts['11'] > 900)  # High probability of correct answer

    def test_simulate_quantum_circuit(self):
        # Test a simple Bell state
        num_qubits = 2
        gates = [
            {'type': 'h', 'qubit': 0},
            {'type': 'cx', 'qubit': (0, 1)},
        ]
        result = simulate_quantum_circuit(num_qubits, gates)
        
        # We expect to see only '00' and '11' states with roughly equal probability
        self.assertIn('00', result)
        self.assertIn('11', result)
        self.assertNotIn('01', result)
        self.assertNotIn('10', result)
        
        # Check if probabilities are roughly equal (within 10% margin)
        total_shots = sum(result.values())
        self.assertAlmostEqual(result['00'] / total_shots, 0.5, delta=0.1)
        self.assertAlmostEqual(result['11'] / total_shots, 0.5, delta=0.1)

    def test_simulate_quantum_circuit_more_gates(self):
        # Test a more complex circuit
        num_qubits = 3
        gates = [
            {'type': 'h', 'qubit': 0},
            {'type': 'cx', 'qubit': (0, 1)},
            {'type': 'h', 'qubit': 2},
            {'type': 'cx', 'qubit': (1, 2)},
        ]
        result = simulate_quantum_circuit(num_qubits, gates)
        
        # We expect to see all states with roughly equal probability
        for state in ['000', '001', '010', '011', '100', '101', '110', '111']:
            self.assertIn(state, result)
        
        total_shots = sum(result.values())
        for state in result:
            self.assertAlmostEqual(result[state] / total_shots, 1/8, delta=0.1)

    def test_grover_search(self):
        # Example test for Grover's algorithm
        database = [0, 1, 1, 0]
        target = 1
        result = run_grover(database, target)
        assert result in [1, 2]  # Indices where target is found

    def test_quantum_circuit_creation(self):
        circuit = QuantumCircuit(2)
        self.assertEqual(circuit.num_qubits, 2)
        self.assertEqual(len(circuit.gates), 0)

    def test_add_gate(self):
        circuit = QuantumCircuit(2)
        circuit.add_gate('H', 0)
        self.assertEqual(len(circuit.gates), 1)
        self.assertEqual(circuit.gates[0], ('H', 0))

    def test_measure(self):
        circuit = QuantumCircuit(1)
        circuit.add_gate('H', 0)
        result = circuit.measure()
        self.assertIn(result, [0, 1])

    def test_error_handling(self):
        circuit = QuantumCircuit(1)
        with self.assertRaises(ValueError):
            circuit.add_gate('InvalidGate', 0)

    def test_entanglement(self):
        circuit = QuantumCircuit(2)
        circuit.add_gate('H', 0)
        circuit.add_gate('CNOT', (0, 1))
        state = circuit.get_state()
        expected_state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
        np.testing.assert_array_almost_equal(state, expected_state)

    def test_noise_model(self):
        circuit = QuantumCircuit(1, noise_model='depolarizing')
        circuit.add_gate('H', 0)
        noisy_result = circuit.measure(shots=1000)
        # Check if the results are close to 50/50 but not exactly
        self.assertTrue(400 < noisy_result.count(0) < 600)

if __name__ == '__main__':
    unittest.main()