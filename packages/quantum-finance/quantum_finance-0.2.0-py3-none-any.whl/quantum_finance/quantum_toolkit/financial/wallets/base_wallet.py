"""
Base Wallet Interface

This module defines the abstract base class for quantum-enhanced financial wallets.
All wallet implementations must inherit from this class and implement its methods.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

class BaseWallet(ABC):
    """
    Abstract base class for quantum-enhanced financial wallets.
    
    This class defines the interface that all wallet implementations must follow.
    It provides methods for wallet initialization, updates, and metrics calculation.
    """
    
    def __init__(self, initial_capital: float = 0.0):
        """
        Initialize the wallet with starting capital.
        
        Args:
            initial_capital: Initial amount of capital in the wallet
        """
        self._capital = initial_capital
        self._holdings: Dict[str, float] = {}  # Asset symbol -> quantity
        self._transactions: List[Dict[str, Any]] = []
        self._creation_time = datetime.now()
        self._last_update_time: Optional[datetime] = None
        
    @property
    def capital(self) -> float:
        """Get the current capital in the wallet."""
        return self._capital
    
    @property
    def holdings(self) -> Dict[str, float]:
        """Get the current holdings in the wallet."""
        return self._holdings.copy()
    
    @property
    def transactions(self) -> List[Dict[str, Any]]:
        """Get the list of all transactions."""
        return self._transactions.copy()
    
    @abstractmethod
    def initialize(self, initial_capital: float) -> None:
        """
        Initialize wallet with starting capital.
        
        Args:
            initial_capital: Initial amount of capital
        """
        pass
    
    @abstractmethod
    def update(self, timestamp: datetime, market_data: Dict[str, Any]) -> None:
        """
        Update wallet state for given timestamp and market data.
        
        Args:
            timestamp: Current timestamp
            market_data: Dictionary containing market data
        """
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, float]:
        """
        Get performance metrics for the wallet.
        
        Returns:
            Dictionary containing performance metrics
        """
        pass
    
    @abstractmethod
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
            True if trade was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def rebalance(self, target_weights: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Rebalance the portfolio to match target weights.
        
        Args:
            target_weights: Dictionary mapping asset symbols to target weights
            
        Returns:
            List of executed rebalancing trades
        """
        pass
    
    @abstractmethod
    def get_allocation(self) -> Dict[str, float]:
        """
        Get current portfolio allocation as weights.
        
        Returns:
            Dictionary mapping asset symbols to current weights
        """
        pass
    
    @abstractmethod
    def get_value_at_risk(self, 
                         confidence_level: float = 0.95,
                         time_horizon: int = 1) -> float:
        """
        Calculate Value at Risk using quantum-enhanced methods.
        
        Args:
            confidence_level: Confidence level (default: 0.95)
            time_horizon: Time horizon in days (default: 1)
            
        Returns:
            Value at Risk estimate
        """
        pass
    
    @abstractmethod
    def get_expected_shortfall(self,
                             confidence_level: float = 0.95,
                             time_horizon: int = 1) -> float:
        """
        Calculate Expected Shortfall using quantum-enhanced methods.
        
        Args:
            confidence_level: Confidence level (default: 0.95)
            time_horizon: Time horizon in days (default: 1)
            
        Returns:
            Expected Shortfall estimate
        """
        pass
    
    def record_transaction(self,
                         transaction_type: str,
                         asset: str,
                         quantity: float,
                         price: float,
                         timestamp: datetime,
                         **kwargs) -> None:
        """
        Record a transaction in the wallet's history.
        
        Args:
            transaction_type: Type of transaction (e.g., 'BUY', 'SELL')
            asset: Asset symbol
            quantity: Quantity traded
            price: Price per unit
            timestamp: Transaction timestamp
            **kwargs: Additional transaction details
        """
        transaction = {
            'type': transaction_type,
            'asset': asset,
            'quantity': quantity,
            'price': price,
            'timestamp': timestamp,
            'value': quantity * price,
            **kwargs
        }
        self._transactions.append(transaction)
    
    def get_transaction_history(self,
                              start_time: Optional[datetime] = None,
                              end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get transaction history within the specified time range.
        
        Args:
            start_time: Start of time range (optional)
            end_time: End of time range (optional)
            
        Returns:
            List of transactions within the time range
        """
        if start_time is None and end_time is None:
            return self.transactions
            
        filtered_transactions = []
        for tx in self.transactions:
            tx_time = tx['timestamp']
            if start_time and tx_time < start_time:
                continue
            if end_time and tx_time > end_time:
                continue
            filtered_transactions.append(tx)
            
        return filtered_transactions
    
    def get_total_value(self, market_prices: Dict[str, float]) -> float:
        """
        Calculate total portfolio value using current market prices.
        
        Args:
            market_prices: Dictionary mapping asset symbols to current prices
            
        Returns:
            Total portfolio value
        """
        total_value = self._capital
        for asset, quantity in self._holdings.items():
            if asset in market_prices:
                total_value += quantity * market_prices[asset]
        return total_value
    
    def get_returns(self, 
                   start_time: datetime,
                   end_time: datetime) -> Tuple[float, float]:
        """
        Calculate absolute and percentage returns over the specified period.
        
        Args:
            start_time: Start of period
            end_time: End of period
            
        Returns:
            Tuple of (absolute_return, percentage_return)
        """
        start_transactions = [tx for tx in self.transactions 
                            if tx['timestamp'] <= start_time]
        end_transactions = [tx for tx in self.transactions 
                          if tx['timestamp'] <= end_time]
        
        if not start_transactions or not end_transactions:
            return 0.0, 0.0
            
        start_value = sum(tx['value'] for tx in start_transactions)
        end_value = sum(tx['value'] for tx in end_transactions)
        
        abs_return = end_value - start_value
        pct_return = (abs_return / start_value) if start_value != 0 else 0.0
        
        return abs_return, pct_return 