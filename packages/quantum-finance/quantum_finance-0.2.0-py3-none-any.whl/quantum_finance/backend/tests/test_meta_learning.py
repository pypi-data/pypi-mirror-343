import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from quantum_finance.backend.meta_learning import meta_optimizer, gradient_free_optimization


def test_meta_optimizer():
    """Test that meta_optimizer returns None as a stub."""
    optimizer = meta_optimizer([])
    assert optimizer is None, "Expected meta_optimizer to return None as stub."


def test_gradient_free_optimization():
    """Test that gradient_free_optimization returns initial parameters unchanged as a stub."""
    # Define a dummy objective function that returns a constant value
    objective_fn = lambda x: 42
    initial_params = [1.0, 2.0, 3.0]
    optimized_params = gradient_free_optimization(objective_fn, initial_params)
    # As a stub, gradient_free_optimization should return initial_params unchanged
    assert optimized_params == initial_params, "Expected gradient_free_optimization to return initial parameters unchanged."


if __name__ == '__main__':
    test_meta_optimizer()
    test_gradient_free_optimization()
    print('All meta_learning tests passed!') 