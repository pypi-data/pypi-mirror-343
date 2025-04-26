#!/usr/bin/env python3

"""
Uncertainty Metrics Module

This module provides a data structure to store and manipulate uncertainty metrics
for quantum measurements and AI predictions.
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class UncertaintyMetrics:
    """Metrics quantifying uncertainty in quantum measurements."""

    # Statistical uncertainties
    shot_noise: float = 0.0
    standard_error: float = 0.0
    confidence_interval: Tuple[float, float] = (0.0, 0.0)

    # Quantum-specific uncertainties
    entanglement_entropy: float = 0.0
    measurement_basis_error: float = 0.0
    gate_error_estimate: float = 0.0

    # Composite metrics
    total_uncertainty: Optional[float] = None

    # Additional statistical metrics
    variance: float = 0.0
    coefficient_of_variation: float = 0.0
    margin_of_error: float = 0.0

    # Quantum noise metrics
    decoherence_estimate: float = 0.0
    readout_error: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert tuple to list for JSON serialization
        data["confidence_interval"] = list(data["confidence_interval"])
        return data

    # Add alias for to_dictionary to maintain backward compatibility
    def to_dictionary(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (alias for to_dict)."""
        return self.to_dict()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UncertaintyMetrics":
        """Create from dictionary."""
        if "confidence_interval" in data and isinstance(
            data["confidence_interval"], list
        ):
            data["confidence_interval"] = tuple(data["confidence_interval"])
        return cls(**data)

    # Add alias for from_dictionary to maintain backward compatibility
    @classmethod
    def from_dictionary(cls, data: Dict[str, Any]) -> "UncertaintyMetrics":
        """Create from dictionary (alias for from_dict)."""
        return cls.from_dict(data)

    def combine_with(self, other: "UncertaintyMetrics") -> "UncertaintyMetrics":
        """Combine two uncertainty metrics."""
        # For most metrics, take the max value as a conservative approach
        return UncertaintyMetrics(
            shot_noise=max(self.shot_noise, other.shot_noise),
            standard_error=max(self.standard_error, other.standard_error),
            confidence_interval=(
                min(self.confidence_interval[0], other.confidence_interval[0]),
                max(self.confidence_interval[1], other.confidence_interval[1]),
            ),
            entanglement_entropy=max(
                self.entanglement_entropy, other.entanglement_entropy
            ),
            measurement_basis_error=self.measurement_basis_error
            + other.measurement_basis_error,
            gate_error_estimate=max(
                self.gate_error_estimate, other.gate_error_estimate
            ),
            total_uncertainty=self.total_uncertainty + other.total_uncertainty,
            variance=max(self.variance, other.variance),
            coefficient_of_variation=max(
                self.coefficient_of_variation, other.coefficient_of_variation
            ),
            margin_of_error=max(self.margin_of_error, other.margin_of_error),
            decoherence_estimate=max(
                self.decoherence_estimate, other.decoherence_estimate
            ),
            readout_error=self.readout_error + other.readout_error,
        )

    def calculate_total_uncertainty(self, weights=None) -> float:
        """Calculate composite uncertainty from all components.

        Args:
            weights: Optional dictionary of weights for different uncertainty components

        Returns:
            float: Total uncertainty as a weighted combination of all metrics.
        """
        if weights is None:
            # For the unweighted version, use root sum of squares
            total = np.sqrt(
                self.shot_noise**2 +
                self.standard_error**2 +
                self.gate_error_estimate**2 +
                self.entanglement_entropy**2 +
                self.measurement_basis_error**2 +
                self.readout_error**2
            )
        else:
            # For the weighted version, multiply each component by its weight before computing root sum of squares
            total = np.sqrt(
                (weights.get('shot_noise', 1.0) * self.shot_noise)**2 +
                (weights.get('standard_error', 1.0) * self.standard_error)**2 +
                (weights.get('gate_error_estimate', 1.0) * self.gate_error_estimate)**2 +
                (weights.get('entanglement_entropy', 1.0) * self.entanglement_entropy)**2 +
                (weights.get('measurement_basis_error', 1.0) * self.measurement_basis_error)**2 +
                (weights.get('readout_error', 1.0) * self.readout_error)**2
            )

        # Update total_uncertainty field
        self.total_uncertainty = total
        return total

    def estimate_from_counts(
        self, counts: Dict[str, int], shots: int
    ) -> "UncertaintyMetrics":
        """Estimate uncertainty metrics from measurement counts.

        Args:
            counts: Dictionary of bitstring counts
            shots: Number of measurement shots

        Returns:
            Updated UncertaintyMetrics instance
        """
        # Calculate basic statistical metrics
        if shots > 0:
            # Shot noise estimated as 1/sqrt(shots)
            self.shot_noise = 1.0 / np.sqrt(shots)

            # Calculate variance and standard error for the most probable outcome
            if counts:
                max_count = max(counts.values())
                probability = max_count / shots
                self.variance = probability * (1 - probability) / shots
                self.standard_error = np.sqrt(self.variance)

                # Confidence interval (95%)
                z_score = 1.96  # For 95% confidence
                margin = z_score * self.standard_error
                self.margin_of_error = margin
                self.confidence_interval = (
                    max(0.0, probability - margin),
                    min(1.0, probability + margin),
                )

                # Coefficient of variation
                if probability > 0:
                    self.coefficient_of_variation = self.standard_error / probability

        # Update total uncertainty
        self.calculate_total_uncertainty()

        return self

    def visualize_radar(self, ax=None, title="Uncertainty Metrics"):
        """Create a radar chart of uncertainty metrics.

        Args:
            ax: Matplotlib axis to draw on (creates new figure if None)
            title: Title for the plot

        Returns:
            Matplotlib figure
        """
        # Create figure if ax not provided
        if ax is None:
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, polar=True)
        else:
            fig = ax.figure

        # Define metrics to display
        metrics = [
            "Shot Noise",
            "Standard Error",
            "Variance",
            "Entanglement Entropy",
            "Measurement Error",
            "Gate Error",
            "Decoherence",
            "Readout Error",
        ]

        # Get corresponding values
        values = [
            self.shot_noise,
            self.standard_error,
            self.variance,
            self.entanglement_entropy,
            self.measurement_basis_error,
            self.gate_error_estimate,
            self.decoherence_estimate,
            self.readout_error,
        ]

        # Normalize values to 0-1 range for visualization
        max_val = max(values) if max(values) > 0 else 1
        values_norm = [v / max_val for v in values]

        # Number of metrics
        N = len(metrics)

        # Create angles for each metric
        angles = [n / N * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        values_norm += values_norm[:1]  # Close the loop

        # Draw the plot
        ax.plot(angles, values_norm, linewidth=2, linestyle="solid")
        ax.fill(angles, values_norm, alpha=0.25)

        # Fix axis to go in the right order and start at the top
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        # Draw axis lines for each metric
        plt.xticks(angles[:-1], metrics)

        # Draw y-axis labels with original values
        ax.set_rlabel_position(0)
        max_tick = max_val if max_val > 0 else 1.0
        plt.yticks(
            [0.25, 0.5, 0.75],
            [f"{0.25*max_tick:.3f}", f"{0.5*max_tick:.3f}", f"{0.75*max_tick:.3f}"],
            color="grey",
            size=8,
        )
        plt.ylim(0, 1)

        # Add title
        plt.title(title, size=11, y=1.1)

        return fig
