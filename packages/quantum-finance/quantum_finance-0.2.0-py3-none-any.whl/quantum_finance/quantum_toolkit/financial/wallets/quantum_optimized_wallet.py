"""
Quantum Optimized Wallet Implementation

This module implements a wallet that uses quantum optimization techniques
for portfolio management and risk assessment.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from copy import deepcopy

from quantum_finance.quantum_toolkit.stochastic.stochastic_quantum_finance import StochasticQuantumFinance
from .base_wallet import BaseWallet

class QuantumOptimizedWallet(BaseWallet):
    """
    A wallet implementation that uses quantum optimization for portfolio management.
    
    This wallet leverages quantum stochastic methods for:
    - Portfolio optimization
    - Risk assessment
    - Value at Risk calculation
    - Expected Shortfall estimation
    """
    
    def __init__(self,
                 initial_capital: float = 0.0,
                 num_trajectories: int = 1000,
                 risk_aversion: float = 1.0,
                 rebalance_threshold: float = 0.05):
        """
        Initialize the quantum optimized wallet.
        
        Args:
            initial_capital: Initial amount of capital
            num_trajectories: Number of quantum trajectories for simulation
            risk_aversion: Risk aversion parameter (higher = more conservative)
            rebalance_threshold: Threshold for portfolio rebalancing
        """
        super().__init__(initial_capital)
        self.risk_aversion = risk_aversion
        self.rebalance_threshold = rebalance_threshold
        
        # Initialize quantum finance engine
        self._quantum_finance = None  # Lazy initialization
        self._num_trajectories = num_trajectories
        
        # Cache for optimization results
        self._last_optimization_time = None
        self._last_optimal_weights = None
        self._optimization_cache_ttl = 3600  # 1 hour
        
        # Market data cache
        self._market_data_cache = {}
        self._price_history = {}
        
    def initialize(self, initial_capital: float) -> None:
        """
        Initialize wallet with starting capital.
        
        Args:
            initial_capital: Initial amount of capital
        """
        self._capital = initial_capital
        self._holdings.clear()
        self._transactions.clear()
        self._creation_time = datetime.now()
        self._last_update_time = None
        
    def _ensure_quantum_finance(self, num_assets: int):
        """
        Ensure quantum finance engine is initialized with correct dimensions.
        
        Args:
            num_assets: Number of assets to model
        """
        if (self._quantum_finance is None or 
            self._quantum_finance.num_assets != num_assets):
            self._quantum_finance = StochasticQuantumFinance(
                num_assets=num_assets,
                num_trajectories=self._num_trajectories
            )
    
    def update(self, timestamp: datetime, market_data: Dict[str, Any]) -> None:
        """
        Update wallet state with new market data.
        
        Args:
            timestamp: Current timestamp
            market_data: Dictionary containing market data
        """
        # Update market data cache
        self._market_data_cache = market_data
        
        # Update price history
        for asset, data in market_data.items():
            if 'price' in data:
                if asset not in self._price_history:
                    self._price_history[asset] = []
                self._price_history[asset].append((timestamp, data['price']))
        
        # Check if rebalancing is needed
        if self._should_rebalance():
            self.rebalance(self._get_optimal_weights())
        
        self._last_update_time = timestamp
    
    def _should_rebalance(self) -> bool:
        """
        Determine if portfolio should be rebalanced.
        
        Returns:
            True if rebalancing is needed
        """
        if not self._last_optimal_weights:
            return True
            
        current_weights = self.get_allocation()
        
        # Check deviation from optimal weights
        for asset, target_weight in self._last_optimal_weights.items():
            if asset in current_weights:
                deviation = abs(current_weights[asset] - target_weight)
                if deviation > self.rebalance_threshold:
                    return True
        
        return False
    
    def _get_optimal_weights(self) -> Dict[str, float]:
        """
        Get optimal portfolio weights using quantum optimization.
        
        Returns:
            Dictionary mapping assets to optimal weights
        """
        # Check cache
        now = datetime.now()
        if (self._last_optimization_time and 
            self._last_optimal_weights and
            (now - self._last_optimization_time).total_seconds() < self._optimization_cache_ttl):
            return self._last_optimal_weights
        
        # Prepare price data for optimization
        assets = list(self._market_data_cache.keys())
        num_assets = len(assets)
        
        if num_assets == 0:
            return {}
            
        self._ensure_quantum_finance(num_assets)
        
        # Prepare price paths for optimization
        price_paths = np.zeros((num_assets, self._num_trajectories))
        for i, asset in enumerate(assets):
            if asset in self._price_history:
                prices = [p[1] for p in self._price_history[asset]]
                if len(prices) > 1:
                    # Use historical prices for simulation
                    price_paths[i] = np.random.choice(
                        prices, 
                        size=self._num_trajectories
                    )
                else:
                    # Use current price with random variation
                    current_price = self._market_data_cache[asset]['price']
                    price_paths[i] = current_price * (1 + np.random.normal(
                        0, 0.1, self._num_trajectories
                    ))
        
        # Optimize portfolio weights
        optimal_weights = [] # Default empty weights
        if self._quantum_finance: # Check if quantum_finance is initialized
            optimal_weights = self._quantum_finance.optimize_portfolio(
                price_paths=price_paths,
                risk_aversion=self.risk_aversion
            )
        else:
            print("Warning: _quantum_finance not initialized in _get_optimal_weights.")
            # Fallback: equal weights or handle error
            num_assets = len(assets)
            if num_assets > 0:
                 optimal_weights = [1.0 / num_assets] * num_assets

        # Convert to dictionary
        weight_dict = {
            asset: weight for asset, weight in zip(assets, optimal_weights)
        }
        
        # Update cache
        self._last_optimization_time = now
        self._last_optimal_weights = weight_dict
        
        return weight_dict
    
    def execute_trade(self,
                     asset: str,
                     quantity: float,
                     price: float,
                     timestamp: datetime) -> bool:
        """
        Execute a trade for the given asset.
        
        Args:
            asset: Asset symbol
            quantity: Quantity to trade (positive for buy, negative for sell)
            price: Price per unit
            timestamp: Trade timestamp
            
        Returns:
            True if trade was successful
        """
        trade_value = quantity * price
        
        # Check if we have enough capital/holdings
        if quantity > 0:  # Buy
            if trade_value > self._capital:
                return False
            self._capital -= trade_value
        else:  # Sell
            current_holding = self._holdings.get(asset, 0)
            if abs(quantity) > current_holding:
                return False
            self._capital += abs(trade_value)
        
        # Update holdings
        if asset not in self._holdings:
            self._holdings[asset] = 0
        self._holdings[asset] += quantity
        
        # Record transaction
        self.record_transaction(
            transaction_type='BUY' if quantity > 0 else 'SELL',
            asset=asset,
            quantity=quantity,
            price=price,
            timestamp=timestamp
        )
        
        return True
    
    def rebalance(self, target_weights: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Rebalance portfolio to match target weights.
        
        Args:
            target_weights: Dictionary mapping assets to target weights
            
        Returns:
            List of executed rebalancing trades
        """
        executed_trades = []
        total_value = self.get_total_value(
            {asset: data['price'] for asset, data in self._market_data_cache.items()}
        )
        
        current_weights = self.get_allocation()
        
        for asset, target_weight in target_weights.items():
            if asset not in self._market_data_cache:
                continue
                
            current_price = self._market_data_cache[asset]['price']
            current_value = self._holdings.get(asset, 0) * current_price
            current_weight = current_value / total_value if total_value > 0 else 0
            
            # Calculate trade size
            target_value = total_value * target_weight
            value_difference = target_value - current_value
            quantity = value_difference / current_price
            
            # Execute trade if significant
            if abs(quantity) * current_price > 1.0:  # Minimum trade size $1
                if self.execute_trade(
                    asset=asset,
                    quantity=quantity,
                    price=current_price,
                    timestamp=datetime.now()
                ):
                    executed_trades.append({
                        'asset': asset,
                        'quantity': quantity,
                        'price': current_price,
                        'old_weight': current_weight,
                        'new_weight': target_weight
                    })
        
        return executed_trades
    
    def get_allocation(self) -> Dict[str, float]:
        """
        Get current portfolio allocation as weights.
        
        Returns:
            Dictionary mapping assets to current weights
        """
        total_value = self.get_total_value(
            {asset: data['price'] for asset, data in self._market_data_cache.items()}
        )
        
        if total_value == 0:
            return {asset: 0.0 for asset in self._holdings}
            
        weights = {}
        for asset, quantity in self._holdings.items():
            if asset in self._market_data_cache:
                current_price = self._market_data_cache[asset]['price']
                weights[asset] = (quantity * current_price) / total_value
                
        return weights
    
    def get_metrics(self) -> Dict[str, float]:
        """
        Get performance metrics for the wallet.
        
        Returns:
            Dictionary containing performance metrics
        """
        metrics = {}
        
        # Basic metrics
        total_value = self.get_total_value(
            {asset: data['price'] for asset, data in self._market_data_cache.items()}
        )
        metrics['total_value'] = total_value
        metrics['cash_ratio'] = self._capital / total_value if total_value > 0 else 1.0
        
        # Risk metrics
        metrics['value_at_risk'] = self.get_value_at_risk()
        metrics['expected_shortfall'] = self.get_expected_shortfall()
        
        # Return metrics if we have history
        if self._creation_time and self._last_update_time:
            abs_return, pct_return = self.get_returns(
                self._creation_time,
                self._last_update_time
            )
            metrics['absolute_return'] = abs_return
            metrics['percentage_return'] = pct_return
        
        return metrics
    
    def get_value_at_risk(self,
                         confidence_level: float = 0.95,
                         time_horizon: int = 1) -> float:
        """
        Calculate Value at Risk using quantum methods.
        
        Args:
            confidence_level: Confidence level
            time_horizon: Time horizon in days
            
        Returns:
            Value at Risk estimate
        """
        if not self._holdings or not self._market_data_cache:
            return 0.0
            
        assets = list(self._holdings.keys())
        num_assets = len(assets)
        
        self._ensure_quantum_finance(num_assets)
        
        # Prepare initial prices
        initial_prices = np.array([
            self._market_data_cache[asset]['price']
            for asset in assets
        ])
        
        # Calculate VaR using quantum finance engine
        var = 0.0 # Default VaR
        if self._quantum_finance: # Check if quantum_finance is initialized
            var = self._quantum_finance.calculate_var(
                confidence_level=confidence_level
            )
        else:
            print("Warning: _quantum_finance not initialized in get_value_at_risk.")
        
        return var
    
    def get_expected_shortfall(self,
                             confidence_level: float = 0.95,
                             time_horizon: int = 1) -> float:
        """
        Calculate Expected Shortfall using quantum methods.
        
        Args:
            confidence_level: Confidence level
            time_horizon: Time horizon in days
            
        Returns:
            Expected Shortfall estimate
        """
        if not self._holdings or not self._market_data_cache:
            return 0.0
            
        # Calculate VaR first
        var = self.get_value_at_risk(
            confidence_level=confidence_level,
            time_horizon=time_horizon
        )
        
        # Use quantum simulation to estimate expected loss beyond VaR
        assets = list(self._holdings.keys())
        num_assets = len(assets)
        
        self._ensure_quantum_finance(num_assets)
        
        # Prepare initial prices
        initial_prices = np.array([
            self._market_data_cache[asset]['price']
            for asset in assets
        ])
        
        # Run Monte Carlo simulation
        expected_shortfall = 0.0 # Default ES
        if self._quantum_finance: # Check if quantum_finance is initialized
            expected_shortfall = self._quantum_finance.calculate_expected_shortfall(
                confidence_level=confidence_level
            )
        else:
             print("Warning: _quantum_finance not initialized in get_expected_shortfall.")
        
        return expected_shortfall 