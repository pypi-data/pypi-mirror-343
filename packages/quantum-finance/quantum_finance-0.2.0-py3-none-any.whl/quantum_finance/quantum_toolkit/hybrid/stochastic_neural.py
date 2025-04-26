# src/quantum_finance/quantum_toolkit/hybrid/stochastic_neural.py
import numpy as np
from src.quantum_finance.quantum_risk.utils.logging_util import setup_logger
from src.quantum_finance.quantum_toolkit.hybrid.regime_detection import MarketRegimeDetector

class StochasticNeuralBridge:
    """
    Connects a stochastic simulator with a neural network and manages their interaction.
    """

    def __init__(self, stochastic_simulator, neural_network, config=None):
        """
        Initialize the stochastic-neural bridge.
        
        Args:
            stochastic_simulator: An object implementing simulate and predict interfaces
            neural_network: An object implementing condition_on_trajectories and predict interfaces
            config: Optional dict with keys 'stochastic_weight', 'neural_weight', 
                    'adaptive_weighting', 'uncertainty_threshold'
        """
        self.stochastic_simulator = stochastic_simulator
        self.neural_network = neural_network
        default_config = {
            'stochastic_weight': 0.5,
            'neural_weight': 0.5,
            'adaptive_weighting': True,
            'uncertainty_threshold': 0.2,
            'use_regime_weights': False,
            'regime_detector_config': None
        }
        # Merge provided config over defaults
        self.config = default_config.copy()
        if config:
            self.config.update(config)
        # Instantiate regime detector
        self.regime_detector = MarketRegimeDetector(self.config.get('regime_detector_config'))
        self.logger = setup_logger(__name__)
        self.logger.info("Initialized StochasticNeuralBridge with weights: "
                         f"stochastic={self.config['stochastic_weight']}, "
                         f"neural={self.config['neural_weight']}")

    def predict(self, market_data):
        """
        Generate a combined prediction by coordinating stochastic and neural components.

        Args:
            market_data: Input data for prediction (e.g., pandas DataFrame or equivalent)

        Returns:
            Dict with 'predicted_price', 'confidence', and 'components' breakdown.
        """
        # Optionally adjust weights based on detected regime
        if self.config.get('use_regime_weights', False):
            regime = self.regime_detector.detect_regime(market_data)
            weights = self.regime_detector.get_recommended_weights(regime)
            self.config['stochastic_weight'] = weights['stochastic_weight']
            self.config['neural_weight'] = weights['neural_weight']
            self.logger.info(f"Applied regime '{regime}' weights: {weights}")
        # 1. Generate stochastic trajectories (fallback to simulate if necessary)
        if hasattr(self.stochastic_simulator, 'simulate_trajectories'):
            trajectories = self.stochastic_simulator.simulate_trajectories(market_data)
        elif hasattr(self.stochastic_simulator, 'simulate'):
            sim_result = self.stochastic_simulator.simulate(market_data)
            trajectories = [sim_result]
        else:
            raise AttributeError("Simulator must implement simulate_trajectories or simulate")

        # 2. Condition neural network on those trajectories
        self.neural_network.condition_on_trajectories(trajectories)

        # 3. Generate neural prediction from conditioned network
        neural_prediction = self.neural_network.predict(market_data)

        # 4. Generate stochastic prediction from simulator
        stochastic_prediction = self.stochastic_simulator.predict(market_data)

        # 5. Combine predictions based on weights
        combined_prediction = self._combine_predictions(
            stochastic_prediction,
            neural_prediction
        )
        return combined_prediction

    def _combine_predictions(self, stochastic_prediction, neural_prediction):
        """
        Combine stochastic and neural predictions based on weights.

        Args:
            stochastic_prediction: Dict with keys 'predicted_price' and 'confidence'
            neural_prediction: Dict with same keys

        Returns:
            Combined prediction dictionary.
        """
        stochastic_weight = self.config['stochastic_weight']
        neural_weight = self.config['neural_weight']
        total_weight = stochastic_weight + neural_weight
        if total_weight == 0:
            self.logger.error("Total weight is zero, cannot combine predictions.")
            raise ValueError("Invalid weights: sum to zero.")
        sw = stochastic_weight / total_weight
        nw = neural_weight / total_weight

        combined_price = (stochastic_prediction['predicted_price'] * sw +
                          neural_prediction['predicted_price'] * nw)
        combined_confidence = (stochastic_prediction['confidence'] * sw +
                               neural_prediction['confidence'] * nw)

        return {
            'predicted_price': combined_price,
            'confidence': combined_confidence,
            'components': {
                'stochastic': stochastic_prediction,
                'neural': neural_prediction,
                'weights': {'stochastic': sw, 'neural': nw}
            }
        }

    def update_weights(self, market_data, actual_outcome):
        """
        Adaptively update component weights based on prediction errors.
        """
        if not self.config.get('adaptive_weighting', False):
            return
        # Generate individual predictions
        stochastic_prediction = self.stochastic_simulator.predict(market_data)
        neural_prediction = self.neural_network.predict(market_data)
        # Calculate prediction errors
        stochastic_error = abs(stochastic_prediction['predicted_price'] - actual_outcome)
        neural_error = abs(neural_prediction['predicted_price'] - actual_outcome)
        # Avoid division by zero
        eps = np.finfo(float).eps
        stochastic_error = stochastic_error if stochastic_error != 0 else eps
        neural_error = neural_error if neural_error != 0 else eps
        # Compute inverse error weights
        total_inverse = (1.0 / stochastic_error) + (1.0 / neural_error)
        self.config['stochastic_weight'] = (1.0 / stochastic_error) / total_inverse
        self.config['neural_weight'] = (1.0 / neural_error) / total_inverse
        self.logger.info(f"Updated weights: stochastic={self.config['stochastic_weight']:.3f}, neural={self.config['neural_weight']:.3f}")

    def get_uncertainty_estimate(self):
        """
        Get combined uncertainty estimate from both components.
        """
        # Retrieve uncertainties from components
        try:
            stochastic_uncertainty = self.stochastic_simulator.get_uncertainty()
        except AttributeError:
            self.logger.warning("Stochastic simulator does not implement get_uncertainty(). Using 0.0.")
            stochastic_uncertainty = 0.0
        try:
            neural_uncertainty = self.neural_network.get_uncertainty()
        except AttributeError:
            self.logger.warning("Neural network does not implement get_uncertainty(). Using 0.0.")
            neural_uncertainty = 0.0
        # Normalize weights
        total_weight = self.config.get('stochastic_weight', 0) + self.config.get('neural_weight', 0)
        if total_weight == 0:
            return 0.0
        sw = self.config['stochastic_weight'] / total_weight
        nw = self.config['neural_weight'] / total_weight
        # Combine uncertainties
        combined_uncertainty = (stochastic_uncertainty * sw) + (neural_uncertainty * nw)
        return combined_uncertainty 