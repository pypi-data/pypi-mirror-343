import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from quantum_finance.backend.distributed_computing import distributed_simulation


class DummyCircuitSegment:
    def __init__(self, value):
        self.value = value
    
    def run(self):
        # Simply return the stored value
        return self.value


class TestDistributedComputing(unittest.TestCase):

    def test_distributed_simulation(self):
        # Create a list of dummy circuit segments
        segments = [DummyCircuitSegment(i) for i in range(5)]
        # Run the distributed simulation
        results = distributed_simulation(segments)
        # Verify the results are as expected (i.e., each segment returns its value)
        expected = [i for i in range(5)]
        self.assertEqual(results, expected)


if __name__ == '__main__':
    unittest.main() 