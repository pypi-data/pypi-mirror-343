''' 
Module: test_quantum_simulator.py
Description: Unit tests for the quantum_simulator.py module. 
This test suite verifies the correctness of the basic quantum gate operations: Hadamard, Pauli-X, and the stubbed CNOT.
'''

import numpy as np
import pytest
from backend import quantum_simulator


# Define expected quantum states for convenience
ket_zero = np.array([[1.0], [0.0]], dtype=complex)
ket_one = np.array([[0.0], [1.0]], dtype=complex)


def test_apply_hadamard_on_ket_zero():
    '''
    Test the Hadamard operation on the |0> state.
    Expected result is 1/√2 * ([1, 1])
    '''
    result = quantum_simulator.apply_hadamard(ket_zero)
    expected = (1/np.sqrt(2)) * np.array([[1.0], [1.0]], dtype=complex)
    np.testing.assert_allclose(result, expected, rtol=1e-5, atol=1e-8)


def test_apply_pauli_x_on_ket_zero():
    '''
    Test the Pauli-X operation on the |0> state.
    Expected result is |1> state.
    '''
    result = quantum_simulator.apply_pauli_x(ket_zero)
    np.testing.assert_allclose(result, ket_one, rtol=1e-5, atol=1e-8)


def test_apply_cnot_with_control_ket_one():
    '''
    Test the CNOT operation where control is |1>. 
    According to our stub, if control is |1> then target gets a Pauli-X applied.
    For target starting as |0>, applying Pauli-X gives |1>.
    '''
    control = ket_one.copy()
    target = ket_zero.copy()
    new_control, new_target = quantum_simulator.apply_cnot(control, target)
    # The control should remain |1>
    np.testing.assert_allclose(new_control, ket_one, rtol=1e-5, atol=1e-8)
    # The target should be flipped to |1>
    np.testing.assert_allclose(new_target, ket_one, rtol=1e-5, atol=1e-8)


def test_apply_cnot_with_control_ket_zero():
    '''
    Test the CNOT operation where control is |0>.
    In this case, the target should remain unchanged.
    '''
    control = ket_zero.copy()
    target = ket_one.copy()
    new_control, new_target = quantum_simulator.apply_cnot(control, target)
    np.testing.assert_allclose(new_control, ket_zero, rtol=1e-5, atol=1e-8)
    np.testing.assert_allclose(new_target, ket_one, rtol=1e-5, atol=1e-8)


if __name__ == '__main__':
    pytest.main([__file__]) 