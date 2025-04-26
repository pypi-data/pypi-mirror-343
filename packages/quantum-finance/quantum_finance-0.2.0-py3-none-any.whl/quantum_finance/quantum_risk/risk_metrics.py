#!/usr/bin/env python3

"""
Risk Metrics Calculator for Quantum Risk Assessment

This module calculates classical risk metrics for cryptocurrency market data,
providing the foundation for both classical and quantum-enhanced risk assessment.

Author: Quantum-AI Team
"""

from typing import Dict, Any
import numpy as np

# Internal relative imports
from .utils.logging_util import setup_logger

logger = setup_logger(__name__)

class RiskMetricsCalculator:
    """
    Risk metrics calculator that computes various risk metrics from market data.
    """
    
    @staticmethod
    def calculate_classical_risk_metrics(order_book: Dict[str, Any], stats_24hr: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """
        Calculate classical risk metrics for a cryptocurrency.
        
        Args:
            order_book: Order book data with bids and asks
            stats_24hr: 24-hour statistics
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            
        Returns:
            Dictionary with risk metrics
        """
        # Extract and calculate risk metrics
        
        # 1. Bid-ask spread
        bid_price = float(stats_24hr.get('bidPrice', 0))
        ask_price = float(stats_24hr.get('askPrice', 0))
        
        if bid_price > 0 and ask_price > 0:
            bid_ask_spread = (ask_price - bid_price) / ask_price
        else:
            bid_ask_spread = 0.01  # Default value
        
        # 2. Volatility (use price change percent)
        volatility = min(1.0, abs(float(stats_24hr.get('priceChangePercent', 0)) / 100))
        
        # 3. Order book depth
        bid_volume = sum(float(level['quantity']) for level in order_book['bids'])
        ask_volume = sum(float(level['quantity']) for level in order_book['asks'])
        total_volume = bid_volume + ask_volume
        
        # Normalize order book depth (higher is better)
        # Assumption: 1000 units is considered "deep" in this example
        normalized_depth = min(1.0, total_volume / 1000.0)
        
        # 4. Order book imbalance
        if total_volume > 0:
            imbalance = abs((bid_volume - ask_volume) / total_volume)
        else:
            imbalance = 0.0
        
        # 5. Calculate price impact for a standard trade size
        # For simplicity, we'll use a hypothetical trade size of 10 BTC
        # Note: In a real implementation, this would be scaled by market cap
        trade_size = 10.0
        
        # Calculate price impact (simplified version)
        # In a real implementation, this would be imported from quantum_market_encoding
        # But we inline it here to avoid circular imports
        impact = 0.01  # Default impact value
        try:
            # Try to calculate actual impact if possible - Use relative import
            from src.quantum_finance.quantum_market_encoding import encode_price_impact
            _, impact = encode_price_impact(order_book, trade_size)
        except ModuleNotFoundError:  # Catch the specific error
            # Handle the case where the optional quantum module isn't available
            logger.warning(
                "quantum_market_encoding module not found. Using default price impact."
            )
            # Keep the default impact value
            pass
        
        # 6. Recent trading volume (24h)
        daily_volume = float(stats_24hr.get('volume', 0))
        
        # Normalize trading volume (higher is better)
        # Assumption: 10,000 units is considered "high volume" in this example
        normalized_volume = min(1.0, daily_volume / 10000.0)
        
        # 7. Risk metrics (higher = more risk)
        liquidity_risk = (0.3 * (1 - normalized_depth) + 
                          0.3 * (1 - normalized_volume) + 
                          0.4 * bid_ask_spread) * 100
        
        volatility_risk = volatility * 100
        
        market_depth_risk = (0.7 * (1 - normalized_depth) + 
                            0.3 * imbalance) * 100
        
        price_impact_risk = impact * 100
        
        # Overall risk (weighted average)
        overall_risk = (0.3 * liquidity_risk + 
                        0.3 * volatility_risk + 
                        0.2 * market_depth_risk + 
                        0.2 * price_impact_risk)
        
        # Return as dictionary
        return {
            'symbol': symbol,
            'current_price': float(stats_24hr.get('lastPrice', 0)),
            'bid_ask_spread': bid_ask_spread,
            'volatility': volatility,
            'normalized_depth': normalized_depth,
            'imbalance': imbalance,
            'price_impact': impact,
            'normalized_volume': normalized_volume,
            'liquidity_risk': liquidity_risk,
            'volatility_risk': volatility_risk,
            'market_depth_risk': market_depth_risk,
            'price_impact_risk': price_impact_risk,
            'overall_risk': overall_risk
        } 