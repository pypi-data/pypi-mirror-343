"""
Visualization script for the StochasticQuantumFinance results.

This script loads a saved model and generates visualizations of the
simulation results.
"""

import numpy as np
import matplotlib.pyplot as plt
from .stochastic_quantum_finance import StochasticQuantumFinance
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load the saved model
model = StochasticQuantumFinance.load_model("finance_model.pkl")

# --- Validate loaded model data --- 
if model.price_paths is None:
    logging.error("Loaded model does not contain price path data. Cannot generate asset price plot.")
else:
    # Create a figure for asset price paths
    plt.figure(figsize=(12, 8))
    # Ensure price_paths is a numpy array before using mean
    if isinstance(model.price_paths, np.ndarray):
        for i in range(model.num_assets):
            plt.plot(np.mean(model.price_paths[:, :, i], axis=0), label=f"Asset {i+1}")
        plt.title("Average Asset Price Paths")
        plt.xlabel("Time (Days)")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.savefig("asset_prices.png")
        plt.close()
    else:
         logging.error("model.price_paths is not a numpy array.")

if model.portfolio_values is None:
    logging.error("Loaded model does not contain portfolio value data. Cannot generate portfolio plots or risk metrics.")
else:
    # Ensure portfolio_values is a numpy array
    if isinstance(model.portfolio_values, np.ndarray):
        # Create a figure for portfolio value distribution
        plt.figure(figsize=(12, 8))
        final_values = model.portfolio_values[:, -1]
        plt.hist(final_values, bins=30, alpha=0.7)
        mean_final_value = np.mean(final_values)
        if isinstance(mean_final_value, (int, float, np.number)): # Check for numpy numbers too
             # Cast to standard float for matplotlib compatibility
             vline_pos = float(mean_final_value)
             plt.axvline(vline_pos, color='r', linestyle='dashed', linewidth=2, label=f'Mean: {vline_pos:.2f}')
        plt.title("Final Portfolio Value Distribution")
        plt.xlabel("Portfolio Value")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)
        plt.savefig("portfolio_distribution.png")
        plt.close()

        # Create a figure for portfolio value over time
        plt.figure(figsize=(12, 8))
        # Plot a subset of portfolio paths
        sample_indices = np.random.choice(model.num_trajectories, min(20, model.num_trajectories), replace=False)
        for i in sample_indices:
            plt.plot(model.portfolio_values[i, :], 'b-', alpha=0.3)
        # Ensure mean calculation is valid
        mean_portfolio_path = np.mean(model.portfolio_values, axis=0)
        plt.plot(mean_portfolio_path, 'r-', linewidth=2, label="Mean")
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Time (Days)")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.grid(True)
        plt.savefig("portfolio_values.png")
        plt.close()

        # Create a figure for risk metrics
        confidence_levels = np.arange(0.9, 1.0, 0.01)
        var_values = []
        es_values = []

        # Check if calculate_var and calculate_expected_shortfall exist
        has_var = hasattr(model, 'calculate_var') and callable(model.calculate_var)
        has_es = hasattr(model, 'calculate_expected_shortfall') and callable(model.calculate_expected_shortfall)

        if has_var and has_es:
            for conf in confidence_levels:
                try:
                    var = model.calculate_var(confidence_level=conf)
                    es = model.calculate_expected_shortfall(confidence_level=conf)
                    var_values.append(var)
                    es_values.append(es)
                except Exception as risk_calc_e:
                    logging.error(f"Error calculating risk metrics at confidence {conf}: {risk_calc_e}")
                    var_values.append(np.nan) # Append NaN on error
                    es_values.append(np.nan)

            plt.figure(figsize=(12, 8))
            plt.plot(confidence_levels * 100, var_values, 'b-', label="Value at Risk (VaR)")
            plt.plot(confidence_levels * 100, es_values, 'r-', label="Expected Shortfall (ES)")
            plt.title("Risk Metrics at Different Confidence Levels")
            plt.xlabel("Confidence Level (%)")
            plt.ylabel("Amount at Risk")
            plt.legend()
            plt.grid(True)
            plt.savefig("risk_metrics.png")
            plt.close()
        else:
             logging.error("Risk calculation methods not found on loaded model.")
    else:
         logging.error("model.portfolio_values is not a numpy array.")

print("Visualizations created successfully!") 