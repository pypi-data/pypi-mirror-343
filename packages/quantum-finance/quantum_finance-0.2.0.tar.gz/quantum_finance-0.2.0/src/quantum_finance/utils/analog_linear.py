"""
analog_linear.py

Wrapper to use IBM's aihwkit AnalogLinear for analog in-memory computing acceleration.
Falls back to torch.nn.Linear if aihwkit is not installed.
"""
from __future__ import annotations

import torch
import torch.nn as nn
from typing import Any
import os

# Determine if analog IMC backend is enabled via environment variable
_ANALOG_ENABLED = os.environ.get("ANALOG_BACKEND_ENABLED", "false").lower() in ("1", "true", "yes")

# Try to import aihwkit's analog linear layer
try:
    from aihwkit.nn import AnalogLinear as _AiAnalogLinear  # type: ignore
    _HAS_AIHWKIT = True
except ImportError:
    _HAS_AIHWKIT = False

class AnalogLinear(nn.Module):
    """
    Analog-aware Linear layer. Uses aihwkit's AnalogLinear backend if available,
    otherwise falls back to standard torch.nn.Linear.
    
    Parameters
    ----------
    in_features : int
        Size of each input sample.
    out_features : int
        Size of each output sample.
    bias : bool, default True
        If set to False, the layer will not learn an additive bias.
    rpu_config : Any, optional
        Configuration for the analog tile (aihwkit-specific). Only used if aihwkit is installed.
    """
    def __init__(
        self,
        in_features: int,
        out_features: int,
        bias: bool = True,
        rpu_config: Any = None,
        **kwargs: Any,  # Accept extra kwargs (e.g., dtype) for compatibility
    ) -> None:
        super().__init__()
        # Use analog IMC only if aihwkit is installed and analog flag is enabled
        if _HAS_AIHWKIT and _ANALOG_ENABLED:
            # Use the aihwkit analog linear layer
            self.layer = _AiAnalogLinear(
                in_features=in_features,
                out_features=out_features,
                bias=bias,
                rpu_config=rpu_config,
            )
        else:
            # Fallback to CPU/GPU digital implementation
            self.layer = nn.Linear(in_features, out_features, bias=bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)

    def extra_repr(self) -> str:
        base = f"in_features={self.layer.in_features}, out_features={self.layer.out_features}, bias={self.layer.bias is not None}"
        if _HAS_AIHWKIT and _ANALOG_ENABLED:
            return f"AnalogLinear({base}, analog_backend=aihwkit)"
        else:
            return f"AnalogLinear({base}, analog_backend=torch)"

# Monkey-patch torch.nn.Linear to use AnalogLinear globally when analog backend is enabled
if _HAS_AIHWKIT and _ANALOG_ENABLED:
    import torch.nn as _nn
    _nn.Linear = AnalogLinear  # type: ignore 