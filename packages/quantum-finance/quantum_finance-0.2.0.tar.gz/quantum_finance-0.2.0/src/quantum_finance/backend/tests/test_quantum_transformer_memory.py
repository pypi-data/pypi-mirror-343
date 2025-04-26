"""
Test suite for the memory-enhanced quantum transformer implementation.

This module tests the integration of quantum memory components with the transformer architecture.
"""

import unittest
import torch
import numpy as np
from quantum_finance.backend.quantum_transformer import QuantumTransformer, QuantumTransformerLayer
from quantum_finance.backend.quantum_memory import QuantumMemristor

class TestQuantumTransformerMemory(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.d_model = 64
        self.n_heads = 4
        self.n_layers = 2
        self.n_qubits = 4
        self.memory_size = 32
        self.batch_size = 8
        self.seq_len = 10
        
        # Create model
        self.model = QuantumTransformer(
            d_model=self.d_model,
            n_heads=self.n_heads,
            n_layers=self.n_layers,
            n_qubits=self.n_qubits,
            memory_size=self.memory_size
        )
        
        # Create sample input
        self.test_input = torch.randn(self.batch_size, self.d_model)
        self.test_seq_input = torch.randn(self.seq_len, self.batch_size, self.d_model)

    def test_transformer_layer_memory(self):
        """Test quantum memory integration in transformer layer"""
        layer = QuantumTransformerLayer(
            d_model=self.d_model,
            n_heads=self.n_heads,
            n_qubits=self.n_qubits,
            memory_size=self.memory_size
        )
        
        # Check memory initialization
        self.assertIsInstance(layer.quantum_memory, QuantumMemristor)
        self.assertEqual(layer.quantum_memory.state_size, self.memory_size)
        
        # Test forward pass
        x = torch.randn(self.seq_len, self.batch_size, self.d_model)
        output = layer(x)
        
        # Check output shape
        self.assertEqual(output.shape, x.shape)
        
        # Check memory state
        memory_state = layer.memory_state
        self.assertIn('conductance', memory_state)
        self.assertIn('phase', memory_state)
        self.assertIn('entanglement', memory_state)

    def test_transformer_memory_reset(self):
        """Test memory reset functionality"""
        # Process input to change memory state
        initial_states = self.model.get_memory_states()
        output = self.model(self.test_input)
        
        # Get updated states
        updated_states = self.model.get_memory_states()
        
        # Verify states changed
        for init_state, updated_state in zip(initial_states, updated_states):
            self.assertFalse(
                np.allclose(
                    init_state['conductance'],
                    updated_state['conductance']
                )
            )
        
        # Reset memory
        self.model.reset_memory()
        reset_states = self.model.get_memory_states()
        
        # Verify states reset
        for reset_state in reset_states:
            self.assertEqual(len(reset_state['entanglement']), self.memory_size)
            self.assertTrue(all(x == 0 for x in reset_state['entanglement']))

    def test_memory_integration(self):
        """Test memory integration in forward pass"""
        # Process sequence input
        output1 = self.model(self.test_seq_input)
        memory_states1 = self.model.get_memory_states()
        
        # Process same input again
        output2 = self.model(self.test_seq_input)
        memory_states2 = self.model.get_memory_states()
        
        # Outputs should be different due to memory effect
        self.assertFalse(torch.allclose(output1, output2))
        
        # Memory states should be different
        for state1, state2 in zip(memory_states1, memory_states2):
            self.assertFalse(
                np.allclose(
                    state1['conductance'],
                    state2['conductance']
                )
            )

    def test_gradient_flow(self):
        """Test gradient flow through memory components"""
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters())
        
        # Forward pass
        output = self.model(self.test_input)
        loss = output.mean()
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        
        # Check gradients
        for layer in self.model.layers:
            self.assertIsNotNone(layer.memory_in_proj.weight.grad)
            self.assertIsNotNone(layer.memory_out_proj.weight.grad)

    def test_memory_size_configuration(self):
        """Test different memory size configurations"""
        # Test with default memory size
        model_default = QuantumTransformer(
            d_model=self.d_model,
            n_heads=self.n_heads,
            n_layers=self.n_layers,
            n_qubits=self.n_qubits
        )
        
        # Memory size should default to d_model
        for layer in model_default.layers:
            self.assertEqual(layer.memory_size, self.d_model)
        
        # Test with custom memory size
        custom_size = 16
        model_custom = QuantumTransformer(
            d_model=self.d_model,
            n_heads=self.n_heads,
            n_layers=self.n_layers,
            n_qubits=self.n_qubits,
            memory_size=custom_size
        )
        
        # Check custom memory size
        for layer in model_custom.layers:
            self.assertEqual(layer.memory_size, custom_size)

    def test_sequential_memory_effects(self):
        """Test memory effects in sequential processing"""
        # Create sequence of inputs
        sequence = [torch.randn(self.batch_size, self.d_model) for _ in range(5)]
        outputs = []
        
        # Process sequence
        for x in sequence:
            outputs.append(self.model(x))
        
        # Check that outputs are different
        for i in range(len(outputs)-1):
            self.assertFalse(torch.allclose(outputs[i], outputs[i+1]))
        
        # Reset memory and process again
        self.model.reset_memory()
        new_outputs = []
        for x in sequence:
            new_outputs.append(self.model(x))
        
        # Check that the new sequence produces different results
        for out1, out2 in zip(outputs, new_outputs):
            self.assertFalse(torch.allclose(out1, out2))

    def test_memory_capacity(self):
        """Test memory capacity tracking"""
        # Get initial capacities
        initial_states = self.model.get_memory_states()
        initial_capacities = [state['capacity'] for state in initial_states]
        
        # Process multiple inputs
        for _ in range(5):
            self.model(self.test_input)
        
        # Get updated capacities
        final_states = self.model.get_memory_states()
        final_capacities = [state['capacity'] for state in final_states]
        
        # Check that capacities changed
        for init_cap, final_cap in zip(initial_capacities, final_capacities):
            self.assertNotEqual(init_cap, final_cap)

if __name__ == '__main__':
    unittest.main() 