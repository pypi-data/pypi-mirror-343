"""
Stochastic Quantum Generator

This module implements the StochasticQuantumGenerator class, which integrates
stochastic quantum methods with generative AI models to enhance sample quality
and diversity.
"""

import numpy as np
import logging
from typing import List, Dict, Tuple, Any, Optional, Callable, Union
import time
from pathlib import Path
import os
import sys

# Canonical import path post-refactor (April 2025): always use absolute import for clarity and reliability
from src.quantum_finance.quantum_toolkit.stochastic.stochastic_quantum_simulator import StochasticQuantumSimulator, Trajectory, ConfigurationPoint
from src.quantum_finance.quantum_toolkit.stochastic.stochastic_quantum_circuit import StochasticQuantumCircuit, StochasticQuantumState

# Configure logging
logger = logging.getLogger(__name__)

class StochasticQuantumGenerator:
    """
    Integrates stochastic quantum methods with generative AI.
    
    This class enhances generative AI models by leveraging quantum stochastic
    processes to improve sample quality and diversity.
    """
    
    def __init__(self, 
                 config_space_dim: int, 
                 latent_dim: int = 10,
                 num_trajectories: int = 1000,
                 dt: float = 0.01,
                 hbar: float = 1.0,
                 mass: float = 1.0,
                 seed: Optional[int] = None,
                 device: str = 'cpu'):
        """
        Initialize the stochastic quantum generator.
        
        Args:
            config_space_dim: Dimension of the configuration space
            latent_dim: Dimension of the latent space for generative models
            num_trajectories: Number of stochastic trajectories to use
            dt: Time step for stochastic evolution
            hbar: Planck's constant (reduced)
            mass: Particle mass
            seed: Random seed for reproducibility
            device: Computation device ('cpu' or 'cuda')
        """
        self.config_space_dim = config_space_dim
        self.latent_dim = latent_dim
        self.num_trajectories = num_trajectories
        self.dt = dt
        self.hbar = hbar
        self.mass = mass
        self.seed = seed
        self.device = device
        
        # Initialize the stochastic quantum simulator
        self.simulator = StochasticQuantumSimulator(
            config_space_dim=config_space_dim,
            num_trajectories=num_trajectories,
            dt=dt,
            hbar=hbar,
            mass=mass,
            seed=seed
        )
        
        # Parameters for the diffusion model
        self.diffusion_steps = 100
        self.beta_schedule = np.linspace(0.0001, 0.02, self.diffusion_steps)
        self.alpha = 1.0 - self.beta_schedule
        self.alpha_cumprod = np.cumprod(self.alpha)
        
        # Model parameters that will be optimized
        self.drift_parameters = np.random.randn(latent_dim, config_space_dim) * 0.01
        self.diffusion_parameters = np.random.randn(latent_dim, config_space_dim) * 0.01
        
        logger.info(f"Initialized StochasticQuantumGenerator with {num_trajectories} trajectories")
    
    def encode_latent_to_quantum(self, latent_vectors: np.ndarray) -> List[np.ndarray]:
        """
        Encode latent vectors from generative models into quantum states.
        
        Args:
            latent_vectors: Batch of latent vectors from generative model
                            Shape: (batch_size, latent_dim)
        
        Returns:
            List of encoded quantum states as configuration space points
        """
        batch_size = latent_vectors.shape[0]
        quantum_states = []
        
        for i in range(batch_size):
            # Project latent vector to configuration space
            config_point = np.dot(latent_vectors[i], self.drift_parameters)
            quantum_states.append(config_point)
            
        logger.debug(f"Encoded {batch_size} latent vectors to quantum states")
        return quantum_states
    
    def quantum_stochastic_diffusion(self, 
                                   initial_states: List[np.ndarray], 
                                   time_steps: int,
                                   conditional_data: Optional[np.ndarray] = None) -> List[Trajectory]:
        """
        Apply quantum stochastic diffusion to initial states.
        
        Args:
            initial_states: List of initial configuration space points
            time_steps: Number of diffusion time steps
            conditional_data: Optional conditioning data for guided generation
        
        Returns:
            List of stochastic trajectories
        """
        trajectories = []
        
        # Define drift and diffusion coefficients based on model parameters
        def drift_coefficient(x, t, conditional=None):
            # Time-dependent drift adjusted by conditional data if provided
            drift = -0.5 * x  # Base drift for diffusion model
            
            if conditional is not None:
                # Modify drift based on conditional data
                drift_adjustment = np.dot(conditional, self.drift_parameters)
                t_factor = 1.0 - t / time_steps  # Time-dependent factor
                drift += t_factor * drift_adjustment
                
            return drift
        
        def diffusion_coefficient(x, t, conditional=None):
            # Base diffusion coefficient from beta schedule
            t_idx = min(int(t / time_steps * len(self.beta_schedule)), len(self.beta_schedule) - 1)
            base_diffusion = np.sqrt(self.beta_schedule[t_idx])
            
            if conditional is not None:
                # Modify diffusion based on conditional data
                diff_adjustment = np.abs(np.dot(conditional, self.diffusion_parameters))
                t_factor = t / time_steps  # Time-dependent factor
                # Ensure diffusion remains positive
                adjusted_diffusion = base_diffusion * (1.0 + t_factor * diff_adjustment)
                return adjusted_diffusion
                
            return base_diffusion * np.ones_like(x)
        
        # Process each initial state
        for i, init_state in enumerate(initial_states):
            conditional = None if conditional_data is None else conditional_data[i]
            
            # Create custom potential function for this trajectory
            def potential_func(x):
                t = self.simulator.current_time
                t_normalized = min(t / (time_steps * self.dt), 1.0)
                drift = drift_coefficient(x, t_normalized * time_steps, conditional)
                return 0.5 * np.sum(drift ** 2)  # Potential related to drift
            
            # Evolve the stochastic process
            trajectory = self.simulator.evolve_stochastic_process(
                initial_state=init_state,
                steps=time_steps,
                potential_func=potential_func,
                drift_func=lambda x, t: drift_coefficient(x, t, conditional),
                diffusion_func=lambda x, t: diffusion_coefficient(x, t, conditional)
            )
            
            trajectories.extend(trajectory)
            
        logger.info(f"Generated {len(trajectories)} stochastic quantum trajectories")
        return trajectories
    
    def decode_trajectories_to_samples(self, 
                                     trajectories: List[Trajectory], 
                                     output_dim: int) -> np.ndarray:
        """
        Convert stochastic quantum trajectories to output samples.
        
        Args:
            trajectories: List of stochastic trajectories
            output_dim: Dimension of the output samples
        
        Returns:
            Array of generated samples
        """
        # Extract final states from trajectories
        final_states = []
        for traj in trajectories:
            if traj.points:  # Ensure the trajectory has points
                final_states.append(traj.points[-1].configuration)
        
        if not final_states:
            logger.warning("No valid trajectories to decode")
            return np.array([])
        
        # Convert to numpy array
        final_states_array = np.array(final_states)
        
        # If output dimension matches configuration space dimension, return as is
        if output_dim == self.config_space_dim:
            return final_states_array
        
        # Otherwise, project to output dimension
        # This is a simple linear projection; more complex decoders could be used
        projection_matrix = np.random.randn(self.config_space_dim, output_dim)
        projected_samples = np.dot(final_states_array, projection_matrix)
        
        # Apply activation function (tanh for bounded outputs)
        samples = np.tanh(projected_samples)
        
        logger.debug(f"Decoded {len(trajectories)} trajectories to {samples.shape} samples")
        return samples
    
    def generate_samples(self, 
                       num_samples: int, 
                       output_dim: int,
                       conditional_data: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Generate samples using the stochastic quantum generator.
        
        Args:
            num_samples: Number of samples to generate
            output_dim: Dimension of the output samples
            conditional_data: Optional conditioning data for guided generation
        
        Returns:
            Array of generated samples
        """
        # Generate random latent vectors
        latent_vectors = np.random.randn(num_samples, self.latent_dim)
        
        # Encode latent vectors to quantum states
        initial_states = self.encode_latent_to_quantum(latent_vectors)
        
        # Apply quantum stochastic diffusion
        trajectories = self.quantum_stochastic_diffusion(
            initial_states=initial_states,
            time_steps=self.diffusion_steps,
            conditional_data=conditional_data
        )
        
        # Decode trajectories to samples
        samples = self.decode_trajectories_to_samples(trajectories, output_dim)
        
        logger.info(f"Generated {len(samples)} samples with dimension {output_dim}")
        return samples
    
    def update_parameters(self, 
                        grad_drift: np.ndarray,
                        grad_diffusion: np.ndarray,
                        learning_rate: float = 0.001):
        """
        Update the model parameters based on gradients.
        
        Args:
            grad_drift: Gradient for drift parameters
            grad_diffusion: Gradient for diffusion parameters
            learning_rate: Learning rate for parameter updates
        """
        self.drift_parameters -= learning_rate * grad_drift
        self.diffusion_parameters -= learning_rate * grad_diffusion
        
        logger.debug("Updated model parameters")
    
    def save_model(self, filepath: str):
        """
        Save the generator model to a file.
        
        Args:
            filepath: Path to save the model
        """
        model_data = {
            'config_space_dim': self.config_space_dim,
            'latent_dim': self.latent_dim,
            'num_trajectories': self.num_trajectories,
            'dt': self.dt,
            'hbar': self.hbar,
            'mass': self.mass,
            'seed': self.seed,
            'diffusion_steps': self.diffusion_steps,
            'beta_schedule': self.beta_schedule,
            'drift_parameters': self.drift_parameters,
            'diffusion_parameters': self.diffusion_parameters
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model
        np.savez(filepath, **model_data)
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load_model(cls, filepath: str) -> 'StochasticQuantumGenerator':
        """
        Load a generator model from a file.
        
        Args:
            filepath: Path to the saved model
        
        Returns:
            Loaded StochasticQuantumGenerator instance
        """
        model_data = np.load(filepath)
        
        # Create instance with saved parameters
        generator = cls(
            config_space_dim=model_data['config_space_dim'],
            latent_dim=model_data['latent_dim'],
            num_trajectories=model_data['num_trajectories'],
            dt=model_data['dt'],
            hbar=model_data['hbar'],
            mass=model_data['mass'],
            seed=model_data['seed']
        )
        
        # Restore additional parameters
        generator.diffusion_steps = model_data['diffusion_steps']
        generator.beta_schedule = model_data['beta_schedule']
        generator.drift_parameters = model_data['drift_parameters']
        generator.diffusion_parameters = model_data['diffusion_parameters']
        
        logger.info(f"Model loaded from {filepath}")
        return generator 