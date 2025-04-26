"""
Quantum Diffusion Models Package

This package implements quantum-enhanced diffusion models for generative tasks.
It includes implementations of Q-Dense and QU-Net architectures
based on quantum circuits.

Components:
- QDenseDiffusion: Dense quantum circuit implementation for diffusion models
- QUNetDiffusion: U-Net inspired architecture with quantum convolutions
- Examples for MNIST and CIFAR-10 data generation

Note:
This is an experimental implementation focused on exploring parameter efficiency
and performance characteristics of quantum diffusion models.
"""

from experimental.quantum_diffusion.qdense_model import QDenseDiffusion
from experimental.quantum_diffusion.qunet_model import QUNetDiffusion, QuantumConvolution

__all__ = ['QDenseDiffusion', 'QUNetDiffusion', 'QuantumConvolution'] 