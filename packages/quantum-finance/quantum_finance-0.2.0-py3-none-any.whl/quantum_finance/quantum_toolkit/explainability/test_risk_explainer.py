"""
Tests for the RiskExplainer functionality.

This module contains tests for the RiskExplainer class and its methods,
ensuring that risk factor analysis, natural language explanation, and
visualization functions work correctly.

Author: Quantum-AI Team
"""

import os
import json
import shutil
import unittest
import tempfile
from datetime import datetime

import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend for testing

from quantum.explainability.risk_explainer import RiskExplainer

class TestRiskExplainer(unittest.TestCase):
    """Test case for the RiskExplainer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.explainer = RiskExplainer(output_dir=self.temp_dir)
        
        # Sample risk assessment data for Bitcoin
        self.btc_risk_assessment = {
            'id': 'btc_test_1',
            'symbol': 'BTC',
            'timestamp': datetime.now().isoformat(),
            'overall_risk': 65.8,
            'risk_factors': {
                'market_volatility': {
                    'risk_score': 72.5,
                    'weight': 1.2
                },
                'liquidity': {
                    'risk_score': 45.3,
                    'weight': 1.0
                },
                'market_depth': {
                    'risk_score': 58.7,
                    'weight': 0.9
                },
                'order_book_imbalance': {
                    'risk_score': 68.2,
                    'weight': 1.1
                },
                'regulatory_risk': {
                    'risk_score': 35.4,
                    'weight': 0.8
                }
            },
            'quantum_advantage': {
                'value': 0.12,
                'description': 'Quantum analysis detected correlation patterns not visible in classical analysis'
            },
            'model_version': '1.0.3'
        }
        
        # Sample risk assessment data for Ethereum
        self.eth_risk_assessment = {
            'id': 'eth_test_1',
            'symbol': 'ETH',
            'timestamp': datetime.now().isoformat(),
            'overall_risk': 52.4,
            'risk_factors': {
                'market_volatility': {
                    'risk_score': 62.1,
                    'weight': 1.2
                },
                'liquidity': {
                    'risk_score': 39.8,
                    'weight': 1.0
                },
                'market_depth': {
                    'risk_score': 51.2,
                    'weight': 0.9
                },
                'order_book_imbalance': {
                    'risk_score': 58.6,
                    'weight': 1.1
                },
                'regulatory_risk': {
                    'risk_score': 40.2,
                    'weight': 0.8
                }
            },
            'quantum_advantage': {
                'value': 0.08,
                'description': 'Quantum analysis provided improved risk distribution estimates'
            },
            'model_version': '1.0.3'
        }
        
        # Market data for testing
        self.market_data = {
            'BTC': {
                'price': 42356.78,
                'volume_24h': 28765432.12,
                'market_cap': 798345678901.23,
                'price_change_24h': -2.34
            },
            'ETH': {
                'price': 2845.67,
                'volume_24h': 15678932.45,
                'market_cap': 342567890123.45,
                'price_change_24h': 1.23
            }
        }
        
    def tearDown(self):
        """Tear down test fixtures"""
        # Clean up temp directory
        shutil.rmtree(self.temp_dir)
    
    def test_analyze_factor_contributions(self):
        """Test the analyze_factor_contributions method"""
        # Analyze BTC risk assessment
        contributions = self.explainer.analyze_factor_contributions(
            self.btc_risk_assessment,
            self.market_data
        )
        
        # Check results
        self.assertIsInstance(contributions, dict)
        self.assertGreater(len(contributions), 0)
        
        # The highest contribution should be market_volatility based on our test data
        highest_factor = max(contributions.items(), key=lambda x: x[1])[0]
        self.assertEqual(highest_factor, 'market_volatility')
        
        # Check if the contribution percentages sum to approximately 100%
        total_contribution = sum(contributions.values())
        self.assertAlmostEqual(total_contribution, 100.0, delta=0.1)
    
    def test_natural_language_explanation(self):
        """Test the generate_natural_language_explanation method"""
        # Generate explanation for BTC
        explanation = self.explainer.generate_natural_language_explanation(self.btc_risk_assessment)
        
        # Check results
        self.assertIsInstance(explanation, str)
        self.assertIn('BTC', explanation)
        self.assertIn('high risk', explanation)  # BTC risk is 65.8, which is high
        
        # Check if the explanation mentions the top risk factors
        self.assertIn('market volatility', explanation.lower())
        
        # Generate explanation for ETH
        explanation = self.explainer.generate_natural_language_explanation(self.eth_risk_assessment)
        
        # Check results
        self.assertIn('ETH', explanation)
        self.assertIn('moderate risk', explanation)  # ETH risk is 52.4, which is moderate
    
    def test_factor_contribution_chart(self):
        """Test the create_factor_contribution_chart method"""
        # Analyze contributions first
        contributions = self.explainer.analyze_factor_contributions(
            self.btc_risk_assessment,
            self.market_data
        )
        
        # Create chart
        chart_path = self.explainer.create_factor_contribution_chart(
            contributions,
            title='BTC Risk Factor Contributions'
        )
        
        # Check results
        self.assertIsInstance(chart_path, str)
        self.assertTrue(os.path.exists(chart_path))
        self.assertTrue(chart_path.endswith('.png'))
    
    def test_quantum_vs_classical_comparison(self):
        """Test the quantum_vs_classical_comparison method"""
        # Create a sample classical risk assessment (slightly different from quantum)
        classical_risk = self.btc_risk_assessment.copy()
        classical_risk['id'] = 'btc_classical_1'
        
        # Modify some risk factors to simulate differences
        for factor in classical_risk['risk_factors']:
            # Add small random adjustments to classical scores
            orig_score = classical_risk['risk_factors'][factor]['risk_score']
            classical_risk['risk_factors'][factor]['risk_score'] = max(0, min(100, orig_score - 5))
        
        # Create comparison
        comparison = self.explainer.quantum_vs_classical_comparison(
            self.btc_risk_assessment,
            classical_risk
        )
        
        # Check results
        self.assertIsInstance(comparison, dict)
        self.assertIn('comparison_metrics', comparison)
        self.assertIn('visualization_path', comparison)
        self.assertTrue(os.path.exists(comparison['visualization_path']))
    
    def test_save_explanation(self):
        """Test the save_explanation method"""
        # Generate explanation
        explanation = self.explainer.generate_natural_language_explanation(self.btc_risk_assessment)
        
        # Create a factor contribution chart
        contributions = self.explainer.analyze_factor_contributions(
            self.btc_risk_assessment,
            self.market_data
        )
        chart_path = self.explainer.create_factor_contribution_chart(contributions)
        
        # Create visualization paths dictionary
        viz_paths = {
            'factor_contributions': chart_path
        }
        
        # Save explanation
        output_path = self.explainer.save_explanation(
            self.btc_risk_assessment,
            explanation,
            viz_paths
        )
        
        # Check results
        self.assertIsInstance(output_path, str)
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.md'))
        
        # Check content of the markdown file
        with open(output_path, 'r') as f:
            content = f.read()
            self.assertIn('# BTC Risk Assessment Explanation', content)
            self.assertIn('## Risk Summary', content)
            self.assertIn('## Visualizations', content)
            self.assertIn('## Metadata', content)
            self.assertIn('```json', content)

if __name__ == '__main__':
    unittest.main() 