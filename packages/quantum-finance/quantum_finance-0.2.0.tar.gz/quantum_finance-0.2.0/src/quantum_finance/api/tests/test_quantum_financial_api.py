#!/usr/bin/env python3

"""
Unit tests for the Quantum Financial API.

These tests verify the functionality of the Quantum Financial API,
focusing on the API interface rather than the individual components.
"""

import unittest
import os
import sys
import json
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock
import numpy as np

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the API
from api.quantum_financial_api import (
    QuantumFinancialAPI,
    QuantumFinancialConfig,
    MarketData,
    AnalysisResult,
    ComponentType
)

class TestQuantumFinancialAPI(unittest.TestCase):
    """Tests for the QuantumFinancialAPI class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test outputs
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test configuration
        self.config = QuantumFinancialConfig(
            save_path=self.temp_dir,
            debug_mode=True,
            als_learning_rate=0.01,
            market_encoding_qubits=4,
            phase_tracker_adaptation_method='innovation',
            phase_tracker_use_imm=True,
            phase_tracker_num_imm_models=2,
            qdense_num_qubits=4,
            qdense_num_layers=2,
            qdense_shots=100,
            sms_config_space_dim=3,
            sms_num_trajectories=10,
            sms_time_step=0.1,
            sms_drift_scale=0.01,
            sms_diffusion_scale=0.1,
            sms_quantum_potential_strength=0.05
        )
        
        # Initialize API with test configuration
        self.api = QuantumFinancialAPI(self.config)
        
        # Create test market data
        self.market_data = MarketData(
            symbol="TEST-USD",
            timestamp=datetime.now(),
            price=1000.0,
            volatility=0.05,
            bid_ask_spread=0.001,
            order_book_depth=0.8,
            trade_volume=100.0,
            order_book_imbalance=0.2,
            liquidity=0.9,
            order_book={
                "bids": [{"price": "990", "quantity": "1.5"}, {"price": "980", "quantity": "2.3"}],
                "asks": [{"price": "1010", "quantity": "1.2"}, {"price": "1020", "quantity": "3.1"}]
            }
        )
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test API initialization."""
        # Test with default configuration
        api = QuantumFinancialAPI()
        self.assertIsInstance(api.config, QuantumFinancialConfig)
        
        # Test with dictionary configuration
        config_dict = {
            "save_path": self.temp_dir,
            "debug_mode": True
        }
        api = QuantumFinancialAPI(config_dict)
        self.assertEqual(api.config.save_path, self.temp_dir)
        self.assertTrue(api.config.debug_mode)
    
    def test_market_data_serialization(self):
        """Test MarketData serialization and deserialization."""
        # Convert to dictionary
        market_data_dict = self.market_data.to_dict()
        
        # Convert back to MarketData
        market_data2 = MarketData.from_dict(market_data_dict)
        
        # Verify values
        self.assertEqual(market_data2.symbol, self.market_data.symbol)
        self.assertEqual(market_data2.price, self.market_data.price)
        self.assertEqual(market_data2.volatility, self.market_data.volatility)
    
    def test_encode_market_data(self):
        """Test market data encoding."""
        # Mock the encode functions to avoid Qiskit dependencies
        with patch('api.quantum_financial_api.encode_order_book_imbalance') as mock_encode_obi, \
             patch('api.quantum_financial_api.encode_market_volatility') as mock_encode_vol:
            
            # Set up mocks
            mock_encode_obi.return_value = MagicMock()
            mock_encode_vol.return_value = MagicMock()
            
            # Call encode_market_data
            result = self.api.encode_market_data(self.market_data)
            
            # Verify encode functions were called
            mock_encode_obi.assert_called_once()
            mock_encode_vol.assert_called_once()
            
            # Verify result contains expected keys
            self.assertIn('order_book_imbalance', result)
            self.assertIn('volatility', result)
    
    @patch('api.quantum_financial_api.AdaptivePhaseTracker')
    def test_analyze_market_phase(self, mock_apt):
        """Test market phase analysis."""
        # Set up mock
        mock_apt_instance = mock_apt.return_value
        mock_apt_instance.update.return_value = (
            MagicMock(
                phase=0.5,
                phase_uncertainty=0.1,
                innovation=0.05,
                state_vector=np.array([0.5, 0.1]),
                covariance_matrix=np.array([[0.01, 0], [0, 0.01]])
            ),
            MagicMock()
        )
        mock_apt_instance.use_imm = True
        mock_apt_instance.get_imm_probabilities.return_value = np.array([0.7, 0.3])
        mock_apt_instance.T = 0.01
        
        # Call analyze_market_phase
        result = self.api.analyze_market_phase(self.market_data)
        
        # Verify result
        self.assertEqual(result.symbol, self.market_data.symbol)
        self.assertEqual(result.component_type, ComponentType.PHASE_TRACKING)
        self.assertIn("phase", result.risk_metrics)
        self.assertIn("regime_0", result.risk_metrics)
    
    @patch('api.quantum_financial_api.AdaptiveLearningSystem')
    def test_predict_with_adaptive_learning(self, mock_als):
        """Test prediction with adaptive learning."""
        # Set up mock
        mock_als_instance = mock_als.return_value
        mock_als_instance.process_new_data.return_value = 1100.0
        mock_als_instance.evaluate_performance.return_value = {'accuracy': 0.95}
        
        # Call predict_with_adaptive_learning
        result = self.api.predict_with_adaptive_learning(self.market_data)
        
        # Verify result
        self.assertEqual(result.symbol, self.market_data.symbol)
        self.assertEqual(result.component_type, ComponentType.ADAPTIVE_LEARNING)
        self.assertIn("predicted_value", result.predictions)
        self.assertIn("confidence", result.risk_metrics)
    
    @patch('api.quantum_financial_api.StochasticMarketSimulator')
    def test_simulate_market_evolution(self, mock_sms):
        """Test market evolution simulation."""
        # Set up mock
        mock_sms_instance = mock_sms.return_value
        
        # Create mock trajectories
        trajectories = [
            [(1000.0, datetime.now())] * 30
            for _ in range(10)
        ]
        
        mock_sms_instance.simulate_price_evolution.return_value = {
            "quantum_trajectories": trajectories,
            "monte_carlo_trajectories": trajectories
        }
        
        # Call simulate_market_evolution
        result = self.api.simulate_market_evolution(self.market_data)
        
        # Verify result
        self.assertEqual(result.symbol, self.market_data.symbol)
        self.assertEqual(result.component_type, ComponentType.STOCHASTIC_SIMULATION)
        self.assertIn("final_price_mean", result.predictions)
        self.assertIn("final_price_median", result.predictions)
    
    def test_analyze_market_data(self):
        """Test comprehensive market data analysis."""
        # Create mocks for individual analysis methods
        with patch.object(self.api, 'predict_with_adaptive_learning') as mock_predict, \
             patch.object(self.api, 'analyze_market_phase') as mock_analyze_phase, \
             patch.object(self.api, 'simulate_market_evolution') as mock_simulate:
            
            # Set up mock returns
            mock_predict.return_value = AnalysisResult(
                symbol=self.market_data.symbol,
                timestamp=datetime.now(),
                component_type=ComponentType.ADAPTIVE_LEARNING,
                predictions={"predicted_value": 1100.0},
                risk_metrics={"confidence": 0.95}
            )
            
            mock_analyze_phase.return_value = AnalysisResult(
                symbol=self.market_data.symbol,
                timestamp=datetime.now(),
                component_type=ComponentType.PHASE_TRACKING,
                predictions={"phase_forecast": 0.6},
                risk_metrics={"phase": 0.5, "phase_uncertainty": 0.1}
            )
            
            mock_simulate.return_value = AnalysisResult(
                symbol=self.market_data.symbol,
                timestamp=datetime.now(),
                component_type=ComponentType.STOCHASTIC_SIMULATION,
                predictions={"final_price_mean": 1200.0},
                risk_metrics={"var_95": 0.15}
            )
            
            # Call analyze_market_data
            results = self.api.analyze_market_data(self.market_data)
            
            # Verify results
            self.assertEqual(len(results), 3)
            self.assertIn(ComponentType.ADAPTIVE_LEARNING, results)
            self.assertIn(ComponentType.PHASE_TRACKING, results)
            self.assertIn(ComponentType.STOCHASTIC_SIMULATION, results)
    
    def test_save_analysis_results(self):
        """Test saving analysis results."""
        # Create test results
        results = {
            ComponentType.ADAPTIVE_LEARNING: AnalysisResult(
                symbol=self.market_data.symbol,
                timestamp=datetime.now(),
                component_type=ComponentType.ADAPTIVE_LEARNING,
                predictions={"predicted_value": 1100.0},
                risk_metrics={"confidence": 0.95}
            )
        }
        
        # Call save_analysis_results
        saved_paths = self.api.save_analysis_results(results, base_filename="test_analysis")
        
        # Verify paths
        self.assertIn(ComponentType.ADAPTIVE_LEARNING, saved_paths)
        self.assertTrue(os.path.exists(saved_paths[ComponentType.ADAPTIVE_LEARNING]))
        
        # Verify file content
        with open(saved_paths[ComponentType.ADAPTIVE_LEARNING], 'r') as f:
            data = json.load(f)
            self.assertEqual(data["symbol"], self.market_data.symbol)
            self.assertEqual(data["component_type"], ComponentType.ADAPTIVE_LEARNING.value)
    
    def test_create_ensemble_prediction(self):
        """Test creating ensemble predictions."""
        # Create test results
        results = {
            ComponentType.ADAPTIVE_LEARNING: AnalysisResult(
                symbol=self.market_data.symbol,
                timestamp=datetime.now(),
                component_type=ComponentType.ADAPTIVE_LEARNING,
                predictions={"predicted_value": 1100.0},
                risk_metrics={"confidence": 0.9}
            ),
            ComponentType.PHASE_TRACKING: AnalysisResult(
                symbol=self.market_data.symbol,
                timestamp=datetime.now(),
                component_type=ComponentType.PHASE_TRACKING,
                predictions={"predicted_value": 1050.0},
                risk_metrics={"confidence": 0.8}
            )
        }
        
        # Test with default weights
        ensemble = self.api.create_ensemble_prediction(results)
        self.assertIn("predictions", ensemble)
        self.assertIn("risk_metrics", ensemble)
        self.assertIn("predicted_value", ensemble["predictions"])
        self.assertIn("confidence", ensemble["risk_metrics"])
        
        # Test with custom weights
        weights = {
            ComponentType.ADAPTIVE_LEARNING: 0.7,
            ComponentType.PHASE_TRACKING: 0.3
        }
        ensemble = self.api.create_ensemble_prediction(results, weights)
        self.assertIn("weights", ensemble)
        self.assertEqual(ensemble["weights"], {
            ComponentType.ADAPTIVE_LEARNING.value: 0.7,
            ComponentType.PHASE_TRACKING.value: 0.3
        })
        
        # Verify weighted value
        expected_value = 1100.0 * 0.7 + 1050.0 * 0.3
        self.assertAlmostEqual(ensemble["predictions"]["predicted_value"], expected_value)

if __name__ == "__main__":
    unittest.main() 