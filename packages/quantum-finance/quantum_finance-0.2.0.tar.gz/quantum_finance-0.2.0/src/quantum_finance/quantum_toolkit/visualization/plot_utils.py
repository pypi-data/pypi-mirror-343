"""
Visualization Utilities for Stochastic Quantum Simulator

This module provides functions to plot results from the StochasticQuantumSimulator,
including trajectory paths and phase/confidence evolution.
"""

import matplotlib.pyplot as plt
# import matplotlib.cm as cm # Remove this import
import numpy as np
from typing import List, Optional, TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from ..stochastic.stochastic_quantum_simulator import Trajectory, StateEstimate 

# Assuming Trajectory and StateEstimate are defined elsewhere, 
# potentially import them or define simplified versions for type hints if needed.
# from ..stochastic.stochastic_quantum_simulator import Trajectory, StateEstimate 
# For now, use simple type hints
# Trajectory = 'Trajectory' 
# StateEstimate = 'StateEstimate' 

def plot_trajectory_paths(trajectories: List['Trajectory'], # Keep string hint for runtime
                          max_trajectories: Optional[int] = 10,
                          title: str = "Stochastic Trajectory Paths",
                          dims_to_plot: tuple = (0, 1),
                          output_file: Optional[str] = None):
    """
    Plots the configuration space paths of stochastic trajectories.

    Args:
        trajectories: List of Trajectory objects.
        max_trajectories: Maximum number of trajectories to plot (default: 10). 
                          If None, plots all.
        title: Title for the plot.
        dims_to_plot: Tuple indicating which dimensions to plot (e.g., (0, 1) for x-y). 
                      Only supports 1D (plots dim 0 vs time) and 2D plots currently.
        output_file: Optional path to save the figure. If None, shows the plot.
    """
    if not trajectories:
        print("No trajectories to plot.")
        return

    config_dim = trajectories[0].points[0].configuration.shape[0]
    
    plt.figure(figsize=(10, 8))
    
    num_to_plot = min(max_trajectories if max_trajectories is not None else len(trajectories), len(trajectories))
    
    # Use a colormap for trajectories via plt.get_cmap
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, num_to_plot)) # Use cmap function

    for i, traj in enumerate(trajectories[:num_to_plot]):
        times = np.array([p.time for p in traj.points])
        configs = np.array([p.configuration for p in traj.points])

        if config_dim == 1 or len(dims_to_plot) == 1:
            # Plot configuration vs time for 1D
            dim_idx = dims_to_plot[0] if dims_to_plot else 0
            plt.plot(times, configs[:, dim_idx], color=colors[i], alpha=0.7)
            plt.xlabel("Time")
            plt.ylabel(f"Configuration (Dimension {dim_idx})")
        elif config_dim >= 2 and len(dims_to_plot) == 2:
             # Plot specified 2D projection
             dim_x, dim_y = dims_to_plot
             if dim_x >= config_dim or dim_y >= config_dim:
                 print(f"Warning: Specified dimensions {dims_to_plot} out of bounds for config_dim {config_dim}. Skipping trajectory {i}.")
                 continue
             plt.plot(configs[:, dim_x], configs[:, dim_y], color=colors[i], alpha=0.7, marker='.', linestyle='-', markersize=2)
             # Mark start and end points
             plt.scatter(configs[0, dim_x], configs[0, dim_y], color=colors[i], marker='o', s=50, label=f'Traj {i} Start' if i < 5 else None) # Label first few starts
             plt.scatter(configs[-1, dim_x], configs[-1, dim_y], color=colors[i], marker='x', s=50)
             plt.xlabel(f"Configuration (Dimension {dim_x})")
             plt.ylabel(f"Configuration (Dimension {dim_y})")
        else:
            print(f"Plotting for {config_dim}D configuration space with dims_to_plot={dims_to_plot} not supported yet. Skipping.")
            return # Stop if dimension handling is not supported

    plt.title(title)
    if config_dim >= 2 and len(dims_to_plot) == 2:
        plt.legend() # Only show legend for 2D plots with start markers
    plt.grid(True, alpha=0.3)
    
    if output_file:
        plt.savefig(output_file)
        print(f"Trajectory plot saved to {output_file}")
    else:
        plt.show()
    plt.close() # Close the figure


def plot_phase_confidence(estimates_history: List[List['StateEstimate']], # Keep string hint
                          trajectory_indices: Optional[List[int]] = None,
                          max_trajectories: int = 5,
                          title: str = "Phase and Confidence Evolution",
                          output_file: Optional[str] = None):
    """
    Plots the estimated phase and confidence for selected trajectories over time.

    Args:
        estimates_history: List of lists, where each inner list contains 
                           StateEstimate objects for a single trajectory over time.
        trajectory_indices: Specific indices of trajectories to plot. If None, plots
                            up to max_trajectories.
        max_trajectories: Maximum number of trajectories to plot if indices not given.
        title: Title for the plot.
        output_file: Optional path to save the figure. If None, shows the plot.
    """
    if not estimates_history:
        print("No estimates history to plot.")
        return

    num_total_trajectories = len(estimates_history)
    if trajectory_indices is None:
        indices_to_plot = list(range(min(max_trajectories, num_total_trajectories)))
    else:
        indices_to_plot = [idx for idx in trajectory_indices if 0 <= idx < num_total_trajectories]

    if not indices_to_plot:
        print("No valid trajectory indices selected for plotting.")
        return
        
    # Determine the number of time steps from the first valid trajectory
    num_steps = 0
    for i in indices_to_plot:
        if estimates_history[i]:
            num_steps = len(estimates_history[i])
            break
    if num_steps == 0:
        print("Could not determine number of steps from selected trajectories.")
        return
        
    time_axis = np.arange(num_steps) # Assuming constant dt for step count

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Use a colormap via plt.get_cmap
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(indices_to_plot))) # Use cmap function

    for i, traj_idx in enumerate(indices_to_plot):
        if not estimates_history[traj_idx]:
             print(f"Warning: Trajectory {traj_idx} has no estimates. Skipping.")
             continue
             
        # Ensure estimates list matches time axis length, pad with NaN if shorter
        current_estimates = estimates_history[traj_idx]
        if len(current_estimates) < num_steps:
            # Need the actual StateEstimate class for instantiation if possible,
            # otherwise, we need a placeholder or handle this differently.
            # Assuming StateEstimate is importable for now via TYPE_CHECKING
            # or globally available.
            # If not, we might need to create dummy objects or handle plotting differently.
            # Let's assume we can access a StateEstimate-like structure for now.
            # We cannot directly instantiate from the string hint.
            # Fallback: Plot only available data without padding, or use dicts? 
            # For now, let's plot what we have and adjust the time axis.
            current_time_axis = time_axis[:len(current_estimates)]
            # This might make plots inconsistent if trajectories end early.
            # A better approach might be needed depending on use case.
            # --- Original padding attempt (commented out due to instantiation issue) ---
            # padding = [StateEstimate(phase=np.nan, confidence=np.nan)] * (num_steps - len(current_estimates))
            # current_estimates.extend(padding)
        elif len(current_estimates) > num_steps:
             current_estimates = current_estimates[:num_steps] # Truncate if longer
             current_time_axis = time_axis
        else:
            current_time_axis = time_axis # Full time axis

        phases = np.array([est.phase for est in current_estimates])
        confidences = np.array([est.confidence for est in current_estimates])

        # Unwrap phases for smoother plotting
        # Handle potential NaNs before unwrapping
        valid_phase_indices = ~np.isnan(phases)
        if np.any(valid_phase_indices):
            unwrapped_phases = np.unwrap(phases[valid_phase_indices])
        else:
            unwrapped_phases = np.array([]) # Empty if no valid phases

        # Adjust time axis for plotting unwrapped phases and confidences
        plot_time_axis_phase = current_time_axis[valid_phase_indices]
        plot_time_axis_conf = current_time_axis # Plot confidence over original axis length
        plot_confidences = confidences # Use original confidences (with NaNs if any)

        if unwrapped_phases.size > 0:
            axes[0].plot(plot_time_axis_phase, unwrapped_phases, label=f"Traj {traj_idx}", color=colors[i], alpha=0.8)
        axes[1].plot(plot_time_axis_conf, plot_confidences, label=f"Traj {traj_idx}", color=colors[i], alpha=0.8)

    axes[0].set_ylabel("Estimated Phase (Unwrapped)")
    axes[0].set_title("Phase Evolution")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].set_ylabel("Estimation Confidence")
    axes[1].set_title("Confidence Evolution")
    axes[1].set_xlabel("Time Step")
    axes[1].set_ylim(0, 1.1) # Confidence is typically between 0 and 1
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.suptitle(title)
    plt.tight_layout(rect=(0, 0.03, 1, 0.95)) # Use tuple for rect

    if output_file:
        plt.savefig(output_file)
        print(f"Phase/Confidence plot saved to {output_file}")
    else:
        plt.show()
    plt.close() # Close the figure

# Example usage (assuming simulator instance 'sim' and estimates 'est_hist'):
# from src.quantum_toolkit.visualization.plot_utils import plot_trajectory_paths, plot_phase_confidence
# plot_trajectory_paths(sim.trajectories, max_trajectories=5)
# plot_phase_confidence(est_hist, max_trajectories=5) 