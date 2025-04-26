"""
Adaptive Phase Tracker Module

This module implements adaptive phase tracking algorithms for quantum systems.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional, Union
import logging
from scipy.linalg import inv

# Configure logging
logger = logging.getLogger(__name__)

class StateEstimate:
    """
    Class representing a quantum state estimate.
    """
    def __init__(self, 
                 phase: float = 0.0, 
                 amplitude: float = 1.0, 
                 confidence: float = 0.0):
        """
        Initialize a state estimate.
        
        Args:
            phase: Estimated phase value
            amplitude: Estimated amplitude value
            confidence: Confidence level in the estimate (0.0 to 1.0)
        """
        # Ensure values are Python float type to avoid numpy type conflicts
        self.phase = float(phase)
        self.amplitude = float(amplitude)
        self.confidence = float(confidence)
        self.history: List[Tuple[float, float, float]] = [(float(phase), float(amplitude), float(confidence))]
    
    def update(self, 
               phase: Optional[float] = None, 
               amplitude: Optional[float] = None, 
               confidence: Optional[float] = None) -> None:
        """
        Update the state estimate with new values.
        
        Args:
            phase: New phase value (if None, keeps current value)
            amplitude: New amplitude value (if None, keeps current value)
            confidence: New confidence value (if None, keeps current value)
        """
        if phase is not None:
            self.phase = float(phase)
        if amplitude is not None:
            self.amplitude = float(amplitude)
        if confidence is not None:
            self.confidence = float(confidence)
        
        self.history.append((self.phase, self.amplitude, self.confidence))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the state estimate to a dictionary.
        
        Returns:
            Dictionary representation of the state estimate
        """
        return {
            'phase': self.phase,
            'amplitude': self.amplitude,
            'confidence': self.confidence,
            'history': self.history
        }


class AdaptivePhaseTracker:
    """
    Adaptive phase tracking algorithm for quantum systems.
    Now implements Particle Filter approach for more robust phase tracking.
    """
    def __init__(self, 
                 num_particles: int = 100,
                 process_noise_scale: float = 0.01,
                 measurement_noise_scale: float = 0.1):
        """
        Initialize the adaptive phase tracker using Particle Filter.
        
        Args:
            num_particles: Number of particles for the Particle Filter
            process_noise_scale: Standard deviation for the process noise
            measurement_noise_scale: Standard deviation for the measurement noise
        """
        self.num_particles = int(num_particles)
        self._process_noise_scale = float(process_noise_scale)
        self._measurement_noise_scale = float(measurement_noise_scale)
        self.current_estimate = StateEstimate()
        
        # Initialize particle filter variables
        self._particles = np.zeros((self.num_particles, 2))  # [phase, phase_velocity]
        self._particle_weights = np.ones(self.num_particles) / self.num_particles
        self._initialized = False
        
        logger.info(f"Particle Filter initialized with {self.num_particles} particles, "
                   f"process_noise={self._process_noise_scale}, "
                   f"measurement_noise={self._measurement_noise_scale}")
        
        # Keep Kalman filter as fallback or for comparison
        self._kf_state = np.array([0.0, 0.0])  # Initial state [phase, phase_velocity]
        self._kf_covariance = np.eye(2) * 0.1  # Initial covariance
        self._kf_transition_matrix = np.array([[1, 1], [0, 1]]) # F: Constant velocity model
        self._kf_observation_matrix = np.array([[1, 0]])      # H: Observe phase directly
        # Configure noise parameters
        self._kf_process_noise_cov = np.eye(2) * self._process_noise_scale # Q
        self._kf_measurement_noise_cov = np.array([[self._measurement_noise_scale]]) # R
    
    def _calculate_circular_mean(self, phases: List[float]) -> float:
        """Calculate the circular mean of a list of phases."""
        if not phases: 
            return 0.0 # Or handle as error/None
        # Convert phases to complex numbers on unit circle, average, convert back to angle
        mean_cos = np.mean(np.cos(phases))
        mean_sin = np.mean(np.sin(phases))
        return np.arctan2(mean_sin, mean_cos)

    def _calculate_angular_difference(self, angle1: Union[float, np.ndarray], angle2: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Calculate the shortest angular difference between two angles (angle1 - angle2)."""
        diff = angle1 - angle2
        return np.mod(diff + np.pi, 2 * np.pi) - np.pi
        
    def _initialize_particles(self, initial_phase: float) -> None:
        """Initialize particles around the given initial phase."""
        # Set all particles' phases to initial_phase with small random offsets
        # and with small random phase velocities
        self._particles[:, 0] = initial_phase + np.random.normal(0, 0.1, self.num_particles)
        self._particles[:, 1] = np.random.normal(0, 0.05, self.num_particles)  # phase velocity
        self._particle_weights = np.ones(self.num_particles) / self.num_particles
        self._initialized = True
        logger.debug(f"Initialized {self.num_particles} particles around phase {initial_phase}")
        
    def _predict_particles(self) -> None:
        """Propagate particles forward according to the state model."""
        # Simple constant velocity model: phase += phase_velocity + noise
        self._particles[:, 0] += self._particles[:, 1] + np.random.normal(0, self._process_noise_scale, self.num_particles)
        # Phase velocity evolves with small random changes
        self._particles[:, 1] += np.random.normal(0, self._process_noise_scale/2, self.num_particles)
        
    def _update_particle_weights(self, measurement: float, neighbour_phases: Optional[List[float]] = None) -> None:
        """Update particle weights based on measurement and optional neighbour phases."""
        # For each particle, calculate likelihood of the measurement
        if neighbour_phases is not None and len(neighbour_phases) > 0:
            # Using neighbour phases - calculate average as reference
            avg_neighbour_phase = self._calculate_circular_mean(neighbour_phases)
            # Likelihood based on difference between measurement and avg neighbour phase
            diff = np.array([self._calculate_angular_difference(measurement, avg_neighbour_phase) 
                             for _ in range(self.num_particles)])
        else:
            # Standard likelihood - based on difference between measurement and particle phases
            diff = np.array([self._calculate_angular_difference(measurement, phase) 
                             for phase in self._particles[:, 0]])
            
        # Calculate likelihood using normal distribution
        likelihoods = np.exp(-0.5 * (diff**2) / (self._measurement_noise_scale**2))
        
        # Update weights
        self._particle_weights *= likelihoods
        
        # Normalize weights
        weight_sum = np.sum(self._particle_weights)
        if weight_sum > 1e-10:  # Avoid division by zero
            self._particle_weights /= weight_sum
        else:
            # Reinitialize if all weights are too small
            logger.warning("All particle weights are near zero. Reinitializing with uniform weights.")
            self._particle_weights = np.ones(self.num_particles) / self.num_particles
            
    def _resample_particles(self) -> None:
        """Resample particles based on their weights to prevent degeneracy."""
        # Calculate effective number of particles
        n_eff = 1.0 / np.sum(self._particle_weights**2)
        
        # Resample if effective number is too low (typically < N/2)
        if n_eff < self.num_particles / 2:
            # Systematic resampling (more efficient than multinomial)
            cumsum = np.cumsum(self._particle_weights)
            step = 1.0 / self.num_particles
            u = np.random.uniform(0, step)
            indices = []
            i = 0
            for j in range(self.num_particles):
                while u > cumsum[i]:
                    i += 1
                indices.append(i)
                u += step
                
            # Create new particle set
            self._particles = self._particles[indices, :]
            # Reset weights
            self._particle_weights = np.ones(self.num_particles) / self.num_particles
            
            logger.debug(f"Resampled particles (effective N: {n_eff:.1f})")
            
    def _estimate_state_from_particles(self) -> Tuple[float, float, float]:
        """Calculate the final state estimate from particles."""
        # For phase, use weighted circular mean
        sin_vals = np.sin(self._particles[:, 0])
        cos_vals = np.cos(self._particles[:, 0])
        weighted_sin = np.sum(sin_vals * self._particle_weights)
        weighted_cos = np.sum(cos_vals * self._particle_weights)
        phase_estimate = np.arctan2(weighted_sin, weighted_cos)
        
        # For velocity, use weighted mean
        velocity_estimate = np.sum(self._particles[:, 1] * self._particle_weights)
        
        # Calculate confidence from particle dispersion
        # Low dispersion = high confidence
        phase_var = np.sum(self._particle_weights * (self._calculate_angular_difference(
            self._particles[:, 0], phase_estimate)**2))
        confidence = np.exp(-phase_var)  # Transform variance to [0,1] confidence
        
        return float(phase_estimate), float(velocity_estimate), float(confidence)

    def estimate_phase(self, 
                       measurement_data: Union[List[float], np.ndarray], 
                       initial_phase: Optional[float] = None,
                       neighbour_phases: Optional[List[float]] = None) -> StateEstimate:
        """
        Estimate the phase using the Particle Filter.
        
        Args:
            measurement_data: Measurement result for the current trajectory (expects a single value).
            initial_phase: Initial phase estimate (used only for the very first estimate, if not None).
            neighbour_phases: Optional list of phases of neighbouring trajectories at the current time.
                             Used for phase coherence.
            
        Returns:
            StateEstimate object with the final estimate.
        """
        # Convert to numpy array if needed
        if not isinstance(measurement_data, np.ndarray):
            measurement_data = np.array(measurement_data)
        
        if measurement_data.size == 0:
            logger.warning("estimate_phase called with empty measurement_data.")
            # Return current estimate without update if no data
            return self.current_estimate
        
        # Use the first measurement if multiple are provided
        measurement = float(measurement_data[0])
        
        # Initialize particles if this is the first call or if init_phase is provided
        if not self._initialized or initial_phase is not None:
            init_phase = initial_phase if initial_phase is not None else measurement
            self._initialize_particles(init_phase)
            
        # Perform Particle Filter steps
        # 1. Predict step - propagate particles forward
        self._predict_particles()
        
        # 2. Update step - update weights based on measurement
        self._update_particle_weights(measurement, neighbour_phases)
        
        # 3. Resample step - prevent degeneracy
        self._resample_particles()
        
        # 4. Calculate final estimate
        phase, velocity, confidence = self._estimate_state_from_particles()
        
        # Update the estimate object
        self.current_estimate.update(
            phase=phase,
            confidence=confidence
        )
        
        # Also update the fallback KF state in case it's used later
        self._kf_state = np.array([phase, velocity])
        
        logger.info(f"Phase estimation complete: {self.current_estimate.phase:.4f} (confidence: {self.current_estimate.confidence:.2f})")
        return self.current_estimate
    
    def track_phase_evolution(self, 
                              time_series_data: List[List[float]],
                              time_points: Optional[List[float]] = None) -> List[StateEstimate]:
        """
        Track phase evolution over time from a series of measurements.
        
        Args:
            time_series_data: List of measurement data at each time point
            time_points: Optional list of time points
            
        Returns:
            List of StateEstimate objects for each time point
        """
        logger.info(f"Tracking phase evolution across {len(time_series_data)} time points")
        
        estimates = []
        # Reset particle filter state
        self._initialized = False
        initial_phase_set = False
        
        for i, measurements in enumerate(time_series_data):
            # Ensure measurements is a list-like structure and not empty
            if not isinstance(measurements, (list, np.ndarray)) or len(measurements) == 0:
                logger.warning(f"Skipping step {i} due to invalid measurements: {measurements}")
                # Append previous estimate or a default if it's the first step
                estimates.append(estimates[-1] if estimates else StateEstimate())
                continue

            # Set initial phase only for the first valid measurement
            init_phase = None
            if not initial_phase_set:
                try:
                    init_phase = float(measurements[0])
                    initial_phase_set = True
                    logger.info(f"Particle Filter initial phase set to first measurement: {init_phase:.4f}")
                except (TypeError, IndexError) as e:
                    logger.warning(f"Could not extract initial phase from measurements {measurements}: {e}. Using None.")
            
            # Update particle filter with this measurement
            try:
                estimate = self.estimate_phase(measurements, initial_phase=init_phase)
                estimates.append(estimate)
            except Exception as e:
                logger.error(f"Error during estimate_phase at step {i}: {e}. Appending last valid estimate.")
                estimates.append(estimates[-1] if estimates else StateEstimate())
            
            if time_points and i < len(time_points):
                est_phase = getattr(estimate, 'phase', float('nan'))
                est_conf = getattr(estimate, 'confidence', float('nan'))
                logger.debug(f"Time {time_points[i]}: Phase = {est_phase:.4f}, Confidence = {est_conf:.4f}")
            elif not time_points:
                est_phase = getattr(estimate, 'phase', float('nan'))
                est_conf = getattr(estimate, 'confidence', float('nan'))
                logger.debug(f"Step {i}: Phase = {est_phase:.4f}, Confidence = {est_conf:.4f}")
        
        return estimates

    # This method remains unchanged for compatibility
    def get_quantum_measurement_result(self) -> np.ndarray:
        """
        Placeholder: Format the current state estimate for the quantum-AI pipeline.
        The format (e.g., 8 elements) needs to be defined based on pipeline requirements.
        """
        # Example: Return phase, confidence, and placeholders
        # This MUST match the expected input shape of the AI model (e.g., shape=(8,))
        phase = self.current_estimate.phase
        confidence = self.current_estimate.confidence
        # Create an 8-element array, potentially including phase velocity, variance etc.
        # This is a placeholder and needs refinement based on the AI model's needs.
        result = np.array([
            phase,  # Element 0: Current phase
            confidence, # Element 1: Current confidence
            self._kf_state[1], # Element 2: Phase velocity estimate
            0.0, # Element 3: Phase variance (to be updated)
            0.0, # Element 4: Velocity variance (to be updated)
            0.0, # Element 5: Phase-velocity covariance (to be updated)
            0.0, # Element 6: Placeholder
            0.0  # Element 7: Placeholder
        ])
        # Ensure the result has the correct shape, padding if necessary
        if result.size < 8:
             result = np.pad(result, (0, 8 - result.size))
        elif result.size > 8:
             result = result[:8] # Truncate if too long

        logger.debug(f"Generated quantum measurement result: {result}")
        return result.astype(float) # Ensure float type 