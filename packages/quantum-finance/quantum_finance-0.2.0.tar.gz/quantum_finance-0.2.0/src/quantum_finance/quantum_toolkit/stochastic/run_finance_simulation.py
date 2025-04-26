"""
Test script for StochasticQuantumFinance module.

This script demonstrates how to use the StochasticQuantumFinance class
for portfolio optimization and risk assessment.
"""

import numpy as np
import matplotlib.pyplot as plt
from .stochastic_quantum_finance import StochasticQuantumFinance
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize model
num_assets = 3
model = StochasticQuantumFinance(
    num_assets=num_assets,
    num_trajectories=500,
    dt=0.01,
    seed=42
)

# Set asset parameters
initial_prices = np.array([100.0, 150.0, 200.0])
volatilities = np.array([0.2, 0.25, 0.3])
drift_rates = np.array([0.05, 0.07, 0.1])

model.set_asset_parameters(
    initial_prices=initial_prices,
    volatilities=volatilities,
    drift_rates=drift_rates
)

# Set correlation matrix
correlation_matrix = np.array([
    [1.0, 0.3, 0.2],
    [0.3, 1.0, 0.4],
    [0.2, 0.4, 1.0]
])
model.set_correlation_matrix(correlation_matrix)

# Simulate stochastic volatility and asset prices
time_horizon = 252  # One trading year
volatility_paths = model.simulate_stochastic_volatility(time_horizon)
price_paths = model.simulate_asset_prices(time_horizon)

# Calculate portfolio values with equal weights initially
equal_weights = np.ones(num_assets) / num_assets
initial_investment = 10000.0
portfolio_values = model.calculate_portfolio_values(equal_weights, initial_investment)

# Optimize portfolio
optimized_weights = model.optimize_portfolio_weights(risk_aversion=1.0, method='qaoa')
print(f"Optimized weights: {optimized_weights}")

# Calculate portfolio values with optimized weights
optimized_portfolio_values = model.calculate_portfolio_values(optimized_weights, initial_investment)

# Calculate risk metrics
var_95 = model.calculate_var(confidence_level=0.95)
es_95 = model.calculate_expected_shortfall(confidence_level=0.95)

print(f"Value at Risk (95%): {var_95:.2f}")
print(f"Expected Shortfall (95%): {es_95:.2f}")

# Save model
model.save_model("finance_model.pkl")

print("Simulation complete!") 