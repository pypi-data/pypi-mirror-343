#!/usr/bin/env python3

"""
Real-Time Risk Assessment System for Quantum Financial System

This module provides a real-time risk monitoring system that continuously evaluates
cryptocurrency market risk using quantum-enhanced risk assessment techniques. It can
process live market data, detect anomalies, and trigger alerts when risk thresholds
are exceeded.

Features:
- Real-time market data processing via WebSocket connections
- Incremental quantum risk assessment updates
- Configurable risk thresholds and alert conditions
- Integration with the unified data pipeline
- Multi-level alerting system

Author: Quantum-AI Team
"""

import os
import json
import time
import logging
import threading
import queue
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable, cast

# Import unified data pipeline
from quantum_finance.unified_data_pipeline import UnifiedDataPipeline

# Import quantum risk analyzer with fallback for testing
try:
    from quantum_finance.quantum_risk import QuantumEnhancedCryptoRiskAnalyzer
except ImportError:
    # Define a mock class for testing import resolution
    class QuantumEnhancedCryptoRiskAnalyzer:
        """Mock class for testing import resolution"""
        def __init__(self, *args, **kwargs):
            self.name = "Mock Analyzer for Import Testing"
        
        def analyze(self, *args, **kwargs):
            """Basic mock analysis method"""
            return {"mock": True}
            
        def update_risk_assessment(self, *args, **kwargs):
            """Mock method for incremental risk assessment updates"""
            return {"mock_update": True, "timestamp": datetime.now().isoformat()}
            
        def analyze_with_quantum(self, *args, **kwargs):
            """Mock method for quantum-enhanced analysis"""
            return {"mock_quantum": True, "enhanced": True}
    
    logging.warning("Using mock QuantumEnhancedCryptoRiskAnalyzer for testing")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AlertLevel:
    """Alert severity levels for risk notifications."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class RiskAlert:
    """Represents a risk alert notification."""
    
    def __init__(self, symbol: str, metric: str, value: float, threshold: float, level: str):
        """
        Initialize a risk alert.
        
        Args:
            symbol: Cryptocurrency symbol
            metric: Risk metric that triggered the alert
            value: Current value of the metric
            threshold: Threshold value that was exceeded
            level: Alert severity level
        """
        self.symbol = symbol
        self.metric = metric
        self.value = value
        self.threshold = threshold
        self.level = level
        self.timestamp = datetime.now()
        
    def __str__(self) -> str:
        return (f"[{self.level}] {self.symbol} {self.metric} ALERT: "
                f"Current value {self.value:.4f} exceeded threshold {self.threshold:.4f} "
                f"at {self.timestamp.isoformat()}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to a dictionary for serialization."""
        return {
            "symbol": self.symbol,
            "metric": self.metric,
            "value": self.value,
            "threshold": self.threshold,
            "level": self.level,
            "timestamp": self.timestamp.isoformat()
        }

class AlertManager:
    """Manages risk alerts and notifications."""
    
    def __init__(self, max_history: int = 100):
        """
        Initialize the alert manager.
        
        Args:
            max_history: Maximum number of alerts to keep in history
        """
        self.max_history = max_history
        self.alert_history: List[RiskAlert] = []
        self.alert_handlers: List[Callable[[RiskAlert], None]] = []
        self.history_lock = threading.Lock()
        
    def add_alert_handler(self, handler: Callable[[RiskAlert], None]) -> None:
        """
        Add a handler function for new alerts.
        
        Args:
            handler: Function to call when a new alert is triggered
        """
        self.alert_handlers.append(handler)
        
    def trigger_alert(self, alert: RiskAlert) -> None:
        """
        Trigger a new risk alert.
        
        Args:
            alert: Risk alert to trigger
        """
        # Add to history
        with self.history_lock:
            self.alert_history.append(alert)
            # Trim history if needed
            if len(self.alert_history) > self.max_history:
                self.alert_history = self.alert_history[-self.max_history:]
        
        # Log the alert
        if alert.level == AlertLevel.CRITICAL:
            logger.critical(str(alert))
        elif alert.level == AlertLevel.WARNING:
            logger.warning(str(alert))
        else:
            logger.info(str(alert))
        
        # Call all handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")
    
    def get_recent_alerts(self, count: Optional[int] = None, level: Optional[str] = None, 
                         symbol: Optional[str] = None) -> List[RiskAlert]:
        """
        Get recent alerts, optionally filtered.
        
        Args:
            count: Maximum number of alerts to return (None for all)
            level: Filter by alert level (None for all)
            symbol: Filter by symbol (None for all)
            
        Returns:
            List of recent alerts matching the filters
        """
        with self.history_lock:
            filtered = self.alert_history.copy()
            
            if level:
                filtered = [a for a in filtered if a.level == level]
            
            if symbol:
                filtered = [a for a in filtered if a.symbol == symbol]
            
            if count:
                filtered = filtered[-count:]
            
            return filtered

class EventProcessor:
    """Processes market events for risk assessment."""
    
    def __init__(self, max_queue_size: int = 1000):
        """
        Initialize the event processor.
        
        Args:
            max_queue_size: Maximum size of the event queue
        """
        self.event_queue = queue.Queue(maxsize=max_queue_size)
        self.event_handlers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self.running = False
        self.worker_thread = None
    
    def register_handler(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a handler for a specific event type.
        
        Args:
            event_type: Type of event to handle
            handler: Function to call when the event is processed
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def push_event(self, event_type: str, data: Dict[str, Any]) -> bool:
        """
        Push a new event to the processing queue.
        
        Args:
            event_type: Type of event
            data: Event data
            
        Returns:
            True if the event was queued, False if the queue is full
        """
        if not self.running:
            logger.warning("Event processor is not running, event ignored")
            return False
        
        try:
            event = {
                "type": event_type,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            self.event_queue.put(event, block=False)
            return True
        except queue.Full:
            logger.warning("Event queue is full, event dropped")
            return False
    
    def _process_events(self) -> None:
        """Process events from the queue (runs in worker thread)."""
        logger.info("Event processor started")
        
        while self.running:
            try:
                # Get next event with timeout to allow for clean shutdown
                try:
                    event = self.event_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                # Process the event
                event_type = event["type"]
                handlers = self.event_handlers.get(event_type, [])
                
                if not handlers:
                    logger.debug(f"No handlers for event type: {event_type}")
                else:
                    for handler in handlers:
                        try:
                            handler(event["data"])
                        except Exception as e:
                            logger.error(f"Error in event handler for {event_type}: {e}")
                
                # Mark as done
                self.event_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error in event processor: {e}")
        
        logger.info("Event processor stopped")
    
    def start(self) -> None:
        """Start the event processor."""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_events, daemon=True)
            self.worker_thread.start()
            logger.info("Event processor started")
    
    def stop(self) -> None:
        """Stop the event processor."""
        if self.running:
            logger.info("Stopping event processor...")
            self.running = False
            if self.worker_thread:
                self.worker_thread.join(timeout=5.0)
            logger.info("Event processor stopped")

class RiskThresholdManager:
    """Manages risk thresholds and detection logic."""
    
    def __init__(self):
        """Initialize the risk threshold manager."""
        self.thresholds: Dict[str, Dict[str, Dict[str, float]]] = {}
        self.threshold_lock = threading.Lock()
        
    def set_threshold(self, symbol: str, metric: str, warning_level: float, 
                     critical_level: float) -> None:
        """
        Set risk thresholds for a specific symbol and metric.
        
        Args:
            symbol: Cryptocurrency symbol
            metric: Risk metric name
            warning_level: Threshold for warning alerts
            critical_level: Threshold for critical alerts
        """
        with self.threshold_lock:
            if symbol not in self.thresholds:
                self.thresholds[symbol] = {}
            
            if metric not in self.thresholds[symbol]:
                self.thresholds[symbol][metric] = {}
            
            self.thresholds[symbol][metric] = {
                "warning": warning_level,
                "critical": critical_level
            }
            
            logger.info(f"Set thresholds for {symbol} {metric}: "
                       f"warning={warning_level:.4f}, critical={critical_level:.4f}")
    
    def load_thresholds(self, config_file: str) -> None:
        """
        Load thresholds from a configuration file.
        
        Args:
            config_file: Path to the threshold configuration file
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            for symbol, metrics in config.items():
                for metric, levels in metrics.items():
                    self.set_threshold(
                        symbol, 
                        metric, 
                        levels.get("warning", 0.5), 
                        levels.get("critical", 0.8)
                    )
            
            logger.info(f"Loaded thresholds from {config_file}")
            
        except Exception as e:
            logger.error(f"Error loading thresholds: {e}")
    
    def save_thresholds(self, config_file: str) -> None:
        """
        Save current thresholds to a configuration file.
        
        Args:
            config_file: Path to save the threshold configuration
        """
        try:
            with self.threshold_lock:
                with open(config_file, 'w') as f:
                    json.dump(self.thresholds, f, indent=2)
            
            logger.info(f"Saved thresholds to {config_file}")
            
        except Exception as e:
            logger.error(f"Error saving thresholds: {e}")
    
    def check_thresholds(self, symbol: str, metric: str, value: float) -> Optional[RiskAlert]:
        """
        Check if a metric value exceeds any thresholds.
        
        Args:
            symbol: Cryptocurrency symbol
            metric: Risk metric name
            value: Current value of the metric
            
        Returns:
            RiskAlert if a threshold was exceeded, None otherwise
        """
        with self.threshold_lock:
            # Check if we have thresholds for this symbol and metric
            if symbol not in self.thresholds or metric not in self.thresholds[symbol]:
                return None
            
            # Get thresholds
            thresholds = self.thresholds[symbol][metric]
            
            # Check critical threshold first
            if value >= thresholds["critical"]:
                return RiskAlert(
                    symbol=symbol,
                    metric=metric,
                    value=value,
                    threshold=thresholds["critical"],
                    level=AlertLevel.CRITICAL
                )
            
            # Check warning threshold
            elif value >= thresholds["warning"]:
                return RiskAlert(
                    symbol=symbol,
                    metric=metric,
                    value=value,
                    threshold=thresholds["warning"],
                    level=AlertLevel.WARNING
                )
            
            # No thresholds exceeded
            return None

class RealTimeRiskMonitor:
    """
    Real-time risk monitoring system with quantum-enhanced risk assessment.
    """
    
    def __init__(self, api_key: Optional[str] = None, update_interval: int = 60,
                polling_mode: bool = True):
        """
        Initialize the real-time risk monitor.
        
        Args:
            api_key: API key for data sources that require authentication
            update_interval: Update interval in seconds for polling mode
            polling_mode: Whether to use polling (True) or WebSocket (False)
        """
        # Initialize components
        self.data_pipeline = UnifiedDataPipeline(api_key=api_key, use_cache=True, cache_expiry=30)
        self.risk_analyzer = QuantumEnhancedCryptoRiskAnalyzer(api_key=api_key)
        self.threshold_manager = RiskThresholdManager()
        self.alert_manager = AlertManager(max_history=1000)
        self.event_processor = EventProcessor(max_queue_size=10000)
        
        # Configuration
        self.update_interval = update_interval
        self.polling_mode = polling_mode
        self.watched_symbols: List[str] = []
        self.running = False
        self.update_thread = None
        
        # State
        self.last_risk_assessments: Dict[str, Dict[str, Any]] = {}
        self.websocket_connections: Dict[str, Any] = {}
        
        # Register event handlers
        self.event_processor.register_handler("market_update", self._handle_market_update)
        self.event_processor.register_handler("risk_assessment", self._handle_risk_assessment)
        
        # Setup default alert handler
        self.alert_manager.add_alert_handler(self._default_alert_handler)
    
    def _default_alert_handler(self, alert: RiskAlert) -> None:
        """Default handler for alerts to log to console."""
        # This could be extended to send emails, SMS, etc.
        print(f"\n{'='*80}\n{alert}\n{'='*80}")
    
    def add_symbol(self, symbol: str) -> None:
        """
        Add a symbol to monitor.
        
        Args:
            symbol: Cryptocurrency symbol to monitor
        """
        if symbol not in self.watched_symbols:
            self.watched_symbols.append(symbol)
            logger.info(f"Added {symbol} to monitored symbols")
            
            # If we're running in WebSocket mode and already started, setup the connection
            if not self.polling_mode and self.running:
                self._setup_websocket(symbol)
    
    def remove_symbol(self, symbol: str) -> None:
        """
        Remove a symbol from monitoring.
        
        Args:
            symbol: Cryptocurrency symbol to stop monitoring
        """
        if symbol in self.watched_symbols:
            self.watched_symbols.remove(symbol)
            logger.info(f"Removed {symbol} from monitored symbols")
            
            # If running in WebSocket mode, close the connection
            if not self.polling_mode and symbol in self.websocket_connections:
                self._close_websocket(symbol)
    
    def _setup_websocket(self, symbol: str) -> None:
        """
        Set up WebSocket connection for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol to connect to
        """
        # This is a placeholder - actual implementation would depend on
        # which exchange's WebSocket API we're using
        logger.info(f"Setting up WebSocket for {symbol}")
        # In a real implementation, we would connect to the WebSocket here
        # and set up callbacks to push events to our event processor
        self.websocket_connections[symbol] = {"status": "connected"}
    
    def _close_websocket(self, symbol: str) -> None:
        """
        Close WebSocket connection for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol to disconnect from
        """
        if symbol in self.websocket_connections:
            # This is a placeholder - actual implementation would depend on
            # which exchange's WebSocket API we're using
            logger.info(f"Closing WebSocket for {symbol}")
            # In a real implementation, we would close the WebSocket connection here
            del self.websocket_connections[symbol]
    
    def _handle_market_update(self, data: Dict[str, Any]) -> None:
        """
        Handle a market update event.
        
        Args:
            data: Market update data
        """
        try:
            symbol = data.get("symbol")
            if not symbol:
                logger.warning("Market update event missing symbol")
                return
            
            # Create incremental risk assessment
            prev_assessment = self.last_risk_assessments.get(symbol)
            
            # Push event for risk assessment
            self.event_processor.push_event("risk_assessment", {
                "symbol": symbol,
                "market_data": data,
                "previous_assessment": prev_assessment
            })
            
        except Exception as e:
            logger.error(f"Error handling market update: {e}")
    
    def _handle_risk_assessment(self, data: Dict[str, Any]) -> None:
        """
        Handle a risk assessment event.
        
        Args:
            data: Risk assessment data
        """
        try:
            symbol = data.get("symbol")
            if not symbol:
                logger.warning("Risk assessment event missing symbol")
                return
            
            # Get market data from the event
            market_data = data.get("market_data", {})
            prev_assessment = data.get("previous_assessment")
            
            # Perform risk assessment
            if prev_assessment:
                # Use the new incremental update method
                logger.debug(f"Performing incremental risk assessment update for {symbol}")
                risk_results = self.risk_analyzer.update_risk_assessment(
                    previous_assessment=prev_assessment,
                    symbol=symbol,
                    order_book=market_data.get("order_book"),
                    stats_24hr=market_data.get("stats_24hr")
                )
            else:
                # Full assessment
                risk_results = self.risk_analyzer.analyze_with_quantum(symbol)
            
            # Store for future reference
            self.last_risk_assessments[symbol] = risk_results
            
            # Check all risk metrics against thresholds
            for metric, value in risk_results.get("risk_metrics", {}).items():
                alert = self.threshold_manager.check_thresholds(symbol, metric, value)
                if alert:
                    self.alert_manager.trigger_alert(alert)
            
        except Exception as e:
            logger.error(f"Error handling risk assessment: {e}")
    
    def _polling_update_loop(self) -> None:
        """Run the polling update loop in a separate thread."""
        logger.info("Polling update loop started")
        
        while self.running:
            try:
                # Process each watched symbol
                for symbol in self.watched_symbols:
                    try:
                        # Get latest market data
                        market_data = self.data_pipeline.get_market_data(symbol)
                        
                        # Push market update event
                        self.event_processor.push_event("market_update", {
                            "symbol": symbol,
                            "timestamp": datetime.now().isoformat(),
                            **market_data
                        })
                        
                    except Exception as e:
                        logger.error(f"Error updating {symbol}: {e}")
                
                # Sleep until next update
                time.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error in polling update loop: {e}")
                # Sleep a bit to avoid tight loop on persistent errors
                time.sleep(5)
        
        logger.info("Polling update loop stopped")
    
    def start(self) -> None:
        """Start the real-time risk monitor."""
        if not self.running:
            logger.info("Starting real-time risk monitor...")
            
            # Start the event processor
            self.event_processor.start()
            
            # Start updates based on mode
            self.running = True
            
            if self.polling_mode:
                # Start polling loop
                self.update_thread = threading.Thread(target=self._polling_update_loop, daemon=True)
                self.update_thread.start()
            else:
                # Set up WebSockets for each symbol
                for symbol in self.watched_symbols:
                    self._setup_websocket(symbol)
            
            logger.info("Real-time risk monitor started")
    
    def stop(self) -> None:
        """Stop the real-time risk monitor."""
        if self.running:
            logger.info("Stopping real-time risk monitor...")
            
            # Stop the running flag
            self.running = False
            
            # Wait for polling thread to finish if applicable
            if self.polling_mode and self.update_thread:
                self.update_thread.join(timeout=10.0)
            
            # Close WebSockets if applicable
            if not self.polling_mode:
                for symbol in list(self.websocket_connections.keys()):
                    self._close_websocket(symbol)
            
            # Stop the event processor
            self.event_processor.stop()
            
            logger.info("Real-time risk monitor stopped")

# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load API key from environment
    load_dotenv()
    api_key = os.getenv("RAPIDAPI_KEY")
    
    # Create the risk monitor
    monitor = RealTimeRiskMonitor(api_key=api_key, update_interval=30)
    
    # Set up thresholds
    monitor.threshold_manager.set_threshold("BTC", "overall_risk", 0.6, 0.8)
    monitor.threshold_manager.set_threshold("BTC", "liquidity_risk", 0.7, 0.85)
    monitor.threshold_manager.set_threshold("BTC", "volatility_risk", 0.5, 0.75)
    
    # Add symbols to monitor
    monitor.add_symbol("BTC")
    
    try:
        # Start monitoring
        monitor.start()
        
        # Keep running until interrupted
        print("Monitoring started. Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    finally:
        # Stop monitoring
        monitor.stop() 