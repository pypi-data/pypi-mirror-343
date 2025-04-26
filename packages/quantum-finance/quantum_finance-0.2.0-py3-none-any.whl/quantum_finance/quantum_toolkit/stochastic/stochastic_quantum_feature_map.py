"""
Stochastic Quantum Feature Map

This module implements the StochasticQuantumFeatureMap class, which provides
quantum-based feature extraction and dimension reduction using stochastic
quantum methods.
"""

import numpy as np
import logging
from typing import List, Dict, Tuple, Any, Optional, Callable, Union
import time
from pathlib import Path
import os
import sys
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from src.quantum_finance.quantum_toolkit.stochastic.stochastic_quantum_simulator import (
    StochasticQuantumSimulator, Trajectory, ConfigurationPoint
)

# Configure logging
logger = logging.getLogger(__name__)

class StochasticQuantumFeatureMap:
    """
    Quantum feature extraction using stochastic quantum methods.
    
    This class implements quantum embedding of classical data into trajectory
    space, extracts features from trajectory statistics, and provides dimension
    reduction techniques.
    """
    
    def __init__(self,
                 input_dim: int,
                 embedding_dim: Optional[int] = None,
                 num_trajectories: int = 1000,
                 evolution_steps: int = 20,
                 dt: float = 0.01,
                 hbar: float = 1.0,
                 seed: Optional[int] = None):
        """
        Initialize the stochastic quantum feature map.
        
        Args:
            input_dim: Dimension of input data
            embedding_dim: Dimension of the quantum embedding space (defaults to input_dim)
            num_trajectories: Number of stochastic trajectories to use
            evolution_steps: Number of steps for stochastic evolution
            dt: Time step for stochastic evolution
            hbar: Planck's constant (reduced)
            seed: Random seed for reproducibility
        """
        self.input_dim = input_dim
        self.embedding_dim = embedding_dim if embedding_dim is not None else input_dim
        self.num_trajectories = num_trajectories
        self.evolution_steps = evolution_steps
        self.dt = dt
        self.hbar = hbar
        self.seed = seed
        
        # Initialize the stochastic quantum simulator
        self.simulator = StochasticQuantumSimulator(
            config_space_dim=self.embedding_dim,
            num_trajectories=num_trajectories,
            dt=dt,
            hbar=hbar,
            mass=1.0,
            seed=seed
        )
        
        # Parameter matrices for the feature map
        # These parameters define the embedding of classical data into quantum configuration space
        self.input_scaling = np.random.randn(input_dim, int(self.embedding_dim)) * 0.1
        
        # Statistics to extract from trajectories (mean, variance, etc.)
        self.feature_statistics = ["mean", "variance", "energy", "entropy"]
        
        # Feature dimension before any reduction
        self.raw_feature_dim = len(self.feature_statistics) * self.embedding_dim
        
        # PCA for dimension reduction
        self.pca = None
        self.is_fitted = False
        
        logger.info(f"Initialized StochasticQuantumFeatureMap with {num_trajectories} trajectories")
    
    def _encode_input_to_quantum(self, input_data: np.ndarray) -> np.ndarray:
        """
        Encode classical input data to quantum configuration space.
        
        Args:
            input_data: Classical input data vector (shape: [input_dim])
        
        Returns:
            Quantum configuration space point (shape: [embedding_dim])
        """
        # Apply nonlinear transformation for richer features
        quantum_state = np.tanh(np.dot(input_data, self.input_scaling))
        return quantum_state
    
    def _create_data_specific_potential(self, input_data: np.ndarray) -> Callable:
        """
        Create a potential function specific to the input data.
        
        Args:
            input_data: Classical input data vector
        
        Returns:
            Potential function for quantum evolution
        """
        # Create a reference point in quantum space
        reference_point = self._encode_input_to_quantum(input_data)
        
        # Define harmonic-like potential around the reference point
        def potential_func(x):
            # Distance from reference point
            distance = np.sum((x - reference_point) ** 2)
            
            # Add some nonlinearity to create more complex features
            nonlinear_term = np.sum(np.sin(x * 5.0) ** 2) * 0.1
            
            return 0.5 * distance + nonlinear_term
        
        return potential_func
    
    def _extract_features_from_trajectories(self, trajectories: List[Trajectory]) -> np.ndarray:
        """
        Extract statistical features from trajectories.
        
        Args:
            trajectories: List of quantum trajectories
        
        Returns:
            Feature vector derived from trajectory statistics
        """
        # Extract configuration points from all trajectories
        configurations = []
        for traj in trajectories:
            for point in traj.points:
                configurations.append(point.configuration)
        
        if not configurations:
            logger.warning("No valid configurations found in trajectories")
            return np.zeros(self.raw_feature_dim)
        
        # Convert to numpy array
        configs_array = np.array(configurations)
        
        # Extract various statistics as features
        features = []
        
        if "mean" in self.feature_statistics:
            # Mean position in configuration space
            mean_position = np.mean(configs_array, axis=0)
            features.extend(mean_position)
        
        if "variance" in self.feature_statistics:
            # Variance of positions
            variance = np.var(configs_array, axis=0)
            features.extend(variance)
        
        if "energy" in self.feature_statistics:
            # Approximate energy as variance of momentum
            # (crude approximation of kinetic energy)
            if len(trajectories[0].points) > 1:
                momenta = []
                dt = self.dt
                for traj in trajectories:
                    for i in range(1, len(traj.points)):
                        # Finite difference approximation of momentum
                        momentum = (traj.points[i].configuration - traj.points[i-1].configuration) / dt
                        momenta.append(momentum)
                
                if momenta:
                    momenta_array = np.array(momenta)
                    kinetic_energy = np.mean(momenta_array**2, axis=0) / 2.0
                    features.extend(kinetic_energy)
                else:
                    features.extend(np.zeros(self.embedding_dim))
            else:
                features.extend(np.zeros(self.embedding_dim))
        
        if "entropy" in self.feature_statistics:
            # Approximate entropy using binned histogram in each dimension
            entropy_per_dim = []
            num_bins = min(20, len(configs_array) // 5)  # Adjust bins based on data size
            
            if num_bins > 0:
                for dim in range(self.embedding_dim):
                    hist, _ = np.histogram(configs_array[:, dim], bins=num_bins, density=True)
                    hist = hist[hist > 0]  # Avoid log(0)
                    # FIX: Ensure float, not numpy bool_, for entropy calculation
                    entropy = float(-1.0 * np.sum(hist * np.log(hist))) if len(hist) > 0 else 0.0
                    entropy_per_dim.append(entropy)
            else:
                entropy_per_dim = [0] * self.embedding_dim
                
            features.extend(entropy_per_dim)
        
        return np.array(features)
    
    def _generate_trajectories(self, input_data: np.ndarray) -> List[Trajectory]:
        """
        Generate quantum trajectories for input data.
        
        Args:
            input_data: Classical input data vector
        
        Returns:
            List of quantum trajectories
        """
        # Encode input to quantum configuration
        initial_state = self._encode_input_to_quantum(input_data)
        
        # Create potential function specific to this data point
        potential_func = self._create_data_specific_potential(input_data)
        
        # Evolve the quantum state using stochastic process
        trajectories = self.simulator.evolve_stochastic_process(
            initial_state=initial_state,
            steps=self.evolution_steps,
            potential_func=potential_func
        )
        
        logger.debug(f"Generated {len(trajectories)} trajectories for input data")
        return trajectories
    
    def transform(self, X: np.ndarray, output_dim: Optional[int] = None) -> np.ndarray:
        """
        Transform input data to quantum-enhanced features.
        
        Args:
            X: Input data array with shape [n_samples, input_dim]
            output_dim: Dimension of output features (None means no reduction)
        
        Returns:
            Transformed features with shape [n_samples, output_dim]
        """
        n_samples = X.shape[0]
        
        if X.shape[1] != self.input_dim:
            raise ValueError(f"Input data dimension {X.shape[1]} doesn't match expected {self.input_dim}")
        
        # Array to store raw features
        raw_features = np.zeros((n_samples, self.raw_feature_dim))
        
        # Process each input sample
        for i in range(n_samples):
            # Generate trajectories
            trajectories = self._generate_trajectories(X[i])
            
            # Extract features from trajectories
            features = self._extract_features_from_trajectories(trajectories)
            
            # Store features
            raw_features[i] = features
        
        # Apply dimension reduction if requested
        if output_dim is not None and output_dim < self.raw_feature_dim:
            if self.pca is None or not hasattr(self.pca, 'n_components') or self.pca.n_components != output_dim:  # type: ignore
                self.pca = PCA(n_components=output_dim)
                self.pca.fit(raw_features)
                self.is_fitted = True
            
            return self.pca.transform(raw_features)
        
        return raw_features
    
    def fit_transform(self, X: np.ndarray, output_dim: Optional[int] = None) -> np.ndarray:
        """
        Fit the feature map to data and transform it.
        
        Args:
            X: Input data array with shape [n_samples, input_dim]
            output_dim: Dimension of output features (None means no reduction)
        
        Returns:
            Transformed features with shape [n_samples, output_dim]
        """
        n_samples = X.shape[0]
        
        if X.shape[1] != self.input_dim:
            raise ValueError(f"Input data dimension {X.shape[1]} doesn't match expected {self.input_dim}")
        
        # Array to store raw features
        raw_features = np.zeros((n_samples, self.raw_feature_dim))
        
        # Process each input sample
        for i in range(n_samples):
            # Generate trajectories
            trajectories = self._generate_trajectories(X[i])
            
            # Extract features from trajectories
            features = self._extract_features_from_trajectories(trajectories)
            
            # Store features
            raw_features[i] = features
        
        # Apply dimension reduction if requested
        if output_dim is not None and output_dim < self.raw_feature_dim:
            self.pca = PCA(n_components=output_dim)
            reduced_features = self.pca.fit_transform(raw_features)
            self.is_fitted = True
            return reduced_features
        
        return raw_features
    
    def quantum_kernel(self, X: np.ndarray, Y: Optional[np.ndarray] = None, 
                      kernel_type: str = 'rbf', gamma: Optional[float] = None,
                      degree: int = 3) -> np.ndarray:
        """
        Compute a quantum-enhanced kernel matrix.
        
        Args:
            X: First data array with shape [n_samples_X, input_dim]
            Y: Second data array with shape [n_samples_Y, input_dim] (optional)
            kernel_type: Type of kernel ('rbf', 'polynomial')
            gamma: Parameter for RBF kernel (defaults to 1/n_features)
            degree: Degree for polynomial kernel
        
        Returns:
            Kernel matrix with shape [n_samples_X, n_samples_Y] or [n_samples_X, n_samples_X]
        """
        # Transform input data to quantum features
        X_features = self.transform(X)
        
        if Y is not None:
            Y_features = self.transform(Y)
        else:
            Y_features = X_features
        
        # Compute kernel matrix
        if kernel_type == 'rbf':
            if gamma is None:
                gamma = 1.0 / X_features.shape[1]
            return rbf_kernel(X_features, Y_features, gamma=gamma)
        elif kernel_type == 'polynomial':
            return polynomial_kernel(X_features, Y_features, degree=degree)
        else:
            raise ValueError(f"Unknown kernel type: {kernel_type}")
    
    def visualize_features(self, X: np.ndarray, y: Optional[np.ndarray] = None, 
                          figsize: Tuple[int, int] = (10, 8)) -> Figure:
        """
        Visualize the quantum features in 2D.
        
        Args:
            X: Input data array with shape [n_samples, input_dim]
            y: Optional labels for coloring points
            figsize: Size of the figure
        
        Returns:
            Matplotlib figure object
        """
        # Transform to features and reduce to 2D for visualization
        features_2d = self.fit_transform(X, output_dim=2)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot points
        if y is not None:
            scatter = ax.scatter(features_2d[:, 0], features_2d[:, 1], c=y, cmap='viridis', alpha=0.8)
            plt.colorbar(scatter, ax=ax, label='Class')
        else:
            ax.scatter(features_2d[:, 0], features_2d[:, 1], alpha=0.8)
        
        ax.set_title('Stochastic Quantum Features (2D)')
        ax.set_xlabel('Feature 1')
        ax.set_ylabel('Feature 2')
        
        return fig
    
    def feature_importance(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Estimate feature importance using correlation with target.
        
        Args:
            X: Input data array with shape [n_samples, input_dim]
            y: Target values with shape [n_samples]
        
        Returns:
            Feature importance scores with shape [raw_feature_dim]
        """
        # Get raw features
        features = self.transform(X)
        
        # Calculate correlation between each feature and target
        importance = np.zeros(features.shape[1])
        
        for i in range(features.shape[1]):
            corr = np.corrcoef(features[:, i], y)[0, 1]
            importance[i] = abs(corr)  # Use absolute correlation as importance
        
        return importance
    
    def save_model(self, filepath: str):
        """
        Save the feature map model to a file.
        
        Args:
            filepath: Path to save the model
        """
        model_data = {
            'input_dim': self.input_dim,
            'embedding_dim': self.embedding_dim,
            'num_trajectories': self.num_trajectories,
            'evolution_steps': self.evolution_steps,
            'dt': self.dt,
            'hbar': self.hbar,
            'seed': self.seed,
            'input_scaling': self.input_scaling,
            'feature_statistics': self.feature_statistics,
            'is_fitted': self.is_fitted
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model
        np.savez(filepath, **model_data)
        
        # Save PCA separately if fitted
        if self.is_fitted and self.pca is not None:
            import pickle
            pca_path = filepath + '.pca'
            with open(pca_path, 'wb') as f:
                pickle.dump(self.pca, f)
        
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load_model(cls, filepath: str) -> 'StochasticQuantumFeatureMap':
        """
        Load a feature map model from a file.
        
        Args:
            filepath: Path to the saved model
        
        Returns:
            Loaded StochasticQuantumFeatureMap instance
        """
        model_data = np.load(filepath, allow_pickle=True)
        
        # Create instance with saved parameters
        feature_map = cls(
            input_dim=model_data['input_dim'],
            embedding_dim=model_data['embedding_dim'],
            num_trajectories=model_data['num_trajectories'],
            evolution_steps=model_data['evolution_steps'],
            dt=model_data['dt'],
            hbar=model_data['hbar'],
            seed=model_data['seed']
        )
        
        # Restore additional parameters
        feature_map.input_scaling = model_data['input_scaling']
        feature_map.feature_statistics = model_data['feature_statistics'].tolist()
        feature_map.is_fitted = model_data['is_fitted'].item()
        
        # Load PCA if available
        if feature_map.is_fitted:
            import pickle
            pca_path = filepath + '.pca'
            if os.path.exists(pca_path):
                with open(pca_path, 'rb') as f:
                    feature_map.pca = pickle.load(f)
        
        logger.info(f"Model loaded from {filepath}")
        return feature_map 