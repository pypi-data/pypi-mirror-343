"""
Portfolio Optimization Module

This module provides portfolio optimization capabilities with quantum computing
acceleration for the StochasticQuantumFinance class. It manages the transition
between quantum and classical optimization methods based on problem characteristics
and available quantum resources.

Notes:
- Uses QuantumHardwareManager to track and limit quantum resource usage
- Implements QAOA and VQE for quantum optimization
- Provides classical fallback methods for when quantum resources are unavailable
"""

import time
import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime

# Conditional imports for quantum optimization
try:
    from qiskit import QuantumCircuit
    # Updated imports for Qiskit 1.0+
    from qiskit.algorithms.minimum_eigensolvers import QAOA, VQE 
    from qiskit.algorithms.optimizers import COBYLA, SPSA
    from qiskit.circuit.library import TwoLocal
    # Primitives will be obtained from HardwareManager
    # from qiskit_ibm_runtime import EstimatorV2 as Estimator, SamplerV2 as Sampler # Example imports
    from qiskit_optimization import QuadraticProgram
    from qiskit_optimization.algorithms import MinimumEigenOptimizer
    HAS_QISKIT_OPTIMIZATION = True
except ImportError as e:
    HAS_QISKIT_OPTIMIZATION = False
    logging.warning(f"Qiskit Optimization or related components not available, using classical methods only. Error: {e}")

# Import our quantum hardware manager
try:
    # Use relative import as the file is in the same directory
    from .quantum_hardware_manager import QuantumHardwareManager
except ImportError:
    logging.error("QuantumHardwareManager not found in the current directory.")
    QuantumHardwareManager = None # Define as None if import fails

# Classical optimization imports
import scipy.optimize as optimize

logger = logging.getLogger(__name__)

class PortfolioOptimizer:
    """
    Portfolio optimization with quantum computing capabilities.
    
    This class provides portfolio optimization using both quantum and classical
    methods, with intelligent selection between them based on problem characteristics
    and available quantum resources.
    """
    
    def __init__(self, 
                hardware_manager: Optional[Any] = None,
                risk_free_rate: float = 0.02):
        """
        Initialize the portfolio optimizer.
        
        Args:
            hardware_manager: QuantumHardwareManager instance for managing quantum resources
            risk_free_rate: Risk-free rate for Sharpe ratio calculation
        """
        self.hardware_manager = hardware_manager or (QuantumHardwareManager() if QuantumHardwareManager else None)
        self.risk_free_rate = risk_free_rate
        
        # Performance metrics
        self.last_execution_time = 0.0
        self.optimization_method_used = "classical"
        
        logger.info("Portfolio optimizer initialized")
        
    def get_available_optimization_methods(self) -> Dict[str, bool]:
        """
        Check which optimization methods are available in the current environment.
        
        Returns:
            Dictionary mapping method names to availability (True/False)
        """
        # Check for quantum optimization methods
        has_qaoa = HAS_QISKIT_OPTIMIZATION and hasattr(QAOA, '__call__') if 'QAOA' in globals() else False
        has_vqe = HAS_QISKIT_OPTIMIZATION and hasattr(VQE, '__call__') if 'VQE' in globals() else False
        
        # Check for quantum hardware access
        has_quantum_hw = self.hardware_manager is not None and getattr(self.hardware_manager, 'service', None) is not None
        
        # Result dictionary
        methods = {
            'classical': True,  # Classical optimization is always available
            'classical_advanced': True,  # Advanced classical methods (e.g., SLSQP) are available
            'qaoa': has_qaoa and has_quantum_hw,
            'vqe': has_vqe and has_quantum_hw,
            'hybrid': has_qaoa and True,  # Hybrid methods use both classical and quantum
        }
        
        return methods
        
    def optimize_portfolio(self, 
                         returns: np.ndarray,
                         cov_matrix: np.ndarray,
                         risk_aversion: float = 1.0,
                         constraints: Optional[Dict[str, Any]] = None,
                         method: str = 'auto') -> Dict[str, Any]:
        """
        Optimize portfolio weights to maximize risk-adjusted returns.
        
        Args:
            returns: Expected returns for each asset
            cov_matrix: Covariance matrix of asset returns
            risk_aversion: Risk aversion parameter (higher = more risk averse)
            constraints: Additional constraints (e.g., sector limits)
            method: Optimization method ('auto', 'qaoa', 'vqe', 'classical')
            
        Returns:
            Dictionary with optimization results (weights, metrics, etc.)
        """
        start_time = time.time()
        
        # Extract problem dimensions
        num_assets = len(returns)
        
        # Determine optimization method if 'auto'
        if method == 'auto':
            # Check if hardware manager exists before calling its method
            if self.hardware_manager:
                method = self.hardware_manager.get_optimization_method(num_assets)
            else:
                logger.warning("Hardware manager not available, defaulting to classical optimization.")
                method = 'classical' # Default if manager is None
        
        # Store the method used
        self.optimization_method_used = method
        
        # Call appropriate optimization function based on method
        if method == 'quantum' and HAS_QISKIT_OPTIMIZATION:
            result = self._quantum_optimize(returns, cov_matrix, risk_aversion, 'qaoa')
        elif method == 'hybrid' and HAS_QISKIT_OPTIMIZATION:
            result = self._hybrid_optimize(returns, cov_matrix, risk_aversion)
        else:
            # Fallback to classical optimization
            if method not in ['classical', 'classical_advanced']:
                logger.warning(f"Method {method} not available, falling back to classical")
            result = self._classical_optimize(returns, cov_matrix, risk_aversion, 
                                             advanced=(method == 'classical_advanced'))
        
        # Calculate execution time
        execution_time = time.time() - start_time
        self.last_execution_time = execution_time
        
        # Log usage if quantum method was used and manager exists
        if method in ['quantum', 'hybrid'] and self.hardware_manager:
            self.hardware_manager.log_usage(
                execution_time=execution_time,
                job_metadata={
                    'method': method,
                    'num_assets': num_assets,
                    'risk_aversion': risk_aversion
                }
            )
        
        # Add execution metadata to result
        result.update({
            'execution_time': execution_time,
            'method_used': method,
            'num_assets': num_assets,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Portfolio optimization completed using {method} method in {execution_time:.2f}s")
        return result
    
    def _quantum_optimize(self, 
                        returns: np.ndarray,
                        cov_matrix: np.ndarray,
                        risk_aversion: float = 1.0,
                        algorithm: str = 'qaoa') -> Dict[str, Any]:
        """
        Optimize portfolio using quantum algorithms (QAOA or VQE).
        
        Args:
            returns: Expected returns for each asset
            cov_matrix: Covariance matrix of asset returns
            risk_aversion: Risk aversion parameter
            algorithm: Quantum algorithm to use ('qaoa' or 'vqe')
            
        Returns:
            Dictionary with optimization results
        """
        if not HAS_QISKIT_OPTIMIZATION:
            logger.error("Qiskit Optimization not available for quantum optimization")
            return self._classical_optimize(returns, cov_matrix, risk_aversion)
            
        num_assets = len(returns)
        
        try:
            # Create quadratic program for mean-variance optimization
            # min -μ'w + λw'Σw  subject to sum(w) = 1, w_i >= 0
            qp = QuadraticProgram(name="portfolio_optimization")
            
            # Add variables (asset weights)
            for i in range(num_assets):
                qp.binary_var(name=f'x{i}')
                
            # Objective function: minimize -returns'w + risk_aversion * w'Σw
            # We convert to a minimization problem
            linear = -returns
            quadratic = risk_aversion * cov_matrix
            
            qp.minimize(linear=linear, quadratic=quadratic)
            
            # Add constraint: sum of weights = 1
            qp.linear_constraint(
                linear=[1.0] * num_assets,
                sense='=',
                rhs=1.0,
                name='budget'
            )
            
            # Ensure hardware manager exists
            if not self.hardware_manager:
                logger.error("Hardware manager not available for quantum optimization.")
                raise RuntimeError("Quantum hardware manager is required but not available.")
                
            # Get appropriate primitives from the hardware manager
            # NOTE: Assumes hardware_manager provides methods like get_estimator_primitive() and get_sampler_primitive()
            # These methods should return configured V2 Primitives (e.g., qiskit_ibm_runtime.EstimatorV2 / SamplerV2)
            num_qubits_estimate = num_assets # Info needed by manager?
            
            estimator_primitive = None
            sampler_primitive = None

            if algorithm.lower() == 'vqe':
                estimator_primitive = self.hardware_manager.get_estimator_primitive(num_qubits=num_qubits_estimate)
                if not estimator_primitive:
                    logger.error("Failed to obtain an Estimator primitive for VQE.")
                    raise RuntimeError("Estimator primitive is required for VQE but could not be obtained.")
            elif algorithm.lower() == 'qaoa':
                 sampler_primitive = self.hardware_manager.get_sampler_primitive(num_qubits=num_qubits_estimate)
                 if not sampler_primitive:
                    logger.error("Failed to obtain a Sampler primitive for QAOA.")
                    raise RuntimeError("Sampler primitive is required for QAOA but could not be obtained.")
            else:
                # Handle unsupported algorithm case if necessary
                logger.error(f"Unsupported quantum algorithm specified: {algorithm}")
                raise ValueError(f"Algorithm {algorithm} not supported for quantum optimization here.")

            # Create quantum algorithm using the appropriate Primitive
            if algorithm.lower() == 'qaoa':
                qaoa = QAOA(
                    sampler=sampler_primitive, # QAOA uses a Sampler
                    optimizer=COBYLA(maxiter=100),
                    reps=2
                )
                optimizer = MinimumEigenOptimizer(qaoa)
            else:  # VQE
                ansatz = TwoLocal(num_assets, 'ry', 'cz', reps=2, entanglement='full')
                vqe = VQE(
                    estimator=estimator_primitive, # VQE uses an Estimator
                    ansatz=ansatz,
                    optimizer=SPSA(maxiter=100)
                )
                optimizer = MinimumEigenOptimizer(vqe)
                
            # Solve problem
            result = optimizer.solve(qp)
            
            # Extract results
            x = np.array([result.x[f'x{i}'] for i in range(num_assets)])
            
            # Normalize weights to ensure they sum to 1
            weights = x / np.sum(x) if np.sum(x) > 0 else np.ones(num_assets) / num_assets
            
            # Calculate expected return and risk
            expected_return = np.sum(returns * weights)
            portfolio_variance = weights.T @ cov_matrix @ weights
            portfolio_risk = np.sqrt(portfolio_variance)
            sharpe_ratio = (expected_return - self.risk_free_rate) / portfolio_risk if portfolio_risk > 0 else 0
            
            return {
                'weights': weights.tolist(),
                'expected_return': float(expected_return),
                'risk': float(portfolio_risk),
                'sharpe_ratio': float(sharpe_ratio),
                'optimal_value': float(result.fval)
            }
            
        except Exception as e:
            logger.error(f"Error in quantum optimization: {str(e)}")
            logger.info("Falling back to classical optimization")
            return self._classical_optimize(returns, cov_matrix, risk_aversion)
    
    def _hybrid_optimize(self, 
                       returns: np.ndarray,
                       cov_matrix: np.ndarray,
                       risk_aversion: float = 1.0) -> Dict[str, Any]:
        """
        Hybrid portfolio optimization combining classical and quantum methods.
        
        This method uses classical optimization for initial solution and refines
        with quantum methods for specific subproblems.
        
        Args:
            returns: Expected returns for each asset
            cov_matrix: Covariance matrix of asset returns
            risk_aversion: Risk aversion parameter
            
        Returns:
            Dictionary with optimization results
        """
        # Start with classical optimization
        classical_result = self._classical_optimize(returns, cov_matrix, risk_aversion)
        classical_weights = np.array(classical_result['weights'])
        
        # If quantum optimization is not available, return classical results
        if not HAS_QISKIT_OPTIMIZATION:
            return classical_result
            
        try:
            # Identify top contributing assets (those with weights > threshold)
            threshold = 0.05  # 5% weight
            significant_indices = np.where(classical_weights > threshold)[0]
            
            # If we have a reasonable number of significant assets, optimize that subset
            if 3 <= len(significant_indices) <= 10:
                # Extract subproblem
                sub_returns = returns[significant_indices]
                sub_cov = cov_matrix[np.ix_(significant_indices, significant_indices)]
                
                # Optimize the subproblem with quantum methods
                sub_result = self._quantum_optimize(sub_returns, sub_cov, risk_aversion)
                sub_weights = np.array(sub_result['weights'])
                
                # Update the weights for significant assets
                hybrid_weights = classical_weights.copy()
                
                # Normalize significant weights
                significant_sum = np.sum(classical_weights[significant_indices])
                for i, idx in enumerate(significant_indices):
                    hybrid_weights[idx] = sub_weights[i] * significant_sum
                
                # Calculate portfolio metrics
                expected_return = np.sum(returns * hybrid_weights)
                portfolio_variance = hybrid_weights.T @ cov_matrix @ hybrid_weights
                portfolio_risk = np.sqrt(portfolio_variance)
                sharpe_ratio = (expected_return - self.risk_free_rate) / portfolio_risk if portfolio_risk > 0 else 0
                
                return {
                    'weights': hybrid_weights.tolist(),
                    'expected_return': float(expected_return),
                    'risk': float(portfolio_risk),
                    'sharpe_ratio': float(sharpe_ratio),
                    'hybrid_method': 'significant_assets'
                }
            else:
                # Not enough significant assets for efficient quantum optimization
                return classical_result
                
        except Exception as e:
            logger.error(f"Error in hybrid optimization: {str(e)}")
            return classical_result
    
    def _classical_optimize(self, 
                          returns: np.ndarray,
                          cov_matrix: np.ndarray,
                          risk_aversion: float = 1.0,
                          advanced: bool = False) -> Dict[str, Any]:
        """
        Optimize portfolio using classical methods.
        
        Args:
            returns: Expected returns for each asset
            cov_matrix: Covariance matrix of asset returns
            risk_aversion: Risk aversion parameter
            advanced: Whether to use advanced classical methods
            
        Returns:
            Dictionary with optimization results
        """
        num_assets = len(returns)
        
        try:
            # Define objective function (negative of utility)
            def objective(weights):
                portfolio_return = np.sum(returns * weights)
                portfolio_risk = np.sqrt(weights.T @ cov_matrix @ weights)
                return -portfolio_return + risk_aversion * portfolio_risk

            # Initial guess: equal weights
            initial_weights = np.ones(num_assets) / num_assets
            
            # Constraints
            constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}]  # Sum of weights = 1
            bounds = tuple((0, 1) for _ in range(num_assets))  # 0 <= weight <= 1
            
            # Use different optimization methods based on problem characteristics
            if advanced and num_assets > 20:
                # For large problems, use SLSQP with multiple restarts
                best_result = None
                best_utility = float('-inf')
                
                # Try multiple random starting points
                for _ in range(5):
                    random_weights = np.random.random(num_assets)
                    random_weights /= np.sum(random_weights)
                    
                    result = optimize.minimize(
                        objective, 
                        random_weights, 
                        method='SLSQP',
                        bounds=bounds,
                        constraints=constraints,
                        options={'maxiter': 1000}
                    )
                    
                    utility = -result['fun']  # Negative because we're minimizing
                    if best_result is None or utility > best_utility:
                        best_result = result
                        best_utility = utility
                
                result = best_result
            else:
                # For smaller problems, standard optimization is sufficient
                result = optimize.minimize(
                    objective, 
                    initial_weights, 
                    method='SLSQP',
                    bounds=bounds,
                    constraints=constraints
                )
            
            # Extract weights
            weights = result['x']
            
            # Calculate portfolio metrics
            expected_return = np.sum(returns * weights)
            portfolio_variance = weights.T @ cov_matrix @ weights
            portfolio_risk = np.sqrt(portfolio_variance)
            sharpe_ratio = (expected_return - self.risk_free_rate) / portfolio_risk if portfolio_risk > 0 else 0
            
            return {
                'weights': weights.tolist(),
                'expected_return': float(expected_return),
                'risk': float(portfolio_risk),
                'sharpe_ratio': float(sharpe_ratio),
                'optimal_value': float(result['fun']),
                'success': result['success'],
                'iterations': result['nit']
            }
            
        except Exception as e:
            logger.error(f"Error in classical optimization: {str(e)}")
            
            # Last resort: equal weights, ensure all expected keys are present
            weights = np.ones(num_assets) / num_assets
            expected_return = np.sum(returns * weights)
            portfolio_variance = weights.T @ cov_matrix @ weights if cov_matrix is not None else 0.0
            portfolio_risk = np.sqrt(portfolio_variance) if portfolio_variance > 0 else 0.0
            sharpe_ratio = (expected_return - self.risk_free_rate) / portfolio_risk if portfolio_risk > 0 else 0.0
            
            return {
                'weights': weights.tolist(),
                'expected_return': float(expected_return),
                'risk': float(portfolio_risk),
                'sharpe_ratio': float(sharpe_ratio),
                'optimal_value': 0.0, # Default value
                'success': False, # Explicitly False
                'iterations': 0, # Default value
                'error': str(e)
            } 