"""
Hybrid Stochastic Quantum Pipeline

This module implements the HybridStochasticPipeline class, which orchestrates
workflows combining classical machine learning with stochastic quantum methods.
"""

import numpy as np
import logging
from typing import List, Dict, Tuple, Any, Optional, Callable, Union
import time
from pathlib import Path
import os
import sys
import json
import uuid
import pickle
from datetime import datetime

# Add the project root to the Python path if needed
try:
    from quantum.stochastic.stochastic_quantum_generator import StochasticQuantumGenerator
    from quantum.stochastic.quantum_stochastic_decision import QuantumStochasticDecisionProcess
    from quantum.stochastic.stochastic_quantum_feature_map import StochasticQuantumFeatureMap
except ImportError:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from quantum.stochastic.stochastic_quantum_generator import StochasticQuantumGenerator
    from quantum.stochastic.quantum_stochastic_decision import QuantumStochasticDecisionProcess
    from quantum.stochastic.stochastic_quantum_feature_map import StochasticQuantumFeatureMap

# Configure logging
logger = logging.getLogger(__name__)

class HybridStochasticPipeline:
    """
    Orchestrates hybrid classical-stochastic-quantum workflows.
    
    This class integrates classical machine learning with stochastic quantum methods,
    providing a unified pipeline for data processing, feature extraction, and modeling.
    """
    
    def __init__(self,
                 pipeline_config: Dict[str, Any] = None,
                 output_dir: Optional[str] = None):
        """
        Initialize the hybrid stochastic pipeline.
        
        Args:
            pipeline_config: Configuration dictionary for the pipeline
            output_dir: Directory for pipeline outputs (models, results, etc.)
        """
        # Set default configuration if none provided
        self.config = pipeline_config or {
            'input_preprocessing': {
                'normalize': True,
                'remove_outliers': False
            },
            'feature_extraction': {
                'use_quantum_features': True,
                'embedding_dim': 8,
                'num_trajectories': 500,
                'output_dim': 10
            },
            'model': {
                'type': 'classifier',  # or 'generator', 'decision'
                'hyperparameters': {}
            },
            'execution': {
                'parallel': False,
                'cache_intermediates': True,
                'batch_size': 32
            }
        }
        
        # Set output directory
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'hybrid_pipeline_output')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Pipeline components
        self.feature_map = None
        self.generator = None
        self.decision_process = None
        self.classical_model = None
        
        # Pipeline metadata
        self.pipeline_id = str(uuid.uuid4())
        self.creation_time = datetime.now().isoformat()
        self.last_run_time = None
        self.execution_history = []
        
        logger.info(f"Initialized HybridStochasticPipeline with ID {self.pipeline_id}")
    
    def _preprocess_data(self, X: np.ndarray) -> np.ndarray:
        """
        Preprocess input data according to pipeline configuration.
        
        Args:
            X: Input data array
        
        Returns:
            Preprocessed data array
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Apply preprocessing steps
        if self.config['input_preprocessing']['normalize']:
            # Simple normalization to [0, 1] range
            X_min = X.min(axis=0)
            X_range = X.max(axis=0) - X_min
            # Avoid division by zero
            X_range[X_range == 0] = 1.0
            X_normalized = (X - X_min) / X_range
            X = X_normalized
        
        if self.config['input_preprocessing']['remove_outliers']:
            # Simple outlier removal (clip values beyond 3 standard deviations)
            mean = np.mean(X, axis=0)
            std = np.std(X, axis=0)
            X_clipped = np.clip(X, mean - 3 * std, mean + 3 * std)
            X = X_clipped
        
        return X
    
    def _setup_feature_extraction(self, input_dim: int):
        """
        Set up feature extraction component if not already initialized.
        
        Args:
            input_dim: Dimension of input data
        """
        if self.feature_map is None and self.config['feature_extraction']['use_quantum_features']:
            self.feature_map = StochasticQuantumFeatureMap(
                input_dim=input_dim,
                embedding_dim=self.config['feature_extraction']['embedding_dim'],
                num_trajectories=self.config['feature_extraction']['num_trajectories']
            )
            logger.info("Initialized quantum feature map")
    
    def _setup_generator(self, input_dim: int):
        """
        Set up generative model if not already initialized.
        
        Args:
            input_dim: Dimension of input data
        """
        if self.generator is None and self.config['model']['type'] == 'generator':
            embedding_dim = self.config['feature_extraction']['embedding_dim']
            self.generator = StochasticQuantumGenerator(
                config_space_dim=embedding_dim,
                latent_dim=min(input_dim, 20),  # Reasonable default
                num_trajectories=self.config['feature_extraction']['num_trajectories']
            )
            logger.info("Initialized stochastic quantum generator")
    
    def _setup_decision_process(self, num_states: int = None, num_actions: int = None):
        """
        Set up decision process if not already initialized.
        
        Args:
            num_states: Number of states in the decision process
            num_actions: Number of possible actions
        """
        if self.decision_process is None and self.config['model']['type'] == 'decision':
            self.decision_process = QuantumStochasticDecisionProcess(
                num_states=num_states or 10,  # Default value
                num_actions=num_actions or 4,  # Default value
                num_trajectories=self.config['feature_extraction']['num_trajectories']
            )
            logger.info("Initialized quantum stochastic decision process")
    
    def _setup_classical_model(self, model_type: str):
        """
        Set up classical ML model if needed.
        
        Args:
            model_type: Type of classical model to initialize
        """
        if self.classical_model is None:
            # Import ML libraries only when needed
            try:
                from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
                from sklearn.linear_model import LogisticRegression, LinearRegression
                
                hyperparams = self.config['model'].get('hyperparameters', {})
                
                if model_type == 'classifier':
                    if self.config['model'].get('algorithm') == 'random_forest':
                        self.classical_model = RandomForestClassifier(**hyperparams)
                    else:
                        self.classical_model = LogisticRegression(**hyperparams)
                elif model_type == 'regressor':
                    if self.config['model'].get('algorithm') == 'random_forest':
                        self.classical_model = RandomForestRegressor(**hyperparams)
                    else:
                        self.classical_model = LinearRegression(**hyperparams)
                
                logger.info(f"Initialized classical {model_type} model")
            except ImportError:
                logger.warning("Could not import scikit-learn. Classical model not initialized.")
    
    def extract_features(self, X: np.ndarray) -> np.ndarray:
        """
        Extract features using quantum or classical methods.
        
        Args:
            X: Input data array
        
        Returns:
            Extracted features
        """
        # Preprocess data
        X_processed = self._preprocess_data(X)
        
        # Set up feature extractor if needed
        self._setup_feature_extraction(X_processed.shape[1])
        
        # Extract features
        if self.feature_map and self.config['feature_extraction']['use_quantum_features']:
            output_dim = self.config['feature_extraction'].get('output_dim')
            features = self.feature_map.transform(X_processed, output_dim=output_dim)
            logger.info(f"Extracted quantum features with shape {features.shape}")
        else:
            # Identity mapping (no feature extraction)
            features = X_processed
            logger.info("Using original features (no quantum feature extraction)")
        
        return features
    
    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> 'HybridStochasticPipeline':
        """
        Fit the pipeline to training data.
        
        Args:
            X: Input data array
            y: Target values (optional, required for supervised models)
        
        Returns:
            Self (fitted pipeline)
        """
        start_time = time.time()
        logger.info(f"Fitting pipeline on data with shape {X.shape}")
        
        # Preprocess data
        X_processed = self._preprocess_data(X)
        
        # Set up components based on model type
        model_type = self.config['model']['type']
        
        if model_type == 'generator':
            # Set up generator
            self._setup_generator(X_processed.shape[1])
            
            # No explicit fitting for generator
            # (parameters are updated during generation)
            logger.info("Generator model ready for sampling")
            
        elif model_type == 'decision':
            # For decision process, we need to set up states and actions
            # This usually comes from domain knowledge
            if y is not None and len(np.unique(y)) < 20:  # Use classes as states if reasonable
                num_states = len(np.unique(y))
                num_actions = min(num_states, 10)  # Arbitrary default
            else:
                # Default values
                num_states = 10
                num_actions = 4
            
            # Set up decision process
            self._setup_decision_process(num_states, num_actions)
            
            # No explicit fitting for decision process
            # (parameters are updated during policy iteration)
            logger.info(f"Decision process ready with {num_states} states and {num_actions} actions")
            
        else:  # classifier or regressor
            # Extract features
            if self.config['feature_extraction']['use_quantum_features']:
                self._setup_feature_extraction(X_processed.shape[1])
                X_features = self.feature_map.fit_transform(
                    X_processed, 
                    output_dim=self.config['feature_extraction'].get('output_dim')
                )
            else:
                X_features = X_processed
            
            # Initialize the appropriate classical model
            if y is not None:
                # Determine if classification or regression
                if np.issubdtype(y.dtype, np.integer) or len(np.unique(y)) < 10:
                    model_subtype = 'classifier'
                else:
                    model_subtype = 'regressor'
                
                self._setup_classical_model(model_subtype)
                
                # Fit the classical model
                if self.classical_model is not None:
                    self.classical_model.fit(X_features, y)
                    logger.info(f"Fitted classical {model_subtype} model")
                else:
                    logger.warning("No classical model available for fitting")
            else:
                logger.warning("No target values provided for supervised model fitting")
        
        # Record execution
        self.last_run_time = datetime.now().isoformat()
        execution_time = time.time() - start_time
        
        self.execution_history.append({
            'operation': 'fit',
            'timestamp': self.last_run_time,
            'data_shape': X.shape,
            'execution_time_seconds': execution_time,
            'model_type': model_type
        })
        
        logger.info(f"Pipeline fitting completed in {execution_time:.2f} seconds")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the fitted pipeline.
        
        Args:
            X: Input data array
        
        Returns:
            Predictions
        """
        start_time = time.time()
        logger.info(f"Generating predictions for data with shape {X.shape}")
        
        # Preprocess data
        X_processed = self._preprocess_data(X)
        
        # Get model type
        model_type = self.config['model']['type']
        
        if model_type == 'generator':
            if self.generator is None:
                self._setup_generator(X_processed.shape[1])
            
            # Generate samples
            output_dim = X_processed.shape[1]
            predictions = self.generator.generate_samples(
                num_samples=len(X_processed),
                output_dim=output_dim,
                conditional_data=X_processed
            )
            
        elif model_type == 'decision':
            if self.decision_process is None:
                self._setup_decision_process()
            
            # Convert inputs to state indices
            # This is a simplified approach; real applications need more sophisticated mapping
            if X_processed.ndim > 1 and X_processed.shape[1] > 1:
                # Use clustering to map inputs to states
                try:
                    from sklearn.cluster import KMeans
                    kmeans = KMeans(n_clusters=self.decision_process.num_states)
                    state_indices = kmeans.fit_predict(X_processed)
                except ImportError:
                    # Fallback method
                    state_indices = np.argmin(
                        np.abs(X_processed - np.mean(X_processed, axis=0, keepdims=True)), 
                        axis=1
                    ) % self.decision_process.num_states
            else:
                # Simple binning for 1D data
                bins = np.linspace(
                    np.min(X_processed), 
                    np.max(X_processed), 
                    self.decision_process.num_states + 1
                )
                state_indices = np.digitize(X_processed.ravel(), bins) - 1
                state_indices = np.clip(state_indices, 0, self.decision_process.num_states - 1)
            
            # Get actions for each state
            predictions = np.array([
                self.decision_process.suggest_action(int(state_idx)) 
                for state_idx in state_indices
            ])
            
        else:  # classifier or regressor
            # Extract features
            if self.config['feature_extraction']['use_quantum_features'] and self.feature_map is not None:
                X_features = self.feature_map.transform(
                    X_processed, 
                    output_dim=self.config['feature_extraction'].get('output_dim')
                )
            else:
                X_features = X_processed
            
            # Make predictions with classical model
            if self.classical_model is not None:
                predictions = self.classical_model.predict(X_features)
            else:
                logger.error("No fitted model available for predictions")
                predictions = np.zeros(len(X_processed))
        
        # Record execution
        execution_time = time.time() - start_time
        self.execution_history.append({
            'operation': 'predict',
            'timestamp': datetime.now().isoformat(),
            'data_shape': X.shape,
            'execution_time_seconds': execution_time,
            'model_type': model_type
        })
        
        logger.info(f"Prediction completed in {execution_time:.2f} seconds")
        return predictions
    
    def optimize_quantum_policy(self, 
                              transitions: Optional[np.ndarray] = None, 
                              rewards: Optional[np.ndarray] = None,
                              max_iterations: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Optimize a quantum stochastic decision policy.
        
        Args:
            transitions: Optional transition probability matrix
            rewards: Optional reward matrix
            max_iterations: Maximum iterations for policy optimization
        
        Returns:
            Tuple of (policy, value_function)
        """
        if self.config['model']['type'] != 'decision':
            logger.error("Policy optimization is only available for decision models")
            return None, None
        
        if self.decision_process is None:
            self._setup_decision_process()
        
        # Set transition and reward matrices if provided
        if transitions is not None:
            self.decision_process.set_transition_probabilities(transitions)
        
        if rewards is not None:
            self.decision_process.set_rewards(rewards)
        
        # Run policy iteration
        start_time = time.time()
        policy, value_function = self.decision_process.quantum_policy_iteration(
            max_iterations=max_iterations
        )
        
        # Record execution
        execution_time = time.time() - start_time
        self.execution_history.append({
            'operation': 'optimize_policy',
            'timestamp': datetime.now().isoformat(),
            'execution_time_seconds': execution_time,
            'iterations': max_iterations
        })
        
        logger.info(f"Policy optimization completed in {execution_time:.2f} seconds")
        return policy, value_function
    
    def quantify_uncertainty(self, 
                           X: np.ndarray) -> List[Dict[str, float]]:
        """
        Quantify uncertainty in predictions using quantum methods.
        
        Args:
            X: Input data array
        
        Returns:
            List of uncertainty metrics for each input
        """
        # Preprocess data
        X_processed = self._preprocess_data(X)
        
        # Get model type
        model_type = self.config['model']['type']
        
        uncertainty_metrics = []
        
        if model_type == 'decision' and self.decision_process is not None:
            # Convert inputs to state indices (similar to predict method)
            if X_processed.ndim > 1 and X_processed.shape[1] > 1:
                # Use clustering to map inputs to states
                try:
                    from sklearn.cluster import KMeans
                    kmeans = KMeans(n_clusters=self.decision_process.num_states)
                    state_indices = kmeans.fit_predict(X_processed)
                except ImportError:
                    # Fallback method
                    state_indices = np.argmin(
                        np.abs(X_processed - np.mean(X_processed, axis=0, keepdims=True)), 
                        axis=1
                    ) % self.decision_process.num_states
            else:
                # Simple binning for 1D data
                bins = np.linspace(
                    np.min(X_processed), 
                    np.max(X_processed), 
                    self.decision_process.num_states + 1
                )
                state_indices = np.digitize(X_processed.ravel(), bins) - 1
                state_indices = np.clip(state_indices, 0, self.decision_process.num_states - 1)
            
            # Get uncertainty metrics for each state
            for state_idx in state_indices:
                metrics = self.decision_process.uncertainty_quantification(int(state_idx))
                uncertainty_metrics.append(metrics)
            
        elif model_type in ['classifier', 'regressor'] and self.classical_model is not None:
            # Use quantum feature map for uncertainty estimation if available
            if self.config['feature_extraction']['use_quantum_features'] and self.feature_map is not None:
                # Generate multiple feature representations with variations
                ensemble_predictions = []
                
                # Temporarily reduce number of trajectories for speed
                original_trajectories = self.feature_map.num_trajectories
                self.feature_map.num_trajectories = max(100, original_trajectories // 5)
                
                # Generate 10 different feature representations
                for _ in range(10):
                    # Add small random noise to input to simulate uncertainty
                    X_noisy = X_processed + np.random.normal(0, 0.05, X_processed.shape)
                    
                    # Extract features
                    X_features = self.feature_map.transform(
                        X_noisy, 
                        output_dim=self.config['feature_extraction'].get('output_dim')
                    )
                    
                    # Make predictions
                    if hasattr(self.classical_model, 'predict_proba'):
                        preds = self.classical_model.predict_proba(X_features)
                        if preds.shape[1] == 2:  # Binary classification
                            preds = preds[:, 1]  # Use probability of positive class
                    else:
                        preds = self.classical_model.predict(X_features)
                    
                    ensemble_predictions.append(preds)
                
                # Restore original number of trajectories
                self.feature_map.num_trajectories = original_trajectories
                
                # Calculate uncertainty metrics
                ensemble_predictions = np.array(ensemble_predictions)
                
                for i in range(len(X_processed)):
                    metrics = {
                        'mean': np.mean(ensemble_predictions[:, i]),
                        'std': np.std(ensemble_predictions[:, i]),
                        'min': np.min(ensemble_predictions[:, i]),
                        'max': np.max(ensemble_predictions[:, i]),
                        'range': np.max(ensemble_predictions[:, i]) - np.min(ensemble_predictions[:, i])
                    }
                    uncertainty_metrics.append(metrics)
            else:
                # Simple placeholder for models without quantum features
                for _ in range(len(X_processed)):
                    uncertainty_metrics.append({
                        'uncertainty': 0.5,  # Default value
                        'note': 'Quantum uncertainty quantification not available'
                    })
        else:
            # Default uncertainty for unsupported model types
            for _ in range(len(X_processed)):
                uncertainty_metrics.append({
                    'uncertainty': 0.5,  # Default value
                    'note': 'Uncertainty quantification not supported for this model type'
                })
        
        logger.info(f"Generated uncertainty metrics for {len(X_processed)} inputs")
        return uncertainty_metrics
    
    def save(self, filepath: Optional[str] = None):
        """
        Save the pipeline to a file.
        
        Args:
            filepath: Path to save the pipeline (default: in output_dir)
        """
        if filepath is None:
            filepath = os.path.join(self.output_dir, f"pipeline_{self.pipeline_id}.pkl")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create a deep copy of the pipeline without unpicklable objects
        pipeline_data = {
            'config': self.config,
            'pipeline_id': self.pipeline_id,
            'creation_time': self.creation_time,
            'last_run_time': self.last_run_time,
            'execution_history': self.execution_history
        }
        
        # Save pipeline metadata
        with open(filepath + '.json', 'w') as f:
            json.dump(pipeline_data, f, indent=2)
        
        # Save individual components separately
        if self.feature_map is not None:
            feature_map_path = os.path.join(os.path.dirname(filepath), f"feature_map_{self.pipeline_id}.npz")
            self.feature_map.save_model(feature_map_path)
        
        if self.generator is not None:
            generator_path = os.path.join(os.path.dirname(filepath), f"generator_{self.pipeline_id}.npz")
            self.generator.save_model(generator_path)
        
        if self.decision_process is not None:
            decision_path = os.path.join(os.path.dirname(filepath), f"decision_{self.pipeline_id}.npz")
            self.decision_process.save_model(decision_path)
        
        if self.classical_model is not None:
            try:
                model_path = os.path.join(os.path.dirname(filepath), f"classical_model_{self.pipeline_id}.pkl")
                with open(model_path, 'wb') as f:
                    pickle.dump(self.classical_model, f)
            except Exception as e:
                logger.warning(f"Could not save classical model: {e}")
        
        logger.info(f"Pipeline saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'HybridStochasticPipeline':
        """
        Load a pipeline from a file.
        
        Args:
            filepath: Path to the saved pipeline
        
        Returns:
            Loaded HybridStochasticPipeline instance
        """
        # Load pipeline metadata
        with open(filepath + '.json', 'r') as f:
            pipeline_data = json.load(f)
        
        # Create new pipeline instance
        pipeline = cls(
            pipeline_config=pipeline_data['config'],
            output_dir=os.path.dirname(filepath)
        )
        
        # Restore metadata
        pipeline.pipeline_id = pipeline_data['pipeline_id']
        pipeline.creation_time = pipeline_data['creation_time']
        pipeline.last_run_time = pipeline_data['last_run_time']
        pipeline.execution_history = pipeline_data['execution_history']
        
        # Load individual components if they exist
        feature_map_path = os.path.join(os.path.dirname(filepath), f"feature_map_{pipeline.pipeline_id}.npz")
        if os.path.exists(feature_map_path):
            pipeline.feature_map = StochasticQuantumFeatureMap.load_model(feature_map_path)
        
        generator_path = os.path.join(os.path.dirname(filepath), f"generator_{pipeline.pipeline_id}.npz")
        if os.path.exists(generator_path):
            pipeline.generator = StochasticQuantumGenerator.load_model(generator_path)
        
        decision_path = os.path.join(os.path.dirname(filepath), f"decision_{pipeline.pipeline_id}.npz")
        if os.path.exists(decision_path):
            pipeline.decision_process = QuantumStochasticDecisionProcess.load_model(decision_path)
        
        model_path = os.path.join(os.path.dirname(filepath), f"classical_model_{pipeline.pipeline_id}.pkl")
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    pipeline.classical_model = pickle.load(f)
            except Exception as e:
                logger.warning(f"Could not load classical model: {e}")
        
        logger.info(f"Pipeline loaded from {filepath}")
        return pipeline
    
    def get_pipeline_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the pipeline.
        
        Returns:
            Dictionary with pipeline summary information
        """
        return {
            'pipeline_id': self.pipeline_id,
            'creation_time': self.creation_time,
            'last_run_time': self.last_run_time,
            'model_type': self.config['model']['type'],
            'components': {
                'feature_map': self.feature_map is not None,
                'generator': self.generator is not None,
                'decision_process': self.decision_process is not None,
                'classical_model': self.classical_model is not None
            },
            'execution_history': self.execution_history
        } 