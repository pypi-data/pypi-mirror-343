#!/usr/bin/env python3

"""
Quantum Financial API

A comprehensive unified API for quantum financial components that provides a seamless interface
between all the advanced components we've developed, enabling end-to-end market analysis and
risk assessment.

This API integrates:
- Adaptive Learning System
- Quantum Market Microstructure Analysis
- Advanced Phase Tracking
- Quantum Diffusion Models
- Stochastic Market Simulation

Author: Quantum-AI Team
"""

import os
import sys
import logging
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path
import time
import gc
import concurrent.futures
import psutil
import traceback
import threading
from typing import Callable

# Add project root to path to ensure imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import component implementations
from quantum_finance.backend.adaptive_learning import AdaptiveLearningSystem
from quantum_finance.quantum_market_encoding import (
    encode_order_book_imbalance,
    encode_market_volatility,
    encode_price_impact,
    encode_liquidity_risk,
    combined_market_risk_encoding
)
from quantum_finance.quantum_toolkit.phase_tracking.adaptive_phase_tracker import AdaptivePhaseTracker, StateEstimate
from experimental.quantum_diffusion.qdense_model import QDenseDiffusion
from examples.stochastic_quantum_crypto import StochasticMarketSimulator, MarketState

# Import optimization modules
# Assuming clients are in 'quantum_finance.api_clients'
from quantum_finance.api_clients.mempool_client import MempoolClient, MempoolConfig, MempoolNetwork
from quantum_finance.api_clients.coindesk_client import CoinDeskClient, CoinDeskConfig
from quantum_finance.api_clients.coincap_client import CoinCapClient, CoinCapConfig, Interval
# Core modules might be directly under api.core
from quantum_finance.api.core.cache_manager import CacheManager, CacheItemType
from quantum_finance.api.core.parallel_manager import ParallelManager, TaskPriority, ExecutionMode
from quantum_finance.api.core.performance_monitor import PerformanceMonitor, ComponentType as PerfComponentType
from quantum_finance.api.core.memory_optimizer import (
    MemoryOptimizer,
    DataCompressionLevel,
    MemoryOptimizationStrategy
)
from quantum_finance.api.core.mempool_analyzer import MempoolAnalyzer, MempoolMetrics
from quantum_finance.api.core.coindesk_analyzer import CoinDeskAnalyzer, PriceMetrics
from quantum_finance.api.core.coincap_analyzer import CoinCapAnalyzer, MarketMetrics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration management for the unified API
@dataclass
class QuantumFinancialConfig:
    """Configuration for the Quantum Financial API components."""
    
    # General configuration
    save_path: str = "./output"
    debug_mode: bool = False
    
    # AdaptiveLearningSystem config
    als_learning_rate: float = 0.01
    
    # Market encoding config
    market_encoding_qubits: int = 8
    
    # AdaptivePhaseTracker config (Updated for Particle Filter)
    phase_tracker_num_particles: int = 100
    phase_tracker_process_noise: float = 0.01
    phase_tracker_measurement_noise: float = 0.1
    # phase_tracker_adaptation_method: str = 'innovation' # Old param
    # phase_tracker_use_imm: bool = True                 # Old param
    # phase_tracker_num_imm_models: int = 3              # Old param
    
    # QDenseDiffusion config
    qdense_num_qubits: int = 7
    qdense_num_layers: int = 47
    qdense_shots: int = 1000
    
    # StochasticMarketSimulator config
    sms_config_space_dim: int = 5
    sms_num_trajectories: int = 1000
    sms_time_step: float = 0.1
    sms_drift_scale: float = 0.01
    sms_diffusion_scale: float = 0.1
    sms_quantum_potential_strength: float = 0.05
    
    # Bitcoin Mempool Analysis Config
    enable_mempool_analysis: bool = True
    mempool_api_url: str = "https://mempool.space/api"
    mempool_network: str = "mainnet"  # "mainnet", "testnet", or "signet"
    mempool_analysis_interval_minutes: int = 15  # How often to analyze mempool data
    mempool_data_retention_days: int = 7  # How many days of mempool data to retain
    
    # CoinDesk Bitcoin Price Analysis Config
    enable_bitcoin_price_analysis: bool = True
    coindesk_api_base_url: str = "https://blockchain.info"
    coindesk_default_currency: str = "USD"
    bitcoin_price_analysis_interval_minutes: int = 60  # How often to analyze price data
    bitcoin_price_data_retention_days: int = 90  # How many days of price data to retain
    
    # CoinCap Market Data Analysis Config
    enable_coincap_analysis: bool = True
    coincap_api_base_url: str = "https://api.coincap.io/v2"
    coincap_api_key: Optional[str] = None  # API key for authentication
    coincap_default_assets: List[str] = field(default_factory=lambda: ["bitcoin", "ethereum", "xrp", "cardano", "solana"])
    coincap_analysis_interval_minutes: int = 60  # How often to analyze market data
    coincap_data_retention_days: int = 90  # How many days of market data to retain
    
    # Performance Optimization Configurations
    
    # Cache optimization config
    enable_caching: bool = True
    cache_max_results: int = 1000  # Maximum number of analysis results to cache
    cache_max_memory_mb: float = 512  # Maximum memory for results cache (MB)
    cache_ttl_seconds: float = 3600  # Default TTL for cached items (1 hour)
    
    # Performance monitoring config
    enable_performance_monitoring: bool = False
    performance_max_history: int = 100  # Maximum number of performance records to keep
    performance_log_threshold_ms: float = 100.0  # Log operations taking longer than this (ms)
    
    # Parallel processing config
    enable_parallel_processing: bool = False
    parallel_execution_mode: str = "thread"  # "thread" or "process"
    parallel_max_workers: int = 4  # Maximum number of worker threads/processes
    parallel_max_memory_percent: float = 75.0  # Maximum memory usage percentage
    
    # Memory optimization config
    enable_memory_optimization: bool = True
    memory_compression_level: int = 1  # Compression level (0-9, 0=none, 9=max)
    memory_chunk_size: int = 1024 * 1024  # Chunk size for memory operations (1MB)
    memory_warning_threshold_percent: float = 80.0  # Warning threshold for memory usage
    memory_critical_threshold_percent: float = 90.0  # Critical threshold for memory usage
    
    @classmethod
    def from_json(cls, json_path: str) -> 'QuantumFinancialConfig':
        """Load configuration from JSON file."""
        try:
            with open(json_path, 'r') as f:
                config_dict = json.load(f)
            return cls(**config_dict)
        except Exception as e:
            logger.error(f"Error loading configuration from {json_path}: {e}")
            logger.info("Using default configuration")
            return cls()
    
    def to_json(self, json_path: str) -> None:
        """Save configuration to JSON file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            
            with open(json_path, 'w') as f:
                json.dump(self.__dict__, f, indent=2)
            logger.info(f"Configuration saved to {json_path}")
        except Exception as e:
            logger.error(f"Error saving configuration to {json_path}: {e}")

class ComponentType(Enum):
    """Types of quantum financial components."""
    ADAPTIVE_LEARNING = "adaptive_learning"
    MARKET_ENCODING = "market_encoding"
    PHASE_TRACKING = "phase_tracking"
    QUANTUM_DIFFUSION = "quantum_diffusion"
    STOCHASTIC_SIMULATION = "stochastic_simulation"
    MEMPOOL_ANALYSIS = "mempool_analysis"
    BITCOIN_PRICE_ANALYSIS = "bitcoin_price_analysis"
    COINCAP_MARKET_ANALYSIS = "coincap_market_analysis"
    ALL = "all"

@dataclass
class MarketData:
    """Container for market data used across components."""
    
    # Basic market data
    symbol: str
    timestamp: datetime
    price: float
    
    # Order book data
    order_book: Optional[Dict[str, List]] = None
    
    # Market metrics
    volatility: Optional[float] = None
    bid_ask_spread: Optional[float] = None
    order_book_depth: Optional[float] = None
    trade_volume: Optional[float] = None
    order_book_imbalance: Optional[float] = None
    liquidity: Optional[float] = None
    
    # Historical data
    historical_prices: Optional[pd.DataFrame] = None
    
    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> 'MarketData':
        """Create MarketData from dictionary."""
        if 'timestamp' in data_dict and isinstance(data_dict['timestamp'], str):
            data_dict['timestamp'] = datetime.fromisoformat(data_dict['timestamp'])
        return cls(**data_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = self.__dict__.copy()
        # Convert timestamp to string for JSON serialization
        if result['timestamp'] is not None:
            result['timestamp'] = result['timestamp'].isoformat()
        # Convert DataFrame to dict if present
        if result['historical_prices'] is not None:
            result['historical_prices'] = result['historical_prices'].to_dict()
        return result
    
    def to_market_state(self) -> MarketState:
        """Convert to MarketState for stochastic simulation."""
        return MarketState(
            price=self.price,
            order_book_imbalance=self.order_book_imbalance or 0.0,
            volatility=self.volatility or 0.0,
            liquidity=self.liquidity or 0.0,
            market_depth=self.order_book_depth or 0.0,
            timestamp=self.timestamp
        )

@dataclass
class AnalysisResult:
    """Container for analysis results from quantum financial components."""
    
    # Metadata
    symbol: str
    timestamp: datetime
    component_type: ComponentType
    
    # Analysis results
    risk_metrics: Dict[str, float] = field(default_factory=dict)
    predictions: Dict[str, Any] = field(default_factory=dict)
    visualizations: Dict[str, str] = field(default_factory=dict)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'symbol': self.symbol,
            'timestamp': self.timestamp.isoformat(),
            'component_type': self.component_type.value,
            'risk_metrics': self.risk_metrics,
            'predictions': self.predictions,
            'visualizations': self.visualizations,
            'raw_data': self.raw_data
        }
        return result
    
    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> 'AnalysisResult':
        """Create AnalysisResult from dictionary."""
        # Handle component_type conversion
        if 'component_type' in data_dict:
            data_dict['component_type'] = ComponentType(data_dict['component_type'])
        
        # Handle timestamp conversion
        if 'timestamp' in data_dict and isinstance(data_dict['timestamp'], str):
            data_dict['timestamp'] = datetime.fromisoformat(data_dict['timestamp'])
        
        return cls(**data_dict)
    
    def save_to_file(self, filepath: Union[str, Path]) -> None:
        """Save analysis result to JSON file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.info(f"Analysis result saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving analysis result to {filepath}: {e}")

class QuantumFinancialAPI:
    """
    Unified API for quantum financial components.
    
    This API provides a seamless interface for all quantum financial components,
    including:
    - Adaptive Learning System
    - Market Encoding
    - Phase Tracking
    - Quantum Diffusion Models
    - Stochastic Market Simulation
    - Mempool Analysis
    - Bitcoin Price Analysis (via CoinDesk)
    
    The API includes optimization features for performance, memory usage, and
    parallel processing.
    """
    
    def __init__(self, config: Optional[Union[Dict, QuantumFinancialConfig]] = None):
        """Initialize the Quantum Financial API."""
        
        # Convert dict to config if needed
        if isinstance(config, dict):
            self.config = QuantumFinancialConfig(**config)
        elif config is None:
            self.config = QuantumFinancialConfig()
        else:
            self.config = config
        
        # Create save directory
        os.makedirs(self.config.save_path, exist_ok=True)
        
        # Initialize main components
        self.adaptive_learning = AdaptiveLearningSystem()
        
        self.phase_tracker = AdaptivePhaseTracker(
            num_particles=self.config.phase_tracker_num_particles,
            process_noise_scale=self.config.phase_tracker_process_noise,
            measurement_noise_scale=self.config.phase_tracker_measurement_noise
        )
        
        self.quantum_diffusion = QDenseDiffusion(
            num_qubits=self.config.qdense_num_qubits,
            num_layers=self.config.qdense_num_layers,
            shots=self.config.qdense_shots
        )
        
        self.stochastic_simulator = StochasticMarketSimulator(
            config_space_dim=self.config.sms_config_space_dim,
            num_trajectories=self.config.sms_num_trajectories,
            time_step=self.config.sms_time_step,
            drift_scale=self.config.sms_drift_scale,
            diffusion_scale=self.config.sms_diffusion_scale,
            quantum_potential_strength=self.config.sms_quantum_potential_strength
        )
        
        # Initialize optimization components
        self._init_optimization_components()
        
        # Initialize market analysis components
        if self.config.enable_mempool_analysis:
            self._init_mempool_components()
        else:
            self.mempool_client = None
            self.mempool_analyzer = None
            self._mempool_analysis_thread = None
            
        if self.config.enable_bitcoin_price_analysis:
            self._init_bitcoin_price_components()
        else:
            self.coindesk_client = None
            self.coindesk_analyzer = None
            self._bitcoin_price_analysis_thread = None
            
        if self.config.enable_coincap_analysis:
            self._init_coincap_components()
        else:
            self.coincap_client = None
            self.coincap_analyzer = None
            self._coincap_analysis_thread = None
            
        logger.info("Quantum Financial API initialized successfully")
    
    def _init_optimization_components(self):
        """Initialize performance optimization components based on configuration."""
        # Initialize components one by one to verify each works independently
        try:
            # Step 1: Initialize cache manager if enabled
            if self.config.enable_caching:
                from .core.cache_manager import get_cache_manager, CacheManager
                try:
                    # First try to use the singleton pattern
                    self._cache_manager = get_cache_manager()
                    # Configure with our settings if needed
                    logger.info("Cache manager initialized (singleton)")
                except Exception as e:
                    logger.warning(f"Could not get singleton cache manager: {e}, creating new instance")
                    # Fall back to direct instantiation
                    self._cache_manager = CacheManager(
                        max_results_size=self.config.cache_max_results,
                        max_results_memory_mb=self.config.cache_max_memory_mb,
                        results_ttl=self.config.cache_ttl_seconds
                    )
                    logger.info("Cache manager initialized (direct)")
            else:
                self._cache_manager = None
                logger.info("Caching disabled")
            
            # Step 2: Initialize performance monitor if enabled
            if self.config.enable_performance_monitoring:
                from .core.performance_monitor import get_performance_monitor, PerformanceMonitor
                try:
                    # First try to use the singleton pattern
                    self._performance_monitor = get_performance_monitor()
                    logger.info("Performance monitor initialized (singleton)")
                except Exception as e:
                    logger.warning(f"Could not get singleton performance monitor: {e}, creating new instance")
                    # Fall back to direct instantiation
                    self._performance_monitor = PerformanceMonitor(
                        enabled=True,
                        max_history_size=self.config.performance_max_history,
                        log_threshold_ms=self.config.performance_log_threshold_ms
                    )
                    logger.info("Performance monitoring enabled (direct)")
            else:
                self._performance_monitor = None
                logger.info("Performance monitoring disabled")
            
            # Step 3: Initialize parallel manager if enabled
            if self.config.enable_parallel_processing:
                from .core.parallel_manager import get_parallel_manager, ParallelManager, ExecutionMode
                try:
                    # First try to use the singleton pattern
                    self._parallel_manager = get_parallel_manager()
                    logger.info("Parallel manager initialized (singleton)")
                except Exception as e:
                    logger.warning(f"Could not get singleton parallel manager: {e}, creating new instance")
                    # Convert string mode to enum
                    mode_map = {
                        "thread": ExecutionMode.THREAD,
                        "process": ExecutionMode.PROCESS,
                        "auto": ExecutionMode.AUTO
                    }
                    exec_mode = mode_map.get(self.config.parallel_execution_mode, ExecutionMode.AUTO)
                    
                    # Fall back to direct instantiation
                    self._parallel_manager = ParallelManager(
                        max_workers=self.config.parallel_max_workers,
                        execution_mode=exec_mode,
                        max_memory_percent=self.config.parallel_max_memory_percent
                    )
                    logger.info(f"Parallel manager initialized (direct) with mode {exec_mode}")
            else:
                self._parallel_manager = None
                logger.info("Parallel processing disabled")
            
            # Step 4: Initialize memory optimizer if enabled
            if self.config.enable_memory_optimization:
                from .core.memory_optimizer import get_memory_optimizer, MemoryOptimizer, DataCompressionLevel
                try:
                    # First try to use the singleton pattern
                    self._memory_optimizer = get_memory_optimizer()
                    logger.info("Memory optimizer initialized (singleton)")
                except Exception as e:
                    logger.warning(f"Could not get singleton memory optimizer: {e}, creating new instance")
                    # Convert int level to enum
                    comp_level_map = {
                        0: DataCompressionLevel.NONE,
                        1: DataCompressionLevel.LOW,
                        5: DataCompressionLevel.MEDIUM,
                        9: DataCompressionLevel.HIGH
                    }
                    # Use closest available level
                    available_levels = list(comp_level_map.keys())
                    closest_level = min(available_levels, key=lambda x: abs(x - self.config.memory_compression_level))
                    compression_level = comp_level_map.get(closest_level, DataCompressionLevel.MEDIUM)
                    
                    # Fall back to direct instantiation
                    self._memory_optimizer = MemoryOptimizer(
                        enable_compression=True,
                        enable_lazy_loading=True,
                        enable_chunk_processing=True,
                        compression_level=compression_level,
                        chunk_size=self.config.memory_chunk_size,
                        memory_warning_threshold_percent=self.config.memory_warning_threshold_percent,
                        memory_critical_threshold_percent=self.config.memory_critical_threshold_percent
                    )
                    logger.info(f"Memory optimizer initialized (direct) with compression level {compression_level}")
            else:
                self._memory_optimizer = None
                logger.info("Memory optimization disabled")
                
        except Exception as e:
            logger.error(f"Error initializing optimization components: {e}")
            logger.info("Optimization components disabled due to initialization error")
            # Disable all components on error
            self._cache_manager = None
            self._performance_monitor = None
            self._parallel_manager = None
            self._memory_optimizer = None
    
    def _init_mempool_components(self):
        """Initialize Bitcoin mempool analysis components if enabled."""
        if self.config.enable_mempool_analysis:
            try:
                # Configure mempool client
                mempool_config = MempoolConfig(
                    base_url=self.config.mempool_api_url,
                    network=MempoolNetwork(self.config.mempool_network)
                )
                
                # Create mempool client
                self.mempool_client = MempoolClient(mempool_config)
                
                # Create mempool analyzer with output path matching our config
                mempool_save_path = os.path.join(self.config.save_path, "mempool_analysis")
                self.mempool_analyzer = MempoolAnalyzer(
                    mempool_client=self.mempool_client,
                    save_path=mempool_save_path
                )
                
                logger.info("Mempool analysis components initialized")
            except Exception as e:
                logger.error(f"Error initializing mempool components: {e}")
                self.config.enable_mempool_analysis = False
                self.mempool_client = None
                self.mempool_analyzer = None
        else:
            self.mempool_client = None
            self.mempool_analyzer = None
            logger.info("Mempool analysis is disabled")
    
    def _init_bitcoin_price_components(self):
        """Initialize the Bitcoin price analysis components using CoinDesk API."""
        try:
            # Import dependencies inside function to avoid circular imports
            # Client is likely in api_clients, Analyzer is in api.core
            from quantum_finance.api_clients.coindesk_client import CoinDeskClient, CoinDeskConfig
            from quantum_finance.api.core.coindesk_analyzer import CoinDeskAnalyzer
            
            # Create the CoinDesk client config
            coindesk_config = CoinDeskConfig(
                base_url=self.config.coindesk_api_base_url
            )
            
            # Initialize the CoinDesk client
            self.coindesk_client = CoinDeskClient(config=coindesk_config)
            
            # Initialize the CoinDesk analyzer
            bitcoin_price_save_path = os.path.join(self.config.save_path, "bitcoin_price_analysis")
            self.bitcoin_price_analyzer = CoinDeskAnalyzer(
                coindesk_client=self.coindesk_client,
                save_path=bitcoin_price_save_path
            )
            
            logger.info("Bitcoin price analysis components initialized")
        except Exception as e:
            logger.error(f"Error initializing Bitcoin price analysis components: {e}")
            raise
    
    def _init_coincap_components(self):
        """Initialize CoinCap API components."""
        logger.info("Initializing CoinCap components...")
        
        # Create save directory for CoinCap analysis
        coincap_save_path = os.path.join(self.config.save_path, "coincap_analysis")
        os.makedirs(coincap_save_path, exist_ok=True)
        
        # Initialize CoinCap client
        coincap_config = CoinCapConfig(
            base_url=self.config.coincap_api_base_url,
            api_key=self.config.coincap_api_key
        )
        self.coincap_client = CoinCapClient(config=coincap_config)
        
        # Initialize CoinCap analyzer
        self.coincap_analyzer = CoinCapAnalyzer(
            coincap_client=self.coincap_client,
            save_path=coincap_save_path
        )
        
        self._coincap_analysis_thread = None
        logger.info("CoinCap components initialized")
    
    def _get_component(self, component_type: ComponentType) -> Any:
        """Get a specific component by type."""
        if component_type == ComponentType.ADAPTIVE_LEARNING:
            return self.adaptive_learning
        elif component_type == ComponentType.MARKET_ENCODING:
            # No specific class, just imported functions
            return None
        elif component_type == ComponentType.PHASE_TRACKING:
            return self.phase_tracker
        elif component_type == ComponentType.QUANTUM_DIFFUSION:
            return self.quantum_diffusion
        elif component_type == ComponentType.STOCHASTIC_SIMULATION:
            return self.stochastic_simulator
        elif component_type == ComponentType.MEMPOOL_ANALYSIS:
            return self.mempool_analyzer
        elif component_type == ComponentType.BITCOIN_PRICE_ANALYSIS:
            return self.coindesk_analyzer
        elif component_type == ComponentType.COINCAP_MARKET_ANALYSIS:
            return self.coincap_analyzer
        else:
            logger.warning(f"Unknown component type: {component_type}")
            return None
    
    def encode_market_data(self, market_data: MarketData) -> Dict[str, Any]:
        """
        Encode market data into quantum states using quantum market encoding.
        
        Args:
            market_data: Market data to encode
            
        Returns:
            Dictionary of quantum circuits for different aspects of market data
        """
        result = {}
        
        # Encode order book imbalance if available
        if market_data.order_book is not None:
            result['order_book_imbalance'] = encode_order_book_imbalance(
                market_data.order_book,
                num_qubits=self.config.market_encoding_qubits
            )
        
        # Encode volatility if available
        if market_data.volatility is not None:
            result['volatility'] = encode_market_volatility(
                market_data.volatility,
                num_qubits=self.config.market_encoding_qubits
            )
        
        # Encode price impact if order book and trade volume are available
        if market_data.order_book is not None and market_data.trade_volume is not None:
            circuit, impact = encode_price_impact(
                market_data.order_book,
                market_data.trade_volume,
                num_qubits=self.config.market_encoding_qubits
            )
            result['price_impact'] = circuit
            result['price_impact_value'] = impact
        
        # Encode liquidity risk if relevant metrics are available
        if all(v is not None for v in [
            market_data.bid_ask_spread,
            market_data.order_book_depth,
            market_data.trade_volume
        ]):
            # Assertions to satisfy the type checker
            assert market_data.bid_ask_spread is not None
            assert market_data.order_book_depth is not None
            assert market_data.trade_volume is not None
            
            result['liquidity_risk'] = encode_liquidity_risk(
                market_data.bid_ask_spread,
                market_data.order_book_depth,
                market_data.trade_volume,
                num_qubits=self.config.market_encoding_qubits
            )
        
        # Encode combined market risk if all necessary components are available
        if all(v is not None for v in [
            market_data.order_book,
            market_data.volatility,
            market_data.trade_volume
        ]):
            # Assertions to satisfy the type checker
            assert market_data.order_book is not None
            assert market_data.volatility is not None
            assert market_data.trade_volume is not None
            
            result['combined_risk'] = combined_market_risk_encoding(
                market_data.order_book,
                market_data.volatility,
                market_data.trade_volume / 100,  # Normalize trade volume
                market_data.trade_volume,
                num_qubits=self.config.market_encoding_qubits
            )
        
        return result
    
    def analyze_market_phase(self, market_data: MarketData) -> AnalysisResult:
        """
        Analyze market phase using adaptive phase tracking.
        
        Args:
            market_data: Market data to analyze
            
        Returns:
            Analysis result from phase tracking
        """
        # Get phase tracker component
        phase_tracker = self._get_component(ComponentType.PHASE_TRACKING)
        
        # Create price measurement from market data
        price_measurement = market_data.price
        
        # Update phase tracker with new measurement
        state_estimate, uncertainty_metrics = phase_tracker.update(price_measurement)
        
        # Get IMM model probabilities if available
        if hasattr(phase_tracker, 'get_imm_probabilities') and phase_tracker.use_imm:
            imm_probs = phase_tracker.get_imm_probabilities()
            regime_probs = {f"regime_{i}": float(p) for i, p in enumerate(imm_probs)}
            
            # Determine dominant regime
            dominant_regime = np.argmax(imm_probs)
            regime_names = ["Stable", "Volatile", "Highly Volatile"]
            if dominant_regime < len(regime_names):
                regime_name = regime_names[dominant_regime]
            else:
                regime_name = f"Regime {dominant_regime}"
        else:
            regime_probs = {}
            regime_name = "Unknown"
        
        # Create analysis result
        result = AnalysisResult(
            symbol=market_data.symbol,
            timestamp=market_data.timestamp,
            component_type=ComponentType.PHASE_TRACKING,
            risk_metrics={
                "phase": state_estimate.phase,
                "phase_uncertainty": state_estimate.phase_uncertainty,
                "innovation": state_estimate.innovation,
                **regime_probs
            },
            predictions={
                "phase_forecast": float(state_estimate.state_vector[0] + 
                                        state_estimate.state_vector[1] * phase_tracker.T),
                "frequency": float(state_estimate.state_vector[1])
            },
            raw_data={
                "state_vector": state_estimate.state_vector.tolist(),
                "covariance_matrix": state_estimate.covariance_matrix.tolist(),
                "uncertainty_metrics": uncertainty_metrics.__dict__ if hasattr(uncertainty_metrics, '__dict__') else {},
                "dominant_regime_name": regime_name
            }
        )
        
        return result
    
    def predict_with_adaptive_learning(self, market_data: MarketData) -> AnalysisResult:
        """
        Make predictions using adaptive learning system.
        
        Args:
            market_data: Market data for prediction
            
        Returns:
            Analysis result from adaptive learning
        """
        # Get adaptive learning component
        als = self._get_component(ComponentType.ADAPTIVE_LEARNING)
        
        # Prepare input data
        # This is simplified - in practice, you would extract features from market_data
        input_data = np.array([
            market_data.price,
            market_data.volatility or 0.0,
            market_data.order_book_imbalance or 0.0,
            market_data.liquidity or 0.0
        ])
        
        # Get prediction from adaptive learning system
        prediction = als.process_new_data(input_data)
        
        # Get performance metrics
        performance_metrics = als.evaluate_performance()
        
        # Create analysis result
        result = AnalysisResult(
            symbol=market_data.symbol,
            timestamp=market_data.timestamp,
            component_type=ComponentType.ADAPTIVE_LEARNING,
            predictions={
                "predicted_value": float(prediction) if isinstance(prediction, (int, float, np.number)) else prediction,
            },
            risk_metrics={
                "confidence": performance_metrics.get('accuracy', 0.0)
            },
            raw_data={
                "input_data": input_data.tolist(),
                "performance_metrics": performance_metrics
            }
        )
        
        return result
    
    def simulate_market_evolution(
        self,
        market_data: MarketData,
        days: int = 30
    ) -> AnalysisResult:
        """
        Simulate market evolution over a specified period.
        
        Args:
            market_data: Current market data
            days: Number of days to simulate
            
        Returns:
            Analysis result containing simulation results
        """
        # Start performance monitoring if enabled
        if self._performance_monitor and hasattr(self._performance_monitor, 'function_timer'):
            try:
                # Get the timer decorator
                timer_decorator = self._performance_monitor.function_timer(PerfComponentType.API_CORE)
                
                # Define a wrapper function that can be decorated
                @timer_decorator
                def timed_simulation():
                    return self._simulate_market_evolution_impl(market_data, days)
                
                # Execute the timed function
                return timed_simulation()
            except Exception as e:
                logger.warning(f"Performance monitoring failed: {e}, falling back to direct execution")
                return self._simulate_market_evolution_impl(market_data, days)
        else:
            return self._simulate_market_evolution_impl(market_data, days)
    
    def _simulate_market_evolution_impl(
        self,
        market_data: MarketData,
        days: int = 30
    ) -> AnalysisResult:
        """Implementation of market evolution simulation with memory optimization."""
        # Get stochastic simulator component
        simulator = self._get_component(ComponentType.STOCHASTIC_SIMULATION)
        
        # Convert market data to market state
        market_state = market_data.to_market_state()
        
        # Track memory usage during simulation if memory optimization is enabled
        if self._memory_optimizer:
            with self._memory_optimizer.track_memory_usage("market_simulation"):
                simulation_results, var_metrics = self._run_simulation(simulator, market_data, days)
        else:
            simulation_results, var_metrics = self._run_simulation(simulator, market_data, days)
        
        # Process and compress large trajectories if memory optimization is enabled
        if self._memory_optimizer and "quantum_trajectories" in simulation_results:
            # Use chunk processing for analyzing large trajectory data
            logger.debug("Processing simulation trajectories in chunks")
            
            # Compress trajectory data to save memory
            for traj_type in ["quantum_trajectories", "monte_carlo_trajectories"]:
                if traj_type in simulation_results and simulation_results[traj_type]:
                    try:
                        # Only compress if substantial data
                        if len(simulation_results[traj_type]) > 100:
                            # Check memory_optimizer exists before calling compress_data
                            if self._memory_optimizer:
                                compressed_data, stats = self._memory_optimizer.compress_data(
                                    simulation_results[traj_type]
                                )
                                
                                # Replace with compressed data if compression was effective
                                if stats.compression_ratio > 1.5:  # Only if we save at least 33% space
                                    logger.debug(
                                        f"Compressed {traj_type}: {stats.size_reduction_percent:.1f}% reduction "
                                        f"({stats.original_size_bytes/1024/1024:.2f}MB → "
                                        f"{stats.compressed_size_bytes/1024/1024:.2f}MB)"
                                    )
                                    # Store compressed data with metadata for decompression
                                    simulation_results[traj_type] = {
                                        "compressed": True,
                                        "data": compressed_data,
                                        "compression_stats": stats
                                    }
                            else:
                                logger.warning("_memory_optimizer is None, cannot compress data.")
                                
                    except Exception as e:
                        logger.warning(f"Error compressing {traj_type}: {e}")
        
        # Create analysis result
        result = AnalysisResult(
            symbol=market_data.symbol,
            timestamp=market_data.timestamp,
            component_type=ComponentType.STOCHASTIC_SIMULATION,
            risk_metrics=var_metrics,
            predictions=self._extract_predictions(simulation_results, market_data),
            raw_data={"simulation_metadata": self._get_simulation_metadata(simulation_results)}
        )
        
        # Store full trajectories in a separate file if they're large
        if (simulation_results.get("quantum_trajectories") and 
                isinstance(simulation_results["quantum_trajectories"], list) and 
                len(simulation_results["quantum_trajectories"]) > 100):
            
            # Save trajectories to separate file and store reference
            trajectories_path = os.path.join(
                self.config.save_path, 
                f"trajectories_{market_data.symbol}_{int(time.time())}.json"
            )
            
            try:
                with open(trajectories_path, 'w') as f:
                    json.dump({"trajectories": simulation_results}, f)
                result.raw_data["trajectories_file"] = trajectories_path
                logger.info(f"Large trajectory data saved to {trajectories_path}")
            except Exception as e:
                logger.error(f"Error saving trajectories to file: {e}")
                # Keep trajectories in memory if file save fails
                result.raw_data["simulation_results"] = simulation_results
        else:
            # Store small trajectory data directly in the result
            result.raw_data["simulation_results"] = simulation_results
        
        return result
    
    def _run_simulation(self, simulator, market_data: MarketData, days: int) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """Run market simulation and return results and risk metrics."""
        # Check memory usage before simulation
        if self._memory_optimizer:
            memory_before = self._memory_optimizer.get_memory_stats()
            logger.debug(f"Memory before simulation: {memory_before['system']['percent']:.1f}% used")
        
        # Use simulator directly if it has the right method
        if hasattr(simulator, 'simulate_price_evolution'):
            # Configure memory-optimized parameters if memory optimization is enabled
            if self._memory_optimizer:
                # Adjust simulation parameters based on available memory
                memory_stats = self._memory_optimizer.get_memory_stats()
                available_memory_mb = memory_stats['system']['available_mb']
                system_percent = memory_stats['system']['percent']
                
                # Adapt trajectory count based on available memory
                original_num_trajectories = getattr(simulator, 'num_trajectories', 1000)
                
                if system_percent > 80:  # High memory pressure
                    # Reduce trajectory count to save memory
                    adjusted_trajectories = max(100, original_num_trajectories // 4)
                    if hasattr(simulator, 'num_trajectories'):
                        logger.info(f"Reducing trajectory count from {original_num_trajectories} to {adjusted_trajectories} due to high memory usage")
                        original_num_trajectories = simulator.num_trajectories
                        simulator.num_trajectories = adjusted_trajectories
                
                # Use chunked processing if possible
                if hasattr(simulator, 'enable_chunk_processing') and self._memory_optimizer and self._memory_optimizer.enable_chunk_processing:
                    # Check simulator is not None before accessing attributes
                    if simulator:
                        simulator.enable_chunk_processing = True
                        simulator.chunk_size = self._memory_optimizer.chunk_size
                        logger.debug(f"Enabled chunk processing with size {simulator.chunk_size}")
            
            try:
                # Run simulation with initial market state
                simulation_results = simulator.simulate_price_evolution(
                    symbol=market_data.symbol,
                    days=days,
                    time_step_days=1.0,
                    compare_with_monte_carlo=True
                )
                
                # Calculate risk metrics if available
                var_metrics = {}
                if hasattr(simulator, 'calculate_var_metrics'):
                    var_metrics = simulator.calculate_var_metrics(simulation_results)
            finally:
                # Restore original parameters if they were modified
                if self._memory_optimizer and hasattr(simulator, 'num_trajectories') and 'original_num_trajectories' in locals():
                    simulator.num_trajectories = original_num_trajectories
        else:
            # Simplified calculation if the direct method is not available
            # Use parallel processing if available
            if self._parallel_manager:
                # Generate trajectories in parallel
                logger.debug("Generating trajectories in parallel")
                
                # Calculate number of trajectories based on memory constraints
                if self._memory_optimizer:
                    memory_stats = self._memory_optimizer.get_memory_stats()
                    available_memory_mb = memory_stats['system']['available_mb']
                    
                    # Estimate trajectories based on available memory (heuristic)
                    # Each trajectory is approximately days * 16 bytes
                    traj_count = min(1000, int(available_memory_mb * 1024 * 0.5 / (days * 16)))
                    logger.debug(f"Memory-optimized trajectory count: {traj_count}")
                else:
                    traj_count = 1000  # Default trajectory count
                
                # Function to generate a batch of trajectories
                # This function must accept a single argument which is the args tuple
                def generate_trajectory_batch(args_tuple):
                    batch_size, is_quantum = args_tuple
                    
                    if is_quantum:
                        # Quantum trajectories have higher volatility
                        volatility = 0.02
                    else:
                        # Classical Monte Carlo trajectories
                        volatility = 0.01
                        
                    return [
                        [(market_data.price * (1 + np.random.normal(0, volatility)), 
                          market_data.timestamp + pd.Timedelta(days=d)) 
                         for d in range(days)]
                        for _ in range(batch_size)
                    ]
                
                # Divide work into batches - use smaller batches if memory is constrained
                batch_size = 50 if self._memory_optimizer and memory_stats['system']['percent'] > 70 else 100
                num_batches = traj_count // batch_size
                
                # Submit tasks for quantum trajectories
                quantum_batch_tasks = []
                for _ in range(num_batches):
                    task_id = self._parallel_manager.submit(
                        func=generate_trajectory_batch,
                        args=(batch_size, True),  # quantum = True
                        priority=TaskPriority.NORMAL
                    )
                    quantum_batch_tasks.append(task_id)
                
                # Submit tasks for Monte Carlo trajectories
                mc_batch_tasks = []
                for _ in range(num_batches):
                    task_id = self._parallel_manager.submit(
                        func=generate_trajectory_batch,
                        args=(batch_size, False),  # quantum = False
                        priority=TaskPriority.NORMAL
                    )
                    mc_batch_tasks.append(task_id)
                
                # Collect quantum trajectory results
                quantum_trajectories = []
                for task_id in quantum_batch_tasks:
                    try:
                        batch_result = self._parallel_manager.get_result(task_id)
                        if batch_result:
                            quantum_trajectories.extend(batch_result)
                    except Exception as e:
                        logger.error(f"Error getting quantum trajectory batch: {e}")
                
                # Collect Monte Carlo trajectory results
                monte_carlo_trajectories = []
                for task_id in mc_batch_tasks:
                    try:
                        batch_result = self._parallel_manager.get_result(task_id)
                        if batch_result:
                            monte_carlo_trajectories.extend(batch_result)
                    except Exception as e:
                        logger.error(f"Error getting Monte Carlo trajectory batch: {e}")
                
                simulation_results = {
                    "quantum_trajectories": quantum_trajectories,
                    "monte_carlo_trajectories": monte_carlo_trajectories
                }
                
            # Generate trajectories in chunks to reduce memory pressure if memory optimizer is enabled
            elif self._memory_optimizer:
                # Calculate number of trajectories based on available memory
                memory_stats = self._memory_optimizer.get_memory_stats()
                available_mb = memory_stats.get("available_mb", 1000)
                
                # Adjust trajectory count based on available memory
                # Each trajectory might take ~10KB, so 100MB allows ~10K trajectories
                traj_count = max(100, min(10000, int(available_mb * 0.1)))
                logger.debug(f"Generating {traj_count} trajectories based on available memory")
                
                # Generate trajectories in chunks
                quantum_trajectories = []
                monte_carlo_trajectories = []
                
                chunk_size = 100
                for i in range(0, traj_count, chunk_size):
                    chunk_count = min(chunk_size, traj_count - i)
                    
                    # Generate trajectories for this chunk
                    quantum_chunk = [
                        [(market_data.price * (1 + np.random.normal(0, 0.02)), 
                          market_data.timestamp + pd.Timedelta(days=d)) 
                         for d in range(days)]
                        for _ in range(chunk_count)
                    ]
                    monte_carlo_chunk = [
                        [(market_data.price * (1 + np.random.normal(0, 0.01)), 
                          market_data.timestamp + pd.Timedelta(days=d)) 
                         for d in range(days)]
                        for _ in range(chunk_count)
                    ]
                    
                    quantum_trajectories.extend(quantum_chunk)
                    monte_carlo_trajectories.extend(monte_carlo_chunk)
                    
                    # Force garbage collection between chunks
                    gc.collect()
                
                simulation_results = {
                    "quantum_trajectories": quantum_trajectories,
                    "monte_carlo_trajectories": monte_carlo_trajectories
                }
            else:
                # Generate all trajectories at once
                simulation_results = {
                    "quantum_trajectories": [
                        [(market_data.price * (1 + np.random.normal(0, 0.02)), 
                          market_data.timestamp + pd.Timedelta(days=i)) 
                         for i in range(days)]
                        for _ in range(100)
                    ],
                    "monte_carlo_trajectories": [
                        [(market_data.price * (1 + np.random.normal(0, 0.01)), 
                          market_data.timestamp + pd.Timedelta(days=i)) 
                         for i in range(days)]
                        for _ in range(100)
                    ]
                }
            
            # Calculate simplified VaR metrics
            final_prices_quantum = [traj[-1][0] for traj in simulation_results["quantum_trajectories"]]
            returns_quantum = [(p - market_data.price) / market_data.price for p in final_prices_quantum]
            # Calculate metrics using numpy
            var_95_np = np.percentile(returns_quantum, 5) * -1
            var_99_np = np.percentile(returns_quantum, 1) * -1
            es_95_np = np.mean([r for r in returns_quantum if r <= np.percentile(returns_quantum, 5)]) * -1
            # Create dictionary with standard python floats
            var_metrics = {
                "var_95": float(var_95_np),
                "var_99": float(var_99_np),
                "expected_shortfall_95": float(es_95_np)
            }
        
        return simulation_results, var_metrics
    
    def _extract_predictions(self, simulation_results: Dict[str, Any], market_data: MarketData) -> Dict[str, Any]:
        """Extract prediction data from simulation results, handling compressed data if needed."""
        predictions = {}
        
        # Handle both compressed and uncompressed trajectory data
        for traj_type in ["quantum_trajectories", "monte_carlo_trajectories"]:
            if traj_type not in simulation_results:
                continue
                
            trajectories = simulation_results[traj_type]
            
            # Decompress if compressed
            if isinstance(trajectories, dict) and trajectories.get("compressed", False):
                if self._memory_optimizer:
                    try:
                        trajectories = self._memory_optimizer.decompress_data(trajectories["data"])
                    except Exception as e:
                        logger.error(f"Error decompressing {traj_type}: {e}")
                        continue
                else:
                    logger.warning(f"Cannot decompress {traj_type} - memory optimizer not available")
                    continue
            
            # Calculate statistics on trajectories
            try:
                # Safe extraction of final prices
                if not trajectories or not isinstance(trajectories, list):
                    continue
                    
                # Process first few trajectories for predictions to save memory
                sample = trajectories[:min(100, len(trajectories))]
                final_prices = [traj[-1][0] for traj in sample if traj and len(traj) > 0]
                
                if not final_prices:
                    continue
                    
                # Calculate basic statistics
                key_prefix = "quantum" if traj_type == "quantum_trajectories" else "monte_carlo"
                predictions[f"{key_prefix}_final_price_mean"] = float(np.mean(final_prices))
                predictions[f"{key_prefix}_final_price_std"] = float(np.std(final_prices))
                predictions[f"{key_prefix}_final_price_min"] = float(np.min(final_prices))
                predictions[f"{key_prefix}_final_price_max"] = float(np.max(final_prices))
                
                # Calculate return statistics
                returns = [(p - market_data.price) / market_data.price for p in final_prices]
                predictions[f"{key_prefix}_return_mean"] = float(np.mean(returns))
                predictions[f"{key_prefix}_return_std"] = float(np.std(returns))
                
            except Exception as e:
                logger.error(f"Error extracting predictions from {traj_type}: {e}")
        
        return predictions
    
    def _get_simulation_metadata(self, simulation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata about the simulation results."""
        metadata = {}
        
        for key, value in simulation_results.items():
            if isinstance(value, list):
                metadata[f"{key}_count"] = len(value)
            elif isinstance(value, dict) and value.get("compressed", False):
                # Handle compressed data
                stats = value.get("compression_stats", {})
                metadata[f"{key}_compressed"] = True
                metadata[f"{key}_original_size_mb"] = stats.get("original_size_bytes", 0) / (1024 * 1024)
                metadata[f"{key}_compressed_size_mb"] = stats.get("compressed_size_bytes", 0) / (1024 * 1024)
                metadata[f"{key}_compression_ratio"] = stats.get("compression_ratio", 0)
        
        return metadata
    
    def analyze_market_data(
        self,
        market_data: MarketData,
        components: Optional[List[ComponentType]] = None
    ) -> Dict[ComponentType, AnalysisResult]:
        """
        Analyze market data using specified or all available components.
        
        Args:
            market_data: Market data to analyze
            components: List of components to use for analysis, or None to use all
            
        Returns:
            Dictionary mapping component types to analysis results
        """
        # Start performance monitoring if enabled
        if self._performance_monitor and hasattr(self._performance_monitor, 'function_timer'):
            try:
                # Get the timer decorator
                timer_decorator = self._performance_monitor.function_timer(PerfComponentType.API_CORE)
                
                # Define a wrapper function that can be decorated
                @timer_decorator
                def timed_analysis():
                    return self._analyze_market_data_impl(market_data, components)
                
                # Execute the timed function
                return timed_analysis()
            except Exception as e:
                logger.warning(f"Performance monitoring failed: {e}, falling back to direct execution")
                return self._analyze_market_data_impl(market_data, components)
        else:
            return self._analyze_market_data_impl(market_data, components)
    
    def _analyze_market_data_impl(
        self,
        market_data: MarketData,
        components: Optional[List[ComponentType]] = None
    ) -> Dict[ComponentType, AnalysisResult]:
        """Implementation of market data analysis with optimization features."""
        if components is None or ComponentType.ALL in components:
            components = [
                ComponentType.ADAPTIVE_LEARNING,
                ComponentType.PHASE_TRACKING,
                ComponentType.STOCHASTIC_SIMULATION
            ]
        
        # Initialize results dictionary
        results = {}
        
        # Check if we can use parallel processing
        use_parallel = (
            self._parallel_manager is not None and 
            len(components) > 1
        )
        
        # Use memory tracking if memory optimization is enabled
        if self._memory_optimizer and self._performance_monitor:
            with self._memory_optimizer.track_memory_usage("analyze_market_data"):
                return self._analyze_with_memory_optimization(market_data, components, use_parallel)
        else:
            return self._analyze_without_memory_optimization(market_data, components, use_parallel)
    
    def _analyze_with_memory_optimization(
        self,
        market_data: MarketData,
        components: List[ComponentType],
        use_parallel: bool
    ) -> Dict[ComponentType, AnalysisResult]:
        """Analyze market data with memory optimization enabled."""
        results = {}
        
        # Compress historical data if present and large
        original_historical_prices = None
        if (market_data.historical_prices is not None and 
            len(market_data.historical_prices) > self._memory_optimizer.chunk_size):
            
            logger.debug(f"Compressing historical data with {len(market_data.historical_prices)} rows")
            original_historical_prices = market_data.historical_prices
            
            # Create a compressed copy to use during analysis
            compressed_data, stats = self._memory_optimizer.compress_data(
                original_historical_prices.to_dict(), 
                compression_level=self._memory_optimizer.compression_level
            )
            
            # Remove the large DataFrame temporarily
            market_data.historical_prices = None
            
            # Force garbage collection
            gc.collect()
            
            logger.debug(
                f"Compressed historical data: {stats.original_size_bytes / (1024*1024):.2f}MB -> "
                f"{stats.compressed_size_bytes / (1024*1024):.2f}MB, "
                f"ratio: {stats.compression_ratio:.2f}"
            )
        
        try:
            if use_parallel:
                # Process components in parallel with memory optimization
                results = self._analyze_parallel_with_memory_opt(market_data, components)
            else:
                # Process components sequentially with memory optimization
                results = self._analyze_sequential_with_memory_opt(market_data, components)
        finally:
            # Restore original data if it was compressed
            if original_historical_prices is not None:
                market_data.historical_prices = original_historical_prices
        
        return results
    
    def _analyze_parallel_with_memory_opt(
        self,
        market_data: MarketData,
        components: List[ComponentType]
    ) -> Dict[ComponentType, AnalysisResult]:
        """Process components in parallel with memory optimization."""
        results = {}
        task_ids = {}
        
        # Check memory state before starting
        memory_stats_before = self._memory_optimizer.get_memory_stats()
        logger.debug(f"Memory before parallel analysis: {memory_stats_before['system']['percent']:.1f}% used")
        
        for component_type in components:
            # Create cache key for analysis result
            cache_key = self._get_analysis_cache_key(market_data, component_type)
            
            # Try to get from cache first
            if self._cache_manager:
                cached_result = self._cache_manager.get_result(cache_key)
                if cached_result is not None:
                    logger.info(f"Using cached result for {component_type.value}")
                    results[component_type] = cached_result
                    continue
            
            # Not in cache, submit task for parallel execution
            logger.debug(f"Submitting {component_type.value} analysis to parallel manager")
            
            # Create a wrapper function that follows the ParallelManager's convention
            # The function must accept a single argument which is the args tuple
            def analyze_wrapper(args_tuple):
                # Use memory tracking for each component analysis
                if self._memory_optimizer:
                    with self._memory_optimizer.track_memory_usage(f"analyze_{component_type.value}"):
                        return self._analyze_with_component(component_type, market_data, cache_key)
                else:
                    return self._analyze_with_component(component_type, market_data, cache_key)
            
            task_id = self._parallel_manager.submit(
                func=analyze_wrapper,
                args=None,  # No args needed as we're using closure
                priority=TaskPriority.NORMAL
            )
            task_ids[component_type] = task_id
        
        # Wait for all tasks to complete
        for component_type, task_id in task_ids.items():
            try:
                # Get result from parallel execution
                result = self._parallel_manager.get_result(task_id, timeout=None)
                if result is not None:
                    results[component_type] = result
            except Exception as e:
                logger.error(f"Error in parallel analysis with {component_type.value}: {e}")
        
        # Check memory state after completion
        memory_stats_after = self._memory_optimizer.get_memory_stats()
        logger.debug(f"Memory after parallel analysis: {memory_stats_after['system']['percent']:.1f}% used")
        
        # Force garbage collection if memory usage is high
        if memory_stats_after['system']['percent'] > self._memory_optimizer.memory_warning_threshold_percent:
            gc_stats = self._memory_optimizer.force_garbage_collection()
            logger.info(f"Forced garbage collection: freed {gc_stats['memory_diff_mb']:.2f}MB")
        
        return results
    
    def _analyze_sequential_with_memory_opt(
        self,
        market_data: MarketData,
        components: List[ComponentType]
    ) -> Dict[ComponentType, AnalysisResult]:
        """Process components sequentially with memory optimization."""
        results = {}
        
        for component_type in components:
            try:
                # Create cache key for analysis result
                cache_key = self._get_analysis_cache_key(market_data, component_type)
                
                # Try to get from cache first
                if self._cache_manager:
                    cached_result = self._cache_manager.get_result(cache_key)
                    if cached_result is not None:
                        logger.info(f"Using cached result for {component_type.value}")
                        results[component_type] = cached_result
                        continue
                
                # Not in cache, perform analysis with memory tracking
                if self._memory_optimizer:
                    with self._memory_optimizer.track_memory_usage(f"analyze_{component_type.value}"):
                        result = self._analyze_with_component(component_type, market_data, cache_key)
                else:
                    result = self._analyze_with_component(component_type, market_data, cache_key)
                
                results[component_type] = result
                
                # Check memory usage after each component and force GC if needed
                if self._memory_optimizer:
                    memory_stats = self._memory_optimizer.get_memory_stats()
                    if memory_stats['system']['percent'] > self._memory_optimizer.memory_warning_threshold_percent:
                        gc_stats = self._memory_optimizer.force_garbage_collection()
                        logger.info(
                            f"Forced garbage collection after {component_type.value}: "
                            f"freed {gc_stats['memory_diff_mb']:.2f}MB"
                        )
                
            except Exception as e:
                logger.error(f"Error during analysis with {component_type.value}: {e}")
                # Continue with other components instead of failing
        
        return results
    
    def _analyze_without_memory_optimization(
        self,
        market_data: MarketData,
        components: List[ComponentType],
        use_parallel: bool
    ) -> Dict[ComponentType, AnalysisResult]:
        """Analyze market data without memory optimization."""
        results = {}
        
        if use_parallel:
            # Process components in parallel
            logger.info(f"Analyzing {len(components)} components in parallel")
            task_ids = {}
            
            for component_type in components:
                # Create cache key for analysis result
                cache_key = self._get_analysis_cache_key(market_data, component_type)
                
                # Try to get from cache first
                if self._cache_manager:
                    cached_result = self._cache_manager.get_result(cache_key)
                    if cached_result is not None:
                        logger.info(f"Using cached result for {component_type.value}")
                        results[component_type] = cached_result
                        continue
                
                # Not in cache, submit task for parallel execution
                logger.debug(f"Submitting {component_type.value} analysis to parallel manager")
                
                # Create a wrapper function that follows the ParallelManager's convention
                # The function must accept a single argument which is the args tuple
                def analyze_wrapper(args_tuple):
                    # No args needed as we're using closure to capture the variables
                    return self._analyze_with_component(component_type, market_data, cache_key)
                
                task_id = self._parallel_manager.submit(
                    func=analyze_wrapper,
                    args=None,  # No args needed as we're using closure
                    priority=TaskPriority.NORMAL
                )
                task_ids[component_type] = task_id
            
            # Wait for all tasks to complete
            for component_type, task_id in task_ids.items():
                try:
                    # Get result from parallel execution
                    result = self._parallel_manager.get_result(task_id, timeout=None)
                    if result is not None:
                        results[component_type] = result
                except Exception as e:
                    logger.error(f"Error in parallel analysis with {component_type.value}: {e}")
        else:
            # Process components sequentially with caching
            for component_type in components:
                try:
                    # Create cache key for analysis result
                    cache_key = self._get_analysis_cache_key(market_data, component_type)
                    
                    # Try to get from cache first
                    if self._cache_manager:
                        cached_result = self._cache_manager.get_result(cache_key)
                        if cached_result is not None:
                            logger.info(f"Using cached result for {component_type.value}")
                            results[component_type] = cached_result
                            continue
                    
                    # Not in cache, perform analysis
                    result = self._analyze_with_component(component_type, market_data, cache_key)
                    results[component_type] = result
                    
                except Exception as e:
                    logger.error(f"Error during analysis with {component_type.value}: {e}")
                    # Continue with other components instead of failing
        
        return results
    
    def _get_analysis_cache_key(self, market_data: MarketData, component_type: ComponentType) -> str:
        """Generate a cache key for an analysis result."""
        return f"analysis_{component_type.value}_{market_data.symbol}_{market_data.timestamp.isoformat()}"
    
    def _analyze_with_component(
        self, 
        component_type: ComponentType, 
        market_data: MarketData,
        cache_key: Optional[str] = None
    ) -> AnalysisResult:
        """Analyze market data with a specific component."""
        
        logger.debug(f"Running analysis with component: {component_type.value}")
        
        if component_type == ComponentType.MARKET_ENCODING:
            result = self.encode_market_data(market_data)
            
        elif component_type == ComponentType.PHASE_TRACKING:
            result = self.analyze_market_phase(market_data)
            
        elif component_type == ComponentType.ADAPTIVE_LEARNING:
            result = self.predict_with_adaptive_learning(market_data)
            
        elif component_type == ComponentType.STOCHASTIC_SIMULATION:
            result = self.simulate_market_evolution(market_data)
            
        elif component_type == ComponentType.MEMPOOL_ANALYSIS:
            result = self.analyze_mempool()
            
        elif component_type == ComponentType.BITCOIN_PRICE_ANALYSIS:
            result = self.analyze_bitcoin_price()
            
        elif component_type == ComponentType.COINCAP_MARKET_ANALYSIS:
            # Use symbol from market data if available, otherwise use default asset
            asset_id = market_data.symbol.lower() if hasattr(market_data, 'symbol') else "bitcoin"
            result = self.analyze_coincap_asset(asset_id)
            
        else:
            logger.error(f"Unsupported component type for analysis: {component_type}")
            raise ValueError(f"Unsupported component type for analysis: {component_type}")
        
        return result
    
    def save_analysis_results(
        self,
        results: Dict[ComponentType, AnalysisResult],
        base_filename: Optional[str] = None
    ) -> Dict[ComponentType, str]:
        """
        Save analysis results to files.
        
        Args:
            results: Dictionary mapping component types to analysis results
            base_filename: Base filename for saved results
                          (defaults to "analysis_results_{timestamp}")
            
        Returns:
            Dictionary mapping component types to saved file paths
        """
        if base_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"analysis_results_{timestamp}"
        
        # Create save directory if it doesn't exist
        save_dir = os.path.join(self.config.save_path, "analysis_results")
        os.makedirs(save_dir, exist_ok=True)
        
        # Initialize paths dictionary
        saved_paths = {}
        
        # Save each result to a file
        for component_type, result in results.items():
            try:
                # Generate filename based on component type and result timestamp
                filename = f"{base_filename}_{component_type.value}.json"
                filepath = os.path.join(save_dir, filename)
                
                # Save result to file
                result.save_to_file(filepath)
                
                # Add to paths dictionary
                saved_paths[component_type] = filepath
            except Exception as e:
                logger.error(f"Error saving result for {component_type.value}: {e}")
        
        return saved_paths
    
    def load_analysis_result(self, filepath: Union[str, Path]) -> AnalysisResult:
        """
        Load analysis result from file.
        
        Args:
            filepath: Path to the analysis result file
            
        Returns:
            Loaded analysis result
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return AnalysisResult.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading analysis result from {filepath}: {e}")
            raise
    
    def cleanup(self):
        """Clean up resources and stop any running tasks."""
        logger.info("Cleaning up resources")
        
        try:
            # Stop any scheduled tasks
            if hasattr(self, '_mempool_analysis_thread') and self._mempool_analysis_thread is not None:
                self.stop_scheduled_mempool_analysis()
                
            if hasattr(self, '_bitcoin_price_analysis_thread') and self._bitcoin_price_analysis_thread is not None:
                self.stop_scheduled_bitcoin_price_analysis()
                
            if hasattr(self, '_coincap_analysis_thread') and self._coincap_analysis_thread is not None:
                self.stop_scheduled_coincap_analysis()
                
            # Clean up cache if it exists
            if hasattr(self, '_cache_manager') and self._cache_manager is not None:
                self._cache_manager.clear()
                
            # Clean up other resources as needed
            
        except Exception as e:
            logger.error(f"Error during API cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup when object is garbage collected."""
        try:
            self.cleanup()
        except Exception as e:
            # Don't raise exceptions in destructor
            print(f"Error during API cleanup: {e}")

    def create_ensemble_prediction(
        self,
        results: Dict[ComponentType, AnalysisResult],
        weights: Optional[Dict[ComponentType, float]] = None
    ) -> Dict[str, Any]:
        """
        Create an ensemble prediction based on multiple analysis results.
        
        Args:
            results: Dictionary mapping component types to analysis results
            weights: Dictionary mapping component types to weights
                     (defaults to equal weights)
            
        Returns:
            Dictionary containing ensemble predictions
        """
        if not results:
            logger.warning("No results provided for ensemble prediction")
            return {}
        
        # Use equal weights if not provided
        if weights is None:
            weights = {component_type: 1.0 / len(results) for component_type in results}
        else:
            # Normalize weights to sum to 1
            total_weight = sum(weights.values())
            weights = {k: v / total_weight for k, v in weights.items()}
        
        # Extract individual predictions
        predictions = {}
        for component_type, result in results.items():
            if component_type in weights:
                # Add weighted predictions to the ensemble
                for key, value in result.predictions.items():
                    if isinstance(value, (int, float, np.number)):
                        if key not in predictions:
                            predictions[key] = 0.0
                        predictions[key] += float(value) * weights[component_type]
        
        # Extract risk metrics
        risk_metrics = {}
        for component_type, result in results.items():
            if component_type in weights:
                # Add weighted risk metrics to the ensemble
                for key, value in result.risk_metrics.items():
                    if isinstance(value, (int, float, np.number)):
                        if key not in risk_metrics:
                            risk_metrics[key] = 0.0
                        risk_metrics[key] += float(value) * weights[component_type]
        
        return {
            "predictions": predictions,
            "risk_metrics": risk_metrics,
            "weights": {k.value: v for k, v in weights.items()}
        }

    def analyze_mempool(self, save_result: bool = True) -> AnalysisResult:
        """
        Analyze the current state of the Bitcoin mempool for market prediction insights.
        
        Args:
            save_result: Whether to save the analysis results to disk
            
        Returns:
            AnalysisResult object containing mempool-based market predictions
        """
        # Check if mempool analysis is enabled
        if not self.config.enable_mempool_analysis or self.mempool_analyzer is None:
            logger.warning("Mempool analysis is disabled or not initialized")
            return AnalysisResult(
                symbol="BTC",
                timestamp=datetime.now(),
                component_type=ComponentType.MEMPOOL_ANALYSIS,
                risk_metrics={"error": "Mempool analysis is disabled"},
                predictions={"error": "Mempool analysis is disabled"}
            )
        
        try:
            # Use performance monitoring if enabled
            if self.config.enable_performance_monitoring and self._performance_monitor:
                @self._performance_monitor.monitor(component=PerfComponentType.ANALYSIS)
                def run_mempool_analysis():
                    # Run mempool analysis
                    metrics = self.mempool_analyzer.analyze_current_mempool(save_result=save_result)
                    signals = self.mempool_analyzer.interpret_market_signals(metrics)
                    
                    # Generate chart if saving results
                    chart_path = ""
                    if save_result:
                        chart_path = self.mempool_analyzer.generate_fee_trend_chart()
                    
                    return metrics, signals, chart_path
                
                metrics, signals, chart_path = run_mempool_analysis()
            else:
                # Run without performance monitoring
                metrics = self.mempool_analyzer.analyze_current_mempool(save_result=save_result)
                signals = self.mempool_analyzer.interpret_market_signals(metrics)
                
                # Generate chart if saving results
                chart_path = ""
                if save_result:
                    chart_path = self.mempool_analyzer.generate_fee_trend_chart()
            
            # Create risk metrics
            risk_metrics = {
                "fee_trend_24h": metrics.fee_trend_24h,
                "fee_volatility": metrics.fee_volatility,
                "congestion_level": metrics.congestion_level,
                "network_demand": metrics.network_demand,
                "urgency_indicator": metrics.urgency_indicator,
                "market_sentiment": metrics.market_sentiment
            }
            
            # Create predictions
            predictions = {
                "short_term_sentiment": signals["prediction"]["short_term_sentiment"],
                "confidence": signals["prediction"]["confidence"],
                "fee_signal": signals["signals"]["fee_trend"]["signal"],
                "congestion_signal": signals["signals"]["congestion"]["signal"],
                "summary": signals["summary"]
            }
            
            # Create visualizations dict
            visualizations = {}
            if chart_path:
                visualizations["fee_trend_chart"] = chart_path
            
            # Create raw data 
            raw_data = {
                "metrics": metrics.to_dict(),
                "signals": signals
            }
            
            # Create and return analysis result
            result = AnalysisResult(
                symbol="BTC",
                timestamp=datetime.now(),
                component_type=ComponentType.MEMPOOL_ANALYSIS,
                risk_metrics=risk_metrics,
                predictions=predictions,
                visualizations=visualizations,
                raw_data=raw_data
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in mempool analysis: {e}")
            logger.debug(traceback.format_exc())
            
            # Return error result
            return AnalysisResult(
                symbol="BTC",
                timestamp=datetime.now(),
                component_type=ComponentType.MEMPOOL_ANALYSIS,
                risk_metrics={"error": str(e)},
                predictions={"error": str(e)},
                raw_data={"traceback": traceback.format_exc()}
            )

    def start_scheduled_mempool_analysis(self, 
                                           interval_minutes: Optional[int] = None, 
                                           callback: Optional[Callable[[AnalysisResult], None]] = None):
        """
        Start a background task to periodically analyze the Bitcoin mempool.
        
        Args:
            interval_minutes: How often to analyze (in minutes), defaults to config value
            callback: Optional function to call with each analysis result
            
        Returns:
            True if scheduled successfully, False otherwise
        """
        if not self.config.enable_mempool_analysis or self.mempool_analyzer is None:
            logger.warning("Mempool analysis is disabled or not initialized")
            return False
        
        if interval_minutes is None:
            interval_minutes = self.config.mempool_analysis_interval_minutes
        
        # Create and start a background thread for scheduled analysis
        def analysis_worker():
            logger.info(f"Starting scheduled mempool analysis every {interval_minutes} minutes")
            
            try:
                while True:
                    # Run analysis
                    result = self.analyze_mempool(save_result=True)
                    
                    # Call callback if provided
                    if callback is not None:
                        try:
                            callback(result)
                        except Exception as e:
                            logger.error(f"Error in mempool analysis callback: {e}")
                    
                    # Sleep until next analysis
                    time.sleep(interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in scheduled mempool analysis: {e}")
                logger.debug(traceback.format_exc())
        
        # Start the worker thread
        import threading
        self._mempool_analysis_thread = threading.Thread(
            target=analysis_worker,
            daemon=True  # Make daemon so it exits when main thread exits
        )
        self._mempool_analysis_thread.start()
        
        return True
    
    def stop_scheduled_mempool_analysis(self):
        """
        Stop the scheduled mempool analysis if running.
        
        Note: Since we're using daemon threads, this isn't strictly necessary,
        but it's included for completeness.
        """
        if hasattr(self, '_mempool_analysis_thread') and self._mempool_analysis_thread.is_alive():
            logger.info("Scheduled mempool analysis will stop when application exits")
            # Daemon threads can't be forcibly stopped in Python
            # They will exit when the main thread exits
            return True
        else:
            logger.info("No scheduled mempool analysis is running")
            return False

    def analyze_bitcoin_price(self, currency: str = None, save_result: bool = True) -> AnalysisResult:
        """
        Analyze Bitcoin price data from CoinDesk API.
        
        Args:
            currency: Currency code to use for price data (default: config default currency)
            save_result: Whether to save the analysis results
            
        Returns:
            AnalysisResult object containing the analysis results
        """
        if not hasattr(self, "bitcoin_price_analyzer"):
            logger.error("Bitcoin price analysis is not enabled")
            raise ValueError("Bitcoin price analysis is not enabled in the configuration")
        
        # Use the default currency from config if not specified
        if currency is None:
            currency = self.config.coindesk_default_currency
        
        logger.info(f"Analyzing Bitcoin price data in {currency}")
        
        try:
            # Run Bitcoin price analysis
            price_metrics = self.bitcoin_price_analyzer.analyze_current_price(
                currency=currency,
                save_result=False  # We'll handle saving ourselves
            )
            
            # Get market signals interpretation
            market_signals = self.bitcoin_price_analyzer.interpret_market_signals(price_metrics)
            
            # Generate price chart
            chart_path = self.bitcoin_price_analyzer.generate_price_chart(days=30)
            
            # Create analysis result
            result = AnalysisResult(
                symbol="BTC",
                timestamp=datetime.now(),
                component_type=ComponentType.BITCOIN_PRICE_ANALYSIS,
                risk_metrics={
                    "volatility_7d": price_metrics.volatility_7d,
                    "volatility_30d": price_metrics.volatility_30d,
                    "price_momentum": price_metrics.price_momentum,
                    "trend_strength": price_metrics.trend_strength,
                    "market_sentiment": price_metrics.market_sentiment,
                    "price_position": price_metrics.price_position
                },
                predictions={
                    "price_trend": market_signals["price_trend"]["signal"],
                    "trend_description": market_signals["price_trend"]["description"],
                    "momentum": market_signals["momentum"]["signal"],
                    "volatility": market_signals["volatility"]["signal"],
                    "overall_sentiment": market_signals["overall_sentiment"]["signal"]
                },
                visualizations={
                    "price_chart": chart_path
                },
                raw_data={
                    "current_price": price_metrics.current_price,
                    "price_change_24h": price_metrics.price_change_24h,
                    "price_change_7d": price_metrics.price_change_7d,
                    "price_change_30d": price_metrics.price_change_30d,
                    "moving_averages": {
                        "sma_7d": price_metrics.sma_7d,
                        "sma_30d": price_metrics.sma_30d,
                        "sma_90d": price_metrics.sma_90d
                    },
                    "currency": price_metrics.currency,
                    "market_signals": market_signals
                }
            )
            
            logger.info(f"Bitcoin price analysis completed with sentiment: {market_signals['overall_sentiment']['signal']}")
            
            # Save the result if requested
            if save_result:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"BTC_price_analysis_{timestamp}"
                
                # Save as JSON
                json_path = os.path.join(self.config.save_path, f"{filename}.json")
                result.save_to_file(json_path)
                
                # Create a summary markdown report
                self._create_price_analysis_report(result, filename)
                
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing Bitcoin price data: {e}")
            
            # Return error result
            return AnalysisResult(
                symbol="BTC",
                timestamp=datetime.now(),
                component_type=ComponentType.BITCOIN_PRICE_ANALYSIS,
                risk_metrics={"error": 1.0},  # Use float for risk metrics to avoid type issues
                predictions={"error": str(e)},
                raw_data={"traceback": traceback.format_exc()}
            )
    
    def _create_price_analysis_report(self, result: AnalysisResult, filename: str) -> str:
        """Create a markdown report from Bitcoin price analysis results."""
        report_path = os.path.join(self.config.save_path, f"{filename}.md")
        
        try:
            with open(report_path, 'w') as f:
                f.write(f"# Bitcoin Price Analysis Report\n\n")
                f.write(f"**Date:** {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write(f"## Summary\n\n")
                f.write(f"**Current Price:** ${result.raw_data['current_price']:,.2f} {result.raw_data['currency']}\n\n")
                f.write(f"**Price Changes:**\n")
                f.write(f"- 24h: {result.raw_data['price_change_24h']:+.2f}%\n")
                f.write(f"- 7d: {result.raw_data['price_change_7d']:+.2f}%\n")
                f.write(f"- 30d: {result.raw_data['price_change_30d']:+.2f}%\n\n")
                
                f.write(f"**Market Sentiment:** {result.predictions['overall_sentiment']}\n\n")
                f.write(f"**Trend:** {result.predictions['price_trend']} - {result.predictions['trend_description']}\n\n")
                
                f.write(f"## Risk Metrics\n\n")
                f.write(f"- Volatility (7d): {result.risk_metrics['volatility_7d']:.4f}\n")
                f.write(f"- Volatility (30d): {result.risk_metrics['volatility_30d']:.4f}\n")
                f.write(f"- Price Momentum: {result.risk_metrics['price_momentum']:.4f}\n")
                f.write(f"- Trend Strength: {result.risk_metrics['trend_strength']:.4f}\n")
                f.write(f"- Market Sentiment: {result.risk_metrics['market_sentiment']:.4f}\n")
                f.write(f"- Price Position: {result.risk_metrics['price_position']:.4f}\n\n")
                
                f.write(f"## Technical Indicators\n\n")
                f.write(f"**Moving Averages:**\n")
                f.write(f"- 7-day SMA: ${result.raw_data['moving_averages']['sma_7d']:,.2f}\n")
                f.write(f"- 30-day SMA: ${result.raw_data['moving_averages']['sma_30d']:,.2f}\n")
                f.write(f"- 90-day SMA: ${result.raw_data['moving_averages']['sma_90d']:,.2f}\n\n")
                
                f.write(f"## Market Signals\n\n")
                for signal_type, signal_data in result.raw_data['market_signals'].items():
                    f.write(f"**{signal_type.replace('_', ' ').title()}:** {signal_data['signal']}\n")
                    f.write(f"- {signal_data['description']}\n")
                    if 'value' in signal_data:
                        f.write(f"- Value: {signal_data['value']:.4f}\n")
                    if 'strength' in signal_data:
                        f.write(f"- Strength: {signal_data['strength']:.4f}\n")
                    f.write("\n")
                
                if 'price_chart' in result.visualizations:
                    f.write(f"## Price Chart\n\n")
                    f.write(f"![Bitcoin Price Chart]({os.path.basename(result.visualizations['price_chart'])})\n\n")
                
                f.write(f"## Disclaimer\n\n")
                f.write(f"This analysis is generated automatically and should not be considered financial advice. ")
                f.write(f"All investment decisions should be made after conducting thorough research and consulting with a financial advisor.\n")
                f.write(f"Price data provided by CoinDesk Bitcoin Price Index (BPI).\n")
            
            logger.info(f"Bitcoin price analysis report saved to {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Error creating Bitcoin price analysis report: {e}")
            return None
    
    def start_scheduled_bitcoin_price_analysis(self, 
                                          interval_minutes: Optional[int] = None, 
                                          callback: Optional[Callable[[AnalysisResult], None]] = None):
        """
        Start scheduled Bitcoin price analysis at regular intervals.
        
        Args:
            interval_minutes: Interval between analyses in minutes (default: from config)
            callback: Optional callback function to call with analysis results
        """
        if not hasattr(self, "bitcoin_price_analyzer"):
            logger.error("Bitcoin price analysis is not enabled")
            raise ValueError("Bitcoin price analysis is not enabled in the configuration")
        
        # Use config interval if not specified
        if interval_minutes is None:
            interval_minutes = self.config.bitcoin_price_analysis_interval_minutes
        
        import threading
        import time
        
        # Create a stop event for the thread
        stop_event = threading.Event()
        self._bitcoin_price_scheduler = stop_event
        
        def analysis_worker():
            """Worker function for the analysis thread."""
            logger.info(f"Starting scheduled Bitcoin price analysis every {interval_minutes} minutes")
            
            while not stop_event.is_set():
                try:
                    # Run the analysis
                    result = self.analyze_bitcoin_price(save_result=True)
                    
                    # Call the callback if provided
                    if callback:
                        try:
                            callback(result)
                        except Exception as cb_error:
                            logger.error(f"Error in Bitcoin price analysis callback: {cb_error}")
                    
                    logger.debug(f"Completed scheduled Bitcoin price analysis. Next run in {interval_minutes} minutes.")
                    
                except Exception as e:
                    logger.error(f"Error in scheduled Bitcoin price analysis: {e}")
                
                # Wait for the next interval or until stopped
                stop_event.wait(interval_minutes * 60)
        
        # Start the analysis worker thread
        analysis_thread = threading.Thread(target=analysis_worker, daemon=True)
        analysis_thread.start()
        
        logger.info(f"Scheduled Bitcoin price analysis started with interval of {interval_minutes} minutes")
        
        return stop_event
    
    def stop_scheduled_bitcoin_price_analysis(self):
        """Stop the scheduled Bitcoin price analysis."""
        if self._bitcoin_price_scheduler:
            logger.info("Stopping scheduled Bitcoin price analysis")
            self._bitcoin_price_scheduler.set()
            self._bitcoin_price_scheduler = None
        else:
            logger.info("No scheduled Bitcoin price analysis running")

    def analyze_coincap_asset(self, asset_id: str = "bitcoin", save_result: bool = True, generate_charts: bool = True) -> AnalysisResult:
        """
        Analyze cryptocurrency data from CoinCap API.

        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            save_result: Whether to save the analysis results
            generate_charts: Whether to generate price charts (should be False in background threads)

        Returns:
            AnalysisResult object with analysis results
        """
        if not self.config.enable_coincap_analysis:
            logger.warning("CoinCap analysis is disabled in configuration")
            raise ValueError("CoinCap analysis is disabled in configuration")

        if not self.coincap_client or not self.coincap_analyzer:
            logger.error("CoinCap components not initialized")
            raise ValueError("CoinCap components not initialized")

        logger.info(f"Analyzing cryptocurrency data for {asset_id} with CoinCap API")

        # Monitor performance
        if self.config.enable_performance_monitoring:
            @self._performance_monitor.monitor(component=PerfComponentType.ANALYSIS)
            def run_coincap_analysis():
                # Run CoinCap analysis
                metrics = self.coincap_analyzer.analyze_asset(
                    asset_id=asset_id, 
                    save_result=False
                )
                
                # Interpret market signals
                signals = self.coincap_analyzer.interpret_market_signals(metrics)
                
                # Generate chart if requested
                chart_path = None
                if generate_charts:
                    chart_path = self.coincap_analyzer.generate_price_chart(
                        asset_id=asset_id,
                        days=90
                    )
                
                return metrics, signals, chart_path
                
            metrics, signals, chart_path = run_coincap_analysis()
        else:
            # Run without performance monitoring
            metrics = self.coincap_analyzer.analyze_asset(
                asset_id=asset_id, 
                save_result=False
            )
            
            # Interpret market signals
            signals = self.coincap_analyzer.interpret_market_signals(metrics)
            
            # Generate chart if requested
            chart_path = None
            if generate_charts:
                chart_path = self.coincap_analyzer.generate_price_chart(
                    asset_id=asset_id,
                    days=90
                )

        # Create analysis result
        result = AnalysisResult(
            symbol=metrics.symbol,
            timestamp=metrics.timestamp,
            component_type=ComponentType.COINCAP_MARKET_ANALYSIS,
            risk_metrics={
                "volatility_7d": metrics.volatility_7d,
                "volatility_30d": metrics.volatility_30d,
                "market_sentiment": metrics.market_sentiment,
                "price_position": metrics.price_position,
                "trend_strength": metrics.trend_strength,
                "volume_to_market_cap": metrics.volume_to_market_cap
            },
            predictions={
                "price_trend_24h": signals["price_trend_24h"],
                "price_trend_30d": signals["price_trend_30d"],
                "moving_average_signal": signals["moving_average_signal"],
                "overall_sentiment": signals["overall_signal"],
                "overall_score": signals["overall_score"],
                "interpretation": signals["interpretation"]
            },
            visualizations={} if chart_path is None else {"price_chart": chart_path},
            raw_data={
                "symbol": metrics.symbol,
                "name": metrics.name,
                "current_price": metrics.current_price,
                "market_cap": metrics.market_cap,
                "volume_24h": metrics.volume_24h,
                "supply": metrics.supply,
                "price_change_24h": metrics.price_change_24h,
                "price_change_7d": metrics.price_change_7d,
                "price_change_30d": metrics.price_change_30d,
                "market_cap_rank": metrics.market_cap_rank,
                "market_dominance": metrics.market_dominance
            }
        )

        # Save the analysis result if requested
        if save_result:
            # Create report file
            report_path = self._create_coincap_analysis_report(result, asset_id)
            result.visualizations["report"] = report_path

        logger.info(f"CoinCap analysis for {asset_id} completed")
        return result

    def _create_coincap_analysis_report(self, result: AnalysisResult, asset_id: str) -> str:
        """
        Create a detailed report from CoinCap analysis results.
        
        Args:
            result: AnalysisResult object
            asset_id: Asset identifier
            
        Returns:
            Path to the generated report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{asset_id}_coincap_analysis_{timestamp}.md"
        file_path = os.path.join(self.config.save_path, "coincap_analysis", filename)
        
        # Format data for the report
        asset_name = result.raw_data["name"]
        symbol = result.raw_data["symbol"]
        current_price = result.raw_data["current_price"]
        market_cap = result.raw_data["market_cap"]
        volume_24h = result.raw_data["volume_24h"]
        price_change_24h = result.raw_data["price_change_24h"]
        price_change_7d = result.raw_data["price_change_7d"]
        price_change_30d = result.raw_data["price_change_30d"]
        market_cap_rank = result.raw_data["market_cap_rank"]
        volatility_7d = result.risk_metrics["volatility_7d"]
        volatility_30d = result.risk_metrics["volatility_30d"]
        market_sentiment = result.risk_metrics["market_sentiment"]
        
        report_content = f"""# {asset_name} ({symbol}) Market Analysis

## Analysis Timestamp: {result.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

## Key Metrics

- **Current Price:** ${current_price:,.2f}
- **Market Cap:** ${market_cap:,.0f}
- **24h Trading Volume:** ${volume_24h:,.0f}
- **Market Cap Rank:** #{market_cap_rank}

## Price Changes

- **24h Change:** {price_change_24h:+.2f}%
- **7d Change:** {price_change_7d:+.2f}%
- **30d Change:** {price_change_30d:+.2f}%

## Risk Analysis

- **7-Day Volatility:** {volatility_7d:.2f}%
- **30-Day Volatility:** {volatility_30d:.2f}%
- **Market Sentiment:** {market_sentiment:.2f} (-1 to +1 scale)

## Market Interpretation

{result.predictions["interpretation"]}

## Signals Summary

- **Short-term Trend (24h):** {result.predictions["price_trend_24h"]}
- **Medium-term Trend (30d):** {result.predictions["price_trend_30d"]}
- **Moving Average Signal:** {result.predictions["moving_average_signal"]}
- **Overall Market Sentiment:** {result.predictions["overall_sentiment"]}

## Price Chart

![{asset_name} Price Chart]({os.path.basename(result.visualizations["price_chart"])})

---
*Analysis performed by Quantum Financial API using CoinCap data*
*Timestamp: {result.timestamp.strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        # Save the report
        with open(file_path, 'w') as f:
            f.write(report_content)
            
        logger.info(f"CoinCap analysis report saved to {file_path}")
        return file_path

    def analyze_coincap_assets(self, assets: Optional[List[str]] = None, save_results: bool = True, generate_charts: bool = True) -> Dict[str, AnalysisResult]:
        """
        Analyze multiple cryptocurrency assets from CoinCap API.

        Args:
            assets: List of asset identifiers (defaults to config.coincap_default_assets)
            save_results: Whether to save the analysis results
            generate_charts: Whether to generate price charts (should be False in background threads)

        Returns:
            Dictionary mapping asset IDs to AnalysisResult objects
        """
        if not self.config.enable_coincap_analysis:
            logger.warning("CoinCap analysis is disabled in configuration")
            raise ValueError("CoinCap analysis is disabled in configuration")

        # Use default assets if none provided
        assets = assets or self.config.coincap_default_assets
        logger.info(f"Analyzing {len(assets)} cryptocurrency assets")

        results = {}
        for asset_id in assets:
            try:
                # Pass the generate_charts parameter to analyze_coincap_asset
                result = self.analyze_coincap_asset(
                    asset_id=asset_id, 
                    save_result=save_results,
                    generate_charts=generate_charts
                )
                results[asset_id] = result
            except Exception as e:
                logger.error(f"Error analyzing asset {asset_id}: {e}")
                # Continue with the next asset

        logger.info(f"Completed analysis of {len(results)} assets")
        return results

    def start_scheduled_coincap_analysis(self, 
                                      interval_minutes: Optional[int] = None, 
                                      assets: Optional[List[str]] = None,
                                      callback: Optional[Callable[[Dict[str, AnalysisResult]], None]] = None):
        """
        Start scheduled analysis of cryptocurrency assets.
        
        Args:
            interval_minutes: Interval between analyses in minutes
                             (defaults to config.coincap_analysis_interval_minutes)
            assets: List of asset identifiers to analyze
                   (defaults to config.coincap_default_assets)
            callback: Optional callback function to be called with analysis results
        
        Returns:
            None
        """
        if not self.config.enable_coincap_analysis:
            logger.warning("CoinCap analysis is disabled in configuration")
            raise ValueError("CoinCap analysis is disabled in configuration")
        
        # Use default interval if none provided
        interval_minutes = interval_minutes or self.config.coincap_analysis_interval_minutes
        
        # Use default assets if none provided
        assets = assets or self.config.coincap_default_assets
        
        # Stop existing thread if running
        if self._coincap_analysis_thread is not None and self._coincap_analysis_thread.is_alive():
            logger.info("Stopping existing scheduled CoinCap analysis")
            self._stop_coincap_analysis = True
            self._coincap_analysis_thread.join(timeout=5)
        
        logger.info(f"Starting scheduled CoinCap analysis for {len(assets)} assets "
                    f"every {interval_minutes} minutes")
        
        self._stop_coincap_analysis = False
        
        def analysis_worker():
            while not self._stop_coincap_analysis:
                try:
                    logger.info(f"Running scheduled CoinCap analysis for {len(assets)} assets")
                    # Disable chart generation in the background thread to avoid matplotlib issues
                    results = self.analyze_coincap_assets(assets=assets, save_results=True, generate_charts=False)
                    
                    # Call callback if provided
                    if callback is not None:
                        try:
                            callback(results)
                        except Exception as e:
                            logger.error(f"Error in CoinCap analysis callback: {e}")
                    
                    # Sleep until next analysis
                    logger.info(f"Waiting {interval_minutes} minutes until next CoinCap analysis")
                    
                    # Check for stop signal periodically
                    for _ in range(interval_minutes * 60 // 10):
                        if self._stop_coincap_analysis:
                            break
                        time.sleep(10)
                        
                except Exception as e:
                    logger.error(f"Error in scheduled CoinCap analysis: {e}")
                    # Sleep shorter time before retry
                    time.sleep(60)
        
        self._coincap_analysis_thread = threading.Thread(target=analysis_worker)
        self._coincap_analysis_thread.daemon = True
        self._coincap_analysis_thread.start()
        
        logger.info("Scheduled CoinCap analysis started")
    
    def stop_scheduled_coincap_analysis(self):
        """
        Stop scheduled CoinCap analysis.
        
        Returns:
            None
        """
        if not self._coincap_analysis_thread or not self._coincap_analysis_thread.is_alive():
            logger.info("No scheduled CoinCap analysis running")
            return
        
        logger.info("Stopping scheduled CoinCap analysis")
        self._stop_coincap_analysis = True
        self._coincap_analysis_thread.join(timeout=5)
        logger.info("Scheduled CoinCap analysis stopped")

# Example usage function
def example_usage():
    """Example usage of the Quantum Financial API."""
    api = QuantumFinancialAPI()
    
    # Create some sample market data
    market_data = MarketData(
        symbol="BTC-USD",
        timestamp=datetime.now(),
        price=50000.0,
        order_book_imbalance=0.2,
        volatility=0.05,
        order_book_depth=10.0,
        liquidity=0.8
    )
    
    # Run analysis with all components
    results = api.analyze_market_data(market_data)
    
    # Save results
    api.save_analysis_results(results)
    
    # Create ensemble prediction
    ensemble = api.create_ensemble_prediction(results)
    print(f"Ensemble prediction: {ensemble}")
    
    # Run mempool analysis
    mempool_result = api.analyze_mempool()
    print(f"Mempool analysis: {mempool_result.risk_metrics}")
    
    # Run Bitcoin price analysis
    bitcoin_result = api.analyze_bitcoin_price()
    print(f"Bitcoin price analysis: {bitcoin_result.risk_metrics}")
    
    # Run CoinCap market analysis
    coincap_result = api.analyze_coincap_asset("ethereum")
    print(f"Ethereum market analysis: {coincap_result.risk_metrics}")
    
    # Clean up
    api.cleanup()
    

if __name__ == "__main__":
    example_usage() 