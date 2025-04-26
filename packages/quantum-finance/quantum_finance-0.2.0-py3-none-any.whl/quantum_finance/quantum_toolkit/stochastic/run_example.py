#!/usr/bin/env python
"""
StochasticQuantumFinance Example Script

This script demonstrates the key capabilities of the StochasticQuantumFinance module,
including stochastic volatility simulation, portfolio optimization, and risk assessment.
"""

import os
import sys
import logging
import numpy as np
from pathlib import Path
import pickle
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Import our StochasticQuantumFinance class
    from stochastic_quantum_finance import StochasticQuantumFinance
    
    def run_basic_example():
        """Run a basic example of the StochasticQuantumFinance module."""
        logger.info("Starting basic StochasticQuantumFinance example")
        
        # Initialize with 5 assets
        num_assets = 5
        sqf = StochasticQuantumFinance(
            num_assets=num_assets,
            num_trajectories=500,  # Number of simulation paths
            dt=0.01,               # Time step
            seed=42                # For reproducibility
        )
        
        # Check for available optimization methods and quantum hardware
        if sqf.portfolio_optimizer:
            methods = sqf.portfolio_optimizer.get_available_optimization_methods()
            logger.info("Available optimization methods:")
            for method, available in methods.items():
                logger.info(f"  - {method}: {'Available' if available else 'Not available'}")
                
        # Check for available quantum backends
        if sqf.hardware_manager and sqf.hardware_manager.service:
            backends = sqf.hardware_manager.available_backends
            logger.info(f"Available quantum backends: {backends}")
            
        # Set asset parameters
        initial_prices = np.array([100.0, 150.0, 200.0, 120.0, 180.0])
        volatilities = np.array([0.2, 0.25, 0.3, 0.22, 0.18])
        drift_rates = np.array([0.05, 0.07, 0.06, 0.04, 0.08])
        
        sqf.set_asset_parameters(
            initial_prices=initial_prices,
            volatilities=volatilities,
            drift_rates=drift_rates
        )
        
        # Set correlation matrix (positive definite)
        correlation_matrix = np.array([
            [1.0, 0.3, 0.2, 0.4, 0.1],
            [0.3, 1.0, 0.5, 0.2, 0.3],
            [0.2, 0.5, 1.0, 0.3, 0.2],
            [0.4, 0.2, 0.3, 1.0, 0.4],
            [0.1, 0.3, 0.2, 0.4, 1.0]
        ])
        sqf.set_correlation_matrix(correlation_matrix)
        
        # Simulate asset prices
        time_horizon = 252  # One year of trading days
        logger.info(f"Simulating asset prices for {time_horizon} time steps")
        price_paths = sqf.simulate_asset_prices(time_horizon)
        
        # Optimize portfolio
        logger.info("Optimizing portfolio")
        optimized_weights = sqf.optimize_portfolio_weights(risk_aversion=2.0)
        logger.info(f"Optimized weights: {optimized_weights}")
        
        # Calculate portfolio values
        initial_investment = 10000.0
        portfolio_values = sqf.calculate_portfolio_values(
            weights=optimized_weights,
            initial_investment=initial_investment
        )
        
        # Calculate risk metrics
        var_95 = sqf.calculate_var(confidence_level=0.95)
        es_95 = sqf.calculate_expected_shortfall(confidence_level=0.95)
        
        logger.info(f"Value at Risk (95%): ${var_95:.2f}")
        logger.info(f"Expected Shortfall (95%): ${es_95:.2f}")
        
        # Visualize results
        logger.info("Generating visualization")
        sqf.visualize_risk_simulation(num_paths=50)
        
        # Save model results instead of whole model to avoid pickling issues
        # Extract key data
        try:
            output_path = Path(current_dir) / "finance_results.json"
            results = {
                "initial_prices": initial_prices.tolist(),
                "volatilities": volatilities.tolist(),
                "drift_rates": drift_rates.tolist(),
                "optimized_weights": optimized_weights.tolist(),
                "var_95": float(var_95),
                "es_95": float(es_95),
                "mean_portfolio_value": np.mean(portfolio_values[:, -1]).item(),
                "timestamp": str(datetime.now())
            }
            
            # Save as JSON
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
                
            logger.info(f"Results saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
        
        return True
    
    if __name__ == "__main__":
        success = run_basic_example()
        if success:
            logger.info("Example completed successfully")
        else:
            logger.error("Example failed")
            
except ImportError as e:
    logger.error(f"Import error: {str(e)}. Please ensure all dependencies are installed.")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}") 