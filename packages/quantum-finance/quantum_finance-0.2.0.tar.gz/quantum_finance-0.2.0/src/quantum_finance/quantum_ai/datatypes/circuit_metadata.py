#!/usr/bin/env python3

"""
Circuit Metadata Module

This module provides a data structure to store metadata about quantum circuit executions.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict


@dataclass
class CircuitMetadata:
    """Metadata about a quantum circuit execution."""

    num_qubits: int
    circuit_depth: int
    gate_counts: Dict[str, int] = field(default_factory=dict)
    topology: str = "linear"
    optimization_level: int = 1
    simulation_method: str = "statevector"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

    # Add alias for to_dictionary to maintain backward compatibility
    def to_dictionary(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization (alias for to_dict)."""
        return self.to_dict()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CircuitMetadata":
        """Create from dictionary."""
        return cls(**data)

    # Add alias for from_dictionary to maintain backward compatibility
    @classmethod
    def from_dictionary(cls, data: Dict[str, Any]) -> "CircuitMetadata":
        """Create from dictionary (alias for from_dict)."""
        return cls.from_dict(data)
