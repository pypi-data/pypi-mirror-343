"""
Advanced analysis using the StochasticQuantumFinance module.

This script demonstrates more advanced uses of the StochasticQuantumFinance
module including scenario analysis, stress testing, and correlation analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
# Use relative import for module in the same directory
from .stochastic_quantum_finance import StochasticQuantumFinance
import logging
from scipy.stats import norm, pearsonr
import os

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Check if we should create a new model or use an existing one
create_new_model = False
if os.path.exists("finance_model.pkl"):
    try:
        model = StochasticQuantumFinance.load_model("finance_model.pkl")
        logging.info(f"Loaded existing model with {model.num_assets} assets from finance_model.pkl")
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        create_new_model = True
else:
    create_new_model = True
    
if create_new_model:
    logging.info("Creating new model")
    # Initialize model with more assets and paths for advanced analysis
    num_assets = 5
    model = StochasticQuantumFinance(
        num_assets=num_assets,
        num_trajectories=1000,
        dt=0.01,
        seed=42
    )

    # Set asset parameters (technology, finance, healthcare, energy, consumer)
    initial_prices = np.array([150.0, 100.0, 200.0, 80.0, 120.0])
    volatilities = np.array([0.3, 0.2, 0.25, 0.35, 0.22])
    drift_rates = np.array([0.08, 0.05, 0.06, 0.04, 0.07])

    model.set_asset_parameters(
        initial_prices=initial_prices,
        volatilities=volatilities,
        drift_rates=drift_rates
    )

    # Set correlation matrix - more realistic cross-sector correlations
    correlation_matrix = np.array([
        [1.00, 0.50, 0.30, 0.20, 0.45],  # Tech
        [0.50, 1.00, 0.35, 0.25, 0.40],  # Finance
        [0.30, 0.35, 1.00, 0.15, 0.25],  # Healthcare
        [0.20, 0.25, 0.15, 1.00, 0.30],  # Energy
        [0.45, 0.40, 0.25, 0.30, 1.00]   # Consumer
    ])
    model.set_correlation_matrix(correlation_matrix)

    # Simulate for one year
    time_horizon = 252  # One trading year
    model.simulate_asset_prices(time_horizon)

    # Calculate initial portfolio (equal weights)
    equal_weights = np.ones(num_assets) / num_assets
    initial_investment = 10000.0
    model.calculate_portfolio_values(equal_weights, initial_investment)
    
    # Save the new model
    model.save_model("finance_model_advanced.pkl")
    logging.info("Saved new model to finance_model_advanced.pkl")

# ---------- Advanced Analysis -----------

# 1. Sector-based Portfolio Analysis
print("\n==== Sector-based Portfolio Analysis ====")

# Adapt to the number of assets in the model
if model.num_assets == 3:
    sectors = ["Technology", "Finance", "Healthcare"]
    sector_weights = {
        "Technology-heavy": np.array([0.60, 0.20, 0.20]),
        "Finance-heavy": np.array([0.20, 0.60, 0.20]),
        "Healthcare-heavy": np.array([0.20, 0.20, 0.60]),
        "Balanced": np.array([0.33, 0.33, 0.34])
    }
elif model.num_assets == 5:
    sectors = ["Technology", "Finance", "Healthcare", "Energy", "Consumer"]
    sector_weights = {
        "Technology-heavy": np.array([0.40, 0.20, 0.15, 0.10, 0.15]),
        "Finance-heavy": np.array([0.15, 0.45, 0.15, 0.10, 0.15]),
        "Healthcare-heavy": np.array([0.15, 0.15, 0.40, 0.10, 0.20]),
        "Energy-heavy": np.array([0.10, 0.15, 0.15, 0.45, 0.15]),
        "Balanced": np.array([0.20, 0.20, 0.20, 0.20, 0.20])
    }
else:
    # Generic case - equal weights for all portfolios except one specialized
    sectors = [f"Asset {i+1}" for i in range(model.num_assets)]
    balanced_weights = np.ones(model.num_assets) / model.num_assets
    
    sector_weights = {
        "Balanced": balanced_weights.copy()
    }
    
    # Create a specialized portfolio for each asset
    for i in range(model.num_assets):
        weights = balanced_weights.copy() * 0.5  # Reduce all weights by half
        weights[i] = 0.5 + (0.5 / model.num_assets)  # Increase this asset's weight
        sector_weights[f"{sectors[i]}-heavy"] = weights

# Results storage
portfolio_results = {}
investment = 10000.0

for name, weights in sector_weights.items():
    portfolio_values = model.calculate_portfolio_values(weights, investment)
    final_values = portfolio_values[:, -1]
    
    # Calculate metrics
    mean_return = (np.mean(final_values) - investment) / investment
    volatility = np.std(final_values) / investment
    sharpe = mean_return / volatility if volatility > 0 else 0
    var95 = model.calculate_var(confidence_level=0.95) / investment
    
    portfolio_results[name] = {
        "mean_return": mean_return * 100,  # as percentage
        "volatility": volatility * 100,    # as percentage
        "sharpe_ratio": sharpe,
        "var95_percent": var95 * 100      # as percentage
    }
    
    print(f"\n{name} Portfolio:")
    print(f"  Expected Return: {mean_return*100:.2f}%")
    print(f"  Volatility: {volatility*100:.2f}%")
    print(f"  Sharpe Ratio: {sharpe:.3f}")
    print(f"  VaR (95%): {var95*100:.2f}%")

# Visualize sector portfolio comparison
plt.figure(figsize=(10, 6))
names = list(portfolio_results.keys())
returns = [portfolio_results[name]["mean_return"] for name in names]
risks = [portfolio_results[name]["volatility"] for name in names]
sharpes = [portfolio_results[name]["sharpe_ratio"] for name in names]

# Size bubbles by Sharpe ratio
sharpe_sizes = [max(s * 100, 50) for s in sharpes]

plt.scatter(risks, returns, s=sharpe_sizes, alpha=0.6, 
           c=range(len(names)), cmap='viridis')

# Add labels
for i, name in enumerate(names):
    plt.annotate(name, (risks[i], returns[i]),
               xytext=(5, 5), textcoords='offset points')

plt.xlabel('Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.title('Risk-Return Profile of Different Portfolio Allocations')
plt.grid(True, alpha=0.3)
plt.savefig('sector_comparison.png')
plt.close()


# 2. Stress Testing - Market Crash Scenario
print("\n==== Stress Testing - Market Crash Scenario ====")

# Create a model copy for stress testing
model_stress = StochasticQuantumFinance(
    num_assets=model.num_assets,
    num_trajectories=1000,
    dt=model.dt,
    seed=43  # Different seed
)

# Set parameters with increased volatility and negative drift (market crash)
model_stress.set_asset_parameters(
    initial_prices=model.initial_prices,
    volatilities=model.volatilities * 2.0,  # Double volatility
    drift_rates=model.drift_rates * -3.0    # Negative drift (market crash)
)
model_stress.set_correlation_matrix(model.correlation_matrix)

# Simulate shorter period (3 months of market crash)
crash_horizon = 63  # ~3 months
model_stress.simulate_asset_prices(crash_horizon)

print("\nStress Test Results (Market Crash Scenario):")
for name, weights in sector_weights.items():
    portfolio_values = model_stress.calculate_portfolio_values(weights, investment)
    final_values = portfolio_values[:, -1]
    
    # Calculate drawdown metrics
    mean_final = np.mean(final_values)
    mean_drawdown = (investment - mean_final) / investment * 100
    worst_case = np.percentile(final_values, 5)
    worst_drawdown = (investment - worst_case) / investment * 100
    
    print(f"\n{name} Portfolio in Market Crash:")
    print(f"  Expected Drawdown: {mean_drawdown:.2f}%")
    print(f"  Worst-Case Drawdown (5%): {worst_drawdown:.2f}%")

# Visualize stress test
plt.figure(figsize=(12, 8))
for name, weights in sector_weights.items():
    portfolio_values = model_stress.calculate_portfolio_values(weights, investment)
    plt.plot(np.mean(portfolio_values, axis=0), label=name)

plt.axhline(y=investment, color='black', linestyle='--', alpha=0.5, label='Initial Investment')
plt.title('Portfolio Performance During Market Crash')
plt.xlabel('Trading Days')
plt.ylabel('Portfolio Value')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('stress_test.png')
plt.close()

# 3. Correlation Analysis
print("\n==== Asset Correlation Analysis ====")

# Extract price paths for correlation analysis
price_paths = model.price_paths
returns = np.diff(price_paths, axis=1) / price_paths[:, :-1]
mean_returns = np.mean(returns, axis=0)

# Calculate realized correlation matrix
realized_corr = np.zeros((model.num_assets, model.num_assets))
for i in range(model.num_assets):
    for j in range(model.num_assets):
        # Calculate correlation for each asset pair
        corr, _ = pearsonr(mean_returns[:, i], mean_returns[:, j])
        realized_corr[i, j] = corr

# Print input vs. realized correlation
print("\nInput Correlation Matrix:")
for i in range(model.num_assets):
    print("  " + " ".join([f"{x:.2f}" for x in model.correlation_matrix[i]]))
    
print("\nRealized Correlation Matrix:")
for i in range(model.num_assets):
    print("  " + " ".join([f"{x:.2f}" for x in realized_corr[i]]))

# Visualize correlation matrices
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

im1 = ax1.imshow(model.correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
ax1.set_title('Input Correlation Matrix')
ax1.set_xticks(range(model.num_assets))
ax1.set_yticks(range(model.num_assets))
ax1.set_xticklabels(sectors)
ax1.set_yticklabels(sectors)

im2 = ax2.imshow(realized_corr, cmap='coolwarm', vmin=-1, vmax=1)
ax2.set_title('Realized Correlation Matrix')
ax2.set_xticks(range(model.num_assets))
ax2.set_yticks(range(model.num_assets))
ax2.set_xticklabels(sectors)
ax2.set_yticklabels(sectors)

fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

plt.tight_layout()
plt.savefig('correlation_analysis.png')
plt.close()

# 4. Return Distribution Analysis
print("\n==== Return Distribution Analysis ====")

# For return distribution, use balanced and the first specialized portfolio
balanced_weights = sector_weights["Balanced"]
specialized_key = next(key for key in sector_weights.keys() if key != "Balanced")
specialized_weights = sector_weights[specialized_key]

balanced_portfolio = model.calculate_portfolio_values(balanced_weights, investment)
specialized_portfolio = model.calculate_portfolio_values(specialized_weights, investment)

# Calculate returns
balanced_returns = (balanced_portfolio[:, -1] - investment) / investment * 100
specialized_returns = (specialized_portfolio[:, -1] - investment) / investment * 100

# Fit normal distributions
balanced_mean, balanced_std = norm.fit(balanced_returns)
specialized_mean, specialized_std = norm.fit(specialized_returns)

print(f"\nBalanced Portfolio Return Distribution:")
print(f"  Mean: {balanced_mean:.2f}%")
print(f"  Standard Deviation: {balanced_std:.2f}%")

print(f"\n{specialized_key} Portfolio Return Distribution:")
print(f"  Mean: {specialized_mean:.2f}%")
print(f"  Standard Deviation: {specialized_std:.2f}%")

# Calculate excess kurtosis 
balanced_kurtosis = (np.sum((balanced_returns - balanced_mean)**4) / 
                     (len(balanced_returns) * balanced_std**4)) - 3
specialized_kurtosis = (np.sum((specialized_returns - specialized_mean)**4) / 
                       (len(specialized_returns) * specialized_std**4)) - 3

print(f"  Balanced Portfolio Excess Kurtosis: {balanced_kurtosis:.3f}")
print(f"  {specialized_key} Portfolio Excess Kurtosis: {specialized_kurtosis:.3f}")

# Visualize return distributions
plt.figure(figsize=(12, 8))

# Histogram for balanced portfolio
plt.hist(balanced_returns, bins=30, alpha=0.5, label='Balanced Portfolio')
# Histogram for specialized portfolio
plt.hist(specialized_returns, bins=30, alpha=0.5, label=f'{specialized_key} Portfolio')

# Plot normal distributions
x = np.linspace(min(np.min(balanced_returns), np.min(specialized_returns)),
               max(np.max(balanced_returns), np.max(specialized_returns)), 100)
plt.plot(x, norm.pdf(x, balanced_mean, balanced_std) * len(balanced_returns) * (x[1]-x[0]),
        'k--', linewidth=2, label='Balanced Normal Fit')
plt.plot(x, norm.pdf(x, specialized_mean, specialized_std) * len(specialized_returns) * (x[1]-x[0]),
        'r--', linewidth=2, label=f'{specialized_key} Normal Fit')

plt.title('Return Distribution Analysis')
plt.xlabel('Return (%)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('return_distribution.png')
plt.close()

print("\nAdvanced analysis completed. Check the generated PNG files for visualizations.") 