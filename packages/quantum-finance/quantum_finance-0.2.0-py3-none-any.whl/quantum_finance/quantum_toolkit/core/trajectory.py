"""
Trajectory Representation Module

This module defines the core trajectory representations for quantum simulations.
"""

import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class ConfigurationPoint:
    """Represents a point in configuration space with associated time."""
    configuration: np.ndarray
    time: float
    phase: float = 0.0
    coherence: float = 1.0  # Coherence parameter for phase stability

@dataclass
class Trajectory:
    """Represents a stochastic trajectory in configuration space."""
    points: List[ConfigurationPoint]
    weight: float = 1.0
    id: int = 0
    neighbors: List[int] = field(default_factory=list)  # Store indices of neighboring trajectories for phase coherence 