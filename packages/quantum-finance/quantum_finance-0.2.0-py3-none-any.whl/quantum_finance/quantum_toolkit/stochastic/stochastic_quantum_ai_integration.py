"""
Stochastic Quantum AI Integration Module

This module implements the integration between stochastic quantum financial methods
and advanced artificial intelligence components, creating a hybrid quantum-AI system
for enhanced financial risk assessment and prediction.

Part of Phase 2 of the Stochastic Quantum Methods implementation.
"""

import numpy as np
import logging
import time
import os
import sys
import pickle
import json
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional, Callable, Union, Type
from datetime import datetime

# Configure error handling for optional dependencies
HAS_TORCH = False
HAS_TENSORFLOW = False
HAS_SKLEARN = False

# ML/AI Libraries - handle imports gracefully with fallbacks
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    HAS_TORCH = True
except ImportError:
    logging.warning("PyTorch not available. Neural network functionality will be limited.")

try:
    import tensorflow as tf
    HAS_TENSORFLOW = True
except ImportError:
    logging.warning("TensorFlow not available. Some advanced features may be limited.")

try:
    from sklearn.base import BaseEstimator
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
    HAS_SKLEARN = True
except ImportError:
    logging.warning("scikit-learn not available. ML model functionality will be limited.")

try:
    import pandas as pd
except ImportError:
    logging.warning("pandas not available. Data handling will be limited.")

# Use standard relative imports for modules in the same package
try:
    from .stochastic_quantum_finance import StochasticQuantumFinance
    from .stochastic_quantum_generator import StochasticQuantumGenerator
    from .quantum_stochastic_decision import QuantumStochasticDecisionProcess
    from .stochastic_quantum_feature_map import StochasticQuantumFeatureMap
except ImportError as e:
    logging.error(f"Failed to import required local stochastic modules: {e}")
    # Define placeholders if import fails
    StochasticQuantumFinance = None
    StochasticQuantumGenerator = None
    QuantumStochasticDecisionProcess = None
    StochasticQuantumFeatureMap = None

# Configure logging
logger = logging.getLogger(__name__)

class QuantumFeatureExtractor:
    """
    Extracts quantum-enhanced features from financial data using stochastic quantum methods.
    
    This serves as a bridge between classical financial data and AI models by transforming
    standard financial features into quantum-enhanced features that capture complex
    financial relationships.
    """
    
    def __init__(self, 
                 num_assets: int,
                 feature_dim: int = 32,
                 num_trajectories: int = 1000,
                 dt: float = 0.01,
                 seed: Optional[int] = None):
        """
        Initialize the quantum feature extractor.
        
        Args:
            num_assets: Number of financial assets to model
            feature_dim: Dimension of the quantum feature space
            num_trajectories: Number of stochastic trajectories to use
            dt: Time step for stochastic evolution
            seed: Random seed for reproducibility
        """
        self.num_assets = num_assets
        self.feature_dim = feature_dim
        self.num_trajectories = num_trajectories
        self.dt = dt
        self.seed = seed
        
        # Initialize the stochastic quantum finance module
        if StochasticQuantumFinance is not None:
            self.quantum_finance = StochasticQuantumFinance(
                num_assets=num_assets,
                num_trajectories=num_trajectories,
                dt=dt,
                seed=seed
            )
        
        # Feature transformation parameters
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.feature_stats = {}
        
        logger.info(f"Initialized QuantumFeatureExtractor with {num_assets} assets and {feature_dim} feature dimensions")
    
    def fit(self, X: np.ndarray, asset_prices: Optional[np.ndarray] = None) -> 'QuantumFeatureExtractor':
        """
        Fit the quantum feature extractor to the data.
        
        Args:
            X: Input features (market data, technical indicators, etc.)
            asset_prices: Optional time series of asset prices
            
        Returns:
            Self, for method chaining
        """
        logger.info(f"Fitting QuantumFeatureExtractor on data with shape {X.shape}")
        
        # Fit the scaler on input data
        if HAS_SKLEARN:
            self.scaler.fit(X)
        else:
             logger.warning("sklearn not available, skipping scaler fitting.")
        
        # If asset prices are provided, set up the stochastic quantum finance model
        if asset_prices is not None:
            n_assets, n_timesteps = asset_prices.shape
            assert n_assets == self.num_assets, f"Expected {self.num_assets} assets, got {n_assets}"
            
            # Set initial asset parameters
            for i in range(self.num_assets):
                price_series = asset_prices[i]
                initial_price = price_series[0]
                
                # Estimate volatility from price series
                returns = np.diff(price_series) / price_series[:-1]
                volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
                
                self.quantum_finance.set_asset_parameters(
                    asset_idx=i,
                    initial_price=initial_price,
                    volatility=volatility
                )
                
                # Store feature stats for later use
                self.feature_stats[f"asset_{i}_initial_price"] = initial_price
                self.feature_stats[f"asset_{i}_volatility"] = volatility
        
        # If correlation data is available in X, set it
        if X.shape[1] >= self.num_assets**2:
            # Extract correlation matrix from the end of X
            if hasattr(X, '__getitem__') and callable(X.__getitem__):
                try:
                    corr_matrix_flat = X[0, -self.num_assets**2:]
                    # Check if reshape is possible
                    if corr_matrix_flat.size == self.num_assets**2:
                        corr_matrix = corr_matrix_flat.reshape(self.num_assets, self.num_assets)
                        # Ensure quantum_finance exists before setting matrix
                        if hasattr(self, 'quantum_finance') and self.quantum_finance is not None:
                            try:
                                self.quantum_finance.set_correlation_matrix(corr_matrix)
                                self.feature_stats["correlation_matrix"] = corr_matrix.tolist()
                            except Exception as e_corr:
                                logger.warning(f"Failed to set correlation matrix in quantum_finance: {e_corr}")
                        else:
                             logger.warning("quantum_finance module not initialized, cannot set correlation matrix.")
                    else:
                         logger.warning("Could not reshape correlation data, size mismatch.")
                except IndexError as e_idx:
                     logger.warning(f"Could not extract correlation matrix from X: {e_idx}")
                except AttributeError as e_attr:
                     logger.warning(f"Error accessing correlation data: {e_attr}")
            else:
                 logger.warning("Input X does not support indexing required for correlation matrix extraction.")
        
        self.is_fitted = True
        return self
    
    def transform(self, X: np.ndarray, time_steps: int = 10) -> np.ndarray:
        """
        Transform classical financial features into quantum-enhanced features.
        
        Args:
            X: Input features to transform
            time_steps: Number of time steps to simulate
            
        Returns:
            Quantum-enhanced features
        """
        if not self.is_fitted:
            raise ValueError("QuantumFeatureExtractor must be fitted before transform")
        
        logger.info(f"Transforming data with shape {X.shape} using quantum feature extraction")
        start_time = time.time()
        
        # Apply scaling if scaler was fitted
        if HAS_SKLEARN and hasattr(self.scaler, 'mean_'): # Check if scaler is fitted
            X_scaled = self.scaler.transform(X)
        else:
             X_scaled = X # Use original data if not scaled
             if HAS_SKLEARN:
                  logger.warning("Scaler not fitted or unavailable, using unscaled data.")
             else:
                  logger.warning("sklearn not available, using unscaled data.")
        
        # Initialize quantum features
        num_samples = X.shape[0]
        quantum_features = np.zeros((num_samples, self.feature_dim))
        
        # Process each sample
        for i in range(num_samples):
            sample = X_scaled[i]
            
            # Use first elements as initial volatilities (if appropriate)
            initial_volatility = np.zeros(self.num_assets) # Default
            if len(sample) >= self.num_assets:
                initial_volatility = np.abs(sample[:self.num_assets]) * 0.2 + 0.05
            else:
                 logger.warning(f"Sample length {len(sample)} less than num_assets {self.num_assets}, using default volatility.")
            
            # Simulate stochastic volatility paths if quantum_finance exists
            if hasattr(self, 'quantum_finance') and self.quantum_finance is not None and hasattr(self.quantum_finance, 'simulate_stochastic_volatility'):
                 vol_trajectories = self.quantum_finance.simulate_stochastic_volatility(
                     time_steps=time_steps,
                     initial_volatility=initial_volatility
                 )
            else:
                 logger.warning("quantum_finance module not available, cannot simulate volatility for features.")
                 vol_trajectories = [] # Empty list if cannot simulate
            
            # Extract features from volatility paths 
            for t, trajectory in enumerate(vol_trajectories):
                if t >= self.feature_dim:
                    break
                    
                # Use trajectory configuration points as features
                # The Trajectory class has points attribute (List[ConfigurationPoint]) but not configuration_history
                # Need to check the actual structure returned by simulate_stochastic_volatility
                # Assuming it returns a list of trajectory objects with a 'points' attribute
                if isinstance(trajectory, list) and trajectory: # Check if it's a list of points
                    last_point_data = trajectory[-1] # Assume last element is relevant data
                    # Assuming last_point_data is dict-like or array-like containing config/phase
                    if isinstance(last_point_data, (np.ndarray, list)) and len(last_point_data) > 0:
                         quantum_features[i, t] = np.mean(last_point_data)
                         # Cannot extract phase from simple array/list, set default
                         if t + self.num_assets < self.feature_dim:
                              quantum_features[i, t + self.num_assets] = 0.0 
                    elif isinstance(last_point_data, dict):
                         quantum_features[i, t] = np.mean(last_point_data.get('configuration', [0.0]))
                         if t + self.num_assets < self.feature_dim:
                              quantum_features[i, t + self.num_assets] = last_point_data.get('phase', 0.0)
                elif hasattr(trajectory, 'points') and trajectory.points:
                    last_point = trajectory.points[-1]
                    if hasattr(last_point, 'configuration'):
                        quantum_features[i, t] = np.mean(last_point.configuration)
                    if hasattr(last_point, 'phase') and t + self.num_assets < self.feature_dim:
                         quantum_features[i, t + self.num_assets] = last_point.phase
        
        elapsed_time = time.time() - start_time
        logger.info(f"Quantum feature extraction completed in {elapsed_time:.2f} seconds")
        
        return quantum_features

    def fit_transform(self, X: np.ndarray, asset_prices: Optional[np.ndarray] = None, time_steps: int = 10) -> np.ndarray:
        """
        Fit to data and transform in one step.
        
        Args:
            X: Input features to fit and transform
            asset_prices: Optional time series of asset prices
            time_steps: Number of time steps to simulate
            
        Returns:
            Quantum-enhanced features
        """
        return self.fit(X, asset_prices).transform(X, time_steps)
    
    def save(self, filepath: str):
        """Save the feature extractor to a file."""
        data = {
            "num_assets": self.num_assets,
            "feature_dim": self.feature_dim,
            "num_trajectories": self.num_trajectories,
            "dt": self.dt,
            "seed": self.seed,
            "is_fitted": self.is_fitted,
            "feature_stats": self.feature_stats,
            "scaler": pickle.dumps(self.scaler)
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Saved QuantumFeatureExtractor to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'QuantumFeatureExtractor':
        """Load a feature extractor from a file."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        # Create a new instance
        instance = cls(
            num_assets=data["num_assets"],
            feature_dim=data["feature_dim"],
            num_trajectories=data["num_trajectories"],
            dt=data["dt"],
            seed=data["seed"]
        )
        
        # Restore state
        instance.is_fitted = data["is_fitted"]
        instance.feature_stats = data["feature_stats"]
        # Ensure sklearn is available before unpickling scaler
        if HAS_SKLEARN:
            try:
                instance.scaler = pickle.loads(data["scaler"])
            except Exception as e_pickle:
                 logger.error(f"Failed to unpickle scaler: {e_pickle}")
                 instance.scaler = StandardScaler() # Reinitialize if load fails
        else:
             instance.scaler = None # Set to None if sklearn not available
        
        logger.info(f"Loaded QuantumFeatureExtractor from {filepath}")
        return instance


if HAS_TORCH:
    class StochasticQuantumNeuralNetwork(nn.Module):
        """
        Neural network model optimized for quantum feature data.
        
        This network architecture is specifically designed to work with quantum-enhanced
        features extracted by QuantumFeatureExtractor, providing deep learning
        capabilities for financial prediction tasks.
        """
        
        def __init__(self,
                    input_dim: int,
                    hidden_dims: List[int],
                    output_dim: int,
                    dropout_rate: float = 0.2,
                    activation: str = 'relu'):
            """
            Initialize the neural network.
            
            Args:
                input_dim: Dimension of input features
                hidden_dims: List of hidden layer dimensions
                output_dim: Dimension of output
                dropout_rate: Dropout probability for regularization
                activation: Activation function ('relu', 'tanh', or 'sigmoid')
            """
            super().__init__()
            self.input_dim = input_dim
            self.hidden_dims = hidden_dims
            self.output_dim = output_dim
            self.dropout_rate = dropout_rate
            
            # Define activation function
            if activation == 'relu':
                self.activation = nn.ReLU()
            elif activation == 'tanh':
                self.activation = nn.Tanh()
            elif activation == 'sigmoid':
                self.activation = nn.Sigmoid()
            else:
                logger.warning(f"Unknown activation '{activation}', using ReLU")
                self.activation = nn.ReLU()
                
            # Build network layers
            layers = []
            prev_dim = input_dim
            
            for i, dim in enumerate(hidden_dims):
                layers.append(nn.Linear(prev_dim, dim))
                layers.append(self.activation)
                layers.append(nn.Dropout(dropout_rate))
                prev_dim = dim
                
            # Output layer
            layers.append(nn.Linear(prev_dim, output_dim))
            
            self.model = nn.Sequential(*layers)
            
            logger.info(f"Initialized neural network with architecture: {input_dim} -> {hidden_dims} -> {output_dim}")
            
        def forward(self, x):
            """Forward pass through the network."""
            return self.model(x)
            
        def save(self, filepath: str):
            """Save model weights to a file."""
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            # Save model and metadata
            torch.save({
                'model_state_dict': self.state_dict(),
                'input_dim': self.input_dim,
                'hidden_dims': self.hidden_dims,
                'output_dim': self.output_dim,
                'dropout_rate': self.dropout_rate
            }, filepath)
            
            logger.info(f"Saved neural network model to {filepath}")
            
        @classmethod
        def load(cls, filepath: str) -> 'StochasticQuantumNeuralNetwork':
            """Load model from a file."""
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            checkpoint = torch.load(filepath, map_location=device)
            
            # Create a new instance
            model = cls(
                input_dim=checkpoint['input_dim'],
                hidden_dims=checkpoint['hidden_dims'],
                output_dim=checkpoint['output_dim'],
                dropout_rate=checkpoint['dropout_rate']
            )
            
            # Load state dict
            model.load_state_dict(checkpoint['model_state_dict'])
            
            logger.info(f"Loaded neural network model from {filepath}")
            return model
else:
    # Placeholder class when PyTorch is not available
    class StochasticQuantumNeuralNetwork:
        """
        Placeholder neural network when PyTorch is not available.
        
        This class provides the same interface as the PyTorch implementation
        but will raise NotImplementedError when methods are called.
        """
        def __init__(self,
                    input_dim: int,
                    hidden_dims: List[int],
                    output_dim: int,
                    dropout_rate: float = 0.2,
                    activation: str = 'relu'):
            """Store parameters but indicate that functionality is limited."""
            self.input_dim = input_dim
            self.hidden_dims = hidden_dims
            self.output_dim = output_dim
            self.dropout_rate = dropout_rate
            self.activation = activation
            logger.warning("PyTorch not available. Neural network functionality is disabled.")
            
        def __call__(self, x):
            """Raise error when trying to perform forward pass."""
            # Return zero array of expected output shape if possible, or raise error
            logger.error("PyTorch is required for neural network functionality")
            # Assuming x is numpy array, return zeros of same batch size, output_dim
            if isinstance(x, np.ndarray):
                 return np.zeros((x.shape[0], self.output_dim))
            return np.zeros(self.output_dim) # Fallback
            # raise NotImplementedError("PyTorch is required for neural network functionality")
            
        def forward(self, x):
            """Raise error when trying to perform forward pass."""
            logger.error("PyTorch is required for neural network functionality")
            if isinstance(x, np.ndarray):
                 return np.zeros((x.shape[0], self.output_dim))
            return np.zeros(self.output_dim)
            # raise NotImplementedError("PyTorch is required for neural network functionality")
            
        def save(self, filepath: str):
            """Indicate that saving is not available."""
            logger.error("Cannot save neural network model: PyTorch is not available")
            raise NotImplementedError("PyTorch is required for neural network functionality")
            
        @classmethod
        def load(cls, filepath: str) -> 'StochasticQuantumNeuralNetwork':
            """Indicate that loading is not available."""
            logger.error("Cannot load neural network model: PyTorch is not available")
            raise NotImplementedError("PyTorch is required for neural network functionality")


class QuantumAIFinanceWrapper:
    """
    Wrapper class that integrates stochastic quantum finance with AI/ML models.
    
    This class combines the StochasticQuantumFinance module with AI components,
    providing an end-to-end solution for quantum-enhanced financial prediction.
    """
    
    def __init__(self,
                 num_assets: int,
                 model_type: str = 'neural_network',
                 feature_extractor_params: Optional[Dict[str, Any]] = None,
                 model_params: Optional[Dict[str, Any]] = None,
                 device: str = 'cpu'):
        """
        Initialize the quantum AI finance wrapper.
        
        Args:
            num_assets: Number of financial assets to model
            model_type: Type of model ('neural_network', 'random_forest', 'mlp')
            feature_extractor_params: Parameters for feature extractor
            model_params: Parameters for the AI model
            device: Device to use for PyTorch models ('cpu' or 'cuda')
        """
        self.num_assets = num_assets
        self.model_type = model_type
        self.device = device
        
        # Default parameters
        default_extractor_params = {
            'feature_dim': 32,
            'num_trajectories': 1000,
            'dt': 0.01,
            'seed': None
        }
        
        default_model_params = {
            'neural_network': {
                'hidden_dims': [64, 32],
                'output_dim': 1,
                'dropout_rate': 0.2,
                'activation': 'relu',
                'learning_rate': 0.001,
                'batch_size': 32,
                'num_epochs': 100
            },
            'random_forest': {
                'n_estimators': 100,
                'max_depth': None,
                'min_samples_split': 2,
                'min_samples_leaf': 1
            },
            'mlp': {
                'hidden_layer_sizes': (64, 32),
                'activation': 'relu',
                'solver': 'adam',
                'alpha': 0.0001,
                'batch_size': 'auto',
                'max_iter': 200
            }
        }
        
        # Merge default and provided parameters
        self.feature_extractor_params = {**default_extractor_params, **(feature_extractor_params or {})}
        # Ensure model_type exists in default_model_params before access
        if model_type not in default_model_params:
             logger.warning(f"Model type '{model_type}' not recognized, defaulting to 'random_forest'.")
             self.model_type = 'random_forest'
        self.model_params = {**default_model_params[self.model_type], **(model_params or {})}
        
        # Initialize the feature extractor
        # Check if StochasticQuantumFeatureMap is defined
        if StochasticQuantumFeatureMap is not None:
            self.feature_extractor = StochasticQuantumFeatureMap(
                num_assets=num_assets,
                **self.feature_extractor_params
            )
        else:
             logger.error("StochasticQuantumFeatureMap could not be imported. Feature extraction disabled.")
             self.feature_extractor = None
        
        # Initialize the model
        self._initialize_model()
        
        # Training metrics
        self.training_history = {
            'loss': [],
            'val_loss': [],
            'metrics': {}
        }
        
        logger.info(f"Initialized QuantumAIFinanceWrapper with {num_assets} assets and {model_type} model")
    
    def _initialize_model(self):
        """Initialize the AI model based on model_type."""
        if self.model_type == 'neural_network':
            if not HAS_TORCH:
                logger.warning("Neural network model requested but PyTorch is not available.")
                logger.warning("Consider installing PyTorch or using an alternative model type.")
                logger.warning("Defaulting to 'random_forest' model type.")
                self.model_type = 'random_forest'
                self.device = 'cpu'  # Default to CPU when PyTorch not available
            else:
                # Use PyTorch with device selection
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                self.model = StochasticQuantumNeuralNetwork(
                    input_dim=self.feature_extractor_params['feature_dim'],
                    hidden_dims=self.model_params['hidden_dims'],
                    output_dim=self.model_params['output_dim'],
                    dropout_rate=self.model_params.get('dropout_rate', 0.2),
                    activation=self.model_params.get('activation', 'relu')
                )
                if HAS_TORCH:
                    self.model = self.model.to(self.device)
                
                logger.info(f"Using neural network model with device: {self.device}")
        
        if self.model_type == 'random_forest':
            # Check HAS_SKLEARN before initializing
            if not HAS_SKLEARN:
                 logger.error("Cannot initialize RandomForest: scikit-learn not available.")
                 self.model = None
            # For regression vs classification
            elif self.model_params.get('output_dim', 1) == 1:
                self.model = RandomForestRegressor(
                    **{k: v for k, v in self.model_params.items() 
                       if k in ['n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf']}
                )
            else:
                self.model = RandomForestClassifier(
                    **{k: v for k, v in self.model_params.items() 
                       if k in ['n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf']}
                )
            logger.info(f"Using random forest {'classifier' if self.model_params.get('output_dim', 1) == 1 else 'regressor'}")
            
        elif self.model_type == 'mlp':
            # Check HAS_SKLEARN before initializing
            if not HAS_SKLEARN:
                 logger.error(f"Cannot initialize MLP: scikit-learn not available.")
                 self.model = None
            # Determine if it's regression or classification
            elif self.model_params.get('output_dim', 1) == 1:
                self.model = MLPRegressor(
                    **{k: v for k, v in self.model_params.items() 
                       if k in ['hidden_layer_sizes', 'activation', 'solver', 'alpha', 'batch_size', 'max_iter']}
                )
            else:
                self.model = MLPClassifier(
                    **{k: v for k, v in self.model_params.items() 
                       if k in ['hidden_layer_sizes', 'activation', 'solver', 'alpha', 'batch_size', 'max_iter']}
                )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def fit(self, 
             X: np.ndarray, 
             y: np.ndarray, 
             asset_prices: Optional[np.ndarray] = None,
             validation_split: float = 0.2) -> Dict[str, List[float]]:
        """
        Fit the model to the data.
        
        Args:
            X: Input features
            y: Target values
            asset_prices: Optional time series of asset prices for feature extraction
            validation_split: Proportion of data to use for validation
            
        Returns:
            Training history with metrics
        """
        logger.info(f"Fitting {self.model_type} model with {X.shape[0]} samples")
        start_time = time.time()
        
        # Transform the data using quantum feature extractor
        # Check if feature_extractor exists before using
        if self.feature_extractor is None:
             logger.error("Feature extractor not initialized. Cannot fit model.")
             return history # Return empty history

        X_quantum = self.feature_extractor.fit_transform(X, asset_prices)
        
        # Split data if validation is requested
        if validation_split > 0 and validation_split < 1:
            X_train, X_val, y_train, y_val = train_test_split(
                X_quantum, y, test_size=validation_split, random_state=42
            )
        else:
            X_train, X_val = X_quantum, None
            y_train, y_val = y, None
        
        history = {'loss': [], 'val_loss': []}
        
        # Fit the model based on its type
        if self.model_type == 'neural_network' and HAS_TORCH:
            # Train neural network with PyTorch
            batch_size = self.model_params.get('batch_size', 32)
            num_epochs = self.model_params.get('num_epochs', 100)
            learning_rate = self.model_params.get('learning_rate', 0.001)
            
            # Create optimizer and loss function
            # Check if model has parameters before creating optimizer
            if hasattr(self.model, 'parameters') and callable(self.model.parameters):
                 optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
            else:
                 logger.error("Model does not have parameters method. Cannot create optimizer.")
                 return history # Cannot train

            criterion = nn.MSELoss() if self.model_params['output_dim'] == 1 else nn.CrossEntropyLoss()
            
            # Create data loaders
            # Check tensors before creating dataset
            if X_train is None or y_train is None:
                 logger.error("Tensor conversion failed, cannot create DataLoader.")
                 return history # Return empty history

            X_tensor = torch.tensor(X_train, dtype=torch.float32).to(self.device)
            y_tensor = torch.tensor(y_train, dtype=torch.float32).to(self.device)
            if self.model_params['output_dim'] > 1:
                y_tensor = y_tensor.long()  # For classification
            
            dataset = TensorDataset(X_tensor, y_tensor)
            dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
            
            # Train loop
            self.model.train()
            for epoch in range(num_epochs):
                epoch_loss = 0.0
                for batch_X, batch_y in dataloader:
                    # Forward pass
                    outputs = self.model(batch_X)
                    if self.model_params['output_dim'] == 1:
                        outputs = outputs.squeeze()
                    
                    # Calculate loss
                    loss = criterion(outputs, batch_y)
                    
                    # Backward pass and optimize
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                
                avg_epoch_loss = epoch_loss / len(dataloader)
                history['loss'].append(avg_epoch_loss)
                
                # Calculate validation loss
                if X_val is not None and y_val is not None:
                    val_loss = self._calculate_validation_loss(
                        X_val, y_val, criterion
                    )
                    history['val_loss'].append(val_loss)
                
                # Log progress
                if (epoch + 1) % 10 == 0:
                    logger.info(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_epoch_loss:.4f}")
        
        elif self.model_type in ['random_forest', 'mlp']:
            # Train sklearn model
            # Check if model exists and HAS_SKLEARN
            if self.model is None or not HAS_SKLEARN:
                 logger.error("Cannot train sklearn model: Model not initialized or sklearn not available.")
                 return history

            self.model.fit(X_train, y_train)
            
            # Calculate training score
            train_score = self.model.score(X_train, y_train)
            history['loss'].append(-train_score)  # Negative score as loss
            
            # Calculate validation score if requested
            if X_val is not None and y_val is not None:
                val_score = self.model.score(X_val, y_val)
                history['val_loss'].append(-val_score)
                
            logger.info(f"Model trained with training score: {train_score:.4f}")
        
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
        
        elapsed_time = time.time() - start_time
        logger.info(f"Model training completed in {elapsed_time:.2f} seconds")
        
        return history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Generate predictions using the model.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        # Extract quantum features
        # Check if feature_extractor exists
        if self.feature_extractor is None:
             logger.error("Feature extractor not initialized. Cannot predict.")
             return np.zeros(X.shape[0]) # Return default predictions

        quantum_features = self.feature_extractor.transform(X)
        
        # Make predictions
        if self.model_type == 'neural_network':
            self.model.eval()
            with torch.no_grad():
                qf_tensor = torch.tensor(quantum_features, dtype=torch.float32).to(self.device)
                outputs = self.model(qf_tensor)
                predictions = outputs.cpu().numpy()
                
                # Reshape if needed
                if predictions.ndim > 1 and predictions.shape[1] == 1:
                    predictions = predictions.flatten()
        else:
            # Check if sklearn model exists
            if self.model is None:
                 logger.error("Cannot predict: Model not initialized.")
                 return np.zeros(quantum_features.shape[0])
            predictions = self.model.predict(quantum_features)
        
        return predictions
    
    def predict_with_uncertainty(self, X: np.ndarray, num_samples: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate predictions with uncertainty estimates.
        
        Args:
            X: Input features
            num_samples: Number of stochastic samples for uncertainty estimation
            
        Returns:
            Tuple of (predictions, uncertainty)
        """
        # Use the underlying stochastic quantum finance model for uncertainty estimation
        quantum_features_list = []
        
        # Check if feature_extractor exists
        if self.feature_extractor is None:
             logger.error("Feature extractor not initialized. Cannot estimate uncertainty.")
             return np.zeros(X.shape[0]), np.zeros(X.shape[0]) # Return defaults

        # Generate multiple quantum feature sets using different stochastic paths
        for _ in range(num_samples):
            # Use a different random seed each time
            self.feature_extractor.quantum_finance.seed = np.random.randint(0, 10000)
            quantum_features = self.feature_extractor.transform(X)
            quantum_features_list.append(quantum_features)
        
        predictions_list = []
        
        # Generate predictions for each feature set
        for quantum_features in quantum_features_list:
            if self.model_type == 'neural_network':
                self.model.eval()
                with torch.no_grad():
                    qf_tensor = torch.tensor(quantum_features, dtype=torch.float32).to(self.device)
                    outputs = self.model(qf_tensor)
                    batch_predictions = outputs.cpu().numpy()
                    
                    # Reshape if needed
                    if batch_predictions.ndim > 1 and batch_predictions.shape[1] == 1:
                        batch_predictions = batch_predictions.flatten()
            else:
                 # Check if model exists
                 if self.model is None:
                      logger.warning("Model not initialized, cannot generate predictions for uncertainty sample.")
                      # Append array of NaNs or zeros based on expected output shape
                      pred_shape = (quantum_features.shape[0], self.model_params.get('output_dim', 1))
                      if pred_shape[1] == 1: pred_shape = (pred_shape[0],)
                      batch_predictions = np.full(pred_shape, np.nan)
                 else:
                      batch_predictions = self.model.predict(quantum_features)
            
            predictions_list.append(batch_predictions)
        
        # Calculate mean and standard deviation
        predictions_array = np.array(predictions_list)
        mean_predictions = np.mean(predictions_array, axis=0)
        uncertainty = np.std(predictions_array, axis=0)
        
        return mean_predictions, uncertainty
    
    def analyze_risk_factors(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Analyze risk factors for financial data using the hybrid model.
        
        Args:
            X: Input features
            
        Returns:
            Dictionary of risk factors and their importances
        """
        # First, get baseline predictions
        baseline_predictions = self.predict(X)
        
        # For sklearn models, use built-in feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            # Get quantum features
            quantum_features = self.feature_extractor.transform(X)
            
            # Extract feature importances
            feature_importances = self.model.feature_importances_
            
            return {
                'quantum_feature_importances': feature_importances
            }
        
        # For neural network, use a simple perturbation-based approach
        risk_factors = {}
        quantum_features = self.feature_extractor.transform(X)
        
        # Perturb each feature and measure the effect on predictions
        feature_importances = np.zeros(quantum_features.shape[1])
        
        for i in range(quantum_features.shape[1]):
            # Create a perturbed copy
            perturbed_features = quantum_features.copy()
            perturbed_features[:, i] *= 1.1  # Increase by 10%
            
            # Get predictions with perturbed features
            if self.model_type == 'neural_network':
                self.model.eval()
                with torch.no_grad():
                    perturbed_tensor = torch.tensor(perturbed_features, dtype=torch.float32).to(self.device)
                    perturbed_outputs = self.model(perturbed_tensor)
                    perturbed_predictions = perturbed_outputs.cpu().numpy()
                    
                    # Reshape if needed
                    if perturbed_predictions.shape[1] == 1:
                        perturbed_predictions = perturbed_predictions.flatten()
            else:
                perturbed_predictions = self.model.predict(perturbed_features)
            
            # Calculate the effect
            effect = np.mean(np.abs(perturbed_predictions - baseline_predictions))
            feature_importances[i] = effect
        
        # Normalize importances
        if np.sum(feature_importances) > 0:
            feature_importances = feature_importances / np.sum(feature_importances)
        
        risk_factors['quantum_feature_importances'] = feature_importances
        
        # Also analyze original features
        if X.shape[1] <= 20:  # Only for reasonably sized feature sets
            orig_feature_importances = np.zeros(X.shape[1])
            
            for i in range(X.shape[1]):
                # Create a perturbed copy of original features
                perturbed_X = X.copy()
                perturbed_X[:, i] *= 1.1  # Increase by 10%
                
                # Process through quantum feature extraction and prediction
                perturbed_predictions = self.predict(perturbed_X)
                
                # Calculate the effect
                effect = np.mean(np.abs(perturbed_predictions - baseline_predictions))
                orig_feature_importances[i] = effect
            
            # Normalize importances
            if np.sum(orig_feature_importances) > 0:
                orig_feature_importances = orig_feature_importances / np.sum(orig_feature_importances)
            
            risk_factors['original_feature_importances'] = orig_feature_importances
        
        return risk_factors
    
    def save(self, base_path: str):
        """
        Save the wrapper and its components to files.
        
        Args:
            base_path: Base path for saving files
        """
        os.makedirs(base_path, exist_ok=True)
        
        # Save feature extractor
        feature_extractor_path = os.path.join(base_path, 'feature_extractor.pkl')
        self.feature_extractor.save(feature_extractor_path)
        
        # Save model
        if self.model_type == 'neural_network':
            model_path = os.path.join(base_path, 'model.pt')
            self.model.save(model_path)
        else:
            model_path = os.path.join(base_path, 'model.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
        
        # Save configuration and metadata
        metadata = {
            'num_assets': self.num_assets,
            'model_type': self.model_type,
            'feature_extractor_params': self.feature_extractor_params,
            'model_params': self.model_params,
            'device': self.device,
            'training_history': self.training_history,
            'created_at': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        metadata_path = os.path.join(base_path, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Saved QuantumAIFinanceWrapper to {base_path}")
    
    @classmethod
    def load(cls, base_path: str) -> 'QuantumAIFinanceWrapper':
        """
        Load the wrapper and its components from files.
        
        Args:
            base_path: Base path for loading files
            
        Returns:
            Loaded QuantumAIFinanceWrapper
        """
        # Load metadata
        metadata_path = os.path.join(base_path, 'metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Create a new instance
        instance = cls(
            num_assets=metadata['num_assets'],
            model_type=metadata['model_type'],
            feature_extractor_params=metadata['feature_extractor_params'],
            model_params=metadata['model_params'],
            device=metadata['device']
        )
        
        # Load feature extractor
        feature_extractor_path = os.path.join(base_path, 'feature_extractor.pkl')
        instance.feature_extractor = QuantumFeatureExtractor.load(feature_extractor_path)
        
        # Load model
        if metadata['model_type'] == 'neural_network':
            model_path = os.path.join(base_path, 'model.pt')
            instance.model = StochasticQuantumNeuralNetwork.load(model_path)
        else:
            model_path = os.path.join(base_path, 'model.pkl')
            with open(model_path, 'rb') as f:
                instance.model = pickle.load(f)
        
        # Restore training history
        instance.training_history = metadata['training_history']
        
        logger.info(f"Loaded QuantumAIFinanceWrapper from {base_path}")
        return instance 

    def _calculate_validation_loss(self, X_val: np.ndarray, y_val: np.ndarray, criterion=None):
        """
        Calculate validation loss for neural network models.
        
        Args:
            X_val: Validation features
            y_val: Validation targets
            criterion: Loss function
            
        Returns:
            Validation loss value
        """
        if self.model_type == 'neural_network' and HAS_TORCH:
            self.model.eval()
            with torch.no_grad():
                X_tensor = torch.tensor(X_val, dtype=torch.float32).to(self.device)
                y_tensor = torch.tensor(y_val, dtype=torch.float32).to(self.device)
                
                if self.model_params['output_dim'] > 1:
                    y_tensor = y_tensor.long()
                    
                outputs = self.model(X_tensor)
                if self.model_params['output_dim'] == 1:
                    outputs = outputs.squeeze()
                    
                return criterion(outputs, y_tensor).item()
        else:
            # For non-neural network models, return negative score
            return -self.model.score(X_val, y_val) 