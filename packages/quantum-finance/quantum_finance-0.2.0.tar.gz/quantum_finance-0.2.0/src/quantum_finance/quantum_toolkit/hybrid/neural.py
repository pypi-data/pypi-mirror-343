# src/quantum_finance/quantum_toolkit/hybrid/neural.py
import numpy as np
from src.quantum_finance.quantum_risk.utils.logging_util import setup_logger

class TrajectoryConditionedNetwork:
    """
    Neural network that conditions on stochastic trajectories for prediction.
    """

    def __init__(self, input_dim, hidden_dims, output_dim, config=None):
        """
        Initialize the trajectory-conditioned network.

        Args:
            input_dim: Dimension of input features
            hidden_dims: List of hidden layer sizes
            output_dim: Dimension of network output
            config: Optional dict for settings like learning_rate, dropout_rate
        """
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        self.output_dim = output_dim
        self.config = config or {
            'learning_rate': 0.001,
            'dropout_rate': 0.2,
            'trajectory_feature_dim': 20,
            'use_trajectories': True
        }
        self.trajectory_features = None
        self.logger = setup_logger(__name__)
        self.logger.info(f"Initializing TrajectoryConditionedNetwork: input={input_dim}, hidden={hidden_dims}, output={output_dim}")

    def condition_on_trajectories(self, trajectories):
        """
        Extract and store features from stochastic trajectories.

        Args:
            trajectories: Array or list of trajectories
        """
        # If no trajectories provided or default behavior, indicate not implemented
        if trajectories is None:
            raise NotImplementedError("Trajectory conditioning not implemented for None input")
        if not self.config.get('use_trajectories', False):
            self.trajectory_features = None
            return
        # Convert trajectories to numpy array and ensure floats
        arr = np.array(trajectories, dtype=float)
        # Clean NaN/Infinite values
        if np.isnan(arr).any() or np.isinf(arr).any():
            self.logger.warning("Detected NaN/Inf in trajectories; replacing with zeros")
            arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
        # Fallback if no valid trajectories
        if arr.size == 0 or arr.shape[0] == 0:
            dim = min(
                self.config.get('trajectory_feature_dim', arr.shape[1] if arr.ndim > 1 else 0),
                arr.shape[1] if arr.ndim > 1 else 0
            )
            fallback_length = dim * 2 + 3  # mean_feat + std_feat + max + min + slope
            self.logger.warning(f"No valid trajectories after cleaning; using zero features of length {fallback_length}")
            self.trajectory_features = np.zeros(fallback_length, dtype=float)
            return
        # Compute statistical features: mean, std, max, min
        mean_traj = np.mean(arr, axis=0)
        std_traj = np.std(arr, axis=0)
        max_traj = np.max(arr, axis=0)
        min_traj = np.min(arr, axis=0)
        # Compute final slopes of each trajectory
        final_slopes = [traj[-1] - traj[-2] for traj in arr if len(traj) >= 2]
        mean_slope = float(np.mean(final_slopes)) if final_slopes else 0.0
        # Determine feature dimension
        full_dim = mean_traj.shape[0]
        dim = min(self.config.get('trajectory_feature_dim', full_dim), full_dim)
        # Extract trailing segments of mean and std
        mean_feat = mean_traj[-dim:]
        std_feat = std_traj[-dim:]
        # Prepare scalar features
        max_feat = np.array([float(np.mean(max_traj))])
        min_feat = np.array([float(np.mean(min_traj))])
        slope_feat = np.array([mean_slope])
        # Combine features into one vector
        self.trajectory_features = np.concatenate((mean_feat, std_feat, max_feat, min_feat, slope_feat))
        self.logger.info(f"Conditioned network on {len(trajectories)} trajectories, extracted features length {len(self.trajectory_features)}")

    def _extract_features(self, market_data):
        """
        Extract raw features from market data for prediction.

        Args:
            market_data: Input data frame or array

        Returns:
            Feature vector
        """
        # Basic placeholder: flatten or extract initial features
        # If market_data is array-like, flatten; else return zeros
        try:
            # Ensure numeric conversion, invalid inputs will raise
            data_arr = np.array(market_data, dtype=float)
            feat = data_arr.flatten()
            # Trim or pad to input_dim
            if feat.size >= self.input_dim:
                return feat[:self.input_dim]
            else:
                return np.pad(feat, (0, self.input_dim - feat.size), 'constant')
        except Exception:
            return np.zeros(self.input_dim)

    def predict(self, market_data):
        """
        Generate a prediction based on market data and trajectory features.

        Args:
            market_data: Input data for prediction

        Returns:
            Dict with 'predicted_price', 'confidence', and metadata
        """
        # Default behavior not implemented when no market data is supplied
        if market_data is None:
            raise NotImplementedError("Predict method not implemented for None input")
        # Extract base features
        base_feat = self._extract_features(market_data)
        # Combine with trajectory-conditioned features if available
        if self.trajectory_features is not None:
            combined = np.concatenate((base_feat, self.trajectory_features))
            mode = 'trajectory-conditioned'
        else:
            combined = base_feat
            mode = 'standard'
        # Placeholder prediction: mean of combined features
        predicted_price = float(np.mean(combined)) if combined.size > 0 else 0.0
        # Confidence placeholder (e.g., inverse of dropout)
        confidence = float(1.0 - self.config.get('dropout_rate', 0.0))
        self.logger.info(f"Generated prediction with {mode} model using {combined.size} features")
        return {
            'predicted_price': predicted_price,
            'confidence': confidence,
            'features_used': int(combined.size)
        }

    def get_uncertainty(self):
        """
        Estimate predictive uncertainty.

        Returns:
            Float uncertainty
        """
        # Require conditioning before uncertainty if using trajectories
        if self.config.get('use_trajectories', False) and self.trajectory_features is None:
            raise NotImplementedError("Uncertainty estimation requires conditioning on trajectories first")
        # Return configured dropout rate as the uncertainty estimate
        return float(self.config.get('dropout_rate', 0.0))

    def disable_trajectory_features(self):
        """
        Disable using trajectory features in predictions.
        """
        self.config['use_trajectories'] = False
        self.trajectory_features = None
        self.logger.info("Disabled trajectory conditioning")

    def enable_trajectory_features(self):
        """
        Enable using trajectory features in predictions.
        """
        self.config['use_trajectories'] = True
        self.logger.info("Enabled trajectory conditioning") 