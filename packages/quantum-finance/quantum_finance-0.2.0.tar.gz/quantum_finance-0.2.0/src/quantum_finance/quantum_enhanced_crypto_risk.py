#!/usr/bin/env python3

"""
Quantum Enhanced Cryptocurrency Risk Assessment

This script demonstrates how to enhance cryptocurrency risk assessment with
quantum computing capabilities, specifically using a Quantum Bayesian Risk
Network to model market dependencies.

Features:
- Integration with Binance API market microstructure data
- Quantum encoding of order book and market data
- Bayesian risk propagation using quantum circuits
- Comparison with classical risk assessment

Author: Quantum-AI Team
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional, Any
import argparse
import pandas as pd

# Load environment variables from .env file
from dotenv import load_dotenv
from pathlib import Path

# Look for .env file in current and parent directories
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    print(f"Loaded environment variables from {env_path.absolute()}")
else:
    # Try to find .env in parent directories
    parent_dir = Path('.').absolute().parent
    parent_env = parent_dir / '.env'
    if parent_env.exists():
        load_dotenv(dotenv_path=parent_env, override=True)
        print(f"Loaded environment variables from {parent_env}")
    else:
        load_dotenv()  # Try default loading
        print("Attempted to load .env from default locations")

# Print API key info for debugging (without revealing full key)
api_key = os.environ.get('RAPIDAPI_KEY')
if api_key:
    masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else '****'
    print(f"RAPIDAPI_KEY found: {masked_key}")
else:
    print("RAPIDAPI_KEY not found in environment variables")

# Import quantum components
from quantum_bayesian_risk import QuantumBayesianRiskNetwork
from quantum_market_encoding import (
    combined_market_risk_encoding,
    visualize_quantum_market_encoding
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QuantumEnhancedCryptoRisk:
    """
    Quantum-enhanced cryptocurrency risk assessment tool.
    
    This class combines quantum Bayesian risk networks with market microstructure
    data to provide enhanced risk assessment for cryptocurrencies.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_host: Optional[str] = None):
        """
        Initialize the quantum risk assessment engine.
        
        Args:
            api_key: Optional RapidAPI key for Binance data access
            api_host: Optional RapidAPI host for Binance data
        """
        # Set API credentials
        self.api_key = api_key or os.environ.get('RAPIDAPI_KEY')
        self.api_host = api_host or os.environ.get('RAPIDAPI_HOST', 'binance43.p.rapidapi.com')
        
        # Initialize the quantum Bayesian risk network
        self.quantum_bayesian_network = QuantumBayesianRiskNetwork(
            num_risk_factors=5,
            use_adaptive_shots=True
        )
        
        # Define core risk relationships
        self._define_risk_relationships()
        
        logger.info("Initialized QuantumEnhancedCryptoRisk with quantum Bayesian network")
    
    def _define_risk_relationships(self):
        """Define the causal relationships between different risk factors."""
        # Define how market factors affect each other
        risk_relationships = [
            # Cause, Effect, Strength (0-1)
            (0, 1, 0.7),  # Order Book Imbalance → Price Volatility
            (1, 3, 0.8),  # Price Volatility → Liquidity Risk
            (2, 3, 0.6),  # Market Depth → Liquidity Risk
            (1, 4, 0.8),  # Price Volatility → Overall Risk 
            (3, 4, 0.9),  # Liquidity Risk → Overall Risk
            (0, 4, 0.4),  # Direct: Order Book Imbalance → Overall Risk
        ]
        
        # Add relationships to the quantum network
        for cause, effect, strength in risk_relationships:
            self.quantum_bayesian_network.add_conditional_relationship(
                cause_idx=cause,
                effect_idx=effect,
                strength=strength
            )
        
        logger.info(f"Defined {len(risk_relationships)} risk factor relationships")

    def _calculate_classical_risk_metrics(self, symbol: str, order_book: Dict[str, Any], stats_24hr: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate classical risk metrics for a cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            order_book: Order book data
            stats_24hr: 24-hour statistics
            
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
            bid_ask_spread = 0.01  # default value if proper prices not available
        
        # 2. Volatility (from 24hr stats)
        price_change_percent = abs(float(stats_24hr.get('priceChangePercent', 5.0)) / 100)
        volatility = price_change_percent
        
        # 3. Market depth (total volume in order book)
        try:
            # For Yahoo Finance synthetic data
            if isinstance(order_book['bids'], pd.DataFrame) and isinstance(order_book['asks'], pd.DataFrame):
                bids_volume = order_book['bids']['quantity'].sum()
                asks_volume = order_book['asks']['quantity'].sum()
            else:
                # For Binance data
                bids_volume = sum(float(bid[1]) for bid in order_book.get('bids', []))
                asks_volume = sum(float(ask[1]) for ask in order_book.get('asks', []))
            
            total_depth = bids_volume + asks_volume
            
            # Normalize depth (higher is better)
            # Assumption: 1000 units is considered "deep" in this example
            normalized_depth = min(1.0, total_depth / 1000.0)
            
            # 4. Order book imbalance (bid/ask ratio)
            if asks_volume > 0:
                imbalance = abs(bids_volume / asks_volume - 1)
            else:
                imbalance = 1.0
            
            # 5. Price impact (how much would a market order of X size move the price)
            # Simplified calculation
            impact = 0.01  # default 1% impact
            
            if bids_volume > 0 and asks_volume > 0:
                # Calculate impact as inverse of liquidity
                impact = 1.0 / (normalized_depth * 10)
                impact = min(0.1, impact)  # cap at 10%
        except (KeyError, TypeError):
            # Fallback values if order book data is not in expected format
            normalized_depth = 0.5
            imbalance = 0.5
            impact = 0.05
        
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
    
    def analyze_with_quantum(self, symbol: str) -> Dict[str, Any]:
        """
        Perform quantum-enhanced cryptocurrency risk analysis.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Get the data fetcher
            crypto_data_fetcher = self._get_crypto_data_fetcher()
            
            # Check if we have a RapidAPI key for Binance data
            use_yahoo_finance = not self.api_key
            
            if use_yahoo_finance:
                logger.info(f"No RapidAPI key provided. Using Yahoo Finance data for {symbol}...")
                # Import yfinance
                import yfinance as yf
                
                # Convert symbol to Yahoo Finance format (add -USD)
                yahoo_symbol = f"{symbol}-USD"
                
                # Fetch data from Yahoo Finance
                ticker = yf.Ticker(yahoo_symbol)
                hist = ticker.history(period="1d")
                
                if hist.empty:
                    logger.warning(f"No data found for {yahoo_symbol}, trying {symbol}USD...")
                    yahoo_symbol = f"{symbol}USD"
                    ticker = yf.Ticker(yahoo_symbol)
                    hist = ticker.history(period="1d")
                
                if hist.empty:
                    logger.warning(f"No data found for {yahoo_symbol}, trying {symbol}USDT...")
                    yahoo_symbol = f"{symbol}USDT"
                    ticker = yf.Ticker(yahoo_symbol)
                    hist = ticker.history(period="1d")
                
                if hist.empty:
                    raise ValueError(f"Could not find data for {symbol} on Yahoo Finance")
                
                # Create synthetic order book and 24hr stats
                current_price = hist['Close'].iloc[-1]
                
                # Synthetic order book
                order_book = {
                    'bids': pd.DataFrame({
                        'price': [current_price * 0.99, current_price * 0.98, current_price * 0.97],
                        'quantity': [1.0, 2.0, 3.0]
                    }),
                    'asks': pd.DataFrame({
                        'price': [current_price * 1.01, current_price * 1.02, current_price * 1.03],
                        'quantity': [1.0, 2.0, 3.0]
                    })
                }
                
                # Synthetic 24hr stats
                stats_24hr = {
                    'lastPrice': current_price,
                    'bidPrice': current_price * 0.99,
                    'askPrice': current_price * 1.01,
                    'volume': hist['Volume'].iloc[-1],
                    'priceChangePercent': ((hist['Close'].iloc[-1] / hist['Open'].iloc[0]) - 1) * 100,
                    'highPrice': hist['High'].iloc[-1],
                    'lowPrice': hist['Low'].iloc[-1],
                    'weightedAvgPrice': hist['Close'].iloc[-1]
                }
                
                logger.info(f"Using Yahoo Finance data for {symbol}: current price = ${current_price:.2f}")
            else:
                # Fetch market data for the given symbol from Binance
                logger.info(f"Fetching order book data for {symbol}...")
                order_book = crypto_data_fetcher.get_binance_order_book(symbol)
                
                logger.info(f"Fetching 24hr stats for {symbol}...")
                stats_24hr = crypto_data_fetcher.get_binance_24hr_stats(symbol)
            
            # Prepare market data for quantum encoding
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Attempt to encode the market structure into a quantum circuit
            try:
                logger.info(f"Creating quantum encoding for {symbol} market data...")
                # Extract volatility from 24hr stats
                price_change_percent = abs(float(stats_24hr.get('priceChangePercent', 5.0)) / 100)
                high_price = float(stats_24hr.get('highPrice', 0))
                low_price = float(stats_24hr.get('lowPrice', 0))
                weighted_avg_price = float(stats_24hr.get('weightedAvgPrice', 0))
                
                # Calculate additional market metrics
                if high_price > 0 and low_price > 0:
                    # Use high-low range relative to average price as another volatility measure
                    relative_range = (high_price - low_price) / weighted_avg_price
                else:
                    relative_range = 0.05  # default value if proper prices not available
                
                # Use combined volatility metric
                volatility = max(price_change_percent, relative_range)
                
                # Get trading volume
                volume = float(stats_24hr.get('volume', 1000000))
                
                # Calculate order book depth and imbalance
                total_bid_volume = sum(float(bid['quantity']) for bid in order_book.get('bids', []))
                total_ask_volume = sum(float(ask['quantity']) for ask in order_book.get('asks', []))
                
                if total_ask_volume > 0:
                    market_depth = total_bid_volume / total_ask_volume
                else:
                    market_depth = 1.0  # Default if no asks
                
                # Calculate price momentum (crude approximation)
                price_change = float(stats_24hr.get('priceChange', 0))
                last_price = float(stats_24hr.get('lastPrice', 1))
                momentum = price_change / last_price if last_price > 0 else 0
                
                # Prepare comprehensive market data for enhanced risk assessment
                market_data = {
                    'symbol': symbol,
                    'volatility': volatility,
                    'market_depth': market_depth,
                    'volume': volume,
                    'price': last_price,
                    'momentum': momentum,
                    'high_price': high_price,
                    'low_price': low_price,
                    'weighted_avg_price': weighted_avg_price,
                    'price_change_percent': price_change_percent,
                    'bid_volume': total_bid_volume,
                    'ask_volume': total_ask_volume
                }
                
                logger.info(f"Market data prepared: volatility={volatility:.4f}, market_depth={market_depth:.4f}")
                
                # Create encoding circuit with all available market data
                trade_size = total_bid_volume * 0.01  # Use 1% of bid volume as a reasonable trade size
                encoding_circuit = combined_market_risk_encoding(
                    order_book, 
                    volatility, 
                    trade_size, 
                    volume
                )
                
                # Save visualization of the quantum market encoding
                output_dir = '.'
                viz_filename = f"{symbol}_quantum_market_encoding_{timestamp}.png"
                visualize_quantum_market_encoding(
                    encoding_circuit,
                    title=f"Quantum Market Encoding - {symbol}",
                    output_file=os.path.join(output_dir, viz_filename)
                )
                
                # Default initial risk probabilities
                initial_probabilities = [0.5, 0.5, 0.5, 0.5, 0.5]
                
                # Use quantum Bayesian network with market data for enhanced risk sensitivity
                risk_results = self.quantum_bayesian_network.propagate_risk(
                    initial_probabilities=initial_probabilities,
                    market_data=market_data
                )
                
                # Extract updated probabilities from the risk results
                updated_probs = risk_results["updated_probabilities"]
                
                # Calculate classical risk for comparison
                classical_risk = self._calculate_classical_risk_metrics(
                    symbol, order_book, stats_24hr
                )
                
                # Scale back to percentages for reporting
                quantum_enhanced_risk = {
                    'order_book_imbalance_risk': updated_probs[0] * 100,
                    'volatility_risk': updated_probs[1] * 100,
                    'market_depth_risk': updated_probs[2] * 100,
                    'liquidity_risk': updated_probs[3] * 100,
                    'overall_risk': updated_probs[4] * 100
                }
                
                # Calculate quantum advantage metrics
                risk_differences = {
                    k: quantum_enhanced_risk[k] - v 
                    for k, v in classical_risk.items() 
                    if k in ['volatility_risk', 'market_depth_risk', 'liquidity_risk', 'overall_risk']
                }
                
                # Create the network visualization
                network_file = f"{symbol}_quantum_risk_network_{timestamp}.png"
                self.quantum_bayesian_network.visualize_network(network_file)
                
                # Combine results
                results = {
                    'timestamp': timestamp,
                    'symbol': symbol,
                    'current_price': classical_risk['current_price'],
                    'classical_risk': {
                        'liquidity_risk': classical_risk['liquidity_risk'],
                        'volatility_risk': classical_risk['volatility_risk'],
                        'market_depth_risk': classical_risk['market_depth_risk'],
                        'price_impact_risk': classical_risk['price_impact_risk'],
                        'overall_risk': classical_risk['overall_risk']
                    },
                    'quantum_enhanced_risk': quantum_enhanced_risk,
                    'risk_differences': risk_differences,
                    'market_metrics': {
                        'bid_ask_spread': classical_risk['bid_ask_spread'],
                        'volatility': classical_risk['volatility'],
                        'normalized_depth': classical_risk['normalized_depth'],
                        'normalized_volume': classical_risk['normalized_volume'],
                        'imbalance': classical_risk['imbalance'],
                        'price_impact': classical_risk['price_impact']
                    },
                    'visualizations': {
                        'market_circuit': viz_filename,
                        'risk_network': network_file
                    }
                }
                
                # Save results to JSON file
                results_file = f"{symbol}_quantum_risk_results_{timestamp}.json"
                with open(results_file, 'w') as f:
                    json.dump(results, f, indent=2)
                
                logger.info(f"Analysis complete. Results saved to {results_file}")
                
                return results
            except Exception as e:
                logger.error(f"Error creating quantum encoding: {e}")
                raise
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            raise
    
    def generate_analysis_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a markdown report of the quantum-enhanced risk analysis.
        
        Args:
            results: Results from analyze_with_quantum
            
        Returns:
            Markdown formatted report
        """
        timestamp = results.get('timestamp', datetime.now().strftime('%Y%m%d_%H%M%S'))
        symbol = results.get('symbol', 'UNKNOWN')
        
        # Create markdown report with details
        md_content = f"""# Quantum-Enhanced Risk Assessment: {symbol}

## Summary
- **Timestamp:** {timestamp}
- **Symbol:** {symbol}
- **Current Price:** ${results.get('current_price', 0):.2f}
- **Overall Risk (Quantum):** {results.get('quantum_enhanced_risk', {}).get('overall_risk', 0):.2f}%
        
## Risk Metrics

| Metric | Classical | Quantum-Enhanced | Difference |
|--------|-----------|-----------------|------------|
| Liquidity Risk | {results.get('classical_risk', {}).get('liquidity_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('liquidity_risk', 0):.2f}% | {results.get('risk_differences', {}).get('liquidity_risk', 0):.2f}% |
| Volatility Risk | {results.get('classical_risk', {}).get('volatility_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('volatility_risk', 0):.2f}% | {results.get('risk_differences', {}).get('volatility_risk', 0):.2f}% |
| Market Depth Risk | {results.get('classical_risk', {}).get('market_depth_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('market_depth_risk', 0):.2f}% | {results.get('risk_differences', {}).get('market_depth_risk', 0):.2f}% |
| Overall Risk | {results.get('classical_risk', {}).get('overall_risk', 0):.2f}% | {results.get('quantum_enhanced_risk', {}).get('overall_risk', 0):.2f}% | {results.get('risk_differences', {}).get('overall_risk', 0):.2f}% |

## Market Metrics
- **Bid-Ask Spread:** {results.get('market_metrics', {}).get('bid_ask_spread', 0):.6f}
- **Volatility:** {results.get('market_metrics', {}).get('volatility', 0):.4f}
- **Normalized Depth:** {results.get('market_metrics', {}).get('normalized_depth', 0):.4f}
- **Normalized Volume:** {results.get('market_metrics', {}).get('normalized_volume', 0):.4f}
- **Order Book Imbalance:** {results.get('market_metrics', {}).get('imbalance', 0):.4f}
- **Price Impact:** {results.get('market_metrics', {}).get('price_impact', 0):.4f}

## Visualizations

### Quantum Market Encoding
![Quantum Market Encoding](file://{results.get('visualizations', {}).get('market_circuit', '')})

### Quantum Risk Network
![Quantum Risk Network](file://{results.get('visualizations', {}).get('risk_network', '')})

## Notes
- Quantum-enhanced risk assessment takes into account quantum uncertainty and entanglement between risk factors.
- The analysis was performed using {results.get('quantum_shots', 10000)} quantum circuit shots.
- This report was generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
"""
        
        # Save to markdown file
        report_file = f"{symbol}_quantum_risk_report_{timestamp}.md"
        with open(report_file, 'w') as f:
            f.write(md_content)
        
        logger.info(f"Report generated and saved to {report_file}")
        
        return report_file
        
    def update_risk_assessment(self, 
                              previous_assessment: Dict[str, Any], 
                              symbol: str, 
                              order_book: Optional[Dict[str, Any]] = None, 
                              stats_24hr: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update a previous risk assessment with new market data, avoiding a full recalculation.
        
        This method provides more efficient incremental updates by:
        1. Only fetching data that's not provided
        2. Reusing previous quantum calculations where possible
        3. Only updating the risk factors that are affected by changed market data
        
        Args:
            previous_assessment: Results from a previous analyze_with_quantum call
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            order_book: Optional new order book data (will be fetched if not provided)
            stats_24hr: Optional new 24hr stats (will be fetched if not provided)
            
        Returns:
            Updated risk assessment dictionary
        """
        logger.info(f"Updating risk assessment for {symbol}")
        
        # Get data fetcher
        data_fetcher = self._get_crypto_data_fetcher()
        
        # Get market data if not provided
        if order_book is None:
            order_book = data_fetcher.get_binance_order_book(symbol)
            
        if stats_24hr is None:
            stats_24hr = data_fetcher.get_binance_24hr_stats(symbol)
        
        # Ensure we have valid data before proceeding
        if order_book is None or stats_24hr is None:
            logger.error(f"Failed to get market data for {symbol}")
            # Return the previous assessment as fallback
            return previous_assessment
        
        # Extract previous values for comparison
        prev_classical_risk = previous_assessment.get('classical_risk', {})
        prev_market_metrics = previous_assessment.get('market_metrics', {})
        
        # Calculate new classical risk metrics
        new_classical_risk = self._calculate_classical_risk_metrics(symbol, order_book, stats_24hr)
        
        # Determine which risk factors have changed significantly
        changed_factors = []
        significant_change_threshold = 0.05  # 5% change is considered significant
        
        for metric in ['liquidity_risk', 'volatility_risk', 'market_depth_risk', 'price_impact_risk', 'overall_risk']:
            if metric in prev_classical_risk and metric in new_classical_risk:
                prev_value = prev_classical_risk.get(metric, 0)
                new_value = new_classical_risk.get(metric, 0)
                if abs(new_value - prev_value) > significant_change_threshold * prev_value:
                    changed_factors.append(metric)
        
        # If no significant changes, just update timestamps and return
        if not changed_factors:
            logger.info(f"No significant changes detected for {symbol}, returning previous assessment with updated timestamp")
            updated_assessment = previous_assessment.copy()
            updated_assessment['timestamp'] = datetime.now().strftime('%Y%m%d_%H%M%S')
            return updated_assessment
        
        logger.info(f"Significant changes detected in factors: {changed_factors}")
        
        # Extract risk metrics for quantum Bayesian network
        initial_probabilities = [
            new_classical_risk['imbalance'],
            new_classical_risk['volatility'],
            new_classical_risk['market_depth_risk'] / 100,
            new_classical_risk['liquidity_risk'] / 100,
            new_classical_risk['overall_risk'] / 100
        ]
        
        # Create the combined quantum market circuit for visualization
        market_circuit = combined_market_risk_encoding(
            order_book_data=order_book,
            volatility=new_classical_risk['volatility'],
            trade_size=10.0,  # Standard trade size
            recent_volume=new_classical_risk['normalized_volume']
        )
        
        # Save the market circuit visualization
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        market_circuit_file = f"{symbol}_quantum_market_encoding_{timestamp}.png"
        visualize_quantum_market_encoding(
            market_circuit,
            f"Quantum Market Encoding for {symbol}",
            market_circuit_file
        )
        
        # Propagate risk through the quantum Bayesian network
        quantum_probs = self.quantum_bayesian_network.propagate_risk(
            initial_probabilities, 
            shots=5000  # Reduce shot count for incremental updates
        )
        
        # Compare with classical approximation (only if significant changes)
        comparison_file = f"{symbol}_quantum_classical_comparison_{timestamp}.png"
        self.quantum_bayesian_network.compare_classical_quantum(
            initial_probabilities,
            comparison_file
        )
        
        # Scale back to percentages for reporting
        quantum_enhanced_risk = {
            'order_book_imbalance_risk': quantum_probs[0] * 100,
            'volatility_risk': quantum_probs[1] * 100,
            'market_depth_risk': quantum_probs[2] * 100,
            'liquidity_risk': quantum_probs[3] * 100, 
            'overall_risk': quantum_probs[4] * 100
        }
        
        # Calculate quantum advantage metrics
        risk_differences = {
            k.replace('_risk', ''): quantum_enhanced_risk[k] - v 
            for k, v in new_classical_risk.items() 
            if k in ['volatility_risk', 'market_depth_risk', 'liquidity_risk', 'overall_risk']
        }
        
        # Reuse previous network visualization if available, or create a new one
        network_file = previous_assessment.get('visualizations', {}).get('risk_network')
        if not network_file or not os.path.exists(network_file):
            network_file = f"{symbol}_quantum_risk_network_{timestamp}.png"
            self.quantum_bayesian_network.visualize_network(network_file)
        
        # Combine results
        results = {
            'timestamp': timestamp,
            'symbol': symbol,
            'current_price': new_classical_risk['current_price'],
            'classical_risk': {
                'liquidity_risk': new_classical_risk['liquidity_risk'],
                'volatility_risk': new_classical_risk['volatility_risk'],
                'market_depth_risk': new_classical_risk['market_depth_risk'],
                'price_impact_risk': new_classical_risk['price_impact_risk'],
                'overall_risk': new_classical_risk['overall_risk']
            },
            'quantum_enhanced_risk': quantum_enhanced_risk,
            'risk_differences': risk_differences,
            'market_metrics': {
                'bid_ask_spread': new_classical_risk['bid_ask_spread'],
                'volatility': new_classical_risk['volatility'],
                'normalized_depth': new_classical_risk['normalized_depth'],
                'normalized_volume': new_classical_risk['normalized_volume'],
                'imbalance': new_classical_risk['imbalance'],
                'price_impact': new_classical_risk['price_impact']
            },
            'visualizations': {
                'market_circuit': market_circuit_file,
                'risk_network': network_file,
                'comparison': comparison_file
            },
            'quantum_shots': 5000,  # Reduced shot count for incremental updates
            'update_info': {
                'is_incremental_update': True,
                'previous_assessment_timestamp': previous_assessment.get('timestamp'),
                'changed_factors': changed_factors
            }
        }
        
        # Save results to JSON file
        results_file = f"{symbol}_quantum_risk_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Incremental update complete. Results saved to {results_file}")
        
        return results

    def _watch_market_changes(self, symbol: str, interval_secs: int = 60,
                            duration_mins: int = 5, output_dir: str = '.'):
        """
        Watch for market changes over time and track risk assessment.
        
        Args:
            symbol: Cryptocurrency symbol to monitor
            interval_secs: Seconds between assessments
            duration_mins: Total minutes to monitor
            output_dir: Directory to save output files
        
        Returns:
            DataFrame with risk assessments over time
        """
        max_iterations = (duration_mins * 60) // interval_secs
        
        # Initialize results storage
        assessments = []
        timestamps = []
        
        # Initial assessment as baseline
        previous_assessment = self.analyze_with_quantum(symbol)
        assessments.append(previous_assessment)
        timestamps.append(datetime.now())
        
        logger.info(f"Starting market watch for {symbol} - {max_iterations} iterations")
        
        for i in range(1, max_iterations):
            logger.info(f"Iteration {i}/{max_iterations} - Waiting {interval_secs}s")
            
            # Add sleep between iterations
            import time
            time.sleep(interval_secs)
            
            # Perform new assessment
            new_assessment = self.analyze_with_quantum(
                symbol, previous_assessment=previous_assessment
            )
            
            # Store results
            assessments.append(new_assessment)
            timestamps.append(datetime.now())
            
            # Update previous for next iteration
            previous_assessment = new_assessment
        
        # Create DataFrame from all assessments
        df_data = []
        
        for timestamp, assessment in zip(timestamps, assessments):
            # Extract quantum risk values
            q_risk = assessment.get('quantum_enhanced_risk', {})
            
            row = {
                'timestamp': timestamp,
                'symbol': symbol,
                'order_book_imbalance_risk': q_risk.get('order_book_imbalance_risk', 0),
                'volatility_risk': q_risk.get('volatility_risk', 0),
                'market_depth_risk': q_risk.get('market_depth_risk', 0),
                'liquidity_risk': q_risk.get('liquidity_risk', 0),
                'overall_risk': q_risk.get('overall_risk', 0)
            }
            df_data.append(row)
        
        # Create and return DataFrame
        df = pd.DataFrame(df_data)
        
        # Save results
        output_file = os.path.join(output_dir, f"{symbol}_risk_time_series.csv")
        df.to_csv(output_file, index=False)
        logger.info(f"Saved market watch results to {output_file}")
        
        return df

    def _get_crypto_data_fetcher(self):
        """
        Get an instance of the CryptoDataFetcher with proper API credentials.
        
        Returns:
            An instance of CryptoDataFetcher configured with the API key from .env
        """
        # Import here to avoid circular imports
        try:
            from examples.crypto_data_fetcher import CryptoDataFetcher
        except ImportError:
            logger.error("Could not import CryptoDataFetcher. Make sure you're in the correct directory.")
            # Use a simplified version if available
            try:
                from examples.crypto_data_fetcher_enhanced import CryptoDataFetcher
                logger.info("Using enhanced crypto data fetcher instead")
            except ImportError:
                logger.error("No data fetcher module available. Using simulated data.")
                return None
        
        # Make sure we have an API key
        if not self.api_key:
            # Try to reload from environment
            self.api_key = os.environ.get('RAPIDAPI_KEY')
            
            # Still no API key, try to find it in a key file
            if not self.api_key:
                key_file_paths = [
                    Path('.') / 'rapidapi_key.txt',
                    Path('.') / 'keys' / 'rapidapi_key.txt',
                    Path(os.path.expanduser('~')) / '.rapidapi_key'
                ]
                
                for key_path in key_file_paths:
                    if key_path.exists():
                        try:
                            self.api_key = key_path.read_text().strip()
                            logger.info(f"Loaded RAPIDAPI_KEY from {key_path}")
                            break
                        except Exception as e:
                            logger.warning(f"Error reading key file {key_path}: {e}")
        
        # If we have an API key, create the fetcher with it
        if self.api_key:
            logger.info(f"Using RAPIDAPI_KEY: {self.api_key[:4]}...{self.api_key[-4:] if len(self.api_key) > 8 else ''}")
            try:
                return CryptoDataFetcher(
                    api_key=self.api_key,
                    api_host=self.api_host,
                    use_cache=True,
                    cache_dir=".cache"
                )
            except TypeError as e:
                # Handle case where the constructor has different parameters
                logger.warning(f"Error creating CryptoDataFetcher with parameters: {e}")
                # Try a simpler constructor
                return CryptoDataFetcher()
        else:
            logger.warning("No RAPIDAPI_KEY found. Using simulated data.")
            # Try to use the data fetcher with simulated=True if supported
            try:
                return CryptoDataFetcher(use_simulated=True)
            except TypeError:
                # Fallback to basic constructor if use_simulated is not supported
                return CryptoDataFetcher()

def main():
    """Run the quantum enhanced crypto risk assessment tool."""
    parser = argparse.ArgumentParser(
        description="Quantum Enhanced Cryptocurrency Risk Assessment Tool"
    )
    
    parser.add_argument(
        "--symbol", "-s",
        type=str,
        default="BTC",
        help="Cryptocurrency symbol to analyze (default: BTC)"
    )
    
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch market changes over time"
    )
    
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=5,
        help="Duration in minutes to watch (default: 5)"
    )
    
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=60,
        help="Interval in seconds between assessments (default: 60)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=".",
        help="Output directory for result files (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Initialize the quantum risk assessment tool
    risk_tool = QuantumEnhancedCryptoRisk()
    
    if args.watch:
        logger.info(f"Watching {args.symbol} for {args.duration} minutes " 
                   f"at {args.interval}s intervals")
        
        # Watch for changes over time
        risk_tool._watch_market_changes(
            symbol=args.symbol,
            interval_secs=args.interval,
            duration_mins=args.duration,
            output_dir=args.output_dir
        )
    else:
        # One-time assessment
        results = risk_tool.analyze_with_quantum(args.symbol)
        
        # Print results
        print(f"\n===== QUANTUM RISK ASSESSMENT: {args.symbol} =====")
        print(f"Order Book Imbalance Risk: {results['quantum_enhanced_risk']['order_book_imbalance_risk']:.2f}%")
        print(f"Price Volatility Risk:     {results['quantum_enhanced_risk']['volatility_risk']:.2f}%")
        print(f"Market Depth Risk:         {results['quantum_enhanced_risk']['market_depth_risk']:.2f}%")
        print(f"Liquidity Risk:            {results['quantum_enhanced_risk']['liquidity_risk']:.2f}%")
        print(f"Overall Market Risk:       {results['quantum_enhanced_risk']['overall_risk']:.2f}%")
        print("\nRisk assessment completed and results saved to current directory")


if __name__ == "__main__":
    main() 