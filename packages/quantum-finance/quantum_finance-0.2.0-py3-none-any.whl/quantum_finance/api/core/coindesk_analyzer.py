#!/usr/bin/env python3

"""
CoinDesk Data Analyzer

This module analyzes Bitcoin price data from the CoinDesk API to derive insights
for cryptocurrency market predictions. It identifies trends in Bitcoin prices,
volatility patterns, and price movement indicators that can signal potential
market directions.

The analysis is based on several key indicators:
1. Price trend analysis - Identifying short and long-term trends
2. Volatility calculation - Measuring price stability/instability
3. Moving averages - For trend confirmation
4. Relative price performance - Comparing current prices to historical ranges

Author: Quantum-AI Team
"""

import os
import logging
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import stats
from dataclasses import dataclass, field

# Import the CoinDesk client using the correct absolute path
from quantum_finance.api_clients.coindesk_client import CoinDeskClient, CoinDeskConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PriceMetrics:
    """Container for calculated price metrics."""
    # Current price
    current_price: float
    
    # Price changes
    price_change_24h: float  # Change in price over last 24 hours (percent)
    price_change_7d: float   # Change in price over last 7 days (percent)
    price_change_30d: float  # Change in price over last 30 days (percent)
    
    # Volatility metrics
    volatility_7d: float  # 7-day price volatility (standard deviation of daily returns)
    volatility_30d: float  # 30-day price volatility
    
    # Moving averages
    sma_7d: float  # 7-day simple moving average
    sma_30d: float  # 30-day simple moving average
    sma_90d: float  # 90-day simple moving average
    
    # Trend indicators
    price_momentum: float  # Momentum indicator (-1 to 1)
    trend_strength: float  # Strength of current trend (0 to 1)
    
    # Market indicators
    market_sentiment: float  # -1 to 1 scale (bearish to bullish)
    price_position: float    # Current position in 52-week range (0 to 1)
    
    # Timestamp of the analysis
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Currency used for analysis
    currency: str = "USD"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to a dictionary."""
        result = {k: v for k, v in self.__dict__.items() if k != 'timestamp'}
        result['timestamp'] = self.timestamp.isoformat()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PriceMetrics':
        """Create metrics from a dictionary."""
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data = data.copy()  # Create a copy to avoid modifying the original
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class CoinDeskAnalyzer:
    """
    Analyzes Bitcoin price data to derive market indicators.
    
    This class calculates various metrics and indicators based on historical and
    current Bitcoin price data from CoinDesk, which can be used to inform 
    cryptocurrency market predictions.
    """
    
    def __init__(self, coindesk_client: Optional[CoinDeskClient] = None, 
                save_path: str = "./output/coindesk_analysis"):
        """
        Initialize the CoinDesk analyzer.
        
        Args:
            coindesk_client: Optional CoinDeskClient instance to use.
                           If None, a new instance will be created.
            save_path: Directory to save analysis results to
        """
        self.client = coindesk_client or CoinDeskClient()
        self.save_path = save_path
        
        # Ensure the save path exists
        os.makedirs(self.save_path, exist_ok=True)
        
        logger.info(f"Initialized CoinDeskAnalyzer with save path: {self.save_path}")
    
    def analyze_current_price(self, currency: str = "USD", save_result: bool = False) -> PriceMetrics:
        """
        Analyze the current Bitcoin price data and calculate metrics.
        
        Args:
            currency: Currency code to use for price data (default: "USD")
            save_result: Whether to save the metrics to a file
            
        Returns:
            PriceMetrics object containing the calculated metrics
        """
        logger.info(f"Analyzing current Bitcoin price data in {currency}")
        
        try:
            # Get current price
            current_price_data = self.client.get_current_price(currency)
            
            if not current_price_data or 'bpi' not in current_price_data:
                logger.error(f"Failed to retrieve current price data: {current_price_data}")
                raise ValueError("Invalid price data received from CoinDesk API")
            
            # Extract the current price for the specified currency
            if currency.upper() in current_price_data['bpi']:
                current_price = current_price_data['bpi'][currency.upper()]['rate_float']
            else:
                logger.error(f"Currency {currency} not found in BPI data")
                raise ValueError(f"Currency {currency} not available in CoinDesk BPI")
            
            # Get historical data for analysis (last 90 days)
            now = datetime.now()
            start_date = now - timedelta(days=90)
            historical_data = self.client.get_historical_prices_as_dataframe(
                start_date=start_date,
                end_date=now,
                currency=currency
            )
            
            if historical_data.empty:
                logger.error("Failed to retrieve historical price data")
                raise ValueError("Unable to retrieve historical price data from CoinDesk API")
            
            # Calculate price changes
            price_24h_ago = self._get_price_n_days_ago(historical_data, 1)
            price_7d_ago = self._get_price_n_days_ago(historical_data, 7)
            price_30d_ago = self._get_price_n_days_ago(historical_data, 30)
            
            price_change_24h = self._calculate_percentage_change(current_price, price_24h_ago)
            price_change_7d = self._calculate_percentage_change(current_price, price_7d_ago)
            price_change_30d = self._calculate_percentage_change(current_price, price_30d_ago)
            
            # Calculate volatility
            volatility_7d = self._calculate_volatility(historical_data, 7)
            volatility_30d = self._calculate_volatility(historical_data, 30)
            
            # Calculate moving averages
            sma_7d = self._calculate_sma(historical_data, 7)
            sma_30d = self._calculate_sma(historical_data, 30)
            sma_90d = self._calculate_sma(historical_data, 90)
            
            # Calculate trend indicators
            price_momentum = self._calculate_momentum(historical_data)
            trend_strength = self._calculate_trend_strength(historical_data)
            
            # Calculate market indicators
            market_sentiment = self._calculate_market_sentiment(
                price_change_24h, price_change_7d, price_momentum
            )
            price_position = self._calculate_price_position(historical_data, current_price)
            
            # Create metrics object
            metrics = PriceMetrics(
                current_price=current_price,
                price_change_24h=price_change_24h,
                price_change_7d=price_change_7d,
                price_change_30d=price_change_30d,
                volatility_7d=volatility_7d,
                volatility_30d=volatility_30d,
                sma_7d=sma_7d,
                sma_30d=sma_30d,
                sma_90d=sma_90d,
                price_momentum=price_momentum,
                trend_strength=trend_strength,
                market_sentiment=market_sentiment,
                price_position=price_position,
                currency=currency
            )
            
            logger.info(f"Analysis complete: current price {currency} {current_price}, "
                        f"24h change: {price_change_24h:.2f}%, "
                        f"sentiment: {market_sentiment:.2f}")
            
            # Save the results if requested
            if save_result:
                self._save_metrics(metrics)
                
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing price data: {e}")
            raise
    
    def _get_price_n_days_ago(self, historical_data: pd.DataFrame, n_days: int) -> float:
        """Get the price from n days ago from a DataFrame of historical data."""
        # Find the date n days ago
        target_date = datetime.now().date() - timedelta(days=n_days)
        
        # Find the closest date in the data
        closest_date = self._find_closest_date(historical_data.index, target_date)
        
        if closest_date is not None:
            return float(historical_data.at[closest_date, 'price'])
        
        # Fall back to the oldest available price if no match
        return float(historical_data.iloc[0]['price'])
    
    def _find_closest_date(self, dates: pd.Index, target_date) -> Optional[pd.Timestamp]:
        """Find the closest date in a pandas Index to a target date."""
        if isinstance(target_date, datetime):
            target_date = target_date.date()
            
        # Convert all timestamps to date objects for comparison
        date_diffs = {}
        for date in dates:
            if hasattr(date, 'date'):  # Check if it's a datetime-like object
                date_diff = abs((date.date() - target_date).days)
                date_diffs[date] = date_diff
        
        # Find the date with the minimum difference
        if not date_diffs:
            return None
        
        closest_dates = sorted(date_diffs.items(), key=lambda x: x[1])
        
        return closest_dates[0][0] if closest_dates else None
    
    def _calculate_percentage_change(self, current: float, previous: float) -> float:
        """Calculate percentage change between two values."""
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100
    
    def _calculate_volatility(self, df: pd.DataFrame, days: int) -> float:
        """Calculate the volatility (standard deviation of daily returns) over a period."""
        # Get the most recent data
        recent_data = df.iloc[-days:] if len(df) >= days else df
        
        # Calculate daily returns
        returns = recent_data['price'].pct_change().dropna()
        
        # Return the standard deviation of returns (annualized)
        return float(returns.std() * np.sqrt(365)) if not returns.empty else 0
    
    def _calculate_sma(self, df: pd.DataFrame, window: int) -> float:
        """Calculate the Simple Moving Average for a given window."""
        if len(df) < window:
            # If we don't have enough data, use what we have
            return float(df['price'].mean())
        
        return float(df['price'].iloc[-window:].mean())
    
    def _calculate_momentum(self, df: pd.DataFrame) -> float:
        """
        Calculate a momentum indicator based on recent price movements.
        
        Returns a value between -1 (strong downward momentum) and 1 (strong upward momentum).
        """
        if len(df) < 14:
            return 0
        
        # Use 14-day Rate of Change (ROC) as momentum indicator
        roc = ((df['price'].iloc[-1] / df['price'].iloc[-14]) - 1) * 100
        
        # Normalize to -1 to 1 range (assuming typical ROC values between -20 and 20)
        normalized_roc = max(min(roc / 20, 1), -1)
        
        return float(normalized_roc)
    
    def _calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """
        Calculate the strength of the current trend.
        
        Returns a value between 0 (weak/no trend) and 1 (strong trend).
        """
        if len(df) < 30:
            return 0.0
        
        try:
            # Get the most recent 30 days of price data
            recent_prices = df['price'].iloc[-30:].values
            days = np.arange(len(recent_prices))
            
            # Simple calculation based on the price change and consistency
            price_change = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
            
            # Convert to a 0-1 scale (0.2 or 20% change is considered strong)
            normalized_change = min(abs(price_change) / 0.2, 1.0)
            
            # Factor in the direction (positive = stronger trend)
            direction_factor = 0.5
            if price_change > 0:
                direction_factor = 0.7  # Upward trends get a boost
            elif price_change < 0:
                direction_factor = 0.3  # Downward trends get reduced
            
            # Calculate consistency by comparing daily movements
            consistent_days = 0
            for i in range(1, len(recent_prices)):
                if price_change > 0 and recent_prices[i] >= recent_prices[i-1]:
                    consistent_days += 1
                elif price_change < 0 and recent_prices[i] <= recent_prices[i-1]:
                    consistent_days += 1
            
            consistency = consistent_days / (len(recent_prices) - 1)
            
            # Combine factors for final trend strength
            trend_strength = normalized_change * direction_factor * consistency
            
            return float(trend_strength)
        except Exception as e:
            logger.warning(f"Error calculating trend strength: {e}")
            return 0.0
    
    def _calculate_market_sentiment(
        self, 
        price_change_24h: float, 
        price_change_7d: float, 
        momentum: float
    ) -> float:
        """
        Calculate a market sentiment indicator based on recent price changes and momentum.
        
        Returns a value between -1 (bearish) and 1 (bullish).
        """
        # Weight recent price changes and momentum
        weights = {
            'price_change_24h': 0.4,
            'price_change_7d': 0.3,
            'momentum': 0.3
        }
        
        # Normalize price changes to -1 to 1 range (assuming ±10% is significant)
        normalized_24h = max(min(price_change_24h / 10, 1), -1)
        normalized_7d = max(min(price_change_7d / 20, 1), -1)
        
        # Calculate weighted sentiment
        sentiment = (
            weights['price_change_24h'] * normalized_24h +
            weights['price_change_7d'] * normalized_7d +
            weights['momentum'] * momentum
        )
        
        return float(sentiment)
    
    def _calculate_price_position(self, df: pd.DataFrame, current_price: float) -> float:
        """
        Calculate the current price position within the 52-week range.
        
        Returns a value between 0 (at 52-week low) and 1 (at 52-week high).
        """
        if df.empty:
            return 0.5
        
        # Find the min and max price in the dataframe
        min_price = df['price'].min()
        max_price = df['price'].max()
        
        if max_price == min_price:
            return 0.5
        
        # Calculate the position as a percentage of the range
        position = (current_price - min_price) / (max_price - min_price)
        
        return float(position)
    
    def interpret_market_signals(self, metrics: PriceMetrics) -> Dict[str, Any]:
        """
        Interpret the calculated metrics to provide market insights.
        
        Args:
            metrics: The PriceMetrics object to interpret
            
        Returns:
            Dictionary containing market signals and interpretations
        """
        signals = {
            'price_trend': {
                'signal': 'neutral',
                'strength': 0,
                'description': 'Market direction is unclear'
            },
            'volatility': {
                'signal': 'normal',
                'value': metrics.volatility_30d,
                'description': 'Market volatility is within normal range'
            },
            'momentum': {
                'signal': 'neutral',
                'value': metrics.price_momentum,
                'description': 'No significant momentum detected'
            },
            'market_position': {
                'signal': 'mid_range',
                'value': metrics.price_position,
                'description': 'Price is in the middle of its recent range'
            },
            'moving_averages': {
                'signal': 'neutral',
                'description': 'No clear moving average signals'
            },
            'overall_sentiment': {
                'signal': 'neutral',
                'value': metrics.market_sentiment,
                'description': 'Overall market sentiment is neutral'
            }
        }
        
        # Interpret price trend
        if metrics.price_change_7d > 5:
            signals['price_trend'] = {
                'signal': 'bullish',
                'strength': min(metrics.price_change_7d / 10, 1),
                'description': f'Strong upward trend with {metrics.price_change_7d:.1f}% 7-day gain'
            }
        elif metrics.price_change_7d < -5:
            signals['price_trend'] = {
                'signal': 'bearish',
                'strength': min(abs(metrics.price_change_7d) / 10, 1),
                'description': f'Strong downward trend with {abs(metrics.price_change_7d):.1f}% 7-day loss'
            }
        elif metrics.price_change_7d > 2:
            signals['price_trend'] = {
                'signal': 'mildly_bullish',
                'strength': metrics.price_change_7d / 5,
                'description': f'Mild upward trend with {metrics.price_change_7d:.1f}% 7-day gain'
            }
        elif metrics.price_change_7d < -2:
            signals['price_trend'] = {
                'signal': 'mildly_bearish',
                'strength': abs(metrics.price_change_7d) / 5,
                'description': f'Mild downward trend with {abs(metrics.price_change_7d):.1f}% 7-day loss'
            }
        
        # Interpret volatility
        if metrics.volatility_30d > 0.8:
            signals['volatility'] = {
                'signal': 'very_high',
                'value': metrics.volatility_30d,
                'description': 'Extremely high market volatility, indicating uncertainty'
            }
        elif metrics.volatility_30d > 0.5:
            signals['volatility'] = {
                'signal': 'high',
                'value': metrics.volatility_30d,
                'description': 'High market volatility, potential for rapid price movements'
            }
        elif metrics.volatility_30d < 0.2:
            signals['volatility'] = {
                'signal': 'low',
                'value': metrics.volatility_30d,
                'description': 'Low market volatility, indicating stability'
            }
        
        # Interpret momentum
        if metrics.price_momentum > 0.5:
            signals['momentum'] = {
                'signal': 'strong_positive',
                'value': metrics.price_momentum,
                'description': 'Strong positive momentum, suggesting continued upward movement'
            }
        elif metrics.price_momentum > 0.2:
            signals['momentum'] = {
                'signal': 'positive',
                'value': metrics.price_momentum,
                'description': 'Positive momentum, suggesting upward bias'
            }
        elif metrics.price_momentum < -0.5:
            signals['momentum'] = {
                'signal': 'strong_negative',
                'value': metrics.price_momentum,
                'description': 'Strong negative momentum, suggesting continued downward movement'
            }
        elif metrics.price_momentum < -0.2:
            signals['momentum'] = {
                'signal': 'negative',
                'value': metrics.price_momentum,
                'description': 'Negative momentum, suggesting downward bias'
            }
        
        # Interpret market position
        if metrics.price_position > 0.8:
            signals['market_position'] = {
                'signal': 'near_high',
                'value': metrics.price_position,
                'description': 'Price is near its recent high, potential resistance'
            }
        elif metrics.price_position < 0.2:
            signals['market_position'] = {
                'signal': 'near_low',
                'value': metrics.price_position,
                'description': 'Price is near its recent low, potential support'
            }
        
        # Interpret moving averages
        if metrics.current_price > metrics.sma_7d > metrics.sma_30d > metrics.sma_90d:
            signals['moving_averages'] = {
                'signal': 'strong_uptrend',
                'description': 'All moving averages aligned in uptrend configuration'
            }
        elif metrics.current_price < metrics.sma_7d < metrics.sma_30d < metrics.sma_90d:
            signals['moving_averages'] = {
                'signal': 'strong_downtrend',
                'description': 'All moving averages aligned in downtrend configuration'
            }
        elif metrics.current_price > metrics.sma_30d:
            signals['moving_averages'] = {
                'signal': 'bullish',
                'description': 'Price above 30-day moving average, suggesting bullish bias'
            }
        elif metrics.current_price < metrics.sma_30d:
            signals['moving_averages'] = {
                'signal': 'bearish',
                'description': 'Price below 30-day moving average, suggesting bearish bias'
            }
        
        # Interpret overall sentiment
        if metrics.market_sentiment > 0.6:
            signals['overall_sentiment'] = {
                'signal': 'strongly_bullish',
                'value': metrics.market_sentiment,
                'description': 'Market sentiment is strongly bullish'
            }
        elif metrics.market_sentiment > 0.2:
            signals['overall_sentiment'] = {
                'signal': 'bullish',
                'value': metrics.market_sentiment,
                'description': 'Market sentiment is bullish'
            }
        elif metrics.market_sentiment < -0.6:
            signals['overall_sentiment'] = {
                'signal': 'strongly_bearish',
                'value': metrics.market_sentiment,
                'description': 'Market sentiment is strongly bearish'
            }
        elif metrics.market_sentiment < -0.2:
            signals['overall_sentiment'] = {
                'signal': 'bearish',
                'value': metrics.market_sentiment,
                'description': 'Market sentiment is bearish'
            }
        
        return signals
    
    def generate_price_chart(self, days: int = 30, save_path: Optional[str] = None) -> str:
        """
        Generate a chart showing the Bitcoin price trend over the specified period.
        
        Args:
            days: Number of days to include in the chart
            save_path: Optional path to save the chart to. If None, a default path will be used.
            
        Returns:
            Path to the saved chart image
        """
        try:
            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            historical_data = self.client.get_historical_prices_as_dataframe(
                start_date=start_date,
                end_date=end_date
            )
            
            if historical_data.empty:
                logger.error("Failed to retrieve historical price data for chart")
                raise ValueError("Unable to retrieve historical price data from CoinDesk API")
            
            # Create the chart
            plt.figure(figsize=(12, 6))
            
            # Plot the price line
            plt.plot(historical_data.index, historical_data['price'], 'b-', linewidth=2)
            
            # Plot moving averages if we have enough data
            if len(historical_data) >= 7:
                sma7 = historical_data['price'].rolling(window=7).mean()
                plt.plot(historical_data.index, sma7, 'r--', linewidth=1, label='7-day MA')
            
            if len(historical_data) >= 30:
                sma30 = historical_data['price'].rolling(window=30).mean()
                plt.plot(historical_data.index, sma30, 'g--', linewidth=1, label='30-day MA')
            
            # Add labels and title
            plt.title(f'Bitcoin Price (USD) - Last {days} Days', fontsize=14)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Price (USD)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Format the y-axis as currency
            plt.gca().yaxis.set_major_formatter('${x:,.0f}')
            
            # Add current price annotation
            current_price = historical_data['price'].iloc[-1]
            plt.annotate(f'${current_price:,.2f}', 
                        xy=(historical_data.index[-1], current_price),
                        xytext=(10, 0), 
                        textcoords='offset points',
                        fontsize=12,
                        fontweight='bold')
            
            # Save the chart
            if not save_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                save_path = os.path.join(self.save_path, f'bitcoin_price_chart_{timestamp}.png')
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=100)
            plt.close()
            
            logger.info(f"Price chart saved to {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error generating price chart: {e}")
            raise
    
    def _save_metrics(self, metrics: PriceMetrics) -> str:
        """
        Save the price metrics to a JSON file.
        
        Args:
            metrics: The PriceMetrics object to save
            
        Returns:
            Path to the saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.save_path, f'bitcoin_price_metrics_{timestamp}.json')
        
        try:
            with open(filename, 'w') as f:
                json.dump(metrics.to_dict(), f, indent=2)
            
            logger.info(f"Price metrics saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving price metrics: {e}")
            raise
    
    def schedule_regular_analysis(self, interval_minutes: int = 60, max_runs: Optional[int] = None):
        """
        Schedule regular price analysis at a specified interval.
        
        Args:
            interval_minutes: Interval in minutes between analyses
            max_runs: Maximum number of analyses to run, or None for unlimited
        """
        import time
        from threading import Thread, Event
        
        stop_event = Event()
        
        def analysis_worker():
            runs = 0
            while not stop_event.is_set() and (max_runs is None or runs < max_runs):
                try:
                    # Run the analysis and save the results
                    metrics = self.analyze_current_price(save_result=True)
                    
                    # Generate and save a price chart
                    self.generate_price_chart()
                    
                    # Increment the run counter
                    runs += 1
                    
                    logger.info(f"Completed scheduled analysis run {runs}"
                               f"{f'/{max_runs}' if max_runs else ''}")
                    
                except Exception as e:
                    logger.error(f"Error in scheduled analysis: {e}")
                
                # Wait for the next interval, but check for stop periodically
                for _ in range(interval_minutes * 60 // 10):
                    if stop_event.is_set():
                        break
                    time.sleep(10)
        
        analysis_thread = Thread(target=analysis_worker, daemon=True)
        analysis_thread.start()
        
        logger.info(f"Started scheduled price analysis every {interval_minutes} minutes")
        
        # Return the stop event that can be used to stop the scheduled analysis
        return stop_event 