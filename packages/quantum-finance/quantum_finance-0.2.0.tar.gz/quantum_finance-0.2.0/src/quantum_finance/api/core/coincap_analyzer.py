#!/usr/bin/env python3

"""
CoinCap Data Analyzer

This module analyzes cryptocurrency market data from the CoinCap API to derive insights
for cryptocurrency market predictions. It identifies trends in cryptocurrency prices,
volatility patterns, and market metrics that can signal potential market directions.

The analysis is based on several key indicators:
1. Price trend analysis - Identifying short and long-term trends
2. Volatility calculation - Measuring price stability/instability
3. Moving averages - For trend confirmation
4. Market cap analysis - Evaluating relative market capitalization
5. Volume analysis - Monitoring trading activity

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
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats
from dataclasses import dataclass, field
import time

# Import the CoinCap client
from quantum_finance.api_clients.coincap_client import CoinCapClient, CoinCapConfig, Interval

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class MarketMetrics:
    """Container for calculated market metrics."""
    # Current price and basic info
    symbol: str
    name: str
    current_price: float
    market_cap: float
    volume_24h: float
    supply: float
    
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
    price_position: float    # Current position in historical range (0 to 1)
    
    # Market cap metrics
    market_cap_rank: int  # Rank by market cap
    market_cap_change_24h: float  # Change in market cap over last 24 hours (percent)
    market_dominance: float  # Percentage of total market cap
    
    # Volume metrics
    volume_change_24h: float  # Change in volume over last 24 hours (percent)
    volume_to_market_cap: float  # Volume/Market Cap ratio (measure of liquidity)
    
    # Timestamp of the analysis
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to a dictionary."""
        result = {k: v for k, v in self.__dict__.items() if k != 'timestamp'}
        result['timestamp'] = self.timestamp.isoformat()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketMetrics':
        """Create metrics from a dictionary."""
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data = data.copy()  # Create a copy to avoid modifying the original
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class CoinCapAnalyzer:
    """
    Analyzer for cryptocurrency market data from CoinCap API.
    
    This class provides methods to analyze cryptocurrency data,
    calculate market metrics, and generate visualizations.
    """
    
    def __init__(self, coincap_client: Optional[CoinCapClient] = None, 
                api_key: Optional[str] = None,
                save_path: str = "./output/coincap_analysis"):
        """
        Initialize the CoinCap analyzer.
        
        Args:
            coincap_client: Optional CoinCapClient instance
            api_key: API key for authentication (if client not provided)
            save_path: Directory to save analysis results
        """
        self.client = coincap_client or CoinCapClient(api_key=api_key)
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)
        logger.info(f"CoinCap analyzer initialized with save path: {save_path}")
        
        # Initialize cache for market data
        self._cache = {}
        self._cache_ttl = 60 * 5  # 5 minutes
    
    def analyze_asset(self, asset_id: str = "bitcoin", save_result: bool = False) -> MarketMetrics:
        """
        Analyze a specific cryptocurrency asset.
        
        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            save_result: Whether to save the analysis results
            
        Returns:
            MarketMetrics object with analysis results
        """
        logger.info(f"Analyzing asset: {asset_id}")
        start_time = time.time()
        
        # Get current asset data
        asset_data = self.client.get_asset(asset_id)
        if not asset_data.get('data'):
            logger.error(f"Failed to get data for asset: {asset_id}")
            raise ValueError(f"No data found for asset: {asset_id}")
            
        asset = asset_data['data']
        
        # Get historical price data
        end_date = datetime.now()
        start_date_90d = end_date - timedelta(days=90)
        
        historical_df = self.client.get_asset_prices_as_dataframe(
            asset_id=asset_id,
            interval=Interval.DAY_1,
            start=start_date_90d,
            end=end_date
        )
        
        if historical_df.empty:
            logger.error(f"Failed to get historical data for asset: {asset_id}")
            raise ValueError(f"No historical data found for asset: {asset_id}")
        
        # Get global market data for market dominance calculation
        global_data = self.client.get_assets(limit=1)
        total_market_cap = sum(float(a['marketCapUsd'] or 0) for a in global_data.get('data', []))
        
        # Calculate metrics
        current_price = float(asset['priceUsd'])
        market_cap = float(asset['marketCapUsd'] or 0)
        volume_24h = float(asset['volumeUsd24Hr'] or 0)
        supply = float(asset['supply'] or 0)
        
        # Price changes
        price_change_24h = float(asset['changePercent24Hr'] or 0)
        
        # Calculate additional price changes from historical data
        price_change_7d = self._calculate_price_change(historical_df, days=7)
        price_change_30d = self._calculate_price_change(historical_df, days=30)
        
        # Volatility
        volatility_7d = self._calculate_volatility(historical_df, days=7)
        volatility_30d = self._calculate_volatility(historical_df, days=30)
        
        # Moving averages
        sma_7d = self._calculate_sma(historical_df, window=7)
        sma_30d = self._calculate_sma(historical_df, window=30)
        sma_90d = self._calculate_sma(historical_df, window=90)
        
        # Trend indicators
        price_momentum = self._calculate_momentum(historical_df)
        trend_strength = self._calculate_trend_strength(historical_df)
        
        # Market indicators
        market_sentiment = self._calculate_market_sentiment(
            price_change_24h, price_change_7d, price_momentum
        )
        price_position = self._calculate_price_position(historical_df, current_price)
        
        # Market cap metrics
        market_cap_rank = int(asset['rank'])
        market_cap_change_24h = price_change_24h  # Approximation if not directly available
        market_dominance = (market_cap / total_market_cap * 100) if total_market_cap > 0 else 0
        
        # Volume metrics
        # Note: Volume change would need historical volume data, using 0 as placeholder
        volume_change_24h = 0
        volume_to_market_cap = (volume_24h / market_cap) if market_cap > 0 else 0
        
        # Create metrics object
        metrics = MarketMetrics(
            symbol=asset['symbol'],
            name=asset['name'],
            current_price=current_price,
            market_cap=market_cap,
            volume_24h=volume_24h,
            supply=supply,
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
            market_cap_rank=market_cap_rank,
            market_cap_change_24h=market_cap_change_24h,
            market_dominance=market_dominance,
            volume_change_24h=volume_change_24h,
            volume_to_market_cap=volume_to_market_cap,
            timestamp=datetime.now()
        )
        
        logger.info(f"Analysis completed in {time.time() - start_time:.2f} seconds")
        
        # Save results if requested
        if save_result:
            self._save_metrics(metrics)
            self.generate_price_chart(asset_id, days=90)
            
        return metrics
    
    def analyze_top_assets(self, limit: int = 10, save_results: bool = False) -> List[MarketMetrics]:
        """
        Analyze top cryptocurrencies by market cap.
        
        Args:
            limit: Number of top assets to analyze
            save_results: Whether to save the analysis results
            
        Returns:
            List of MarketMetrics objects with analysis results
        """
        logger.info(f"Analyzing top {limit} assets")
        
        # Get top assets by market cap
        assets_data = self.client.get_assets(limit=limit)
        if not assets_data.get('data'):
            logger.error("Failed to get top assets data")
            raise ValueError("No data found for top assets")
            
        # Analyze each asset
        results = []
        for asset in assets_data['data']:
            try:
                metrics = self.analyze_asset(asset['id'], save_result=save_results)
                results.append(metrics)
            except Exception as e:
                logger.error(f"Error analyzing asset {asset['id']}: {e}")
                
        return results
    
    def _calculate_price_change(self, df: pd.DataFrame, days: int) -> float:
        """
        Calculate percentage price change over a period.
        
        Args:
            df: DataFrame with historical price data
            days: Number of days to calculate change over
            
        Returns:
            Percentage price change
        """
        if df.empty or len(df) < 2:
            return 0.0
            
        # Try to get the price from n days ago
        days_ago = datetime.now() - timedelta(days=days)
        closest_date = self._find_closest_date(df.index, days_ago)
        
        if closest_date is None:
            return 0.0
            
        past_price = df.loc[closest_date, 'priceUsd']
        current_price = df['priceUsd'].iloc[-1]
        
        return ((current_price / past_price) - 1) * 100
    
    def _find_closest_date(self, dates: pd.DatetimeIndex, target_date: datetime) -> Optional[pd.Timestamp]:
        """
        Find the closest date in a DatetimeIndex to a target date.
        
        Args:
            dates: DatetimeIndex of dates
            target_date: Target date to find closest to
            
        Returns:
            Closest date in the index or None if index is empty
        """
        if len(dates) == 0:
            return None
            
        target_date = pd.Timestamp(target_date)
        time_diffs = np.abs((dates - target_date).total_seconds())
        closest_idx = np.argmin(time_diffs)
        return dates[closest_idx]
    
    def _calculate_volatility(self, df: pd.DataFrame, days: int) -> float:
        """
        Calculate price volatility over a period.
        
        Args:
            df: DataFrame with historical price data
            days: Number of days to calculate volatility over
            
        Returns:
            Volatility (standard deviation of daily returns)
        """
        if df.empty or len(df) < 2:
            return 0.0
            
        # Use the last 'days' rows, or all if less are available
        n_rows = min(days, len(df))
        recent_data = df.iloc[-n_rows:]
        
        # Calculate daily returns
        returns = recent_data['priceUsd'].pct_change().dropna()
        
        # Return standard deviation of returns
        return returns.std() * 100
    
    def _calculate_sma(self, df: pd.DataFrame, window: int) -> float:
        """
        Calculate simple moving average.
        
        Args:
            df: DataFrame with historical price data
            window: Window size for SMA calculation
            
        Returns:
            Simple moving average value
        """
        if df.empty or len(df) < window:
            return 0.0
            
        return df['priceUsd'].rolling(window=window).mean().iloc[-1]
    
    def _calculate_momentum(self, df: pd.DataFrame) -> float:
        """
        Calculate price momentum indicator.
        
        The momentum indicator measures the strength of recent price changes,
        normalized to a -1 to 1 scale.
        
        Args:
            df: DataFrame with historical price data
            
        Returns:
            Momentum indicator value (-1 to 1)
        """
        if df.empty or len(df) < 30:
            return 0.0
            
        # Calculate returns over various timeframes
        returns_1d = df['priceUsd'].pct_change(1).iloc[-1]
        returns_7d = df['priceUsd'].pct_change(7).iloc[-1]
        returns_30d = df['priceUsd'].pct_change(30).iloc[-1]
        
        # Weight the returns (more weight to recent returns)
        weighted_momentum = (0.5 * returns_1d) + (0.3 * returns_7d) + (0.2 * returns_30d)
        
        # Normalize to -1 to 1 range using tanh
        return np.tanh(weighted_momentum * 10)
    
    def _calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """
        Calculate the strength of the current price trend.
        
        The trend strength measures how consistently prices are moving in a direction,
        with values closer to 1 indicating stronger trends.
        
        Args:
            df: DataFrame with historical price data
            
        Returns:
            Trend strength value (0 to 1)
        """
        if df.empty or len(df) < 30:
            return 0.0
            
        # Get recent price data
        recent_data = df.iloc[-30:]['priceUsd']
        
        # Calculate daily returns
        returns = recent_data.pct_change().dropna()
        
        if len(returns) < 2:
            return 0.0
            
        # Calculate trend consistency
        # 1. Count how many days the price moved in the same direction as the overall trend
        overall_trend = np.sign(returns.mean())
        consistent_days = sum(np.sign(returns) == overall_trend)
        
        # 2. Calculate R-squared of a linear regression on prices
        x = np.arange(len(recent_data))
        slope, _, r_value, _, _ = stats.linregress(x, recent_data.values)
        r_squared = r_value ** 2
        
        # Combine both metrics
        direction_consistency = consistent_days / len(returns)
        
        # Weighted combination (adjust weights as needed)
        trend_strength = (0.6 * r_squared) + (0.4 * direction_consistency)
        
        return min(1.0, max(0.0, trend_strength))
    
    def _calculate_market_sentiment(
        self, 
        price_change_24h: float, 
        price_change_7d: float, 
        momentum: float
    ) -> float:
        """
        Calculate market sentiment indicator.
        
        The market sentiment indicator combines recent price changes and momentum
        to gauge overall market sentiment, from -1 (bearish) to 1 (bullish).
        
        Args:
            price_change_24h: 24-hour price change percentage
            price_change_7d: 7-day price change percentage
            momentum: Price momentum indicator
            
        Returns:
            Market sentiment value (-1 to 1)
        """
        # Normalize price changes to -1 to 1 range
        norm_24h = np.tanh(price_change_24h / 10)
        norm_7d = np.tanh(price_change_7d / 20)
        
        # Weight the components
        sentiment = (0.4 * norm_24h) + (0.3 * norm_7d) + (0.3 * momentum)
        
        return max(-1.0, min(1.0, sentiment))
    
    def _calculate_price_position(self, df: pd.DataFrame, current_price: float) -> float:
        """
        Calculate current price position in historical range.
        
        This indicates where the current price sits within its historical range,
        from 0 (at the lowest point) to 1 (at the highest point).
        
        Args:
            df: DataFrame with historical price data
            current_price: Current price value
            
        Returns:
            Price position value (0 to 1)
        """
        if df.empty:
            return 0.5
            
        # Get price range
        price_min = df['priceUsd'].min()
        price_max = df['priceUsd'].max()
        
        if price_min == price_max:
            return 0.5
            
        # Calculate position
        position = (current_price - price_min) / (price_max - price_min)
        
        return max(0.0, min(1.0, position))
    
    def interpret_market_signals(self, metrics: MarketMetrics) -> Dict[str, Any]:
        """
        Interpret market signals from metrics.
        
        Provides human-readable interpretations of various market metrics
        and what they suggest about potential market directions.
        
        Args:
            metrics: MarketMetrics object with analysis results
            
        Returns:
            Dictionary of signal interpretations
        """
        # Price trend signals
        if metrics.price_change_24h > 5:
            price_trend_short = "strongly bullish"
        elif metrics.price_change_24h > 2:
            price_trend_short = "bullish"
        elif metrics.price_change_24h > -2:
            price_trend_short = "neutral"
        elif metrics.price_change_24h > -5:
            price_trend_short = "bearish"
        else:
            price_trend_short = "strongly bearish"
            
        if metrics.price_change_30d > 20:
            price_trend_medium = "strongly bullish"
        elif metrics.price_change_30d > 10:
            price_trend_medium = "bullish"
        elif metrics.price_change_30d > -10:
            price_trend_medium = "neutral"
        elif metrics.price_change_30d > -20:
            price_trend_medium = "bearish"
        else:
            price_trend_medium = "strongly bearish"
            
        # Moving average signals
        if metrics.current_price > metrics.sma_7d > metrics.sma_30d > metrics.sma_90d:
            ma_signal = "strongly bullish"
        elif metrics.current_price > metrics.sma_7d > metrics.sma_30d:
            ma_signal = "bullish"
        elif metrics.current_price < metrics.sma_7d < metrics.sma_30d < metrics.sma_90d:
            ma_signal = "strongly bearish"
        elif metrics.current_price < metrics.sma_7d < metrics.sma_30d:
            ma_signal = "bearish"
        else:
            ma_signal = "neutral"
            
        # Volatility signal
        if metrics.volatility_7d > 10:
            volatility_signal = "extremely high"
        elif metrics.volatility_7d > 5:
            volatility_signal = "high"
        elif metrics.volatility_7d > 2:
            volatility_signal = "moderate"
        else:
            volatility_signal = "low"
            
        # Market sentiment signal
        if metrics.market_sentiment > 0.6:
            sentiment_signal = "strongly bullish"
        elif metrics.market_sentiment > 0.2:
            sentiment_signal = "bullish"
        elif metrics.market_sentiment > -0.2:
            sentiment_signal = "neutral"
        elif metrics.market_sentiment > -0.6:
            sentiment_signal = "bearish"
        else:
            sentiment_signal = "strongly bearish"
            
        # Trend strength
        if metrics.trend_strength > 0.8:
            trend_signal = "very strong"
        elif metrics.trend_strength > 0.6:
            trend_signal = "strong"
        elif metrics.trend_strength > 0.4:
            trend_signal = "moderate"
        elif metrics.trend_strength > 0.2:
            trend_signal = "weak"
        else:
            trend_signal = "very weak or sideways"
            
        # Price position
        if metrics.price_position > 0.9:
            position_signal = "at or near all-time high"
        elif metrics.price_position > 0.7:
            position_signal = "in upper historical range"
        elif metrics.price_position > 0.3:
            position_signal = "in mid historical range"
        elif metrics.price_position > 0.1:
            position_signal = "in lower historical range"
        else:
            position_signal = "at or near historical low"
            
        # Volume signal
        if metrics.volume_to_market_cap > 0.2:
            volume_signal = "extremely high"
        elif metrics.volume_to_market_cap > 0.1:
            volume_signal = "high"
        elif metrics.volume_to_market_cap > 0.05:
            volume_signal = "moderate"
        else:
            volume_signal = "low"
            
        # Overall market signal
        trend_signals = [
            1 if price_trend_short in ["bullish", "strongly bullish"] else 
            (-1 if price_trend_short in ["bearish", "strongly bearish"] else 0),
            
            1 if price_trend_medium in ["bullish", "strongly bullish"] else 
            (-1 if price_trend_medium in ["bearish", "strongly bearish"] else 0),
            
            1 if ma_signal in ["bullish", "strongly bullish"] else 
            (-1 if ma_signal in ["bearish", "strongly bearish"] else 0),
            
            1 if sentiment_signal in ["bullish", "strongly bullish"] else 
            (-1 if sentiment_signal in ["bearish", "strongly bearish"] else 0)
        ]
        
        overall_score = sum(trend_signals) / len(trend_signals)
        
        if overall_score > 0.5:
            overall_signal = "bullish"
        elif overall_score > 0:
            overall_signal = "slightly bullish"
        elif overall_score == 0:
            overall_signal = "neutral"
        elif overall_score > -0.5:
            overall_signal = "slightly bearish"
        else:
            overall_signal = "bearish"
            
        return {
            "price_trend_24h": price_trend_short,
            "price_trend_30d": price_trend_medium,
            "moving_average_signal": ma_signal,
            "volatility_level": volatility_signal,
            "market_sentiment": sentiment_signal,
            "trend_strength": trend_signal,
            "price_position": position_signal,
            "volume_signal": volume_signal,
            "overall_signal": overall_signal,
            "overall_score": overall_score,
            "interpretation": f"The market for {metrics.symbol} is showing {overall_signal} signals. "
                             f"Short-term price action is {price_trend_short}, while the medium-term trend is {price_trend_medium}. "
                             f"Moving averages suggest a {ma_signal} outlook. "
                             f"Market sentiment is {sentiment_signal} with {volatility_signal} volatility. "
                             f"The current price is {position_signal} with {volume_signal} trading volume. "
                             f"The trend strength is {trend_signal}."
        }
    
    def generate_price_chart(self, asset_id: str = "bitcoin", days: int = 30, save_path: Optional[str] = None) -> str:
        """
        Generate a price chart for an asset.
        
        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            days: Number of days of historical data to include
            save_path: Path to save the chart (defaults to self.save_path)
            
        Returns:
            Path to the generated chart image
        """
        logger.info(f"Generating price chart for {asset_id} over {days} days")
        
        # Get asset data
        asset_data = self.client.get_asset(asset_id)
        if not asset_data.get('data'):
            logger.error(f"Failed to get data for asset: {asset_id}")
            raise ValueError(f"No data found for asset: {asset_id}")
            
        asset = asset_data['data']
        
        # Get historical price data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        historical_df = self.client.get_asset_prices_as_dataframe(
            asset_id=asset_id,
            interval=Interval.DAY_1,
            start=start_date,
            end=end_date
        )
        
        if historical_df.empty:
            logger.error(f"Failed to get historical data for asset: {asset_id}")
            raise ValueError(f"No historical data found for asset: {asset_id}")
        
        # Calculate moving averages
        historical_df['SMA7'] = historical_df['priceUsd'].rolling(window=7).mean()
        historical_df['SMA30'] = historical_df['priceUsd'].rolling(window=30).mean()
        historical_df['SMA90'] = historical_df['priceUsd'].rolling(window=90).mean()
        
        # Calculate daily returns
        historical_df['DailyReturn'] = historical_df['priceUsd'].pct_change() * 100
        
        # Set up figure and axes
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [4, 1, 1]})
        
        # Plot price and moving averages
        ax1.plot(historical_df.index, historical_df['priceUsd'], label='Price', color='#5D69B1')
        ax1.plot(historical_df.index, historical_df['SMA7'], label='7-Day MA', color='#ED645A')
        ax1.plot(historical_df.index, historical_df['SMA30'], label='30-Day MA', color='#52BCA3')
        
        if days >= 90:  # Only show 90-day MA if we have enough data
            ax1.plot(historical_df.index, historical_df['SMA90'], label='90-Day MA', color='#99C945')
        
        # Format the price axis
        ax1.set_title(f"{asset['name']} ({asset['symbol']}) Price", fontsize=16)
        ax1.set_ylabel('Price (USD)', fontsize=12)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Use log scale for large price ranges
        price_range_ratio = historical_df['priceUsd'].max() / historical_df['priceUsd'].min() if historical_df['priceUsd'].min() > 0 else 1
        if price_range_ratio > 3:
            ax1.set_yscale('log')
        
        # Format the y-axis to show dollar values
        ax1.yaxis.set_major_formatter('${x:,.2f}')
        
        # Plot volume
        if 'volumeUsd' in historical_df.columns:
            volume_column = 'volumeUsd'
        elif 'volume' in historical_df.columns:
            volume_column = 'volume'
        else:
            # If volume data isn't available, create a placeholder
            volume_column = None
            historical_df['volume_placeholder'] = 0
        
        if volume_column:
            ax2.bar(historical_df.index, historical_df[volume_column], color='#5D69B1', alpha=0.7)
        else:
            ax2.bar(historical_df.index, historical_df['volume_placeholder'], color='#5D69B1', alpha=0.3)
            ax2.text(0.5, 0.5, 'Volume data not available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax2.transAxes, fontsize=12, alpha=0.7)
        
        ax2.set_ylabel('Volume (USD)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Format the y-axis to show dollar values with appropriate scale
        ax2.yaxis.set_major_formatter('${x:,.0f}')
        
        # Plot daily returns
        colors = ['#ED645A' if ret < 0 else '#52BCA3' for ret in historical_df['DailyReturn']]
        ax3.bar(historical_df.index, historical_df['DailyReturn'], color=colors, alpha=0.9)
        ax3.axhline(y=0, color='#999999', linestyle='-', alpha=0.4)
        ax3.set_ylabel('Daily Returns (%)', fontsize=12)
        ax3.set_xlabel('Date', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # Format dates on x-axis
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Add annotations with key metrics
        current_price = historical_df['priceUsd'].iloc[-1]
        market_cap = float(asset['marketCapUsd'] or 0)
        price_change_24h = float(asset['changePercent24Hr'] or 0)
        
        annotation_text = (
            f"Current Price: ${current_price:,.2f}\n"
            f"Market Cap: ${market_cap:,.0f}\n"
            f"24h Change: {price_change_24h:+.2f}%\n"
            f"Rank: #{asset['rank']}"
        )
        
        # Place annotation in the top left or right depending on price trend
        if historical_df['priceUsd'].iloc[-1] > historical_df['priceUsd'].iloc[0]:
            ax1.annotate(annotation_text, xy=(0.02, 0.98), xycoords='axes fraction', 
                        va='top', ha='left', fontsize=12, 
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
        else:
            ax1.annotate(annotation_text, xy=(0.98, 0.98), xycoords='axes fraction', 
                        va='top', ha='right', fontsize=12, 
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
        
        # Add title and adjust layout
        fig.suptitle(f"{asset['name']} Market Analysis - {datetime.now().strftime('%Y-%m-%d')}", 
                     fontsize=18, y=0.98)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Save the chart
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            asset_symbol_lower = asset['symbol'].lower()
            save_path = os.path.join(self.save_path, f"{asset_symbol_lower}_price_chart_{timestamp}.png")
            
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Price chart saved to: {save_path}")
        return save_path
    
    def _save_metrics(self, metrics: MarketMetrics) -> str:
        """
        Save market metrics to a JSON file.
        
        Args:
            metrics: MarketMetrics object to save
            
        Returns:
            Path to the saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        symbol_lower = metrics.symbol.lower()
        
        # Create output directory
        os.makedirs(self.save_path, exist_ok=True)
        
        # Save to JSON file
        file_path = os.path.join(self.save_path, f"{symbol_lower}_metrics_{timestamp}.json")
        with open(file_path, 'w') as f:
            json.dump(metrics.to_dict(), f, indent=2)
            
        logger.info(f"Market metrics saved to: {file_path}")
        return file_path
    
    def schedule_regular_analysis(self, asset_id: str = "bitcoin", interval_minutes: int = 60, max_runs: Optional[int] = None):
        """
        Schedule regular analysis of an asset.
        
        This will run the analysis at regular intervals until interrupted.
        
        Args:
            asset_id: Asset identifier to analyze
            interval_minutes: Interval between analyses in minutes
            max_runs: Maximum number of analysis runs (None for unlimited)
        """
        import threading
        
        def analysis_worker():
            runs = 0
            while max_runs is None or runs < max_runs:
                try:
                    logger.info(f"Running scheduled analysis for {asset_id}")
                    metrics = self.analyze_asset(asset_id, save_result=True)
                    self.generate_price_chart(asset_id, days=30)
                    
                    runs += 1
                    if max_runs is not None and runs >= max_runs:
                        logger.info(f"Completed {runs} scheduled analysis runs")
                        break
                        
                    logger.info(f"Waiting {interval_minutes} minutes until next analysis")
                    time.sleep(interval_minutes * 60)
                    
                except Exception as e:
                    logger.error(f"Error in scheduled analysis: {e}")
                    time.sleep(60)  # Wait a minute before retrying after an error
        
        thread = threading.Thread(target=analysis_worker, daemon=True)
        thread.start()
        logger.info(f"Started scheduled analysis for {asset_id} every {interval_minutes} minutes")
        return thread
        

# Example usage
if __name__ == "__main__":
    api_key = os.environ.get("COINCAP_API_KEY")
    analyzer = CoinCapAnalyzer(api_key=api_key)
    metrics = analyzer.analyze_asset(asset_id="bitcoin", save_result=True)
    
    print(f"Current Bitcoin price: ${metrics.current_price:,.2f}")
    print(f"24h change: {metrics.price_change_24h:+.2f}%")
    print(f"Market cap: ${metrics.market_cap:,.0f}")
    
    signals = analyzer.interpret_market_signals(metrics)
    print(f"\nMarket signals: {signals['overall_signal']}")
    print(f"Interpretation: {signals['interpretation']}")
    
    chart_path = analyzer.generate_price_chart(asset_id="bitcoin", days=90)
    print(f"\nPrice chart saved to: {chart_path}") 