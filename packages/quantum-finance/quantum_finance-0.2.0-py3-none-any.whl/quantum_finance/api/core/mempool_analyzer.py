#!/usr/bin/env python3

"""
Mempool Data Analyzer

This module analyzes mempool data from the Bitcoin network to derive insights
for cryptocurrency market predictions. It identifies trends in transaction fees,
mempool congestion, and network activity that can indicate market sentiment
and potential price movements.

The analysis is based on several key indicators:
1. Fee rate trends - Can indicate urgency in transaction processing
2. Mempool congestion - Often correlates with market activity
3. Transaction volume - Can signal increasing/decreasing network usage
4. Fee volatility - Can indicate market uncertainty

Author: Quantum-AI Team
"""

import os
import logging
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import matplotlib
# Set non-interactive backend to avoid GUI issues in background threads
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from dataclasses import dataclass, field

# Import the mempool client using the correct absolute path
from quantum_finance.api_clients.mempool_client import MempoolClient, MempoolConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class MempoolMetrics:
    """Container for calculated mempool metrics."""
    # Basic fee metrics
    current_fast_fee: float
    current_medium_fee: float
    current_slow_fee: float
    
    # Fee trend indicators
    fee_trend_1h: float  # Change in fees over last hour (percent)
    fee_trend_24h: float  # Change in fees over last 24 hours (percent)
    fee_volatility: float  # Standard deviation of fees
    
    # Mempool congestion metrics
    congestion_level: float  # 0-1 scale indicating mempool fullness
    transactions_waiting: int  # Number of transactions waiting
    
    # Network activity metrics
    transaction_volume_btc: float  # Total BTC value waiting in mempool
    average_transaction_size: float  # Average transaction size in vBytes
    
    # Market indicators
    urgency_indicator: float  # 0-1 scale indicating transaction urgency
    network_demand: float  # 0-1 scale indicating overall network demand
    market_sentiment: float  # -1 to 1 scale (bearish to bullish)
    
    # Timestamp of the analysis
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to a dictionary."""
        result = {k: v for k, v in self.__dict__.items() if k != 'timestamp'}
        result['timestamp'] = self.timestamp.isoformat()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MempoolMetrics':
        """Create metrics from a dictionary."""
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data = data.copy()  # Create a copy to avoid modifying the original
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class MempoolAnalyzer:
    """
    Analyzes Bitcoin mempool data to derive market indicators.
    
    This class calculates various metrics and indicators based on the current state
    of the Bitcoin mempool, which can be used to inform cryptocurrency market predictions.
    """
    
    def __init__(self, mempool_client: Optional[MempoolClient] = None, 
                save_path: str = "./output/mempool_analysis"):
        """
        Initialize the analyzer with a mempool client.
        
        Args:
            mempool_client: Optional mempool client to use for fetching data
            save_path: Path to save analysis results and charts
        """
        self.client = mempool_client or MempoolClient()
        self.save_path = save_path
        self.historical_metrics = []
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path, exist_ok=True)
            
        logger.info(f"Initialized MempoolAnalyzer, saving to {self.save_path}")
    
    def analyze_current_mempool(self, save_result: bool = False) -> MempoolMetrics:
        """
        Analyze the current state of the Bitcoin mempool.
        
        Args:
            save_result: Whether to save the analysis results to disk
            
        Returns:
            MempoolMetrics object containing the calculated metrics
        """
        logger.info("Analyzing current mempool state")
        
        try:
            # Get the necessary data
            fees = self.client.get_fees_recommended()
            mempool_stats = self.client.get_mempool_stats()
            mempool_blocks = self.client.get_mempool_blocks()
            
            # Extract key metrics from fees
            fast_fee = float(fees.get('fastestFee', 0))
            medium_fee = float(fees.get('halfHourFee', 0))
            slow_fee = float(fees.get('hourFee', 0))
            
            # Calculate fee trend (requires historical data)
            # For now, we'll use placeholders
            fee_trend_1h = 0.0
            fee_trend_24h = 0.0
            fee_volatility = 0.0
            
            # If we have historical metrics, calculate trends
            if self.historical_metrics:
                recent_metrics = [m for m in self.historical_metrics 
                                 if m.timestamp > datetime.now() - timedelta(hours=24)]
                
                if recent_metrics:
                    # Calculate 1-hour trend
                    one_hour_metrics = [m for m in recent_metrics 
                                       if m.timestamp > datetime.now() - timedelta(hours=1)]
                    if one_hour_metrics:
                        start_fee = one_hour_metrics[0].current_medium_fee
                        if start_fee > 0:
                            fee_trend_1h = ((medium_fee - start_fee) / start_fee) * 100
                    
                    # Calculate 24-hour trend
                    if recent_metrics[0].current_medium_fee > 0:
                        fee_trend_24h = ((medium_fee - recent_metrics[0].current_medium_fee) / 
                                         recent_metrics[0].current_medium_fee) * 100
                    
                    # Calculate fee volatility
                    fee_series = [m.current_medium_fee for m in recent_metrics]
                    if fee_series:
                        # Convert numpy.float64 to Python float for compatibility
                        fee_volatility = float(np.std(fee_series))
            
            # Extract congestion metrics
            # Count of transactions waiting
            waiting_tx_count = mempool_stats.get('count', 0)
            
            # Virtual size of the mempool in bytes
            mempool_size = mempool_stats.get('vsize', 0)
            
            # Estimate congestion level (assuming max mempool size is ~300MB)
            max_mempool_size = 300 * 1024 * 1024  # 300MB in bytes
            congestion_level = min(1.0, mempool_size / max_mempool_size)
            
            # Calculate average transaction size
            avg_tx_size = mempool_size / waiting_tx_count if waiting_tx_count > 0 else 0
            
            # Extract total BTC value waiting in mempool (rough estimate)
            total_btc = 0.0
            for block in mempool_blocks:
                if 'totalFees' in block:
                    total_btc += block.get('totalFees', 0) / 100000000  # Convert sats to BTC
            
            # Calculate market indicators
            
            # Urgency indicator - based on the gap between fast and slow fees
            fee_gap = (fast_fee - slow_fee) / fast_fee if fast_fee > 0 else 0
            urgency_indicator = min(1.0, fee_gap * 2)  # Scale to 0-1
            
            # Network demand - based on congestion and transaction count
            network_demand = (congestion_level * 0.7) + (min(1.0, waiting_tx_count / 50000) * 0.3)
            
            # Market sentiment - combining multiple indicators
            # Positive values suggest bullish sentiment, negative suggest bearish
            fee_trend_component = (fee_trend_24h / 100) * 0.5  # Scale to -0.5 to 0.5
            congestion_component = (congestion_level - 0.5) * 0.3  # Scale to -0.15 to 0.15
            urgency_component = (urgency_indicator - 0.5) * 0.2  # Scale to -0.1 to 0.1
            
            # Combine components, ensuring range is -1 to 1
            market_sentiment = max(-1.0, min(1.0, fee_trend_component + congestion_component + urgency_component))
            
            # Create metrics object
            metrics = MempoolMetrics(
                current_fast_fee=fast_fee,
                current_medium_fee=medium_fee,
                current_slow_fee=slow_fee,
                fee_trend_1h=fee_trend_1h,
                fee_trend_24h=fee_trend_24h,
                fee_volatility=fee_volatility,
                congestion_level=congestion_level,
                transactions_waiting=waiting_tx_count,
                transaction_volume_btc=total_btc,
                average_transaction_size=avg_tx_size,
                urgency_indicator=urgency_indicator,
                network_demand=network_demand,
                market_sentiment=market_sentiment
            )
            
            # Store metrics in historical data
            self.historical_metrics.append(metrics)
            
            # Keep historical metrics to a reasonable size (7 days at 5-minute intervals)
            max_history = 7 * 24 * 12  # 7 days of data at 5-minute intervals
            if len(self.historical_metrics) > max_history:
                self.historical_metrics = self.historical_metrics[-max_history:]
            
            # Save result if requested
            if save_result:
                self._save_metrics(metrics)
                
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing mempool: {e}")
            # Return default metrics in case of error
            return MempoolMetrics(
                current_fast_fee=0,
                current_medium_fee=0,
                current_slow_fee=0,
                fee_trend_1h=0,
                fee_trend_24h=0,
                fee_volatility=0,
                congestion_level=0,
                transactions_waiting=0,
                transaction_volume_btc=0,
                average_transaction_size=0,
                urgency_indicator=0,
                network_demand=0,
                market_sentiment=0
            )
    
    def interpret_market_signals(self, metrics: MempoolMetrics) -> Dict[str, Any]:
        """
        Interpret market signals from mempool metrics.
        
        Args:
            metrics: The mempool metrics to interpret
            
        Returns:
            Dictionary with market signals and interpretations
        """
        signals = {
            "timestamp": metrics.timestamp.isoformat(),
            "summary": "",
            "signals": {},
            "prediction": {
                "short_term_sentiment": "",
                "confidence": 0.0
            }
        }
        
        # Interpret fee trends
        if metrics.fee_trend_24h > 20:
            fee_signal = "strongly_increasing"
            fee_interpretation = "Significant increase in transaction fees indicates high demand for block space."
        elif metrics.fee_trend_24h > 5:
            fee_signal = "increasing"
            fee_interpretation = "Moderate increase in transaction fees suggests growing network activity."
        elif metrics.fee_trend_24h < -20:
            fee_signal = "strongly_decreasing"
            fee_interpretation = "Significant decrease in fees indicates reduced urgency in transactions."
        elif metrics.fee_trend_24h < -5:
            fee_signal = "decreasing"
            fee_interpretation = "Moderate decrease in fees suggests declining network activity."
        else:
            fee_signal = "stable"
            fee_interpretation = "Transaction fees are relatively stable, indicating normal network conditions."
        
        signals["signals"]["fee_trend"] = {
            "signal": fee_signal,
            "interpretation": fee_interpretation,
            "value": metrics.fee_trend_24h
        }
        
        # Interpret congestion
        if metrics.congestion_level > 0.8:
            congestion_signal = "severe"
            congestion_interpretation = "Mempool is highly congested, indicating significant network demand."
        elif metrics.congestion_level > 0.5:
            congestion_signal = "moderate"
            congestion_interpretation = "Moderate mempool congestion suggests active market conditions."
        elif metrics.congestion_level > 0.2:
            congestion_signal = "light"
            congestion_interpretation = "Light mempool congestion indicates normal market activity."
        else:
            congestion_signal = "minimal"
            congestion_interpretation = "Minimal mempool congestion suggests low network usage."
        
        signals["signals"]["congestion"] = {
            "signal": congestion_signal,
            "interpretation": congestion_interpretation,
            "value": metrics.congestion_level
        }
        
        # Interpret market sentiment
        if metrics.market_sentiment > 0.6:
            sentiment_signal = "strongly_bullish"
            sentiment_interpretation = "Mempool indicators suggest strongly bullish market sentiment."
            prediction = "Potentially positive short-term price movement"
            confidence = 0.7 + (metrics.market_sentiment - 0.6) * 0.75  # 0.7-0.85 range
        elif metrics.market_sentiment > 0.2:
            sentiment_signal = "bullish"
            sentiment_interpretation = "Mempool indicators suggest bullish market sentiment."
            prediction = "Possible positive short-term price movement"
            confidence = 0.5 + (metrics.market_sentiment - 0.2) * 0.5  # 0.5-0.7 range
        elif metrics.market_sentiment < -0.6:
            sentiment_signal = "strongly_bearish"
            sentiment_interpretation = "Mempool indicators suggest strongly bearish market sentiment."
            prediction = "Potentially negative short-term price movement"
            confidence = 0.7 + (abs(metrics.market_sentiment) - 0.6) * 0.75  # 0.7-0.85 range
        elif metrics.market_sentiment < -0.2:
            sentiment_signal = "bearish"
            sentiment_interpretation = "Mempool indicators suggest bearish market sentiment."
            prediction = "Possible negative short-term price movement"
            confidence = 0.5 + (abs(metrics.market_sentiment) - 0.2) * 0.5  # 0.5-0.7 range
        else:
            sentiment_signal = "neutral"
            sentiment_interpretation = "Mempool indicators suggest neutral market sentiment."
            prediction = "No clear short-term price direction"
            confidence = 0.3 + abs(metrics.market_sentiment) * 1.5  # 0.3-0.6 range
        
        signals["signals"]["market_sentiment"] = {
            "signal": sentiment_signal,
            "interpretation": sentiment_interpretation,
            "value": metrics.market_sentiment
        }
        
        # Set prediction
        signals["prediction"]["short_term_sentiment"] = prediction
        signals["prediction"]["confidence"] = min(0.95, confidence)  # Cap at 0.95
        
        # Create summary
        signals["summary"] = (
            f"Bitcoin mempool analysis indicates {sentiment_signal} market sentiment "
            f"with {fee_signal} transaction fees and {congestion_signal} network congestion. "
            f"{prediction} (confidence: {confidence:.2f})."
        )
        
        return signals
    
    def generate_fee_trend_chart(self, days: int = 7, save_path: Optional[str] = None) -> str:
        """
        Generate a chart showing fee trends over time.
        
        Args:
            days: Number of days of data to include
            save_path: Optional path to save the chart, defaults to self.save_path
            
        Returns:
            Path to the saved chart file
        """
        if not self.historical_metrics:
            logger.warning("No historical metrics available for chart generation")
            return ""
        
        # Filter metrics for the requested time period
        cutoff_time = datetime.now() - timedelta(days=days)
        metrics = [m for m in self.historical_metrics if m.timestamp >= cutoff_time]
        
        if not metrics:
            logger.warning("No metrics found for the requested time period")
            return ""
        
        # Create dataframe for plotting
        data = {
            'timestamp': [m.timestamp for m in metrics],
            'fast_fee': [m.current_fast_fee for m in metrics],
            'medium_fee': [m.current_medium_fee for m in metrics],
            'slow_fee': [m.current_slow_fee for m in metrics],
            'congestion': [m.congestion_level for m in metrics],
            'sentiment': [m.market_sentiment for m in metrics]
        }
        df = pd.DataFrame(data)
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        
        # Plot fee trends
        ax1.plot(df['timestamp'], df['fast_fee'], label='Fast Fee (1 block)')
        ax1.plot(df['timestamp'], df['medium_fee'], label='Medium Fee (3 blocks)')
        ax1.plot(df['timestamp'], df['slow_fee'], label='Slow Fee (6 blocks)')
        ax1.set_ylabel('Fee Rate (sat/vB)')
        ax1.set_title('Bitcoin Transaction Fee Trends')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot congestion and sentiment
        ax2.plot(df['timestamp'], df['congestion'], label='Mempool Congestion', color='purple')
        ax2.set_ylabel('Congestion Level (0-1)', color='purple')
        ax2.tick_params(axis='y', labelcolor='purple')
        ax2.set_ylim(0, 1)
        
        # Create second Y axis for sentiment
        ax3 = ax2.twinx()
        ax3.plot(df['timestamp'], df['sentiment'], label='Market Sentiment', color='green')
        ax3.set_ylabel('Market Sentiment (-1 to 1)', color='green')
        ax3.tick_params(axis='y', labelcolor='green')
        ax3.set_ylim(-1, 1)
        
        # Add zero line for sentiment
        ax3.axhline(y=0, color='green', linestyle='-', alpha=0.3)
        
        # Add both legends
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax3.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        ax2.set_xlabel('Time')
        ax2.grid(True, alpha=0.3)
        
        # Format X axis
        fig.autofmt_xdate()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the figure
        save_path = save_path or os.path.join(self.save_path, f"fee_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(save_path)
        plt.close()
        
        return save_path
    
    def _save_metrics(self, metrics: MempoolMetrics) -> str:
        """
        Save metrics to disk.
        
        Args:
            metrics: Metrics to save
            
        Returns:
            Path to the saved file
        """
        try:
            timestamp = metrics.timestamp.strftime('%Y%m%d_%H%M%S')
            filepath = os.path.join(self.save_path, f"mempool_metrics_{timestamp}.json")
            
            with open(filepath, 'w') as f:
                json.dump(metrics.to_dict(), f, indent=2)
                
            logger.info(f"Saved metrics to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
            return ""

    def schedule_regular_analysis(self, interval_minutes: int = 5, max_runs: Optional[int] = None):
        """
        Schedule regular analysis of the mempool at specified intervals.
        This method starts a background thread for the analysis.
        
        Args:
            interval_minutes: Minutes between each analysis
            max_runs: Maximum number of analyses to run, None for unlimited
        """
        import time
        import threading
        
        logger.info(f"Starting scheduled analysis every {interval_minutes} minutes")
        
        def analysis_worker():
            runs = 0
            try:
                while max_runs is None or runs < max_runs:
                    # Run analysis
                    try:
                        metrics = self.analyze_current_mempool(save_result=True)
                        signals = self.interpret_market_signals(metrics)
                        
                        logger.info(f"Analysis #{runs+1}: {signals['summary']}")
                        
                        # Generate chart every hour
                        if runs % (60 // max(1, interval_minutes)) == 0:
                            try:
                                self.generate_fee_trend_chart()
                            except Exception as chart_error:
                                logger.error(f"Error generating chart: {chart_error}")
                    except Exception as analysis_error:
                        logger.error(f"Error in analysis run #{runs+1}: {analysis_error}")
                    
                    runs += 1
                    
                    # Wait for next interval, but check for max_runs
                    if max_runs is None or runs < max_runs:
                        time.sleep(interval_minutes * 60)
                    else:
                        logger.info(f"Completed {max_runs} scheduled analyses")
                        break
            except Exception as e:
                logger.error(f"Fatal error in analysis worker thread: {e}")
        
        # Start the analysis in a background thread
        analysis_thread = threading.Thread(target=analysis_worker, daemon=True)
        analysis_thread.start()
        
        return analysis_thread


if __name__ == "__main__":
    # Simple test if run directly
    analyzer = MempoolAnalyzer()
    
    print("Running mempool analysis...")
    metrics = analyzer.analyze_current_mempool()
    
    print("\nCurrent Mempool Metrics:")
    for key, value in metrics.to_dict().items():
        print(f"{key}: {value}")
    
    print("\nMarket Signal Interpretation:")
    signals = analyzer.interpret_market_signals(metrics)
    print(signals["summary"])
    
    # Generate a chart with random historical data for testing
    print("\nGenerating sample chart...")
    
    # Create some fake historical data
    import random
    from datetime import timedelta
    
    # Start 7 days ago
    start_time = datetime.now() - timedelta(days=7)
    
    # Create a metrics entry every 3 hours
    for i in range(7 * 8):  # 7 days, 8 entries per day
        fake_time = start_time + timedelta(hours=i * 3)
        
        # Create some realistic trends
        base_fee = 5 + 3 * np.sin(i / 4)  # Oscillating base fee
        volatility = 1 + 0.5 * np.sin(i / 6)  # Oscillating volatility
        
        fake_metrics = MempoolMetrics(
            current_fast_fee=max(1, base_fee * 2 + random.uniform(-volatility, volatility)),
            current_medium_fee=max(1, base_fee + random.uniform(-volatility, volatility)),
            current_slow_fee=max(1, base_fee * 0.5 + random.uniform(-volatility, volatility)),
            fee_trend_1h=random.uniform(-5, 5),
            fee_trend_24h=random.uniform(-20, 20),
            fee_volatility=float(volatility),  # Ensure volatility is a Python float
            congestion_level=0.2 + 0.3 * np.sin(i / 5) + random.uniform(-0.1, 0.1),
            transactions_waiting=int(10000 + 5000 * np.sin(i / 5) + random.uniform(-1000, 1000)),
            transaction_volume_btc=50 + 20 * np.sin(i / 4) + random.uniform(-5, 5),
            average_transaction_size=250 + random.uniform(-20, 20),
            urgency_indicator=0.3 + 0.2 * np.sin(i / 3) + random.uniform(-0.1, 0.1),
            network_demand=0.4 + 0.3 * np.sin(i / 4) + random.uniform(-0.1, 0.1),
            market_sentiment=-0.5 + 0.7 * np.sin(i / 10) + random.uniform(-0.1, 0.1),
            timestamp=fake_time
        )
        
        analyzer.historical_metrics.append(fake_metrics)
    
    # Generate and save the chart
    chart_path = analyzer.generate_fee_trend_chart()
    print(f"Chart saved to: {chart_path}")
    
    # Run a brief scheduled analysis demo
    print("\nRunning scheduled analysis demo (3 runs, 10 seconds apart)...")
    # Use integer for interval_minutes, 60 seconds = 1 minute
    analyzer.schedule_regular_analysis(interval_minutes=1, max_runs=3) 