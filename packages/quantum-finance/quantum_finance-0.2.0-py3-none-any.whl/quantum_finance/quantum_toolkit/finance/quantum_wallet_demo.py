"""
Quantum Crypto Wallet Demo

This script demonstrates the functionality of the QuantumCryptoWallet with simulated market data.
"""

import logging
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any, Optional

from quantum.financial.wallets.quantum_crypto_wallet import QuantumCryptoWallet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simulate_market_data(days: int = 30, assets: Optional[Dict[str, List[str]]] = None) -> List[Tuple[datetime, Dict[str, Dict[str, Dict[str, float]]]]]:
    """
    Simulate market data for testing.
    
    Args:
        days: Number of days to simulate
        assets: Dictionary mapping asset types to list of symbols
        
    Returns:
        List of (timestamp, market_data) tuples
    """
    if assets is None:
        assets = {
            'crypto': ['BTC', 'ETH', 'SOL'],
            'stocks': ['AAPL', 'GOOGL', 'TSLA']
        }
    
    # Initial prices
    base_prices = {
        'BTC': 50000.0,
        'ETH': 3000.0,
        'SOL': 100.0,
        'AAPL': 150.0,
        'GOOGL': 2800.0,
        'TSLA': 800.0
    }
    
    # Volatilities
    volatilities = {
        'BTC': 0.03,
        'ETH': 0.04,
        'SOL': 0.05,
        'AAPL': 0.02,
        'GOOGL': 0.02,
        'TSLA': 0.03
    }
    
    # Generate price paths
    start_date = datetime.now() - timedelta(days=days)
    market_data = []
    
    current_prices = base_prices.copy()
    
    for day in range(days):
        timestamp = start_date + timedelta(days=day)
        data: Dict[str, Dict[str, Dict[str, float]]] = {
            'crypto': {},
            'stocks': {}
        }
        
        # Update prices with random walk
        for asset in base_prices:
            vol = volatilities[asset]
            price_change = np.random.normal(0, vol)
            current_prices[asset] *= (1 + price_change)
            
            # Add to appropriate category
            category = 'crypto' if asset in assets['crypto'] else 'stocks'
            data[category][asset] = {
                'price': current_prices[asset],
                'volume': np.random.uniform(1000, 10000),
                'high': current_prices[asset] * (1 + np.random.uniform(0, 0.02)),
                'low': current_prices[asset] * (1 - np.random.uniform(0, 0.02)),
                'close': current_prices[asset]
            }
        
        market_data.append((timestamp, data))
    
    return market_data

def main():
    """Run the quantum wallet demonstration."""
    # Initialize wallet with $1M initial capital
    initial_capital = 1_000_000.0
    wallet = QuantumCryptoWallet(
        initial_capital=initial_capital,
        num_trajectories=1000,  # Number of quantum trajectories
        risk_aversion=0.5,      # Risk aversion parameter
        rebalance_threshold=0.05  # Portfolio rebalancing threshold
    )
    
    print(f"\n{'='*80}")
    print("Starting Quantum-Enhanced Crypto Portfolio Simulation")
    print(f"{'='*80}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    
    # Simulate market data
    market_data = simulate_market_data(days=30)
    
    # Run simulation
    for timestamp, data in market_data:
        print(f"\nDay {timestamp.strftime('%Y-%m-%d')}:")
        print("-" * 40)
        
        # Update wallet with new market data
        wallet.update(timestamp, data)
        
        # Get portfolio metrics
        metrics = wallet.get_metrics()
        
        # Print portfolio summary
        print(f"Portfolio Value: ${metrics.get('total_value', initial_capital):,.2f}")
        print(f"Cash: ${metrics.get('capital', initial_capital):,.2f}")
        print(f"Returns:")
        if 'absolute_return' in metrics:
            print(f"  Absolute: ${metrics['absolute_return']:,.2f}")
        if 'percentage_return' in metrics:
            print(f"  Percentage: {metrics['percentage_return']:.2%}")
        
        # Print risk metrics
        print("\nRisk Metrics:")
        if 'var_95' in metrics:
            print(f"Value at Risk (95%): ${metrics['var_95']:,.2f}")
        if 'es_95' in metrics:
            print(f"Expected Shortfall (95%): ${metrics['es_95']:,.2f}")
        if 'volatility' in metrics:
            print(f"Volatility: {metrics['volatility']:.2%}")
        if 'quantum_uncertainty' in metrics:
            print(f"Quantum Uncertainty: {metrics['quantum_uncertainty']:.2%}")
        if 'sharpe_ratio' in metrics:
            print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        if 'portfolio_entropy' in metrics:
            print(f"Portfolio Entropy: {metrics['portfolio_entropy']:.2f}")
        
        # Print current allocation
        print("\nPortfolio Allocation:")
        allocation = wallet.get_allocation()
        total_value = metrics.get('total_value', initial_capital)
        
        for asset, weight in allocation.items():
            asset_category = 'crypto' if asset in data['crypto'] else 'stocks'
            if asset in data[asset_category]:
                current_price = data[asset_category][asset].get('close', 0)
                value = weight * total_value
                print(f"{asset}: {weight:.2%} (${value:,.2f} @ ${current_price:,.2f})")
        
        # Execute some option trades (every 5 days)
        if timestamp.day % 5 == 0:
            for crypto in ['BTC', 'ETH']:
                if crypto in data['crypto']:
                    current_price = data['crypto'][crypto]['close']
                    expiry_date = timestamp + timedelta(days=30)
                    
                    # Execute a call option
                    success = wallet.execute_option_trade(
                        symbol=crypto,
                        option_type='call',
                        strike_price=current_price * 1.1,  # 10% OTM
                        expiry_date=expiry_date,
                        quantity=1.0,
                        premium=current_price * 0.05,  # 5% premium
                        timestamp=timestamp
                    )
                    
                    if success:
                        print(f"\nExecuted {crypto} call option:")
                        print(f"Strike: ${current_price * 1.1:,.2f}")
                        print(f"Expiry: {expiry_date.strftime('%Y-%m-%d')}")
        
        print(f"\n{'='*80}")

if __name__ == "__main__":
    main() 