#!/usr/bin/env python3

"""
Setup configuration for Quantum Finance platform
"""

from setuptools import setup, find_packages
import os

# Read long description from README
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="quantum_finance",
    version="0.2.0",
    description="Quantum-enhanced financial analysis and trading platform",
    author="Quantum Finance Team",
    author_email="quantum@example.com",
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    extras_require={
        # Core dependencies
        "core": [
            "numpy>=1.22.0,<2.0.0",
            "scipy>=1.8.0,<2.0.0",
            "pandas>=2.0.0,<3.0.0",
            "matplotlib>=3.5.0,<4.0.0",
            "python-dotenv>=0.19.0,<1.0.0",
            "pyyaml>=6.0.0,<7.0.0",
            "tqdm>=4.62.0,<5.0.0",
            "typing-extensions>=4.9.0", # Pin for TypeIs compatibility
            "torch>=2.0.0,<3.0.0",     # Added PyTorch dependency
            "numba>=0.58.0,<1.0.0",    # Added Numba for performance
            "seaborn>=0.12.0,<0.13.0", # Added Seaborn for visualization
            "yfinance>=0.2.0,<0.3.0",   # Added yfinance
            "plotly>=5.0.0,<6.0.0",     # Added Plotly
            "memory_profiler>=0.60.0,<0.62.0", # Added memory_profiler
            "hypothesis>=6.0.0,<7.0.0", # Added hypothesis
            "gudhi>=3.5.0,<4.0.0",      # Added gudhi for topological analysis
            "aihwkit>=0.6.0,<1.0.0",    # Added for neuromorphic analog IMC support
            # "tensorflow-metal", # Temporarily removed due to installation issues
        ],
        # Quantum dependencies
        "quantum": [
            "qiskit>=1.4.0,<1.5.0", # Downgraded qiskit
            "qiskit-aer>=0.17.0,<0.18.0",
            "qiskit-ibm-runtime>=0.37.0,<0.38.0",
            "qiskit-ibm-provider>=0.11.0,<0.12.0",
            "qiskit-algorithms>=0.3.0,<0.4.0",
        ],
        # Development dependencies
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "pytest-asyncio>=0.18.0,<0.19.0",
            "pytest-mock>=3.6.0,<4.0.0",
            "pytest-cov>=3.0.0,<4.0.0",
            "black>=22.0.0,<23.0.0",
            "flake8>=5.0.0,<6.0.0",
            "mypy>=0.950,<1.0.0",
            "isort>=5.10.0,<6.0.0",
            "Flask~=2.3.0",            # Pin for Werkzeug compatibility
            "Werkzeug~=2.3.0",         # Pin for Flask compatibility
            "Flask-Cors>=4.0.0,<5.0.0", # Add Flask-Cors dependency
            "Flask-Limiter>=3.0.0,<4.0.0", # Add Flask-Limiter dependency
            "pipdeptree>=2.0.0,<3.0.0", # Add pipdeptree for future use
        ],
        # Documentation dependencies
        "docs": [
            "sphinx>=5.0.0,<6.0.0",
            "sphinx-rtd-theme>=1.0.0,<2.0.0",
            "nbsphinx>=0.8.0,<0.9.0",
            "jupyterlab>=3.4.0,<4.0.0",
        ],
        # All dependencies (Ensure this includes 'core' now)
        "all": [
            # Core
            "numpy>=1.22.0,<2.0.0",
            "scipy>=1.8.0,<2.0.0",
            "pandas>=2.0.0,<3.0.0",
            "matplotlib>=3.5.0,<4.0.0",
            "python-dotenv>=0.19.0,<1.0.0",
            "pyyaml>=6.0.0,<7.0.0",
            "tqdm>=4.62.0,<5.0.0",
            "typing-extensions>=4.9.0", # Pin for TypeIs compatibility
            "torch>=2.0.0,<3.0.0",     # Added PyTorch dependency
            "numba>=0.58.0,<1.0.0",    # Added Numba for performance
            "seaborn>=0.12.0,<0.13.0", # Added Seaborn for visualization
            "yfinance>=0.2.0,<0.3.0",   # Added yfinance
            "plotly>=5.0.0,<6.0.0",     # Added Plotly
            "memory_profiler>=0.60.0,<0.62.0", # Added memory_profiler
            "hypothesis>=6.0.0,<7.0.0", # Added hypothesis
            "gudhi>=3.5.0,<4.0.0",      # Added gudhi for topological analysis
            # "tensorflow-metal", # Temporarily removed due to installation issues
            # Quantum
            "qiskit>=1.4.0,<1.5.0", # Downgraded qiskit
            "qiskit-aer>=0.17.0,<0.18.0",
            "qiskit-ibm-runtime>=0.37.0,<0.38.0",
            "qiskit-ibm-provider>=0.11.0,<0.12.0",
            "qiskit-algorithms>=0.3.0,<0.4.0",
            # Dev
            "pytest>=7.0.0,<8.0.0",
            "pytest-asyncio>=0.18.0,<0.19.0",
            "pytest-mock>=3.6.0,<4.0.0",
            "pytest-cov>=3.0.0,<4.0.0",
            "black>=22.0.0,<23.0.0",
            "flake8>=5.0.0,<6.0.0",
            "mypy>=0.950,<1.0.0",
            "isort>=5.10.0,<6.0.0",
            "Flask~=2.3.0",            # Pin for Werkzeug compatibility
            "Werkzeug~=2.3.0",         # Pin for Flask compatibility
            "Flask-Cors>=4.0.0,<5.0.0", # Add Flask-Cors dependency
            "Flask-Limiter>=3.0.0,<4.0.0", # Add Flask-Limiter dependency
            "pipdeptree>=2.0.0,<3.0.0", # Add pipdeptree for future use
            # Docs
            "sphinx>=5.0.0,<6.0.0",
            "sphinx-rtd-theme>=1.0.0,<2.0.0",
            "nbsphinx>=0.8.0,<0.9.0",
            "jupyterlab>=3.4.0,<4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Office/Business :: Financial",
    ],
    entry_points={
        "console_scripts": [
            "qtrading=quantum.cli:main",
            "qrisk=quantum.cli.risk:main",
            "prisk=src.real_time_risk_monitor:main",
            "pdata=src.unified_data_pipeline:main",
        ],
    },
)