# src/quantum_finance/quantum_toolkit/hybrid/regime_detection.py
from src.quantum_finance.quantum_risk.utils.logging_util import setup_logger
import numpy as np

class MarketRegimeDetector:
    """
    Identifies market regimes to guide the adaptive weighting of stochastic and neural components.
    """

    def __init__(self, config=None):
        """
        Initialize the market regime detector.
        
        Args:
            config: Optional dict with regime thresholds or model parameters.
        """
        default_config = {
            'volatility_window': 20,
            'volatility_thresholds': {
                'low': 0.01,
                'high': 0.05
            },
            'regime_weights': {
                'low': {'stochastic_weight': 0.3, 'neural_weight': 0.7},
                'medium': {'stochastic_weight': 0.5, 'neural_weight': 0.5},
                'high': {'stochastic_weight': 0.7, 'neural_weight': 0.3},
            }
        }
        # Merge user config over defaults
        self.config = default_config
        if config:
            self.config.update(config)
        self.logger = setup_logger(__name__)
        self.logger.info(f"Initialized MarketRegimeDetector with config: {self.config}")

    def detect_regime(self, market_data):
        """
        Detect the current market regime from market_data.
        
        Args:
            market_data: DataFrame or array with market price or return series.

        Returns:
            regime: str, one of 'low', 'medium', 'high'.
        """
        # Convert input to 1D numpy array of prices
        try:
            prices = np.array(market_data, dtype=float).flatten()
        except Exception as e:
            self.logger.error(f"Invalid market_data input: {e}")
            raise
        if prices.size < 2:
            self.logger.warning("Insufficient data to detect regime; defaulting to 'medium'")
            return 'medium'
        # Compute returns and volatility
        returns = np.diff(prices) / prices[:-1]
        window = min(self.config.get('volatility_window', len(returns)), returns.size)
        vol = float(np.std(returns[-window:]))
        thresholds = self.config.get('volatility_thresholds', {})
        low_th = thresholds.get('low', 0.0)
        high_th = thresholds.get('high', float('inf'))
        if vol <= low_th:
            regime = 'low'
        elif vol >= high_th:
            regime = 'high'
        else:
            regime = 'medium'
        self.logger.info(f"Detected {regime} volatility regime (vol={vol:.4f})")
        return regime

    def get_recommended_weights(self, regime):
        """
        Get recommended stochastic and neural weights for a given regime.
        
        Args:
            regime: str, detected market regime.

        Returns:
            Dict with keys 'stochastic_weight' and 'neural_weight'.
        """
        # Retrieve weight mapping for regimes
        weights_map = self.config.get('regime_weights', {})
        if regime not in weights_map:
            self.logger.warning(f"Unknown regime '{regime}'; defaulting to 'medium' weights")
            regime = 'medium'
        weights = weights_map.get(regime, {'stochastic_weight': 0.5, 'neural_weight': 0.5})
        self.logger.info(f"Recommended weights for regime '{regime}': {weights}")
        return weights 