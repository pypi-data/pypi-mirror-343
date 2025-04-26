"""
Quantum Crypto Wallet Implementation

This module implements a simulated cryptocurrency wallet with quantum portfolio optimization
and risk management capabilities.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, cast
import numpy as np
import pandas as pd

# NOTE: Updated import paths for new structure
from .base_wallet import BaseWallet

# Import stochastic quantum finance with proper error handling
try:
    from quantum_finance.quantum_toolkit.stochastic.stochastic_quantum_finance import StochasticQuantumFinance
    HAS_QUANTUM_FINANCE = True
except ImportError:
    HAS_QUANTUM_FINANCE = False
    print("Warning: StochasticQuantumFinance module not available. Using classical fallback methods.")

logger = logging.getLogger(__name__)

class QuantumCryptoWallet(BaseWallet):
    """
    A simulated cryptocurrency wallet with quantum portfolio optimization.
    
    This wallet implementation uses quantum computing techniques for:
    - Portfolio optimization
    - Risk assessment
    - Market regime detection
    - Cross-market correlation analysis
    """
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        num_trajectories: int = 1000,
        risk_aversion: float = 0.5,
        rebalance_threshold: float = 0.05,
        correlation_window: int = 30,
        volatility_window: int = 14
    ):
        """
        Initialize the quantum crypto wallet.
        
        Args:
            initial_capital: Initial capital in USD
            num_trajectories: Number of quantum trajectories for simulation
            risk_aversion: Risk aversion parameter (0 to 1)
            rebalance_threshold: Portfolio rebalance threshold
            correlation_window: Window for correlation calculations (days)
            volatility_window: Window for volatility calculations (days)
        """
        super().__init__(initial_capital)
        
        self.num_trajectories = num_trajectories
        self.risk_aversion = risk_aversion
        self.rebalance_threshold = rebalance_threshold
        self.correlation_window = correlation_window
        self.volatility_window = volatility_window
        
        # Initialize data storage
        self.price_history = pd.DataFrame()
        self.option_positions: Dict[str, List[Dict[str, Any]]] = {}
        self.last_update: Optional[datetime] = None
        self.market_data_cache: Dict[str, Dict[str, Dict[str, float]]] = {
            'crypto': {},
            'stocks': {}
        }
        
        # Quantum finance engine will be initialized on demand
        self._quantum_finance = None
        
        # Initialize the wallet
        self.initialize(initial_capital)
        
        # Initialize market data storage for tests
        self._crypto_market_data: Dict[str, Any] = {}
        self._stock_market_data: Dict[str, Any] = {}
        # Correlation matrix will be computed on update
        self._correlation_matrix = None
    
    def initialize(self, initial_capital: float) -> None:
        """Initialize wallet with starting capital."""
        self._capital = initial_capital
        self._holdings = {}
        self._transactions = []
        self.last_update = None
        self.price_history = pd.DataFrame()
    
    def update(self, timestamp: datetime, market_data: Dict[str, Dict[str, Dict[str, float]]]) -> None:
        """
        Update wallet state with new market data.
        
        Args:
            timestamp: Current timestamp
            market_data: Dictionary containing market data for crypto and stocks
        """
        try:
            # Update market data cache
            self.market_data_cache = market_data
            
            # Extract prices for all assets
            crypto_prices = {
                symbol: data['close']
                for symbol, data in market_data['crypto'].items()
            }
            stock_prices = {
                symbol: data['close']
                for symbol, data in market_data['stocks'].items()
            }
            
            # Create price series
            prices = pd.Series({**crypto_prices, **stock_prices}, name=timestamp)
            
            # Update price history
            if self.price_history.empty:
                self.price_history = pd.DataFrame(columns=prices.index)
            
            # Create a new DataFrame for the current prices
            new_data = pd.DataFrame([prices], index=[timestamp])
            
            # Concatenate with existing data, handling empty DataFrames properly
            if not self.price_history.empty:
                self.price_history = pd.concat([self.price_history, new_data], verify_integrity=True)
            else:
                self.price_history = new_data
            
            # Trim history to keep only necessary data
            max_window = max(self.correlation_window, self.volatility_window)
            if len(self.price_history) > max_window:
                self.price_history = self.price_history.iloc[-max_window:]
            
            self.last_update = timestamp
            
            # Check if rebalancing is needed
            if self._should_rebalance():
                optimal_weights = self._get_optimal_weights()
                if optimal_weights:
                    self.rebalance(optimal_weights)
                
            # Store raw market data for test access
            self._crypto_market_data = market_data.get('crypto', {})
            self._stock_market_data = market_data.get('stocks', {})
            
            # Compute correlation matrix for test validation
            if not self.price_history.empty and len(self.price_history) > 1:
                returns = self.price_history.pct_change().dropna()
                self._correlation_matrix = returns.corr()
            
        except Exception as e:
            logger.error(f"Error updating wallet: {e}")
    
    def get_metrics(self) -> Dict[str, float]:
        """
        Get performance metrics for the wallet.
        
        Returns:
            Dictionary containing performance metrics
        """
        metrics = {}
        
        try:
            # Initialize with basic metrics that should always be available
            metrics['capital'] = self._capital
            
            if not self.price_history.empty and len(self.price_history) > 1:
                # Calculate returns
                returns = self.price_history.pct_change().dropna()
                
                # Portfolio metrics
                current_prices = {
                    symbol: self.price_history[symbol].iloc[-1]
                    for symbol in self.price_history.columns
                }
                total_value = self.get_total_value(current_prices)
                
                metrics['total_value'] = total_value
                
                # Risk metrics with quantum adjustment
                metrics['var_95'] = self.get_value_at_risk(0.95)
                metrics['es_95'] = self.get_expected_shortfall(0.95)
                
                # Volatility with quantum uncertainty
                portfolio_returns = returns.dot(pd.Series(self.get_allocation()))
                classical_vol = float(portfolio_returns.std() * np.sqrt(252))
                
                # Add quantum uncertainty factor
                if HAS_QUANTUM_FINANCE and hasattr(self, '_quantum_finance') and self._quantum_finance is not None:
                    quantum_factor = np.sqrt(self._quantum_finance.hbar / 2)
                    metrics['volatility'] = classical_vol * (1 + quantum_factor)
                    metrics['quantum_uncertainty'] = classical_vol * quantum_factor
                else:
                    metrics['volatility'] = classical_vol
                
                # Calculate quantum-adjusted Sharpe ratio
                risk_free_rate = 0.02  # Assume 2% risk-free rate
                excess_return = float(portfolio_returns.mean() * 252 - risk_free_rate)
                metrics['sharpe_ratio'] = excess_return / metrics['volatility']
                
                # Crypto-specific metrics with quantum correlation
                crypto_metrics = self.get_crypto_metrics()
                metrics.update(crypto_metrics)
                
                # Add portfolio entropy as a quantum measure of diversification
                weights = list(self.get_allocation().values())
                if weights:
                    entropy = -sum(w * np.log(w) if w > 0 else 0 for w in weights)
                    metrics['portfolio_entropy'] = entropy
        
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
        
        # Ensure we always return at least total_value and capital
        if 'total_value' not in metrics:
            if hasattr(self, 'price_history') and not self.price_history.empty:
                # Try to get total value from current prices
                current_prices = {
                    symbol: self.price_history[symbol].iloc[-1]
                    for symbol in self.price_history.columns
                }
                metrics['total_value'] = self.get_total_value(current_prices)
            else:
                # Fallback to just capital if no price history
                metrics['total_value'] = self._capital
                
        if 'capital' not in metrics:
            metrics['capital'] = self._capital
            
        return metrics
    
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
        try:
            total_cost = quantity * price
            
            # Check if we have enough capital for buying
            if quantity > 0 and total_cost > self._capital:
                logger.warning(f"Insufficient capital for trade: {total_cost} > {self._capital}")
                return False
            
            # Check if we have enough assets for selling
            if quantity < 0 and abs(quantity) > self._holdings.get(asset, 0):
                logger.warning(f"Insufficient {asset} balance for trade")
                return False
            
            # Execute trade
            self._capital -= total_cost
            self._holdings[asset] = self._holdings.get(asset, 0) + quantity
            
            # Record transaction
            self.record_transaction(
                transaction_type='BUY' if quantity > 0 else 'SELL',
                asset=asset,
                quantity=quantity,
                price=price,
                timestamp=timestamp
            )
            
            logger.info(f"Executed {asset} trade: {quantity} @ ${price:.2f}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return False
    
    def rebalance(self, target_weights: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Rebalance the portfolio to match target weights.
        
        Args:
            target_weights: Dictionary mapping asset symbols to target weights
            
        Returns:
            List of executed rebalancing trades
        """
        executed_trades = []
        
        try:
            if not self.price_history.empty:
                current_prices = {
                    symbol: self.price_history[symbol].iloc[-1]
                    for symbol in target_weights.keys()
                }
                
                total_value = self.get_total_value(current_prices)
                
                for symbol, target_weight in target_weights.items():
                    current_value = self._holdings.get(symbol, 0) * current_prices[symbol]
                    current_weight = current_value / total_value if total_value > 0 else 0
                    
                    if abs(current_weight - target_weight) > self.rebalance_threshold:
                        target_value = total_value * target_weight
                        target_quantity = target_value / current_prices[symbol]
                        trade_quantity = target_quantity - self._holdings.get(symbol, 0)
                        
                        if abs(trade_quantity) > 1e-8:  # Avoid tiny trades
                            if self.last_update is not None:
                                success = self.execute_trade(
                                    asset=symbol,
                                    quantity=trade_quantity,
                                    price=current_prices[symbol],
                                    timestamp=cast(datetime, self.last_update)
                                )
                                
                                if success:
                                    executed_trades.append({
                                        'symbol': symbol,
                                        'quantity': trade_quantity,
                                        'price': current_prices[symbol],
                                        'timestamp': self.last_update
                                    })
        
        except Exception as e:
            logger.error(f"Error rebalancing portfolio: {e}")
        
        return executed_trades
    
    def get_allocation(self) -> Dict[str, float]:
        """
        Get current portfolio allocation as weights.
        
        Returns:
            Dictionary mapping asset symbols to current weights
        """
        allocation = {}
        
        try:
            if not self.price_history.empty:
                current_prices = {
                    symbol: self.price_history[symbol].iloc[-1]
                    for symbol in self.price_history.columns
                }
                
                total_value = self.get_total_value(current_prices)
                
                if total_value > 0:
                    for symbol in current_prices:
                        value = self._holdings.get(symbol, 0) * current_prices[symbol]
                        allocation[symbol] = value / total_value
        
        except Exception as e:
            logger.error(f"Error calculating allocation: {e}")
        
        return allocation
    
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
        try:
            if not self.price_history.empty and len(self.price_history) > 1:
                returns = self.price_history.pct_change().dropna()
                portfolio_returns = returns.dot(pd.Series(self.get_allocation()))
                
                # Calculate VaR using historical simulation
                var = float(portfolio_returns.quantile(1 - confidence_level))
                total_value = self.get_total_value({
                    symbol: self.price_history[symbol].iloc[-1]
                    for symbol in self.price_history.columns
                })
                
                # Scale VaR by time horizon
                var_adjusted = var * np.sqrt(time_horizon) * total_value
                return abs(var_adjusted)
        
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
        
        return 0.0
    
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
        try:
            if not self.price_history.empty and len(self.price_history) > 1:
                returns = self.price_history.pct_change().dropna()
                portfolio_returns = returns.dot(pd.Series(self.get_allocation()))
                
                # Calculate ES using historical simulation
                var = portfolio_returns.quantile(1 - confidence_level)
                es = float(portfolio_returns[portfolio_returns <= var].mean())
                total_value = self.get_total_value({
                    symbol: self.price_history[symbol].iloc[-1]
                    for symbol in self.price_history.columns
                })
                
                # Scale ES by time horizon
                es_adjusted = es * np.sqrt(time_horizon) * total_value
                return abs(es_adjusted)
        
        except Exception as e:
            logger.error(f"Error calculating ES: {e}")
        
        return 0.0
    
    def get_crypto_metrics(self) -> Dict[str, float]:
        """
        Calculate cryptocurrency-specific metrics.
        
        Returns:
            Dictionary containing volatility and correlation metrics
        """
        metrics = {}
        
        try:
            if not self.price_history.empty and len(self.price_history) > 1:
                # Calculate volatilities
                returns = self.price_history.pct_change().dropna()
                volatilities = returns.std() * np.sqrt(252)  # Annualized
                
                # Calculate correlations with stock market
                crypto_symbols = list(self.market_data_cache['crypto'].keys())
                stock_symbols = list(self.market_data_cache['stocks'].keys())
                
                for crypto in crypto_symbols:
                    if crypto in volatilities:
                        metrics[f"{crypto}_volatility"] = float(volatilities[crypto])
                        
                        # Calculate average correlation with stocks
                        correlations = []
                        for stock in stock_symbols:
                            if stock in returns:
                                corr = returns[crypto].corr(returns[stock])
                                if not np.isnan(corr):
                                    correlations.append(corr)
                        
                        if correlations:
                            metrics[f"{crypto}_stock_correlation"] = float(np.mean(correlations))
        
        except Exception as e:
            logger.error(f"Error calculating crypto metrics: {e}")
        
        return metrics
    
    def execute_option_trade(
        self,
        symbol: str,
        option_type: str,
        strike_price: float,
        expiry_date: datetime,
        quantity: float,
        premium: float,
        timestamp: datetime
    ) -> bool:
        """
        Execute a cryptocurrency option trade with quantum-adjusted pricing.
        
        Args:
            symbol: Cryptocurrency symbol
            option_type: Type of option ('call' or 'put')
            strike_price: Strike price
            expiry_date: Option expiry date
            quantity: Number of contracts
            premium: Option premium per contract
            timestamp: Trade timestamp
            
        Returns:
            True if trade was successful, False otherwise
        """
        try:
            # Calculate quantum-adjusted premium
            if HAS_QUANTUM_FINANCE and hasattr(self, '_quantum_finance') and self._quantum_finance is not None:
                # Get historical volatility
                if not self.price_history.empty:
                    returns = self.price_history[symbol].pct_change().dropna()
                    historical_vol = float(returns.std() * np.sqrt(252))
                    
                    # Calculate time to expiry in years
                    time_to_expiry = (expiry_date - timestamp).days / 365.0
                    
                    # Get current price
                    current_price = self.price_history[symbol].iloc[-1]
                    
                    # Calculate quantum volatility adjustment
                    quantum_factor = np.sqrt(self._quantum_finance.hbar / 2)
                    quantum_vol = historical_vol * (1 + quantum_factor)
                    
                    # Adjust premium based on quantum volatility
                    premium_adjustment = (quantum_vol / historical_vol - 1)
                    adjusted_premium = premium * (1 + premium_adjustment)
                else:
                    adjusted_premium = premium
            else:
                adjusted_premium = premium
            
            total_cost = quantity * adjusted_premium
            
            # Check if we have enough capital
            if total_cost > self._capital:
                logger.warning(f"Insufficient capital for option trade: {total_cost} > {self._capital}")
                return False
            
            # Initialize positions for symbol if not exists
            if symbol not in self.option_positions:
                self.option_positions[symbol] = []
            
            # Add new position with quantum-adjusted data
            position = {
                'type': option_type,
                'strike_price': strike_price,
                'expiry_date': expiry_date,
                'quantity': quantity,
                'premium': adjusted_premium,
                'original_premium': premium,
                'quantum_adjustment': adjusted_premium - premium if 'adjusted_premium' in locals() else 0,
                'timestamp': timestamp
            }
            self.option_positions[symbol].append(position)
            
            # Deduct premium from capital
            self._capital -= total_cost
            
            # Record transaction with quantum adjustment details
            self.record_transaction(
                transaction_type='OPTION',
                asset=symbol,
                quantity=quantity,
                price=adjusted_premium,
                timestamp=timestamp,
                option_type=option_type,
                strike_price=strike_price,
                expiry_date=expiry_date,
                quantum_adjusted=True if 'adjusted_premium' in locals() else False,
                quantum_adjustment=position['quantum_adjustment']
            )
            
            logger.info(f"Executed {symbol} {option_type} option trade: {quantity} contracts @ ${strike_price:.2f} "
                       f"(Premium: ${adjusted_premium:.2f}, Quantum Adj: ${position['quantum_adjustment']:.2f})")
            return True
            
        except Exception as e:
            logger.error(f"Error executing option trade: {e}")
            return False
    
    def get_option_positions(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get current option positions.
        
        Returns:
            Dictionary of option positions by symbol
        """
        # Remove expired options
        current_time = datetime.now()
        for symbol in list(self.option_positions.keys()):
            self.option_positions[symbol] = [
                pos for pos in self.option_positions[symbol]
                if pos['expiry_date'] > current_time
            ]
            if not self.option_positions[symbol]:
                del self.option_positions[symbol]
        
        return self.option_positions
    
    def _get_optimal_weights(self) -> Dict[str, float]:
        """
        Calculate optimal portfolio weights using a uniform distribution fallback.
        Returns:
            Dictionary of uniform weights by symbol
        """
        # Use uniform weights for all assets in price history
        columns = list(self.price_history.columns) if hasattr(self, 'price_history') else []
        num_assets = len(columns)
        if num_assets == 0:
            return {}
        uniform_weight = 1.0 / num_assets
        return {symbol: uniform_weight for symbol in columns}
    
    def _should_rebalance(self) -> bool:
        """
        Check if portfolio rebalancing is needed.
        
        Returns:
            True if rebalancing is needed, False otherwise
        """
        if not self.price_history.empty and len(self.price_history) > 1:
            optimal_weights = self._get_optimal_weights()
            if optimal_weights:
                total_value = self._capital + sum(
                    self.holdings.get(symbol, 0) * self.price_history[symbol].iloc[-1]
                    for symbol in optimal_weights.keys()
                )
                
                for symbol, target_weight in optimal_weights.items():
                    current_value = self.holdings.get(symbol, 0) * self.price_history[symbol].iloc[-1]
                    current_weight = current_value / total_value if total_value > 0 else 0
                    
                    if abs(current_weight - target_weight) > self.rebalance_threshold:
                        return True
        
        return False

    def execute_crypto_trade(self, symbol: str, quantity: float, price: float, timestamp: datetime) -> bool:
        """Execute cryptocurrency spot trade with exchange metadata for backward compatibility."""
        # Perform the core trade using execute_trade
        result = self.execute_trade(symbol, quantity, price, timestamp)
        # Add exchange and trade_type metadata to the latest transaction
        if result and self._transactions:
            txn = self._transactions[-1]
            txn['exchange'] = 'kucoin'
            txn['trade_type'] = 'spot'
        return result

    def record_transaction(self, transaction_type: str, asset: str, quantity: float, price: float, timestamp: datetime, **kwargs) -> None:
        """Override BaseWallet.record_transaction to add exchange and trade_type for spot trades."""
        # Add metadata for spot trades executed via execute_trade
        if transaction_type in ('BUY', 'SELL'):
            kwargs.setdefault('exchange', 'kucoin')
            kwargs.setdefault('trade_type', 'spot')
        # Delegate to base implementation
        super().record_transaction(transaction_type, asset, quantity, price, timestamp, **kwargs) 