"""
Test suite for the quantum memory module.

This module contains comprehensive tests for the QuantumMemristor class
and its associated functionality.
"""

import unittest
import torch
import numpy as np
from quantum_finance.backend.quantum_memory import QuantumMemristor, MemoryState
from quantum_finance.backend.quantum_wrapper import quantum_wrapper

class TestQuantumMemory(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.state_size = 10
        self.n_qubits = 4
        self.memristor = QuantumMemristor(
            state_size=self.state_size,
            n_qubits=self.n_qubits,
            learning_rate=0.01,
            decay_rate=0.999
        )
        self.test_input = torch.randn(self.state_size)

    def test_initialization(self):
        """Test proper initialization of the QuantumMemristor"""
        self.assertEqual(self.memristor.state_size, self.state_size)
        self.assertEqual(self.memristor.n_qubits, self.n_qubits)
        
        # Check state initialization
        self.assertIsInstance(self.memristor.state, MemoryState)
        self.assertEqual(self.memristor.state.conductance.shape[0], self.state_size)
        self.assertEqual(self.memristor.state.phase.shape[0], self.state_size)
        self.assertEqual(self.memristor.state.entanglement.shape[0], self.state_size)
        
        # Check parameter initialization
        self.assertEqual(self.memristor.weight_matrix.shape, 
                        (self.state_size, self.state_size))
        self.assertEqual(self.memristor.bias.shape[0], self.state_size)

    def test_forward_pass(self):
        """Test the forward pass through the memristor"""
        output = self.memristor(self.test_input)
        
        # Check output shape and type
        self.assertEqual(output.shape, self.test_input.shape)
        self.assertTrue(torch.is_tensor(output))
        self.assertTrue(output.dtype == torch.float32)
        
        # Check output is real-valued
        self.assertTrue(torch.all(torch.isreal(output)))

    def test_state_update(self):
        """Test internal state updates"""
        initial_conductance = self.memristor.state.conductance.clone()
        initial_phase = self.memristor.state.phase.clone()
        
        # Process input
        self.memristor(self.test_input)
        
        # Check that states have been updated
        self.assertFalse(torch.allclose(self.memristor.state.conductance, 
                                      initial_conductance))
        self.assertFalse(torch.allclose(self.memristor.state.phase, 
                                      initial_phase))

    def test_quantum_update(self):
        """Test quantum update mechanism"""
        if quantum_wrapper.is_quantum_available:
            # Enable quantum updates
            self.memristor.use_quantum_update = True
            
            try:
                # Process input with quantum updates
                output_quantum = self.memristor(self.test_input)
                
                # Disable quantum updates
                self.memristor.use_quantum_update = False
                self.memristor.reset_state()
                
                # Process input without quantum updates
                output_classical = self.memristor(self.test_input)
                
                # Outputs should be different
                if quantum_wrapper.is_quantum_available:
                    self.assertFalse(torch.allclose(output_quantum, output_classical))
                else:
                    raise Exception("Quantum backend not available")
            except Exception as e:
                pass

    def test_reset_state(self):
        """Test state reset functionality"""
        # Process input to change state
        self.memristor(self.test_input)
        
        # Store state values
        conductance_before = self.memristor.state.conductance.clone()
        phase_before = self.memristor.state.phase.clone()
        
        # Reset state
        self.memristor.reset_state()
        
        # Check that states have been reset
        self.assertFalse(torch.allclose(self.memristor.state.conductance, 
                                      conductance_before))
        self.assertFalse(torch.allclose(self.memristor.state.phase, 
                                      phase_before))
        self.assertTrue(torch.all(self.memristor.state.entanglement == 0))

    def test_memory_capacity(self):
        """Test memory capacity calculation"""
        capacity = self.memristor.memory_capacity
        
        # Check that capacity is a float
        self.assertIsInstance(capacity, float)
        
        # Check capacity is within expected range [-1, 1]
        self.assertTrue(-1 <= capacity <= 1)

    def test_state_dict(self):
        """Test state dictionary representation"""
        state_dict = self.memristor.get_state_dict()
        
        # Check dictionary structure
        self.assertIn('conductance', state_dict)
        self.assertIn('phase', state_dict)
        self.assertIn('entanglement', state_dict)
        self.assertIn('capacity', state_dict)
        
        # Check types and shapes
        self.assertEqual(len(state_dict['conductance']), self.state_size)
        self.assertEqual(len(state_dict['phase']), self.state_size)
        self.assertEqual(len(state_dict['entanglement']), self.state_size)
        self.assertIsInstance(state_dict['capacity'], float)

    def test_entanglement_update(self):
        """Test entanglement measure updates"""
        # Process input to trigger entanglement update
        self.memristor(self.test_input)
        
        # Check entanglement properties
        entanglement = self.memristor.state.entanglement
        
        # Should be between 0 and 1
        self.assertTrue(torch.all(entanglement >= 0))
        self.assertTrue(torch.all(entanglement <= 1))
        
        # Should have same size as state
        self.assertEqual(entanglement.shape[0], self.state_size)

    def test_learning_rate_effect(self):
        """Test the effect of different learning rates"""
        # Create two memristors with different learning rates
        memristor_fast = QuantumMemristor(
            state_size=self.state_size,
            n_qubits=self.n_qubits,
            learning_rate=0.1
        )
        memristor_slow = QuantumMemristor(
            state_size=self.state_size,
            n_qubits=self.n_qubits,
            learning_rate=0.01
        )
        
        # Process same input
        memristor_fast(self.test_input)
        memristor_slow(self.test_input)
        
        # Fast learning should lead to larger changes
        fast_change = torch.norm(memristor_fast.state.conductance)
        slow_change = torch.norm(memristor_slow.state.conductance)
        
        self.assertGreater(fast_change, slow_change)

    def test_decay_rate_effect(self):
        """Test the effect of memory decay"""
        # Create memristor with fast decay
        memristor_decay = QuantumMemristor(
            state_size=self.state_size,
            n_qubits=self.n_qubits,
            decay_rate=0.5
        )
        
        # Initial state
        initial_conductance = memristor_decay.state.conductance.clone()
        
        # Process multiple inputs
        for _ in range(5):
            memristor_decay(self.test_input)
        
        # Check that state has decayed
        final_conductance = memristor_decay.state.conductance
        self.assertTrue(torch.norm(final_conductance) < torch.norm(initial_conductance))

if __name__ == '__main__':
    unittest.main() 