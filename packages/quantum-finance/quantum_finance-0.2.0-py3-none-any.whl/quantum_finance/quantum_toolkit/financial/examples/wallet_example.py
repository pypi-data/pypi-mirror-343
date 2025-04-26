"""
Example usage of the QuantumOptimizedWallet.

This script demonstrates how to use the quantum-enhanced wallet for
portfolio management and risk assessment.
"""

from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

from quantum_toolkit.financial.wallets import QuantumOptimizedWallet

def simulate_market_data(days: int = 30):
    """
    Simulate market data for demonstration.
    
    Args:
        days: Number of days to simulate
        
    Returns:
        List of (timestamp, market_data) tuples
    """
    assets = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    base_prices = {
        'AAPL': 150.0,
        'GOOGL': 2500.0,
        'MSFT': 300.0,
        'AMZN': 3000.0
    }
    
    # Simulate with some randomness and trends
    data = []
    start_time = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        timestamp = start_time + timedelta(days=day)
        market_data = {}
        
        for asset in assets:
            base_price = base_prices[asset]
            # Add random walk and small trend
            price = base_price * (1 + 0.001 * day + np.random.normal(0, 0.02))
            volume = int(np.random.normal(1000000, 200000))
            market_data[asset] = {
                'price': price,
                'volume': volume
            }
            
        data.append((timestamp, market_data))
        
    return data

def plot_portfolio_performance(wallet: QuantumOptimizedWallet,
                             market_data: list):
    """
    Plot portfolio performance over time.
    
    Args:
        wallet: QuantumOptimizedWallet instance
        market_data: List of (timestamp, market_data) tuples
    """
    dates = [data[0] for data in market_data]
    values = []
    cash_ratios = []
    var_values = []
    es_values = []
    
    for _, data in market_data:
        metrics = wallet.get_metrics()
        values.append(metrics['total_value'])
        cash_ratios.append(metrics['cash_ratio'])
        var_values.append(metrics['value_at_risk'])
        es_values.append(metrics['expected_shortfall'])
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot portfolio value
    ax1.plot(dates, values, label='Portfolio Value')
    ax1.set_title('Portfolio Value Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Value ($)')
    ax1.legend()
    ax1.grid(True)
    
    # Plot risk metrics
    ax2.plot(dates, var_values, label='Value at Risk (95%)')
    ax2.plot(dates, es_values, label='Expected Shortfall (95%)')
    ax2.plot(dates, [v * cr for v, cr in zip(values, cash_ratios)], 
             label='Cash Position', linestyle='--')
    ax2.set_title('Risk Metrics Over Time')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Value ($)')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    return fig

def main():
    """Run wallet demonstration."""
    # Initialize wallet
    initial_capital = 1000000.0  # $1M initial capital
    wallet = QuantumOptimizedWallet(
        initial_capital=initial_capital,
        num_trajectories=1000,
        risk_aversion=1.0,
        rebalance_threshold=0.05
    )
    
    # Simulate market data
    market_data = simulate_market_data(days=30)
    
    print("Starting portfolio simulation...")
    print(f"Initial capital: ${initial_capital:,.2f}")
    
    # Run simulation
    for timestamp, data in market_data:
        wallet.update(timestamp, data)
        
        # Print daily summary
        metrics = wallet.get_metrics()
        print(f"\nDay {timestamp.strftime('%Y-%m-%d')}:")
        print(f"Portfolio Value: ${metrics['total_value']:,.2f}")
        print(f"Cash Ratio: {metrics['cash_ratio']:.2%}")
        print(f"VaR (95%): ${metrics['value_at_risk']:,.2f}")
        print(f"ES (95%): ${metrics['expected_shortfall']:,.2f}")
        
        # Print current allocation
        allocation = wallet.get_allocation()
        print("\nCurrent Allocation:")
        for asset, weight in allocation.items():
            print(f"{asset}: {weight:.2%}")
    
    # Plot results
    fig = plot_portfolio_performance(wallet, market_data)
    plt.show()

if __name__ == '__main__':
    main() 