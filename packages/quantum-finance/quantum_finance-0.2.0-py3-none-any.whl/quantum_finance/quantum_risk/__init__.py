"""
Quantum Risk Assessment Package

A comprehensive framework for quantum-enhanced cryptocurrency risk assessment,
leveraging quantum computing for more sophisticated modeling of market dependencies.

Components:
- CryptoDataFetcher: Fetch cryptocurrency market data
- RiskMetricsCalculator: Calculate classical risk metrics
- QuantumEnhancedCryptoRiskAnalyzer: Core risk analysis with quantum enhancement
- ReportGenerator: Generate analysis reports

Author: Quantum-AI Team
"""

from .data_fetcher import CryptoDataFetcher
from .risk_metrics import RiskMetricsCalculator
from .report_generator import ReportGenerator
from .analyzer import QuantumEnhancedCryptoRiskAnalyzer

# ----------------------------------------------------------------------------
# Backward‑compatibility aliases
# ---------------------------------------------------------------------------
# Many modules still reference the historic package names `quantum_risk.*` or
# `src.quantum_finance.quantum_risk.*`.  To avoid widespread breakages while we
# complete the refactor, expose those names as runtime aliases that point to
# the canonical `quantum_finance.quantum_risk` package.  This approach lets us
# migrate incrementally without disrupting downstream imports, and can be
# removed once all references have been updated.
import importlib
import sys

# Map top‑level alias `quantum_risk` → `quantum_finance.quantum_risk`
sys.modules.setdefault('quantum_risk', sys.modules[__name__])
# Ensure subpackages are also reachable through the alias
_subpackages = ['utils', 'configs']
for _sub in _subpackages:
    full_name = f'{__name__}.{_sub}'
    try:
        module = importlib.import_module(full_name)
        sys.modules.setdefault(f'quantum_risk.{_sub}', module)
    except ModuleNotFoundError:
        # Subpackage may not exist; skip gracefully
        pass

# Also alias the previous fully‑qualified path used during transition
sys.modules.setdefault('src.quantum_finance.quantum_risk', sys.modules[__name__])

__all__ = [
    'CryptoDataFetcher',
    'RiskMetricsCalculator', 
    'ReportGenerator',
    'QuantumEnhancedCryptoRiskAnalyzer'
] 