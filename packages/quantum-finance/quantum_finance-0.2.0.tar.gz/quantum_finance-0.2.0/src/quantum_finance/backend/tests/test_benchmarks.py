import pytest
import time
import numpy as np

# This is a sample benchmark test added to ensure performance metrics can be captured.
# It benchmarks a heavy computation function which sums numbers from 0 to 9999.

def heavy_computation():
    total = 0
    for i in range(10000):
        total += i
    return total


def test_heavy_computation():
    """Test performance of a computationally intensive function."""
    
    def heavy_computation(size=1000):
        """A computationally intensive function for benchmarking."""
        matrix = np.random.random((size, size))
        result = np.linalg.svd(matrix)
        return result
    
    # Measure execution time instead of using benchmark fixture
    start_time = time.time()
    result = heavy_computation(size=100)  # Reduced size for faster tests
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Heavy computation executed in {execution_time:.4f} seconds")
    
    # Verify the result has the expected structure
    assert len(result) == 3  # SVD returns 3 arrays 