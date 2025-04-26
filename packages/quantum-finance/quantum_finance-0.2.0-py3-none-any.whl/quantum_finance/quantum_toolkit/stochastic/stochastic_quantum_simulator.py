"""
Stochastic Quantum Simulator Implementation

This module implements the StochasticQuantumSimulator class, which forms the
foundation of our stochastic quantum methods approach based on Barandes' framework.
"""

import numpy as np
import logging
from typing import List, Dict, Tuple, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from scipy.stats import norm
from scipy.spatial.distance import pdist, squareform
import time
import copy # Import the copy module

# Import adaptive phase tracking components
from ..phase_tracking.adaptive_phase_tracker import AdaptivePhaseTracker, StateEstimate

logger = logging.getLogger(__name__)

@dataclass
class ConfigurationPoint:
    """Represents a point in configuration space with associated time."""
    configuration: np.ndarray
    time: float
    phase: float = 0.0
    coherence: float = 1.0  # Added coherence parameter for phase stability
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(0))

@dataclass
class Trajectory:
    """Represents a stochastic trajectory in configuration space."""
    points: List[ConfigurationPoint]
    weight: float = 1.0
    id: int = 0
    neighbors: List[int] = field(default_factory=list)  # Store indices of neighboring trajectories for phase coherence

class StochasticQuantumSimulator:
    """
    Simulator implementing Barandes' stochastic quantum approach.
    Maintains compatibility with existing quantum systems while
    adding stochastic process capabilities.
    """
    
    def __init__(self, 
                config_space_dim: int, 
                num_trajectories: int = 1000,
                dt: float = 0.01,
                hbar: float = 1.0,
                mass: float = 1.0,
                quantum_potential_strength: float = 1.0,
                seed: Optional[int] = None,
                phase_coherence_strength: float = 0.05,  # Added parameter for phase coherence strength
                adaptive_neighbor_count: int = 10,      # Adaptive number of neighbors to consider
                neighbor_update_interval: int = 10):    # How often to update neighbors (steps)
        """
        Initialize the stochastic quantum simulator.
        
        Args:
            config_space_dim: Dimensionality of configuration space
            num_trajectories: Number of stochastic trajectories to simulate
            dt: Time step for stochastic evolution
            hbar: Reduced Planck's constant (set to 1.0 by default)
            mass: Mass parameter (set to 1.0 by default)
            quantum_potential_strength: Strength of quantum potential term
            seed: Random seed for reproducibility
            phase_coherence_strength: Strength of phase coherence between trajectories
            adaptive_neighbor_count: Number of neighbors to consider for phase coherence
            neighbor_update_interval: Frequency (in steps) for recalculating trajectory neighbors.
        """
        self.config_space_dim = config_space_dim
        self.num_trajectories = num_trajectories
        self.dt = dt
        self.hbar = hbar
        self.mass = mass
        self.quantum_potential_strength = quantum_potential_strength
        self.phase_coherence_strength = phase_coherence_strength
        self.adaptive_neighbor_count = min(adaptive_neighbor_count, num_trajectories - 1)
        self.trajectories: List[Trajectory] = []
        self.neighbor_update_interval = neighbor_update_interval
        
        # Create a local random number generator instance
        self.rng = np.random.RandomState(seed)
            
        logger.info(f"Initialized StochasticQuantumSimulator with {config_space_dim}D configuration space, "
                   f"{num_trajectories} trajectories, phase coherence strength {phase_coherence_strength}")
        logger.info(f"Neighbor update interval set to {self.neighbor_update_interval} steps")
    
    def evolve_stochastic_process(self, 
                                 initial_state: np.ndarray,
                                 steps: int,
                                 potential_func: Optional[Callable[[np.ndarray], float]] = None,
                                 drift_func: Optional[Callable[[np.ndarray, float], np.ndarray]] = None) -> List[Trajectory]:
        """
        Evolves the stochastic process in configuration space.
        
        Args:
            initial_state: Initial configuration
            steps: Number of evolution steps
            potential_func: Optional classical potential function V(x)
            drift_func: Optional additional drift function
            
        Returns:
            List of configuration space trajectories
            
        Raises:
            ValueError: If initial_state dimensions don't match config_space_dim
        """
        # Validate initial state dimensions
        if len(initial_state) != self.config_space_dim:
            raise ValueError(f"Initial state dimension {len(initial_state)} does not match configuration space dimension {self.config_space_dim}")
            
        logger.info(f"Evolving stochastic process for {steps} steps")
        start_time = time.time()
        
        # Initialize trajectories
        self.trajectories = []
        
        # Create initial configurations centered around initial_state
        # with Gaussian spread
        sigma = np.sqrt(self.hbar * self.dt / (2 * self.mass))
        
        for i in range(self.num_trajectories):
            # Sample initial configuration from Gaussian distribution
            config = initial_state + sigma * self.rng.randn(self.config_space_dim)
            
            # Create initial configuration point
            point = ConfigurationPoint(
                configuration=config,
                time=0.0
            )
            
            # Create trajectory
            trajectory = Trajectory(
                points=[point],
                weight=1.0 / self.num_trajectories,
                id=i
            )
            
            self.trajectories.append(trajectory)
        
        # Initialize neighbor relationships for phase coherence
        self._initialize_trajectory_neighbors()
        
        # Evolve each trajectory
        for step in range(1, steps + 1):
            current_time = step * self.dt
            
            # Periodically update neighbor relationships based on current positions
            # Ensures coherence is calculated with relevant nearby trajectories
            if step > 0 and step % self.neighbor_update_interval == 0:
                self._update_trajectory_neighbors()
            
            # Get current configurations for all trajectories
            current_configs = [traj.points[-1].configuration for traj in self.trajectories]
            
            # Calculate quantum potential if no drift function provided
            quantum_force = np.zeros((self.num_trajectories, self.config_space_dim))
            
            if drift_func is None:
                quantum_potentials = self._calculate_quantum_potential(current_configs)
                
                # Calculate quantum force from quantum potential
                for i, config in enumerate(current_configs):
                    # Simple finite difference approximation of gradient
                    for dim in range(self.config_space_dim):
                        h = 0.01  # Small step for numerical gradient
                        
                        # Forward point
                        forward_config = config.copy()
                        forward_config[dim] += h
                        forward_configs = current_configs.copy()
                        forward_configs[i] = forward_config
                        forward_potential = self._calculate_quantum_potential(forward_configs)[i]
                        
                        # Backward point
                        backward_config = config.copy()
                        backward_config[dim] -= h
                        backward_configs = current_configs.copy()
                        backward_configs[i] = backward_config
                        backward_potential = self._calculate_quantum_potential(backward_configs)[i]
                        
                        # Gradient (central difference)
                        quantum_force[i, dim] = -(forward_potential - backward_potential) / (2 * h)
            
            # Update phase coherence between trajectories
            self._update_phase_coherence()
            
            # Evolve each trajectory
            for i, trajectory in enumerate(self.trajectories):
                current_config = trajectory.points[-1].configuration
                
                # Calculate drift term
                if drift_func is not None:
                    drift = drift_func(current_config, current_time)
                else:
                    # Use quantum force as drift
                    drift = quantum_force[i]
                
                # Calculate potential force if potential function provided
                if potential_func is not None:
                    # Simple numerical gradient of potential
                    potential_force = np.zeros(self.config_space_dim)
                    for dim in range(self.config_space_dim):
                        h = 0.001  # Smaller step for better numerical accuracy
                        
                        # Forward point
                        forward_config = current_config.copy()
                        forward_config[dim] += h
                        forward_potential = potential_func(forward_config)
                        
                        # Backward point
                        backward_config = current_config.copy()
                        backward_config[dim] -= h
                        backward_potential = potential_func(backward_config)
                        
                        # Gradient (central difference)
                        potential_force[dim] = -(forward_potential - backward_potential) / (2 * h)
                    
                    # Scale potential force by mass
                    force = potential_force
                else:
                    force = np.zeros(self.config_space_dim)
                
                # Get current velocity (from previous step if available)
                if len(trajectory.points) > 1:
                    current_velocity = (current_config - trajectory.points[-2].configuration) / self.dt
                else:
                    current_velocity = np.zeros(self.config_space_dim)
                
                # Deterministic evolution using velocity Verlet
                # First half-step velocity update
                half_velocity = current_velocity + 0.5 * (force / self.mass) * self.dt
                
                # Full position update
                new_config = current_config + half_velocity * self.dt
                
                # Calculate new force at updated position
                if potential_func is not None:
                    new_force = np.zeros(self.config_space_dim)
                    for dim in range(self.config_space_dim):
                        h = 0.001
                        forward_config = new_config.copy()
                        forward_config[dim] += h
                        forward_potential = potential_func(forward_config)
                        
                        backward_config = new_config.copy()
                        backward_config[dim] -= h
                        backward_potential = potential_func(backward_config)
                        
                        new_force[dim] = -(forward_potential - backward_potential) / (2 * h)
                else:
                    new_force = np.zeros(self.config_space_dim)
                
                # Second half-step velocity update
                final_velocity = half_velocity + 0.5 * (new_force / self.mass) * self.dt
                
                # Store deterministic position and velocity
                deterministic_config = new_config.copy()
                deterministic_velocity = final_velocity.copy()
                
                # Stochastic evolution using Ornstein-Uhlenbeck process
                # This preserves the quantum uncertainty while maintaining energy conservation
                gamma = 0.1  # Friction coefficient for energy dissipation
                noise = self.rng.randn(self.config_space_dim)
                diffusion = np.sqrt(2 * gamma * self.hbar / self.mass)
                
                # Update position and velocity with stochastic terms
                stochastic_velocity = diffusion * np.sqrt(self.dt) * noise
                new_config = deterministic_config + 0.5 * stochastic_velocity * self.dt
                
                # Get the phase and coherence from the *last added point*
                current_phase = trajectory.points[-1].phase
                current_coherence = trajectory.points[-1].coherence
                
                # Store the final configuration
                new_point = ConfigurationPoint(
                    configuration=new_config,
                    time=current_time,
                    phase=current_phase,
                    coherence=current_coherence,
                    velocity=deterministic_velocity + stochastic_velocity  # Store total velocity for next step
                )
                
                # Add to trajectory
                trajectory.points.append(new_point)
        
        logger.info(f"Stochastic process evolution completed in {time.time() - start_time:.2f} seconds")
        return self.trajectories
    
    def _initialize_trajectory_neighbors(self) -> None:
        """
        Initialize neighbor relationships between trajectories based on initial configurations.
        """
        if len(self.trajectories) <= 1:
            return
            
        # Get initial configurations
        configs = np.array([traj.points[0].configuration for traj in self.trajectories])
        
        # Calculate pairwise distances
        dists = squareform(pdist(configs))
        
        # For each trajectory, find k nearest neighbors
        k = min(self.adaptive_neighbor_count + 1, len(self.trajectories))
        for i, trajectory in enumerate(self.trajectories):
            # Get indices of k nearest neighbors (including self)
            neighbor_indices = np.argsort(dists[i])[:k]
            # Exclude self
            neighbor_indices = [int(idx) for idx in neighbor_indices if idx != i]
            
            trajectory.neighbors = neighbor_indices
            
        logger.debug(f"Initialized trajectory neighbor relationships with {self.adaptive_neighbor_count} neighbors per trajectory")
    
    def _update_trajectory_neighbors(self) -> None:
        """
        Recalculate neighbor relationships between trajectories based on their current configurations.
        Called periodically during evolution to adapt to trajectory movement.
        """
        if len(self.trajectories) <= 1:
            return
            
        # Get current configurations (using the latest point in each trajectory)
        try:
            configs = np.array([traj.points[-1].configuration for traj in self.trajectories])
        except IndexError:
            logger.warning("_update_trajectory_neighbors called with empty trajectory points.")
            return
        
        if configs.ndim == 1: # Handle case with only one dimension
             configs = configs.reshape(-1, 1)
             
        # Ensure configuration dimensions match before calculating distance
        if configs.shape[1] != self.config_space_dim:
             logger.error(f"Mismatch in configuration dimensions. Expected {self.config_space_dim}, got {configs.shape[1]}")
             # Fallback: use initial neighbors if current configurations are inconsistent
             # This prevents crashes but indicates a potential deeper issue
             self._initialize_trajectory_neighbors() 
             return

        # Calculate pairwise distances
        try:
            dists = squareform(pdist(configs))
        except ValueError as e:
            logger.error(f"Error calculating pdist in _update_trajectory_neighbors: {e}. Configs shape: {configs.shape}")
            # Fallback if pdist fails
            self._initialize_trajectory_neighbors()
            return

        # For each trajectory, find k nearest neighbors
        k = min(self.adaptive_neighbor_count + 1, len(self.trajectories))
        for i, trajectory in enumerate(self.trajectories):
            # Get indices of k nearest neighbors (including self)
            neighbor_indices = np.argsort(dists[i])[:k]
            # Exclude self
            neighbor_indices = [int(idx) for idx in neighbor_indices if idx != i]
            
            trajectory.neighbors = neighbor_indices
            
        logger.debug(f"Updated trajectory neighbor relationships based on current positions")
    
    def _update_phase_coherence(self) -> None:
        """
        Update phase coherence between trajectories to maintain quantum interference effects.
        Uses adaptive phase relationships between neighboring trajectories.
        """
        if not self.trajectories or len(self.trajectories) <= 1:
            return
            
        # Get current phases for all trajectories
        current_phases = np.array([traj.points[-1].phase for traj in self.trajectories])
        
        # Update coherence for each trajectory based on its neighbors
        for i, trajectory in enumerate(self.trajectories):
            if not trajectory.neighbors:
                continue
                
            # Get phases of neighbors
            neighbor_phases = current_phases[trajectory.neighbors]
            
            # Calculate phase difference (considering circular nature of phases)
            phase_diff = neighbor_phases - current_phases[i]
            phase_diff = np.mod(phase_diff + np.pi, 2 * np.pi) - np.pi
            
            # Calculate squared distances to neighbors
            neighbor_configs = np.array([self.trajectories[j].points[-1].configuration for j in trajectory.neighbors])
            current_config = trajectory.points[-1].configuration
            sq_distances = np.sum((neighbor_configs - current_config)**2, axis=1)

            # Adaptive scale for weights: Use half the average squared distance to neighbors
            # Add epsilon to prevent division by zero if all neighbors are at the same point
            adaptive_scale_sq = 0.5 * np.mean(sq_distances) + 1e-10 

            # Calculate weights using adaptive scale
            # Closer neighbors relative to the average distance have more influence
            weights = np.exp(-0.5 * sq_distances / adaptive_scale_sq)

            # Normalize weights
            weights = weights / (np.sum(weights) + 1e-10)

            # Apply weighted phase correction
            phase_correction = np.sum(weights * phase_diff) * self.phase_coherence_strength
            new_phase = trajectory.points[-1].phase + phase_correction
            
            # Update the phase for the latest point
            trajectory.points[-1].phase = new_phase
            
            # Update coherence factor based on neighbor agreement (using original phase_diff)
            phase_variance = np.var(phase_diff)
            coherence_factor = np.exp(-phase_variance)
            trajectory.points[-1].coherence = coherence_factor
    
    def _calculate_quantum_potential(self, configs: List[np.ndarray]) -> List[float]:
        """
        Calculate quantum potential term for stochastic process.
        Now with improved phase tracking for better accuracy.
        
        Args:
            configs: List of configuration points
            
        Returns:
            List of quantum potential values
        """
        if len(configs) < 5:
            return [0.0] * len(configs)
        
        # Convert configs to numpy array
        config_array = np.array(configs)
        
        # Estimate density using kernel density estimation
        dists = squareform(pdist(config_array))
        
        # Adaptive bandwidth based on local density
        # This improves accuracy in regions with varying particle density
        local_distances = np.array([np.sort(d)[1:6] for d in dists])  # 5 nearest neighbors
        local_bandwidth = np.mean(local_distances, axis=1) * 1.2  # Slightly wider for stability
        
        # Use Gaussian kernel with adaptive bandwidth
        density = np.zeros(len(configs))
        
        for i in range(len(configs)):
            # Adaptive kernel: uses local bandwidth for each point
            # Add epsilon to prevent division by zero if bandwidth is zero
            weights = np.exp(-0.5 * (dists[i] / (local_bandwidth[i] + 1e-10)) ** 2)
            density[i] = np.sum(weights) / (len(configs) * np.sqrt(2 * np.pi * (local_bandwidth[i]**2 + 1e-10))) # Epsilon also here
        
        # Calculate quantum potential Q = -λ∇²√ρ/√ρ with improved numerical approximation
        quantum_potential = np.zeros(len(configs))
        max_density_val = np.max(density)
        
        for i in range(len(configs)):
            # Find nearest neighbors, adaptive number based on local density
            # Handle potential NaN or zero max_density
            if max_density_val < 1e-10 or np.isnan(density[i]):
                neighbor_count = 5 # Default if density is ill-defined
            else:
                density_ratio = density[i] / max_density_val
                if np.isnan(density_ratio): # Check ratio itself
                    neighbor_count = 5 # Default if ratio is NaN
                else:
                    neighbor_count = max(5, min(10, int(10 * density_ratio)))
            
            idx = np.argsort(dists[i])[1:neighbor_count+1]  # adaptive nearest neighbors
            
            # Get configurations and densities of neighbors
            neighbor_configs = config_array[idx]
            neighbor_densities = density[idx]
            
            # Approximate Laplacian of √ρ with weighted average
            # This improves numerical stability and accuracy
            sqrt_rho = np.sqrt(density[i])
            sqrt_rho_neighbors = np.sqrt(neighbor_densities)
            
            # Calculate weights based on distance (closer points have more influence)
            distance_weights = 1.0 / (dists[i, idx] + 1e-10)
            distance_weights = distance_weights / (np.sum(distance_weights) + 1e-10) # Epsilon here too
            
            # Weighted Laplacian estimate
            # Add epsilon to the denominator here to prevent division by zero
            mean_neighbor_dist = np.mean(dists[i, idx])
            laplacian_est = np.sum(distance_weights * (sqrt_rho_neighbors - sqrt_rho)) / (mean_neighbor_dist + 1e-10)
            
            # Calculate quantum potential with coherence factor if trajectories exist
            coherence_factor = 1.0
            if self.trajectories and len(self.trajectories) > i:
                if self.trajectories[i].points:
                    coherence_factor = getattr(self.trajectories[i].points[-1], 'coherence', 1.0)
            
            # Apply coherence factor to quantum potential
            # Low coherence reduces quantum potential impact (more classical behavior)
            # High coherence maintains quantum effects
            quantum_potential[i] = -self.quantum_potential_strength * coherence_factor * laplacian_est / (sqrt_rho + 1e-10)
        
        # Convert numpy array to list to match return type
        return quantum_potential.tolist()
    
    def convert_to_wave_function(self, 
                                grid_points: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Converts stochastic trajectories to wave function representation
        for compatibility with existing quantum circuits.
        
        Args:
            grid_points: Grid points in configuration space to evaluate wave function
            
        Returns:
            Tuple of (amplitudes, phases) for the reconstructed wave function
        """
        if not self.trajectories:
            raise ValueError("No trajectories to convert. Run evolve_stochastic_process first.")
        
        # Initialize amplitude and phase arrays
        amplitudes = np.zeros(len(grid_points))
        phases = np.zeros(len(grid_points))
        
        # Get final configurations and weights from trajectories
        final_configs = np.array([traj.points[-1].configuration for traj in self.trajectories])
        weights = np.array([traj.weight for traj in self.trajectories])
        final_phases = np.array([traj.points[-1].phase for traj in self.trajectories])
        
        # Get coherence factors if available
        coherence_factors = np.array([getattr(traj.points[-1], 'coherence', 1.0) for traj in self.trajectories])
        
        # Adaptive bandwidth selection based on configuration space density
        median_distance = float(np.median(pdist(final_configs)))
        # Use moderate kernel bandwidth relative to median distance for smoothing
        bandwidth = max(median_distance / 4.0, 1e-6)
        
        for i, grid_point in enumerate(grid_points):
            # Calculate density at this grid point
            deltas = final_configs - grid_point
            sq_distances = np.sum(deltas**2, axis=1)
            
            # Apply kernel with coherence-weighted contributions
            kernel_values = np.exp(-0.5 * sq_distances / (bandwidth**2))
            kernel_values = kernel_values * coherence_factors  # Weight by coherence
            
            # Weight by trajectory weights
            amplitudes[i] = np.sum(kernel_values * weights) / np.sqrt(2 * np.pi * bandwidth**2)
            
            # Estimate phase by coherence-weighted average of nearby trajectories
            if np.sum(kernel_values) > 0:
                # Calculate circular mean to handle phase wrapping correctly
                phases_sin = np.sum(kernel_values * np.sin(final_phases)) / np.sum(kernel_values)
                phases_cos = np.sum(kernel_values * np.cos(final_phases)) / np.sum(kernel_values)
                phases[i] = np.arctan2(phases_sin, phases_cos)
        
        # Normalize amplitudes
        norm = np.sqrt(np.sum(amplitudes**2))
        if norm > 0:
            amplitudes /= norm
        
        return amplitudes, phases
    
    def quantum_stochastic_correspondence(self, 
                                         quantum_state: np.ndarray,
                                         basis_states: np.ndarray) -> List[Trajectory]:
        """
        Implements the stochastic-quantum correspondence described
        in Barandes' research. Converts a quantum state to stochastic trajectories.
        Now with improved phase tracking and adaptive phase relationships.
        
        Args:
            quantum_state: Quantum state as complex amplitudes
            basis_states: Corresponding basis states in configuration space
            
        Returns:
            List of stochastic trajectories
        """
        # Calculate probability density
        probabilities = np.abs(quantum_state)**2
        
        # Normalize if needed
        total_prob = np.sum(probabilities)
        if not np.isclose(total_prob, 1.0):
             if total_prob > 1e-9: # Avoid division by zero for zero state
                 probabilities = probabilities / total_prob
             else:
                 logger.warning("Quantum state appears to be zero vector. Cannot sample trajectories.")
                 self.trajectories = []
                 return []
        
        # Extract phases
        phases = np.angle(quantum_state)
        
        # Create trajectories by sampling from probability distribution
        num_samples = min(len(quantum_state), self.num_trajectories)
        
        # Improved sampling strategy: ensure representation of significant states
        # For states with significant probability, ensure at least one trajectory
        significant_threshold = 1.0 / num_samples
        significant_states = np.where(probabilities > significant_threshold)[0]
        
        # Reserve trajectories for significant states (up to 50% of total)
        reserved_count = min(len(significant_states), num_samples // 2)
        
        if reserved_count > 0:
            # Sample significant states with probability proportional to amplitude
            sig_probs = probabilities[significant_states]
            sig_probs_norm = np.sum(sig_probs)
            if sig_probs_norm > 1e-9:
                 sig_probs = sig_probs / sig_probs_norm
                 reserved_indices = np.random.choice(significant_states, size=reserved_count, p=sig_probs, replace=True)
            else: # Handle cases where significant probabilities sum to near zero
                 reserved_indices = np.random.choice(significant_states, size=reserved_count, replace=True)
                 logger.warning("Sum of significant probabilities is near zero, sampling uniformly from significant states.")

            # Sample remaining states from full distribution
            remaining_count = num_samples - reserved_count
            if remaining_count > 0:
                 remaining_indices = np.random.choice(len(quantum_state), size=remaining_count, p=probabilities, replace=True)
                 # Combine indices
                 indices = np.concatenate([reserved_indices, remaining_indices])
            else:
                 indices = reserved_indices

        else:
            # If no significant states, sample from full distribution
            indices = np.random.choice(len(quantum_state), size=num_samples, p=probabilities, replace=True)
        
        # Create trajectories
        trajectories = []
        for i, idx in enumerate(indices):
            # Get sampled configuration and phase
            config = basis_states[idx]
            phase = phases[idx]
            
            # Initial coherence based on probability - higher probability states
            # have higher initial coherence (more reliable phase information)
            initial_coherence = min(1.0, float(probabilities[idx] * num_samples))
            
            # Create trajectory with a single point (initial condition)
            point = ConfigurationPoint(
                configuration=config,
                time=0.0,
                phase=float(phase),  # Convert to float to match expected type
                coherence=float(initial_coherence)
            )
            
            trajectory = Trajectory(
                points=[point],
                weight=1.0 / num_samples,
                id=i
            )
            
            trajectories.append(trajectory)
        
        # Store trajectories
        self.trajectories = trajectories
        
        # Initialize neighbor relationships after creating trajectories
        if self.trajectories:
            self._initialize_trajectory_neighbors()
            
        logger.info(f"Created {len(self.trajectories)} trajectories via quantum-stochastic correspondence.")
        return trajectories
    
    def integrate_adaptive_phase_tracker(self,
                                        # Add num_particles for PF
                                        num_particles: int = 100,
                                        # process_noise_scale remains the same
                                        process_noise_scale: float = 0.01,
                                        # Rename coherence_measurement_noise -> measurement_noise_scale
                                        measurement_noise_scale: float = 0.1,
                                        use_neighbours: bool = True # Flag to enable coupled mode
                                        ) -> Tuple[List[List[StateEstimate]], float]: # Return List[List[...]]
        """
        Integrate the adaptive phase tracker (now Particle Filter) with the simulator.
        Applies phase estimation step-by-step, optionally using neighbour information.

        Args:
            num_particles: Number of particles for the Particle Filter.
            process_noise_scale: Standard deviation for the Particle Filter process noise (Q).
            measurement_noise_scale: Standard deviation for the Particle Filter measurement noise (R).
            use_neighbours: If True, pass neighbour phases to the tracker for coupled update.

        Returns:
            Tuple of (list of list of state estimates [traj][time], overall avg confidence)
        """
        mode = "Coupled (Neighbours)" if use_neighbours else "Standard (Individual)"
        logger.info(f"Integrating adaptive phase tracker (Particle Filter, N={num_particles}, {mode} mode) "
                    f"with sigma_process={process_noise_scale}, sigma_measurement={measurement_noise_scale}")

        if not self.trajectories or not self.trajectories[0].points:
            raise ValueError("No trajectories or trajectory points available. Run evolution or correspondence first.")

        # Create adaptive phase tracker (now using Particle Filter)
        tracker = AdaptivePhaseTracker(
            num_particles=num_particles,                  # Correct parameter name
            process_noise_scale=process_noise_scale,      # Correct parameter name
            measurement_noise_scale=measurement_noise_scale # Correct parameter name
        )

        num_trajectories = len(self.trajectories)
        if num_trajectories == 0: return [], 0.0
        num_steps = len(self.trajectories[0].points)
        
        start_time = time.time()
        # Store estimates per trajectory, per time step
        all_estimates_history: List[List[StateEstimate]] = [[] for _ in range(num_trajectories)] 
        total_confidence = 0.0
        total_estimates = 0
        
        # Loop through time steps FIRST, then trajectories for better neighbour access
        for j in range(num_steps): # Time step index
            # Store current phases at this time step for neighbour lookup
            current_step_phases = []
            for traj in self.trajectories:
                if j < len(traj.points):
                    current_step_phases.append(traj.points[j].phase)
                else:
                    current_step_phases.append(np.nan) # Handle incomplete trajectories

            for i in range(num_trajectories): # Trajectory index
                if j >= len(self.trajectories[i].points):
                    # Append a default/empty estimate if trajectory ended early
                    all_estimates_history[i].append(StateEstimate(phase=np.nan, confidence=0.0))
                    continue # Skip processing for this trajectory at this step

                # Get the measurement (which is just the current phase before update)
                measurement = [self.trajectories[i].points[j].phase]
                initial_phase_kf = measurement[0] if j == 0 else None

                # Gather neighbour phases if coupled mode is enabled
                neighbour_phases_for_kf: Optional[List[float]] = None
                if use_neighbours:
                    neighbour_indices = self.trajectories[i].neighbors
                    neighbour_phases_for_kf = []
                    for neighbour_idx in neighbour_indices:
                        if 0 <= neighbour_idx < num_trajectories and neighbour_idx != i:
                            # Get neighbour phase *at the current time step j*
                            if j < len(self.trajectories[neighbour_idx].points):
                                neigh_phase = current_step_phases[neighbour_idx]
                                if not np.isnan(neigh_phase):
                                    neighbour_phases_for_kf.append(neigh_phase)
                            else:
                                logger.warning(f"Neighbour {neighbour_idx} shorter than step {j}")
                        else:
                            logger.warning(f"Invalid neighbour index {neighbour_idx} for trajectory {i}")
                    if not neighbour_phases_for_kf: # Avoid passing empty list if no valid neighbours found
                        neighbour_phases_for_kf = None

                # Process this step for trajectory i using the tracker
                try:
                    # estimate_phase updates the tracker's internal state and returns the estimate
                    # We pass neighbour phases only if use_neighbours is True and we found valid ones
                    current_step_estimate = tracker.estimate_phase(
                        measurement_data=measurement, 
                        initial_phase=initial_phase_kf, 
                        neighbour_phases=neighbour_phases_for_kf if use_neighbours else None
                    )
                    # Store a *copy* of the estimate for this traj/step
                    estimate_copy = StateEstimate(
                        phase=current_step_estimate.phase,
                        amplitude=current_step_estimate.amplitude,
                        confidence=current_step_estimate.confidence
                    )
                    all_estimates_history[i].append(estimate_copy)

                    # --- Update the trajectory point in-place --- 
                    old_phase = self.trajectories[i].points[j].phase
                    new_phase = estimate_copy.phase
                    confidence = estimate_copy.confidence
                    self.trajectories[i].points[j].phase = new_phase
                    # Update coherence based on confidence (higher confidence -> higher coherence)
                    # Let's use confidence directly for now, capping existing coherence if lower
                    self.trajectories[i].points[j].coherence = confidence # Or max(existing, confidence)? Let's overwrite.
                    
                    total_confidence += confidence
                    total_estimates += 1

                    logger.debug(f"Traj {i}, Step {j}: Phase updated {old_phase:.4f} -> {new_phase:.4f} (conf: {confidence:.4f}, using_neigh: {use_neighbours and neighbour_phases_for_kf is not None})")

                except Exception as e:
                    logger.error(f"Error during estimate_phase for traj {i}, step {j}: {e}. Storing NaN.")
                    all_estimates_history[i].append(StateEstimate(phase=np.nan, confidence=0.0))

        # Calculate average confidence as a proxy for performance
        avg_confidence = total_confidence / total_estimates if total_estimates > 0 else 0.0
        
        logger.info(f"Adaptive phase tracking integration completed in {time.time() - start_time:.2f} seconds")
        logger.info(f"Average confidence across all estimates: {avg_confidence:.4f}")
        
        # Return history per trajectory and average confidence
        return all_estimates_history, avg_confidence
    
    def benchmark_with_adaptive_phase_tracking(self,
                                              reference_state: np.ndarray,
                                              # Remove learning_rates/iterations if not used by PF
                                              # learning_rates: List[float] = [0.01, 0.05, 0.1],
                                              # iterations: List[int] = [20, 50, 100],
                                              # Add PF specific parameters to benchmark
                                              num_particles_list: List[int] = [50, 100, 200],
                                              process_noise_scales: List[float] = [0.005, 0.01, 0.05],
                                              measurement_noise_scales: List[float] = [0.05, 0.1, 0.2]
                                              ) -> Dict[str, Any]:
        """
        Benchmark the stochastic quantum simulator with various adaptive phase tracking (Particle Filter) configurations.

        Args:
            reference_state: Reference quantum state for accuracy comparison.
            num_particles_list: List of particle counts to try.
            process_noise_scales: List of process noise scales (sigma_process) to try.
            measurement_noise_scales: List of measurement noise scales (sigma_measurement) to try.

        Returns:
            Dictionary of benchmark results.
        """
        num_configs = len(num_particles_list) * len(process_noise_scales) * len(measurement_noise_scales)
        logger.info(f"Benchmarking adaptive phase tracking (Particle Filter) with {num_configs} configurations")

        results = {
            "configurations": [],
            "accuracy": [],
            "runtime": [],
            "best_config": None,
            "best_accuracy": 0.0
        }

        # --- Modify loops for PF parameters ---
        for n_particles in num_particles_list:
            for q_scale in process_noise_scales:
                for r_scale in measurement_noise_scales:
                    # Save original trajectories to restore after each test
                    # Use deepcopy to ensure points list and ConfigurationPoints are copied independently
                    original_trajectories = [copy.deepcopy(traj) for traj in self.trajectories] # Use deepcopy

                    config = {"num_particles": n_particles, "process_noise_scale": q_scale, "measurement_noise_scale": r_scale}
                    start_time = time.time()
                    try:
                        # --- Modify call to use PF parameters --- Corrected Call ---
                        _, avg_confidence = self.integrate_adaptive_phase_tracker(
                            num_particles=n_particles,          # Pass correct parameter
                            process_noise_scale=q_scale,        # Pass correct parameter
                            measurement_noise_scale=r_scale,    # Pass correct parameter (name fixed)
                            use_neighbours=True                 # Keep coupled mode enabled for benchmark
                        )
                        runtime = time.time() - start_time

                        # Convert current state to wave function
                        # Assuming grid points cover the relevant space
                        target_len = reference_state.shape[0] # Get length of reference state

                        # Find min/max configuration values across all points in all trajectories
                        all_configs = np.concatenate([np.array([p.configuration for p in traj.points]) 
                                                      for traj in original_trajectories if traj.points])
                        
                        if all_configs.size == 0:
                            logger.error("Cannot generate grid: No configuration points found in trajectories.")
                            # Handle error appropriately, maybe skip this benchmark iteration
                            raise ValueError("No configuration points available to define grid bounds.")

                        min_coords = np.min(all_configs, axis=0)
                        max_coords = np.max(all_configs, axis=0)
                        # Add a small margin to ensure coverage
                        margin = (max_coords - min_coords) * 0.1 
                        min_coords -= margin
                        max_coords += margin

                        # Estimate grid points per dimension based on reference state size
                        # Note: This assumes reference_state corresponds to a hypercubic grid
                        grid_points_per_dim = int(round(target_len**(1.0/self.config_space_dim)))
                        num_grid_points_actual = grid_points_per_dim**self.config_space_dim
                        
                        if not np.isclose(num_grid_points_actual, target_len):
                            logger.warning(f"Reference state size {target_len} does not perfectly match a hypercube grid "
                                           f"with dimension {self.config_space_dim}. Using {grid_points_per_dim} points per dim "
                                           f"(total {num_grid_points_actual}). Fidelity calculation might involve padding/truncation.")

                        # Generate grid points
                        axes = [np.linspace(min_coords[d], max_coords[d], grid_points_per_dim) 
                                for d in range(self.config_space_dim)]
                        grid_meshes = np.meshgrid(*axes, indexing='ij') 
                        # Stack and transpose to get N x D array
                        grid_points = np.vstack([mesh.ravel() for mesh in grid_meshes]).T 
                        
                        amplitudes, phases = self.convert_to_wave_function(grid_points)
                        reconstructed_state = amplitudes * np.exp(1j * phases)
                        # Ensure reconstructed state has the same dimension as reference_state
                        # Recalculate target_len here in case it was adjusted due to grid mismatch
                        target_len = reference_state.shape[0] 
                        if reconstructed_state.shape[0] != target_len:
                             logger.warning(f"Adjusting reconstructed state shape from {reconstructed_state.shape[0]} to match reference {target_len}")
                             # Handle mismatch: Pad, truncate, or raise error
                             # Simple padding/truncating (might be incorrect physics-wise)
                             if reconstructed_state.shape[0] < target_len:
                                 reconstructed_state = np.pad(reconstructed_state, (0, target_len - reconstructed_state.shape[0]))
                             elif reconstructed_state.shape[0] > target_len:
                                 reconstructed_state = reconstructed_state[:target_len]

                        # Calculate fidelity with reference state
                        # Ensure normalization before fidelity calculation
                        norm_reconstructed = np.linalg.norm(reconstructed_state)
                        norm_reference = np.linalg.norm(reference_state)
                        if norm_reconstructed > 1e-9 and norm_reference > 1e-9:
                            fidelity = np.abs(np.vdot(reconstructed_state / norm_reconstructed, reference_state / norm_reference))**2
                        else:
                            fidelity = 0.0 # Fidelity is zero if either state is zero

                        # Record results
                        # config defined earlier
                        results["configurations"].append(config)
                        results["accuracy"].append(fidelity)
                        results["runtime"].append(runtime)

                        logger.info(f"Config {config}: Fidelity = {fidelity:.4f}, Runtime = {runtime:.2f}s, AvgConf = {avg_confidence:.4f}")

                        # Track best configuration
                        if fidelity > results["best_accuracy"]:
                            results["best_accuracy"] = fidelity
                            results["best_config"] = config

                    except Exception as e:
                         logger.error(f"Error during benchmarking config {config}: {e}", exc_info=True)
                         # config defined earlier
                         results["configurations"].append(config)
                         results["accuracy"].append(np.nan) # Indicate error
                         results["runtime"].append(time.time() - start_time)


                    # Restore original trajectories for next test
                    self.trajectories = original_trajectories
        # --- End modification ---

        logger.info(f"Best configuration: {results['best_config']} with accuracy {results['best_accuracy']:.4f}")
        return results 

    def continue_evolution(self, 
                           steps: int, 
                           potential_func: Optional[Callable[[np.ndarray], float]] = None,
                           drift_func: Optional[Callable[[np.ndarray, float], np.ndarray]] = None) -> List[Trajectory]:
        """
        Continues the evolution of existing stochastic trajectories.

        Assumes self.trajectories has been initialized (e.g., by 
        evolve_stochastic_process or quantum_stochastic_correspondence).

        Args:
            steps: Number of additional evolution steps.
            potential_func: Optional classical potential function V(x).
            drift_func: Optional additional drift function.
            
        Returns:
            List of updated configuration space trajectories.
        """
        if not self.trajectories:
            raise ValueError("No existing trajectories to continue. Initialize first.")
        
        # Determine the starting step and time based on the last point of the first trajectory
        # Assumes all trajectories have the same number of points initially, or were padded
        if not self.trajectories[0].points:
             raise ValueError("Cannot continue evolution: First trajectory has no points.")
             
        start_step = len(self.trajectories[0].points)
        start_time_offset = self.trajectories[0].points[-1].time
        logger.info(f"Continuing stochastic process for {steps} steps from step {start_step} (time {start_time_offset:.2f})")
        
        evolution_start_time = time.time()

        # Evolve each trajectory for the specified number of additional steps
        for step in range(start_step, start_step + steps):
            current_time = start_time_offset + (step - start_step + 1) * self.dt
            
            # Periodically update neighbor relationships based on current positions
            # Use the overall step count for interval checking
            if step > 0 and step % self.neighbor_update_interval == 0:
                self._update_trajectory_neighbors()
            
            # Get current configurations for all trajectories
            # Handle potential inconsistencies in trajectory lengths if they occurred
            current_configs = []
            valid_traj_indices = []
            for idx, traj in enumerate(self.trajectories):
                if len(traj.points) >= step: # Check if trajectory has enough points for this step
                    current_configs.append(traj.points[-1].configuration)
                    valid_traj_indices.append(idx)
                else:
                    # This trajectory ended early or wasn't updated properly. Log and skip.
                    logger.warning(f"Trajectory {idx} has fewer points ({len(traj.points)}) than current step {step}. Skipping its update.")
            
            if not current_configs:
                logger.error("No valid trajectories found at current step. Stopping evolution.")
                break # Exit loop if no trajectories can be updated
                
            # Calculate quantum potential if no drift function provided
            # Need to recalculate based only on the valid current configs
            quantum_force = np.zeros((len(valid_traj_indices), self.config_space_dim))
            
            if drift_func is None:
                # Pass only the valid configurations to the potential calculator
                quantum_potentials = self._calculate_quantum_potential(current_configs) 
                
                # Calculate quantum force from quantum potential
                for i, config_idx in enumerate(valid_traj_indices):
                    config = current_configs[i]
                    # Simple finite difference approximation of gradient
                    for dim in range(self.config_space_dim):
                        h = 0.01  # Small step for numerical gradient
                        
                        # Forward point (recalculate potential with shifted config)
                        forward_config = config.copy()
                        forward_config[dim] += h
                        forward_configs_temp = current_configs.copy() # Use valid configs
                        forward_configs_temp[i] = forward_config # Modify the i-th valid config
                        # Need to handle potential errors if _calculate_quantum_potential expects full list
                        # For simplicity, assume it returns potentials matching input list length
                        forward_potential = self._calculate_quantum_potential(forward_configs_temp)[i]
                        
                        # Backward point
                        backward_config = config.copy()
                        backward_config[dim] -= h
                        backward_configs_temp = current_configs.copy()
                        backward_configs_temp[i] = backward_config
                        backward_potential = self._calculate_quantum_potential(backward_configs_temp)[i]
                        
                        # Gradient (central difference)
                        quantum_force[i, dim] = -(forward_potential - backward_potential) / (2 * h)
            
            # Update phase coherence between trajectories (uses internal self.trajectories)
            # This might need adjustment if trajectories have varying lengths significantly.
            # Assuming _update_phase_coherence handles accessing traj.points[-1] safely.
            self._update_phase_coherence()
            
            # Evolve each valid trajectory
            for i, traj_idx in enumerate(valid_traj_indices):
                trajectory = self.trajectories[traj_idx]
                current_config = trajectory.points[-1].configuration # Use the latest point
                
                # Calculate drift term
                if drift_func is not None:
                    # Pass the absolute current time to the drift function
                    drift = drift_func(current_config, current_time)
                else:
                    # Use quantum force calculated for the i-th valid trajectory
                    drift = quantum_force[i]
                
                # Calculate potential force if potential function provided
                if potential_func is not None:
                    # Simple numerical gradient of potential
                    potential_force = np.zeros(self.config_space_dim)
                    for dim in range(self.config_space_dim):
                        h = 0.001  # Smaller step for better numerical accuracy
                        
                        forward_config = current_config.copy()
                        forward_config[dim] += h
                        # Pass absolute time if potential_func depends on it (signature allows only config)
                        forward_potential = potential_func(forward_config)
                        
                        backward_config = current_config.copy()
                        backward_config[dim] -= h
                        backward_potential = potential_func(backward_config)
                        
                        potential_force[dim] = -(forward_potential - backward_potential) / (2 * h)
                    
                    # Scale potential force by mass
                    force = potential_force
                else:
                    force = np.zeros(self.config_space_dim)
                
                # Get current velocity (from previous step if available)
                if len(trajectory.points) > 1:
                    current_velocity = (current_config - trajectory.points[-2].configuration) / self.dt
                else:
                    current_velocity = np.zeros(self.config_space_dim)
                
                # Deterministic evolution using velocity Verlet
                # First half-step velocity update
                half_velocity = current_velocity + 0.5 * (force / self.mass) * self.dt
                
                # Full position update
                new_config = current_config + half_velocity * self.dt
                
                # Calculate new force at updated position
                if potential_func is not None:
                    new_force = np.zeros(self.config_space_dim)
                    for dim in range(self.config_space_dim):
                        h = 0.001
                        forward_config = new_config.copy()
                        forward_config[dim] += h
                        forward_potential = potential_func(forward_config)
                        
                        backward_config = new_config.copy()
                        backward_config[dim] -= h
                        backward_potential = potential_func(backward_config)
                        
                        new_force[dim] = -(forward_potential - backward_potential) / (2 * h)
                else:
                    new_force = np.zeros(self.config_space_dim)
                
                # Second half-step velocity update
                final_velocity = half_velocity + 0.5 * (new_force / self.mass) * self.dt
                
                # Store deterministic position and velocity
                deterministic_config = new_config.copy()
                deterministic_velocity = final_velocity.copy()
                
                # Stochastic evolution using Ornstein-Uhlenbeck process
                # This preserves the quantum uncertainty while maintaining energy conservation
                gamma = 0.1  # Friction coefficient for energy dissipation
                noise = self.rng.randn(self.config_space_dim)
                diffusion = np.sqrt(2 * gamma * self.hbar / self.mass)
                
                # Update position and velocity with stochastic terms
                stochastic_velocity = diffusion * np.sqrt(self.dt) * noise
                new_config = deterministic_config + 0.5 * stochastic_velocity * self.dt
                
                # Get the phase and coherence from the *last added point*
                current_phase = trajectory.points[-1].phase
                current_coherence = trajectory.points[-1].coherence
                
                # Store the final configuration
                new_point = ConfigurationPoint(
                    configuration=new_config,
                    time=current_time,
                    phase=current_phase,
                    coherence=current_coherence,
                    velocity=deterministic_velocity + stochastic_velocity  # Store total velocity for next step
                )
                
                # Add the new point to the specific trajectory
                trajectory.points.append(new_point)
        
        logger.info(f"Continued stochastic process evolution completed in {time.time() - evolution_start_time:.2f} seconds")
        return self.trajectories 