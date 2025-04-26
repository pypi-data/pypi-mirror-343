"""
Financial risk assessment using stochastic quantum methods.

This class implements quantum stochastic volatility models, portfolio
optimization, and risk measures using quantum uncertainty.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import logging
import os
import sys
import importlib.util

# Add the current directory to the path to find local modules
# current_dir = os.path.dirname(os.path.abspath(__file__))
# if current_dir not in sys.path:
#     sys.path.append(current_dir)
# NOTE: Removing sys.path manipulation, prefer standard imports

from qiskit_aer import Aer

# Import portfolio optimization module using relative import
# portfolio_path = os.path.join(current_dir, "portfolio_optimization.py")
HAS_PORTFOLIO_OPTIMIZER = False
# if os.path.exists(portfolio_path):
try:
    # spec = importlib.util.spec_from_file_location("portfolio_optimization", portfolio_path)
    # if spec is not None and spec.loader is not None:
    #     portfolio_optimization = importlib.util.module_from_spec(spec)
    #     spec.loader.exec_module(portfolio_optimization)
    #     PortfolioOptimizer = portfolio_optimization.PortfolioOptimizer
    from .portfolio_optimization import PortfolioOptimizer
    HAS_PORTFOLIO_OPTIMIZER = True
    logging.info("Successfully imported PortfolioOptimizer")
    # else:
    #     logging.warning("Could not create module spec for PortfolioOptimizer")
except ImportError as e:
    logging.warning(f"Could not import PortfolioOptimizer: {str(e)}")
    HAS_PORTFOLIO_OPTIMIZER = False
    PortfolioOptimizer = None # Define as None if import fails
# else:
#     logging.warning("PortfolioOptimizer not available, will use fallback methods")

# Import quantum hardware manager module using relative import
# hardware_path = os.path.join(current_dir, "quantum_hardware_manager.py")
HAS_HARDWARE_MANAGER = False
# if os.path.exists(hardware_path):
try:
    # spec = importlib.util.spec_from_file_location("quantum_hardware_manager", hardware_path)
    # if spec is not None and spec.loader is not None:
    #     quantum_hardware_manager = importlib.util.module_from_spec(spec)
    #     spec.loader.exec_module(quantum_hardware_manager)
    #     QuantumHardwareManager = quantum_hardware_manager.QuantumHardwareManager
    from .quantum_hardware_manager import QuantumHardwareManager
    HAS_HARDWARE_MANAGER = True
    logging.info("Successfully imported QuantumHardwareManager")
    # else:
    #     logging.warning("Could not create module spec for QuantumHardwareManager")
except ImportError as e:
    logging.warning(f"Could not import QuantumHardwareManager: {str(e)}")
    HAS_HARDWARE_MANAGER = False
    QuantumHardwareManager = None # Define as None if import fails
# else:
#     logging.warning("QuantumHardwareManager not available, will use simulators only")

logger = logging.getLogger(__name__)

class StochasticQuantumFinance:
    """
    Financial risk assessment using stochastic quantum methods.
    
    This class implements quantum stochastic volatility models, portfolio
    optimization, and risk measures using quantum uncertainty.
    """
    
    def __init__(self,
                 num_assets: int,
                 num_trajectories: int = 1000,
                 dt: float = 0.01,
                 hbar: float = 1.0,
                 seed: Optional[int] = None,
                 hardware_manager: Optional[Any] = None):
        """
        Initialize the stochastic quantum finance model.
        
        Args:
            num_assets: Number of financial assets to model
            num_trajectories: Number of stochastic trajectories to use
            dt: Time step for stochastic evolution
            hbar: Planck's constant (reduced)
            seed: Random seed for reproducibility
            hardware_manager: Optional QuantumHardwareManager instance
        """
        self.num_assets = num_assets
        self.num_trajectories = num_trajectories
        self.dt = dt
        self.hbar = hbar
        self.seed = seed
        
        # Initialize random number generator
        self.rng = np.random.RandomState(seed)
        
        # Initialize asset parameters
        self.initial_prices = np.ones(num_assets)
        self.volatilities = np.ones(num_assets) * 0.2
        self.drift_rates = np.zeros(num_assets)
        self.correlation_matrix = np.eye(num_assets)
        self.correlation_cholesky = np.eye(num_assets)  # Identity matrix as default
        
        # Storage for simulation results
        self.volatility_paths = None
        self.price_paths = None
        self.portfolio_values = None
        
        # Initialize quantum components
        self.quantum_enhanced = True
        
        # Set up hardware manager or use default simulator
        if hardware_manager and HAS_HARDWARE_MANAGER:
            self.hardware_manager = hardware_manager
            logger.info(f"Using provided hardware manager")
        elif HAS_HARDWARE_MANAGER and QuantumHardwareManager is not None: # Check if class is defined
            self.hardware_manager = QuantumHardwareManager()
            logger.info(f"Created new hardware manager")
        else:
            self.hardware_manager = None
            logger.info(f"Hardware manager not available, using simulator only")
            
        # Initialize simulator as fallback
        self.simulator = Aer.get_backend('aer_simulator')
        
        # Initialize portfolio optimizer if available
        if HAS_PORTFOLIO_OPTIMIZER and PortfolioOptimizer is not None: # Check if class is defined
            self.portfolio_optimizer = PortfolioOptimizer(
                hardware_manager=self.hardware_manager
            )
            logger.info(f"Using PortfolioOptimizer with hardware management")
        else:
            self.portfolio_optimizer = None
            logger.info(f"PortfolioOptimizer not available, will use fallback methods")
        
        logger.info(f"Initialized StochasticQuantumFinance with {num_assets} assets")
        
    def set_asset_parameters(self,
                           initial_prices: np.ndarray,
                           volatilities: np.ndarray,
                           drift_rates: np.ndarray) -> None:
        """
        Set asset parameters for simulation.
        
        Args:
            initial_prices: Initial asset prices
            volatilities: Asset volatilities
            drift_rates: Asset drift rates (expected returns)
        """
        if len(initial_prices) != self.num_assets:
            raise ValueError(f"Expected {self.num_assets} initial prices, got {len(initial_prices)}")
        if len(volatilities) != self.num_assets:
            raise ValueError(f"Expected {self.num_assets} volatilities, got {len(volatilities)}")
        if len(drift_rates) != self.num_assets:
            raise ValueError(f"Expected {self.num_assets} drift rates, got {len(drift_rates)}")
            
        self.initial_prices = initial_prices
        self.volatilities = volatilities
        self.drift_rates = drift_rates
        
        logger.info("Asset parameters set successfully")
        
    def set_correlation_matrix(self, correlation_matrix: np.ndarray) -> None:
        """
        Set correlation matrix for asset price movements.
        
        Args:
            correlation_matrix: Correlation matrix (must be positive definite)
        """
        if correlation_matrix.shape != (self.num_assets, self.num_assets):
            raise ValueError(f"Expected correlation matrix of shape ({self.num_assets}, {self.num_assets})")
            
        # Verify that correlation matrix is valid
        if not np.allclose(correlation_matrix, correlation_matrix.T):
            raise ValueError("Correlation matrix must be symmetric")
            
        # Compute Cholesky decomposition for correlated random numbers
        try:
            self.correlation_cholesky = np.linalg.cholesky(correlation_matrix)
            self.correlation_matrix = correlation_matrix
            logger.info("Correlation matrix set successfully")
        except np.linalg.LinAlgError:
            raise ValueError("Correlation matrix is not positive definite")
    
    def optimize_portfolio(self, 
                         price_paths: np.ndarray,
                         risk_aversion: float = 1.0,
                         constraints: Optional[Dict[str, Any]] = None,
                         method: str = 'auto') -> Dict[str, Any]:
        """
        Optimize portfolio using quantum circuits.
        
        Args:
            price_paths: Asset price paths from simulation
            risk_aversion: Risk aversion parameter
            constraints: Optional constraints for optimization
            method: Optimization method ('auto', 'qaoa', 'vqe', 'classical')
            
        Returns:
            Dictionary with optimization results
        """
        # Calculate returns from price paths
        returns = np.diff(price_paths, axis=1) / price_paths[:, :-1]
        
        # Calculate mean returns and covariance matrix
        mean_returns = np.mean(returns, axis=(0, 1))
        cov_matrix = np.cov(np.mean(returns, axis=0).T)
        
        # Ensure covariance matrix is positive definite
        min_eig = np.min(np.real(np.linalg.eigvals(cov_matrix)))
        if min_eig < 0:
            cov_matrix -= 10*min_eig * np.eye(*cov_matrix.shape)
        
        # Use PortfolioOptimizer if available
        if self.portfolio_optimizer and HAS_PORTFOLIO_OPTIMIZER:
            try:
                # Use our advanced portfolio optimizer with quantum hardware management
                result = self.portfolio_optimizer.optimize_portfolio(
                    returns=mean_returns,
                    cov_matrix=cov_matrix,
                    risk_aversion=risk_aversion,
                    constraints=constraints,
                    method=method
                )
                
                # Add quantum uncertainty to weights if quantum-enhanced is enabled
                if self.quantum_enhanced:
                    quantum_factor = np.sqrt(self.hbar)
                    weights = np.array(result['weights'])
                    quantum_adjusted_weights = weights * (1 + quantum_factor * self.rng.normal(0, 0.05, size=len(weights)))
                    
                    # Ensure non-negative weights
                    quantum_adjusted_weights = np.maximum(quantum_adjusted_weights, 0)
                    
                    # Normalize to sum to 1
                    quantum_adjusted_weights = quantum_adjusted_weights / np.sum(quantum_adjusted_weights)
                    
                    result['quantum_adjusted_weights'] = quantum_adjusted_weights.tolist()
                else:
                    result['quantum_adjusted_weights'] = result['weights']
                
                logger.info(f"Portfolio optimized using {result.get('method_used', method)}")
                return result
                
            except Exception as e:
                logger.error(f"Error in portfolio optimization: {str(e)}")
                logger.info("Falling back to classical optimization")
                return self._fallback_classical_optimization(price_paths, risk_aversion)
        else:
            # Use fallback classical optimization
            return self._fallback_classical_optimization(price_paths, risk_aversion)
        
    def _fallback_classical_optimization(self, price_paths: np.ndarray, risk_aversion: float) -> Dict[str, Any]:
        """
        Fallback classical portfolio optimization method using mean-variance optimization.
        
        Args:
            price_paths: Asset price paths from simulation
            risk_aversion: Risk aversion parameter
            
        Returns:
            Dictionary with optimization results
        """
        logger.warning("Using classical portfolio optimization as fallback")
        
        # Calculate returns from price paths
        returns = np.diff(price_paths, axis=1) / price_paths[:, :-1]
        
        # Calculate mean returns and covariance matrix
        mean_returns = np.mean(returns, axis=(0, 1))
        cov_matrix = np.cov(np.mean(returns, axis=0).T)
        
        # Ensure covariance matrix is positive definite
        min_eig = np.min(np.real(np.linalg.eigvals(cov_matrix)))
        if min_eig < 0:
            cov_matrix -= 10*min_eig * np.eye(*cov_matrix.shape)
        
        # Solve mean-variance optimization
        try:
            from scipy.optimize import minimize
            
            # Define objective function (negative Sharpe ratio)
            def objective(weights):
                portfolio_return = np.sum(mean_returns * weights)
                portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                return -portfolio_return + risk_aversion * portfolio_volatility
            
            # Constraints: weights sum to 1 and are non-negative
            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = tuple((0, 1) for _ in range(self.num_assets))
            
            # Initial guess: equal weights
            initial_weights = np.ones(self.num_assets) / self.num_assets
            
            # Perform optimization
            result = minimize(objective, initial_weights, method='SLSQP', 
                             bounds=bounds, constraints=constraints)
            
            # Extract optimal weights
            optimal_weights = result['x']
            
            # Create result dictionary similar to quantum optimization
            optimization_result = {
                'weights': optimal_weights.tolist(),
                'optimal_value': result['fun'],
                'quantum_adjusted_weights': optimal_weights.tolist()  # No quantum adjustment in classical
            }
            
            logger.info("Classical optimization completed successfully")
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Classical optimization failed: {str(e)}")
            
            # Last resort: equal weights
            equal_weights = np.ones(self.num_assets) / self.num_assets
            
            return {
                'weights': equal_weights.tolist(),
                'optimal_value': 0.0,
                'quantum_adjusted_weights': equal_weights.tolist()
            }
        
    def simulate_stochastic_volatility(self, time_horizon: int) -> np.ndarray:
        """
        Simulate stochastic volatility using quantum-enhanced models.
        
        Args:
            time_horizon: Number of time steps to simulate
            
        Returns:
            Volatility paths array of shape (num_trajectories, time_horizon+1, num_assets)
        """
        # Initialize volatility paths
        self.volatility_paths = np.zeros((self.num_trajectories, time_horizon + 1, self.num_assets))
        
        # Set initial volatilities
        self.volatility_paths[:, 0, :] = np.tile(self.volatilities, (self.num_trajectories, 1))
        
        # Parameters for stochastic volatility model
        mean_reversion = 0.1  # Mean reversion rate
        vol_of_vol = 0.2  # Volatility of volatility
        long_term_mean = self.volatilities  # Long-term mean volatility
        
        # Generate correlated random numbers for volatility process
        random_numbers = self.rng.normal(0, 1, size=(self.num_trajectories, time_horizon, self.num_assets))
        
        # Add quantum uncertainty if enabled
        if self.quantum_enhanced:
            quantum_factor = np.sqrt(self.hbar)
            random_numbers += quantum_factor * self.rng.normal(0, 0.1, size=random_numbers.shape)
            
        # Simulate volatility paths
        for t in range(time_horizon):
            # Cox-Ingersoll-Ross process for volatility
            drift = mean_reversion * (long_term_mean - self.volatility_paths[:, t, :])
            diffusion = vol_of_vol * np.sqrt(self.volatility_paths[:, t, :]) * random_numbers[:, t, :]
            
            # Update volatility
            self.volatility_paths[:, t+1, :] = np.maximum(
                self.volatility_paths[:, t, :] + drift * self.dt + diffusion * np.sqrt(self.dt),
                1e-6  # Ensure positive volatility
            )
            
        logger.info(f"Simulated stochastic volatility for {time_horizon} time steps")
        return self.volatility_paths
    
    def simulate_asset_prices(self, time_horizon: int) -> np.ndarray:
        """
        Simulate asset price paths using stochastic volatility.
        
        Args:
            time_horizon: Number of time steps to simulate
            
        Returns:
            Price paths array of shape (num_trajectories, time_horizon+1, num_assets)
        """
        # Ensure volatility has been simulated
        if self.volatility_paths is None or self.volatility_paths.shape[1] != time_horizon + 1:
            self.simulate_stochastic_volatility(time_horizon)
            
        # Initialize price paths
        self.price_paths = np.zeros((self.num_trajectories, time_horizon + 1, self.num_assets))
        
        # Set initial prices
        self.price_paths[:, 0, :] = np.tile(self.initial_prices, (self.num_trajectories, 1))
        
        # Generate correlated Brownian motion
        random_numbers = self.rng.normal(0, 1, size=(self.num_trajectories, time_horizon, self.num_assets))
        
        # Apply correlation structure
        for i in range(self.num_trajectories):
            random_numbers[i] = np.dot(random_numbers[i], self.correlation_cholesky.T)
            
        # Add quantum uncertainty if enabled
        if self.quantum_enhanced:
            quantum_factor = np.sqrt(self.hbar)
            random_numbers += quantum_factor * self.rng.normal(0, 0.1, size=random_numbers.shape)
            
        # Simulate price paths
        for t in range(time_horizon):
            # Geometric Brownian motion with stochastic volatility
            # Make sure volatility_paths is not None before accessing it
            if self.volatility_paths is not None:
                drift = (self.drift_rates - 0.5 * self.volatility_paths[:, t, :]**2) * self.dt
                diffusion = self.volatility_paths[:, t, :] * random_numbers[:, t, :] * np.sqrt(self.dt)
                
                # Update prices
                self.price_paths[:, t+1, :] = self.price_paths[:, t, :] * np.exp(drift + diffusion)
            else:
                logger.error("Volatility paths not computed")
                break
            
        logger.info(f"Simulated asset prices for {time_horizon} time steps")
        return self.price_paths
        
    def calculate_portfolio_values(self, weights: np.ndarray, initial_investment: float) -> np.ndarray:
        """
        Calculate portfolio values based on simulated asset prices.
        
        Args:
            weights: Portfolio weights (sum to 1)
            initial_investment: Initial investment amount
            
        Returns:
            Portfolio values array of shape (num_trajectories, time_horizon+1)
        """
        if self.price_paths is None:
            raise ValueError("Asset prices have not been simulated yet")
            
        if len(weights) != self.num_assets:
            raise ValueError(f"Expected {self.num_assets} weights, got {len(weights)}")
            
        if not np.isclose(np.sum(weights), 1.0):
            logger.warning("Weights do not sum to 1, normalizing")
            weights = weights / np.sum(weights)
            
        # Calculate portfolio values
        self.portfolio_values = np.zeros((self.num_trajectories, self.price_paths.shape[1]))
        
        # Initial portfolio value
        self.portfolio_values[:, 0] = initial_investment
        
        # Calculate asset allocations
        asset_allocations = initial_investment * np.array(weights)
        asset_units = asset_allocations / self.initial_prices
        
        # Calculate portfolio values over time
        for t in range(1, self.price_paths.shape[1]):
            self.portfolio_values[:, t] = np.sum(self.price_paths[:, t, :] * asset_units, axis=1)
            
        logger.info(f"Calculated portfolio values for {len(weights)} assets")
        return self.portfolio_values
        
    def optimize_portfolio_weights(self, risk_aversion: float = 1.0, method: str = 'qaoa') -> np.ndarray:
        """
        Optimize portfolio weights using quantum algorithms.
        
        Args:
            risk_aversion: Risk aversion parameter
            method: Optimization method ('qaoa' or 'vqe')
            
        Returns:
            Optimal portfolio weights
        """
        if self.price_paths is None:
            raise ValueError("Asset prices have not been simulated yet")
            
        # Optimize portfolio
        result = self.optimize_portfolio(
            price_paths=self.price_paths,
            risk_aversion=risk_aversion,
            method=method
        )
        
        # Return quantum-adjusted weights
        return np.array(result['quantum_adjusted_weights'])
        
    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR) for the portfolio.
        
        Args:
            confidence_level: Confidence level for VaR (e.g., 0.95 for 95% confidence)
            
        Returns:
            Value at Risk (VaR)
        """
        if self.portfolio_values is None:
            raise ValueError("Portfolio values have not been calculated yet")
            
        # Calculate portfolio returns
        portfolio_returns = (self.portfolio_values[:, -1] - self.portfolio_values[:, 0]) / self.portfolio_values[:, 0]
        
        # Calculate VaR
        var_percentile = 1 - confidence_level
        var = -np.percentile(portfolio_returns, var_percentile * 100) * self.portfolio_values[:, 0].mean()
        
        logger.info(f"Calculated VaR at {confidence_level*100}% confidence: {var:.2f}")
        return var
        
    def calculate_expected_shortfall(self, confidence_level: float = 0.95) -> float:
        """
        Calculate Expected Shortfall (ES) for the portfolio.
        
        Args:
            confidence_level: Confidence level for ES (e.g., 0.95 for 95% confidence)
            
        Returns:
            Expected Shortfall (ES)
        """
        if self.portfolio_values is None:
            raise ValueError("Portfolio values have not been calculated yet")
            
        # Calculate portfolio returns
        portfolio_returns = (self.portfolio_values[:, -1] - self.portfolio_values[:, 0]) / self.portfolio_values[:, 0]
        
        # Calculate VaR cutoff
        var_percentile = 1 - confidence_level
        var_cutoff = np.percentile(portfolio_returns, var_percentile * 100)
        
        # Calculate Expected Shortfall
        tail_returns = portfolio_returns[portfolio_returns <= var_cutoff]
        es = -np.mean(tail_returns) * self.portfolio_values[:, 0].mean()
        
        logger.info(f"Calculated Expected Shortfall at {confidence_level*100}% confidence: {es:.2f}")
        return es
        
    def visualize_risk_simulation(self, num_paths: int = 100) -> None:
        """
        Visualize risk simulation results.
        
        Args:
            num_paths: Number of paths to visualize
        """
        try:
            import matplotlib.pyplot as plt
            
            if self.price_paths is None:
                raise ValueError("Asset prices have not been simulated yet")
            if self.portfolio_values is None:
                raise ValueError("Portfolio values have not been calculated yet")
                
            # Sample paths to visualize
            sample_indices = np.random.choice(self.num_trajectories, min(num_paths, self.num_trajectories), replace=False)
            
            # Create plots with error handling
            try:
                # Create figure and subplots
                plt.figure(figsize=(12, 15))
                
                # Create and configure first subplot - asset prices
                plt.subplot(3, 1, 1)
                for i in range(self.num_assets):
                    plt.plot(np.mean(self.price_paths[:, :, i], axis=0), label=f"Asset {i+1}")
                plt.title("Average Asset Prices")
                plt.xlabel("Time")
                plt.ylabel("Price")
                plt.legend()
                
                # Create and configure second subplot - volatility
                plt.subplot(3, 1, 2)
                if self.volatility_paths is not None:
                    for i in range(self.num_assets):
                        plt.plot(np.mean(self.volatility_paths[:, :, i], axis=0), label=f"Asset {i+1}")
                    plt.title("Average Volatility Paths")
                    plt.xlabel("Time")
                    plt.ylabel("Volatility")
                    plt.legend()
                
                # Create and configure third subplot - portfolio values
                plt.subplot(3, 1, 3)
                for i in sample_indices[:10]:  # Plot first 10 sample paths
                    plt.plot(self.portfolio_values[i, :], 'b-', alpha=0.1)
                plt.plot(np.mean(self.portfolio_values, axis=0), 'r-', label="Average")
                plt.title("Portfolio Values")
                plt.xlabel("Time")
                plt.ylabel("Value")
                plt.legend()
                
                plt.tight_layout()
                plt.savefig("risk_simulation.png")
                plt.show()
                
            except Exception as e:
                logger.error(f"Error creating plots: {str(e)}")
                
        except ImportError:
            logger.error("Matplotlib not available for visualization")
        
    def save_model(self, filename: str) -> None:
        """
        Save model to file.
        
        Args:
            filename: Output filename
        """
        import pickle
        
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        
        logger.info(f"Model saved to {filename}")
        
    @classmethod
    def load_model(cls, filename: str) -> 'StochasticQuantumFinance':
        """
        Load model from file.
        
        Args:
            filename: Input filename
            
        Returns:
            Loaded StochasticQuantumFinance model
        """
        import pickle
        
        with open(filename, 'rb') as f:
            model = pickle.load(f)
        
        logger.info(f"Model loaded from {filename}")
        return model 