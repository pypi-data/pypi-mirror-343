import pytest
from quantum_finance.backend.quantum_wrapper import quantum_wrapper

def test_quantum_backend_info():
    """Test that the quantum backend info contains the expected keys."""
    backend_info = quantum_wrapper.backend_info
    
    # Check that the quantum_available key exists
    assert 'quantum_available' in backend_info
    
    # In simulation mode, quantum_available should be False
    assert backend_info['quantum_available'] is False 