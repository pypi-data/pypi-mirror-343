"""
Quantum Stochastic Decision Process

This module implements the QuantumStochasticDecisionProcess class, which
provides a framework for quantum-enhanced decision making under uncertainty
using stochastic quantum methods.
"""

import numpy as np
import logging
from typing import List, Dict, Tuple, Any, Optional, Callable, Union
import time
from pathlib import Path
import os
import sys

# Add the project root to the Python path if needed
try:
    from quantum.stochastic.stochastic_quantum_simulator import (
        StochasticQuantumSimulator,
        Trajectory,
        ConfigurationPoint
    )
    from quantum.stochastic.stochastic_quantum_circuit import (
        StochasticQuantumCircuit,
        StochasticQuantumState
    )
except ImportError:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from quantum.stochastic.stochastic_quantum_simulator import (
        StochasticQuantumSimulator,
        Trajectory,
        ConfigurationPoint
    )
    from quantum.stochastic.stochastic_quantum_circuit import (
        StochasticQuantumCircuit,
        StochasticQuantumState
    )

# Configure logging
logger = logging.getLogger(__name__)

class QuantumStochasticDecisionProcess:
    """
    Framework for quantum-enhanced decision making under uncertainty.
    
    This class implements stochastic quantum decision processes, providing tools
    for uncertainty-aware decision algorithms and quantum Bayesian updating.
    """
    
    def __init__(self, 
                 num_states: int,
                 num_actions: int,
                 num_trajectories: int = 1000,
                 dt: float = 0.01,
                 hbar: float = 1.0,
                 discount_factor: float = 0.95,
                 seed: Optional[int] = None):
        """
        Initialize the quantum stochastic decision process.
        
        Args:
            num_states: Number of states in the decision process
            num_actions: Number of possible actions
            num_trajectories: Number of stochastic trajectories to use
            dt: Time step for stochastic evolution
            hbar: Planck's constant (reduced)
            discount_factor: Discount factor for future rewards
            seed: Random seed for reproducibility
        """
        self.num_states = num_states
        self.num_actions = num_actions
        self.num_trajectories = num_trajectories
        self.dt = dt
        self.hbar = hbar
        self.discount_factor = discount_factor
        self.seed = seed
        
        # Initialize the stochastic quantum simulator
        self.simulator = StochasticQuantumSimulator(
            config_space_dim=num_states,
            num_trajectories=num_trajectories,
            dt=dt,
            hbar=hbar,
            mass=1.0,
            seed=seed
        )
        
        # Initialize state-action transition probabilities
        # P[s, a, s'] is probability of transitioning from state s to s' when taking action a
        self.transition_probabilities = np.ones((num_states, num_actions, num_states)) / num_states
        
        # Initialize rewards
        # R[s, a] is reward for taking action a in state s
        self.rewards = np.zeros((num_states, num_actions))
        
        # Initialize value function
        self.value_function = np.zeros(num_states)
        
        # Initialize policy (probability of each action in each state)
        self.policy = np.ones((num_states, num_actions)) / num_actions
        
        # State representation in configuration space
        self.state_representations = np.eye(num_states)
        
        logger.info(f"Initialized QuantumStochasticDecisionProcess with {num_states} states and {num_actions} actions")
    
    def set_transition_probabilities(self, transitions: np.ndarray):
        """
        Set the transition probability matrix.
        
        Args:
            transitions: Transition probability matrix with shape (num_states, num_actions, num_states)
                         transitions[s, a, s'] = P(s' | s, a)
        """
        if transitions.shape != (self.num_states, self.num_actions, self.num_states):
            raise ValueError(f"Transitions shape {transitions.shape} doesn't match expected shape "
                             f"({self.num_states}, {self.num_actions}, {self.num_states})")
        
        # Ensure probabilities sum to 1 for each state-action pair
        for s in range(self.num_states):
            for a in range(self.num_actions):
                transitions[s, a] = transitions[s, a] / np.sum(transitions[s, a])
        
        self.transition_probabilities = transitions
        logger.debug("Set transition probabilities")
    
    def set_rewards(self, rewards: np.ndarray):
        """
        Set the reward matrix.
        
        Args:
            rewards: Reward matrix with shape (num_states, num_actions)
                    rewards[s, a] = R(s, a)
        """
        if rewards.shape != (self.num_states, self.num_actions):
            raise ValueError(f"Rewards shape {rewards.shape} doesn't match expected shape "
                             f"({self.num_states}, {self.num_actions})")
        
        self.rewards = rewards
        logger.debug("Set rewards")
    
    def _encode_state_to_quantum(self, state_idx: int) -> np.ndarray:
        """
        Encode a classical state index to a quantum configuration point.
        
        Args:
            state_idx: Index of the state to encode
        
        Returns:
            Configuration space representation of the state
        """
        return self.state_representations[state_idx]
    
    def _action_potential(self, state_idx: int, action_idx: int) -> Callable:
        """
        Create a potential function for a specific action.
        
        Args:
            state_idx: Current state index
            action_idx: Action index
        
        Returns:
            A potential function for quantum evolution
        """
        # Target state distribution after the action
        target_distribution = self.transition_probabilities[state_idx, action_idx]
        
        def potential_func(x):
            # Distance from target distribution (used to guide trajectories)
            distances = np.array([np.sum((x - self.state_representations[s])**2) 
                                 for s in range(self.num_states)])
            
            # Weight by transition probabilities (lower potential for likely states)
            weighted_potential = np.sum(distances * target_distribution)
            
            # Add reward component to the potential
            reward_component = -self.rewards[state_idx, action_idx] * 0.1
            
            return weighted_potential + reward_component
        
        return potential_func
    
    def quantum_policy_iteration(self, max_iterations: int = 100, tolerance: float = 1e-6) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform quantum-enhanced policy iteration to optimize the policy.
        
        Args:
            max_iterations: Maximum number of policy iterations
            tolerance: Convergence tolerance for value function
        
        Returns:
            Tuple of (optimized policy, value function)
        """
        for iteration in range(max_iterations):
            # Policy evaluation
            delta = self._quantum_policy_evaluation(tolerance)
            
            # Policy improvement
            policy_stable = self._quantum_policy_improvement()
            
            logger.info(f"Iteration {iteration+1}: max value change = {delta}")
            
            # Check for convergence
            if policy_stable and delta < tolerance:
                logger.info(f"Policy iteration converged after {iteration+1} iterations")
                break
                
        return self.policy, self.value_function
    
    def _quantum_policy_evaluation(self, tolerance: float = 1e-6) -> float:
        """
        Evaluate the current policy using quantum stochastic methods.
        
        Args:
            tolerance: Convergence tolerance for value function
        
        Returns:
            Maximum change in value function
        """
        delta = 0.0
        
        # Temporary value function for updates
        new_value = np.zeros_like(self.value_function)
        
        for s in range(self.num_states):
            # Encode state into quantum representation
            quantum_state = self._encode_state_to_quantum(s)
            
            # Accumulate expected value for current policy
            v = 0.0
            
            for a in range(self.num_actions):
                if self.policy[s, a] > 0:
                    # Define potential function for this action
                    potential_func = self._action_potential(s, a)
                    
                    # Evolve quantum state using stochastic process
                    trajectories = self.simulator.evolve_stochastic_process(
                        initial_state=quantum_state,
                        steps=20,  # Short-term evolution to next states
                        potential_func=potential_func
                    )
                    
                    # Extract next states from trajectories
                    next_state_values = []
                    weights = []
                    
                    for traj in trajectories:
                        if not traj.points:
                            continue
                            
                        # Get final point in trajectory
                        final_point = traj.points[-1].configuration
                        
                        # Find closest state representation
                        distances = np.array([np.sum((final_point - self.state_representations[s_prime])**2) 
                                            for s_prime in range(self.num_states)])
                        next_state = np.argmin(distances)
                        
                        # Add value of this next state
                        next_state_values.append(self.value_function[next_state])
                        weights.append(traj.weight)
                    
                    if next_state_values:
                        # Compute weighted average of next state values
                        weights = np.array(weights) / np.sum(weights)
                        expected_next_value = np.sum(np.array(next_state_values) * weights)
                        
                        # Accumulated value with policy probability
                        v += self.policy[s, a] * (self.rewards[s, a] + 
                                                 self.discount_factor * expected_next_value)
            
            # Update value function
            new_value[s] = v
            
            # Track maximum change
            delta = max(delta, abs(self.value_function[s] - v))
        
        # Update value function
        self.value_function = new_value
        
        return delta
    
    def _quantum_policy_improvement(self) -> bool:
        """
        Improve the policy based on the current value function.
        
        Returns:
            True if policy is stable (unchanged), False otherwise
        """
        policy_stable = True
        
        for s in range(self.num_states):
            # Store old policy for this state
            old_action = np.argmax(self.policy[s])
            
            # Quantum-enhanced Q-values
            q_values = np.zeros(self.num_actions)
            
            # Encode state into quantum representation
            quantum_state = self._encode_state_to_quantum(s)
            
            for a in range(self.num_actions):
                # Define potential function for this action
                potential_func = self._action_potential(s, a)
                
                # Evolve quantum state using stochastic process
                trajectories = self.simulator.evolve_stochastic_process(
                    initial_state=quantum_state,
                    steps=20,  # Short-term evolution to next states
                    potential_func=potential_func
                )
                
                # Extract next states from trajectories
                next_state_values = []
                weights = []
                
                for traj in trajectories:
                    if not traj.points:
                        continue
                        
                    # Get final point in trajectory
                    final_point = traj.points[-1].configuration
                    
                    # Find closest state representation
                    distances = np.array([np.sum((final_point - self.state_representations[s_prime])**2) 
                                        for s_prime in range(self.num_states)])
                    next_state = np.argmin(distances)
                    
                    # Add value of this next state
                    next_state_values.append(self.value_function[next_state])
                    weights.append(traj.weight)
                
                if next_state_values:
                    # Compute weighted average of next state values
                    weights = np.array(weights) / np.sum(weights)
                    expected_next_value = np.sum(np.array(next_state_values) * weights)
                    
                    # Q-value for this action
                    q_values[a] = self.rewards[s, a] + self.discount_factor * expected_next_value
                else:
                    # Fallback to classical calculation if no valid trajectories
                    expected_value = np.sum(self.transition_probabilities[s, a] * self.value_function)
                    q_values[a] = self.rewards[s, a] + self.discount_factor * expected_value
            
            # Greedy policy update
            best_action = np.argmax(q_values)
            
            # Update policy (greedy)
            self.policy[s] = np.zeros(self.num_actions)
            self.policy[s, best_action] = 1.0
            
            # Check if policy changed
            if old_action != best_action:
                policy_stable = False
                
        return policy_stable
    
    def quantum_bayesian_update(self, 
                              prior: np.ndarray, 
                              evidence: np.ndarray,
                              likelihood: Callable[[np.ndarray, np.ndarray], np.ndarray]) -> np.ndarray:
        """
        Perform Bayesian update using stochastic quantum methods.
        
        Args:
            prior: Prior probability distribution over states
            evidence: Observed evidence vector
            likelihood: Function that calculates likelihood of evidence given state
                        Takes (state, evidence) and returns likelihood
        
        Returns:
            Posterior probability distribution
        """
        # Initialize trajectories with prior distribution
        initial_trajectories = []
        
        for s in range(self.num_states):
            # Number of trajectories proportional to prior probability
            num_traj = max(1, int(prior[s] * self.num_trajectories))
            
            for _ in range(num_traj):
                # Create trajectory with single point
                point = ConfigurationPoint(
                    configuration=self.state_representations[s],
                    time=0.0
                )
                traj = Trajectory(
                    points=[point],
                    weight=prior[s] / num_traj
                )
                initial_trajectories.append(traj)
        
        # Define potential function based on likelihood
        def bayesian_potential(x):
            # Calculate likelihood for each state
            likelihoods = np.array([likelihood(self.state_representations[s], evidence) 
                                  for s in range(self.num_states)])
            
            # Find closest state
            distances = np.array([np.sum((x - self.state_representations[s])**2) 
                                 for s in range(self.num_states)])
            closest_state = np.argmin(distances)
            
            # Return negative log-likelihood as potential (lower is better)
            return -np.log(likelihoods[closest_state] + 1e-10)
        
        # Evolve trajectories using stochastic process
        updated_trajectories = []
        
        for traj in initial_trajectories:
            if not traj.points:
                continue
                
            # Get initial point from trajectory
            initial_state = traj.points[0].configuration
            
            # Evolve with Bayesian potential
            evolved_trajectories = self.simulator.evolve_stochastic_process(
                initial_state=initial_state,
                steps=20,
                potential_func=bayesian_potential
            )
            
            # Adjust weights based on original trajectory weight
            for evolved_traj in evolved_trajectories:
                evolved_traj.weight *= traj.weight
            
            updated_trajectories.extend(evolved_trajectories)
        
        # Calculate posterior from final trajectory distribution
        posterior = np.zeros(self.num_states)
        total_weight = sum(traj.weight for traj in updated_trajectories)
        
        for traj in updated_trajectories:
            if not traj.points:
                continue
                
            # Get final point in trajectory
            final_point = traj.points[-1].configuration
            
            # Find closest state
            distances = np.array([np.sum((final_point - self.state_representations[s])**2) 
                                for s in range(self.num_states)])
            closest_state = np.argmin(distances)
            
            # Add weight to posterior
            posterior[closest_state] += traj.weight
        
        # Normalize posterior
        if total_weight > 0:
            posterior /= total_weight
        else:
            # Fallback to uniform if no valid trajectories
            posterior = np.ones(self.num_states) / self.num_states
        
        return posterior
    
    def suggest_action(self, state_idx: int) -> int:
        """
        Suggest an action for the given state based on current policy.
        
        Args:
            state_idx: Current state index
        
        Returns:
            Suggested action index
        """
        return np.argmax(self.policy[state_idx])
    
    def uncertainty_quantification(self, state_idx: int) -> Dict[str, Any]:
        """
        Quantify uncertainty in the current state using quantum methods.
        
        Args:
            state_idx: Current state index
        
        Returns:
            Dictionary with uncertainty metrics
        """
        # Encode state into quantum representation
        quantum_state = self._encode_state_to_quantum(state_idx)
        
        # Evolve with no specific potential to explore state space
        trajectories = self.simulator.evolve_stochastic_process(
            initial_state=quantum_state,
            steps=50
        )
        
        # Extract final states from trajectories
        final_states = []
        for traj in trajectories:
            if traj.points:
                final_states.append(traj.points[-1].configuration)
        
        if not final_states:
            logger.warning(f"No valid trajectories for uncertainty quantification in state {state_idx}")
            return {
                'state_entropy': 0.0,
                'state_variance': 0.0,
                'value_uncertainty': 0.0,
                'action_entropy': 0.0
            }
        
        # Convert to array
        final_states_array = np.array(final_states)
        
        # Calculate state distribution
        state_distribution = np.zeros(self.num_states)
        for final_state in final_states_array:
            # Find closest state
            distances = np.array([np.sum((final_state - self.state_representations[s])**2) 
                                for s in range(self.num_states)])
            closest_state = np.argmin(distances)
            state_distribution[closest_state] += 1
        
        # Normalize
        state_distribution = state_distribution / np.sum(state_distribution)
        
        # Calculate state entropy
        state_entropy = -np.sum(state_distribution * np.log(state_distribution + 1e-10))
        
        # Calculate state variance (as spread around mean state)
        state_indices = np.arange(self.num_states)
        mean_state = np.sum(state_indices * state_distribution)
        state_variance = np.sum(((state_indices - mean_state) ** 2) * state_distribution)
        
        # Calculate value uncertainty
        value_uncertainty = np.sum(np.abs(self.value_function) * state_distribution) * state_entropy
        
        # Calculate action entropy (from policy)
        action_distribution = self.policy[state_idx]
        action_entropy = -np.sum(action_distribution * np.log(action_distribution + 1e-10))
        
        return {
            'state_entropy': state_entropy,
            'state_variance': state_variance,
            'value_uncertainty': value_uncertainty,
            'action_entropy': action_entropy
        }
    
    def save_model(self, filepath: str):
        """
        Save the decision process model to a file.
        
        Args:
            filepath: Path to save the model
        """
        model_data = {
            'num_states': self.num_states,
            'num_actions': self.num_actions,
            'num_trajectories': self.num_trajectories,
            'dt': self.dt,
            'hbar': self.hbar,
            'discount_factor': self.discount_factor,
            'seed': self.seed,
            'transition_probabilities': self.transition_probabilities,
            'rewards': self.rewards,
            'value_function': self.value_function,
            'policy': self.policy,
            'state_representations': self.state_representations
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model
        np.savez(filepath, **model_data)
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load_model(cls, filepath: str) -> 'QuantumStochasticDecisionProcess':
        """
        Load a decision process model from a file.
        
        Args:
            filepath: Path to the saved model
        
        Returns:
            Loaded QuantumStochasticDecisionProcess instance
        """
        model_data = np.load(filepath)
        
        # Create instance with saved parameters
        process = cls(
            num_states=model_data['num_states'],
            num_actions=model_data['num_actions'],
            num_trajectories=model_data['num_trajectories'],
            dt=model_data['dt'],
            hbar=model_data['hbar'],
            discount_factor=model_data['discount_factor'],
            seed=model_data['seed']
        )
        
        # Restore additional parameters
        process.transition_probabilities = model_data['transition_probabilities']
        process.rewards = model_data['rewards']
        process.value_function = model_data['value_function']
        process.policy = model_data['policy']
        process.state_representations = model_data['state_representations']
        
        logger.info(f"Model loaded from {filepath}")
        return process 