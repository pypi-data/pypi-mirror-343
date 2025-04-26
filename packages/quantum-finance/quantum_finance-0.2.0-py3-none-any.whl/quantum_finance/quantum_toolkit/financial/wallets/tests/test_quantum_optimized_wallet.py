"""
Tests for the QuantumOptimizedWallet implementation.
"""

import unittest
from datetime import datetime, timedelta
import numpy as np

from quantum.financial.wallets.quantum_optimized_wallet import QuantumOptimizedWallet

class TestQuantumOptimizedWallet(unittest.TestCase):
    """Test cases for QuantumOptimizedWallet."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.initial_capital = 100000.0
        self.wallet = QuantumOptimizedWallet(
            initial_capital=self.initial_capital,
            num_trajectories=100,  # Reduced for testing
            risk_aversion=1.0,
            rebalance_threshold=0.05
        )
        
        # Sample market data
        self.market_data = {
            'AAPL': {'price': 150.0, 'volume': 1000000},
            'GOOGL': {'price': 2500.0, 'volume': 500000},
            'MSFT': {'price': 300.0, 'volume': 750000}
        }
        
    def test_initialization(self):
        """Test wallet initialization."""
        self.assertEqual(self.wallet.capital, self.initial_capital)
        self.assertEqual(len(self.wallet.holdings), 0)
        self.assertEqual(len(self.wallet.transactions), 0)
        
    def test_execute_trade(self):
        """Test trade execution."""
        # Buy AAPL
        success = self.wallet.execute_trade(
            asset='AAPL',
            quantity=100,
            price=150.0,
            timestamp=datetime.now()
        )
        self.assertTrue(success)
        self.assertEqual(self.wallet.holdings['AAPL'], 100)
        self.assertEqual(self.wallet.capital, self.initial_capital - 100 * 150.0)
        
        # Try to buy more than we can afford
        success = self.wallet.execute_trade(
            asset='GOOGL',
            quantity=1000,
            price=2500.0,
            timestamp=datetime.now()
        )
        self.assertFalse(success)
        
        # Sell some AAPL
        success = self.wallet.execute_trade(
            asset='AAPL',
            quantity=-50,
            price=160.0,
            timestamp=datetime.now()
        )
        self.assertTrue(success)
        self.assertEqual(self.wallet.holdings['AAPL'], 50)
        
    def test_update_and_rebalance(self):
        """Test market data updates and rebalancing."""
        # Initial update
        self.wallet.update(datetime.now(), self.market_data)
        
        # Buy some assets manually first
        self.wallet.execute_trade(
            asset='AAPL',
            quantity=100,
            price=150.0,
            timestamp=datetime.now()
        )
        self.wallet.execute_trade(
            asset='GOOGL',
            quantity=10,
            price=2500.0,
            timestamp=datetime.now()
        )
        
        # Update with new prices
        new_market_data = {
            'AAPL': {'price': 160.0, 'volume': 1000000},
            'GOOGL': {'price': 2600.0, 'volume': 500000},
            'MSFT': {'price': 310.0, 'volume': 750000}
        }
        self.wallet.update(datetime.now(), new_market_data)
        
        # Check that holdings exist
        self.assertTrue(len(self.wallet.holdings) > 0)
        
    def test_get_metrics(self):
        """Test metrics calculation."""
        # Setup some holdings
        self.wallet.execute_trade(
            asset='AAPL',
            quantity=100,
            price=150.0,
            timestamp=datetime.now()
        )
        self.wallet.execute_trade(
            asset='GOOGL',
            quantity=10,
            price=2500.0,
            timestamp=datetime.now()
        )
        
        # Update market data
        self.wallet.update(datetime.now(), self.market_data)
        
        # Get metrics
        metrics = self.wallet.get_metrics()
        
        # Check required metrics exist
        self.assertIn('total_value', metrics)
        self.assertIn('cash_ratio', metrics)
        self.assertIn('value_at_risk', metrics)
        self.assertIn('expected_shortfall', metrics)
        
    def test_get_allocation(self):
        """Test portfolio allocation calculation."""
        # Setup holdings
        self.wallet.execute_trade(
            asset='AAPL',
            quantity=100,
            price=150.0,
            timestamp=datetime.now()
        )
        self.wallet.execute_trade(
            asset='GOOGL',
            quantity=10,
            price=2500.0,
            timestamp=datetime.now()
        )
        
        # Update market data
        self.wallet.update(datetime.now(), self.market_data)
        
        # Get allocation
        allocation = self.wallet.get_allocation()
        
        # Check allocations
        self.assertIn('AAPL', allocation)
        self.assertIn('GOOGL', allocation)
        self.assertGreater(allocation['AAPL'], 0)
        self.assertGreater(allocation['GOOGL'], 0)
        
        # Check total allocation is approximately 1
        total_allocation = sum(allocation.values())
        self.assertAlmostEqual(total_allocation, 1.0, places=2)
        
    def test_risk_metrics(self):
        """Test risk metric calculations."""
        # Setup holdings
        self.wallet.execute_trade(
            asset='AAPL',
            quantity=100,
            price=150.0,
            timestamp=datetime.now()
        )
        self.wallet.execute_trade(
            asset='GOOGL',
            quantity=10,
            price=2500.0,
            timestamp=datetime.now()
        )
        
        # Update market data
        self.wallet.update(datetime.now(), self.market_data)
        
        # Test VaR
        var = self.wallet.get_value_at_risk(
            confidence_level=0.95,
            time_horizon=1
        )
        self.assertGreater(var, 0)
        
        # Test Expected Shortfall
        es = self.wallet.get_expected_shortfall(
            confidence_level=0.95,
            time_horizon=1
        )
        self.assertGreater(es, 0)
        self.assertGreater(es, var)  # ES should be larger than VaR
        
    def test_returns_calculation(self):
        """Test returns calculation."""
        # Setup initial trade
        initial_time = datetime.now()
        self.wallet.execute_trade(
            asset='AAPL',
            quantity=100,
            price=150.0,
            timestamp=initial_time
        )
        
        # Update with initial market data
        self.wallet.update(initial_time, self.market_data)
        
        # Simulate price increase after some time
        later_time = initial_time + timedelta(days=1)
        new_market_data = {
            'AAPL': {'price': 160.0, 'volume': 1000000},
            'GOOGL': {'price': 2600.0, 'volume': 500000},
            'MSFT': {'price': 310.0, 'volume': 750000}
        }
        self.wallet.update(later_time, new_market_data)
        
        # Calculate returns
        abs_return, pct_return = self.wallet.get_returns(
            initial_time,
            later_time
        )
        
        # Check returns are positive
        self.assertGreater(abs_return, 0)
        self.assertGreater(pct_return, 0)

if __name__ == '__main__':
    unittest.main() 