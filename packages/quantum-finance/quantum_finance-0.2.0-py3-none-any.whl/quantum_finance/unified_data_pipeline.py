#!/usr/bin/env python3

"""
Unified Data Pipeline for Quantum Financial System

This module provides a standardized interface for accessing cryptocurrency market data
from multiple sources including CoinDesk, Binance, and Mempool. It implements caching,
error handling, and unified data formatting to support quantum financial analysis.

Features:
- Integration with multiple cryptocurrency data sources
- Configurable data caching to reduce API calls
- Standardized data format for quantum processing
- Parallel data fetching for improved performance
- Comprehensive error handling and logging

Author: Quantum-AI Team
"""

import os
import json
import time
import logging
import threading
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import pandas as pd
from functools import lru_cache
from dotenv import load_dotenv
import pytz

# Import local API client modules using absolute paths
from src.quantum_finance.api_clients.coindesk_client import CoinDeskClient
from src.quantum_finance.api_clients.coincap_client import CoinCapClient
from src.quantum_finance.api_clients.mempool_client import MempoolClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarketDataCache:
    """Cache system for market data to prevent redundant API calls."""
    
    def __init__(self, cache_dir: str = ".cache", expiry_seconds: int = 300):
        """
        Initialize the market data cache.
        
        Args:
            cache_dir: Directory to store cache files
            expiry_seconds: Cache expiry time in seconds (default 5 minutes)
        """
        self.cache_dir = cache_dir
        self.expiry_seconds = expiry_seconds
        self.memory_cache = {}
        self.cache_lock = threading.Lock()
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        """Get the file path for a cache key."""
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, key: str) -> Optional[Dict]:
        """
        Get data from cache if available and not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached data or None if not found or expired
        """
        # First check memory cache
        with self.cache_lock:
            if key in self.memory_cache:
                cache_entry = self.memory_cache[key]
                if time.time() - cache_entry['timestamp'] < self.expiry_seconds:
                    logger.debug(f"Memory cache hit for {key}")
                    return cache_entry['data']
                else:
                    # Expired, remove from memory cache
                    del self.memory_cache[key]
        
        # Then check file cache
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    cache_entry = json.load(f)
                
                if time.time() - cache_entry['timestamp'] < self.expiry_seconds:
                    # Update memory cache
                    with self.cache_lock:
                        self.memory_cache[key] = cache_entry
                    logger.debug(f"Disk cache hit for {key}")
                    return cache_entry['data']
            except Exception as e:
                logger.warning(f"Error reading cache for {key}: {e}")
        
        return None
    
    def set(self, key: str, data: Dict) -> None:
        """
        Save data to cache.
        
        Args:
            key: Cache key
            data: Data to cache
        """
        cache_entry = {
            'timestamp': time.time(),
            'data': data
        }
        
        # Update memory cache
        with self.cache_lock:
            self.memory_cache[key] = cache_entry
        
        # Update file cache
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_entry, f)
            logger.debug(f"Cached data for {key}")
        except Exception as e:
            logger.warning(f"Error writing cache for {key}: {e}")
    
    def clear(self, key: Optional[str] = None) -> None:
        """
        Clear cache entries.
        
        Args:
            key: Specific key to clear, or None to clear all
        """
        with self.cache_lock:
            if key is None:
                # Clear all cache
                self.memory_cache = {}
                for file in os.listdir(self.cache_dir):
                    if file.endswith('.json'):
                        try:
                            os.remove(os.path.join(self.cache_dir, file))
                        except Exception as e:
                            logger.warning(f"Error removing cache file {file}: {e}")
            else:
                # Clear specific key
                if key in self.memory_cache:
                    del self.memory_cache[key]
                
                cache_path = self._get_cache_path(key)
                if os.path.exists(cache_path):
                    try:
                        os.remove(cache_path)
                    except Exception as e:
                        logger.warning(f"Error removing cache file for {key}: {e}")

class UnifiedDataPipeline:
    """
    Unified data pipeline for accessing cryptocurrency market data from multiple sources.
    """
    
    def __init__(self, api_key: Optional[str] = None, use_cache: bool = True, cache_expiry: int = 300):
        """
        Initialize the unified data pipeline.
        
        Args:
            api_key: API key for sources that require authentication
            use_cache: Whether to use caching (default: True)
            cache_expiry: Cache expiry time in seconds (default: 5 minutes)
        """
        # Initialize data sources
        self.coindesk_client = CoinDeskClient()
        self.coincap_client = CoinCapClient()
        
        if api_key:
            # Note: BinanceClient is not currently available
            # self.binance_client = BinanceClient(api_key=api_key)
            self.binance_client = None
            logger.warning("Binance client is not currently available.")
        else:
            self.binance_client = None
            logger.warning("No API key provided. Binance client will not be available.")
        
        self.mempool_client = MempoolClient()
        
        # Initialize cache if enabled
        self.use_cache = use_cache
        if use_cache:
            self.cache = MarketDataCache(expiry_seconds=cache_expiry)
        else:
            self.cache = None
        
        self.data_handlers = {
            'coindesk': self._fetch_coindesk_data,
            'coincap': self._fetch_coincap_data,
            'binance': self._fetch_binance_data,
            'mempool': self._fetch_mempool_data
        }
    
    def _fetch_coindesk_data(self, symbol: str, **kwargs) -> Dict:
        """Fetch data from CoinDesk API."""
        if symbol.upper() != 'BTC':
            logger.warning("CoinDesk only supports BTC. Ignoring requested symbol.")
            symbol = 'BTC'
        
        # Get historical data if dates provided
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        days = kwargs.get('days', 30)
        
        try:
            # Current price
            current_price = self.coindesk_client.get_current_price()
            
            # Historical prices
            if start_date and end_date:
                historical_df = self.coindesk_client.get_historical_prices_as_dataframe(
                    start_date=start_date,
                    end_date=end_date
                )
            else:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                historical_df = self.coindesk_client.get_historical_prices_as_dataframe(
                    start_date=start_date,
                    end_date=end_date
                )
            
            return {
                'source': 'coindesk',
                'current_price': current_price,
                'historical_prices': historical_df.to_dict('records'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching CoinDesk data: {e}")
            return {
                'source': 'coindesk',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _fetch_binance_data(self, symbol: str, **kwargs) -> Dict:
        """Fetch data from Binance API."""
        if not self.binance_client:
            logger.error("Binance client not initialized. API key required.")
            return {
                'source': 'binance',
                'error': 'Binance client not initialized. API key required.',
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Get market data
            market_data = self.binance_client.get_market_data(symbol)
            
            # Get order book if requested
            order_book = None
            if kwargs.get('include_order_book', True):
                order_book = self.binance_client.get_order_book(symbol)
            
            # Get recent trades if requested
            recent_trades = None
            if kwargs.get('include_trades', True):
                recent_trades = self.binance_client.get_recent_trades(symbol)
            
            return {
                'source': 'binance',
                'market_data': market_data,
                'order_book': order_book,
                'recent_trades': recent_trades,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching Binance data: {e}")
            return {
                'source': 'binance',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _fetch_mempool_data(self, symbol: str, **kwargs) -> Dict:
        """Fetch data from Mempool.space API."""
        try:
            # Get current block info
            block_info = self.mempool_client.get_blocks()
            
            # Get mempool stats
            mempool_stats = self.mempool_client.get_mempool_stats()
            
            # Get fee estimates
            fee_estimates = self.mempool_client.get_fees_recommended()
            
            return {
                'source': 'mempool',
                'block_info': block_info,
                'mempool_stats': mempool_stats,
                'fee_estimates': fee_estimates,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching Mempool data: {e}")
            return {
                'source': 'mempool',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _fetch_coincap_data(self, symbol: str, **kwargs) -> Dict:
        """Fetch data from CoinCap API."""
        try:
            # Convert ticker symbols to asset IDs
            asset_id_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'SOL': 'solana',
                'ADA': 'cardano',
                'DOT': 'polkadot',
                'XRP': 'xrp',
                'DOGE': 'dogecoin',
                'AVAX': 'avalanche',
                'MATIC': 'polygon',
                'LINK': 'chainlink'
            }
            
            # Convert symbol to asset_id
            asset_id = asset_id_map.get(symbol.upper(), symbol.lower())
            
            # Get current asset data
            asset_data = self.coincap_client.get_asset(asset_id)
            
            # Get historical data if requested
            historical_data = None
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            days = kwargs.get('days', 30)
            
            if kwargs.get('historical', False) or kwargs.get('history', False):
                if start_date and end_date:
                    # Convert string dates to datetime objects
                    if isinstance(start_date, str):
                        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                    else:
                        start_dt = start_date
                        
                    if isinstance(end_date, str):
                        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                    else:
                        end_dt = end_date
                        
                    historical_data = self.coincap_client.get_asset_history(
                        asset_id, 
                        start=start_dt, 
                        end=end_dt
                    )
                else:
                    # If start/end times are provided as timestamps
                    start = kwargs.get('start')
                    end = kwargs.get('end')
                    interval = kwargs.get('interval', 'd1')
                    
                    if start and end:
                        historical_data = self.coincap_client.get_asset_history(
                            asset_id,
                            interval=interval,
                            start=start,
                            end=end
                        )
                    else:
                        end_dt = datetime.now()
                        start_dt = end_dt - timedelta(days=days)
                        historical_data = self.coincap_client.get_asset_history(
                            asset_id, 
                            start=start_dt, 
                            end=end_dt
                        )
            
            # Extract and structure the data properly
            result = {
                'source': 'coincap',
                'timestamp': datetime.now().isoformat(),
                'data': None,
                'error': None
            }
            
            # Handle asset data
            if asset_data and 'data' in asset_data:
                result['data'] = asset_data['data']
            else:
                logger.warning(f"Unexpected asset data structure from CoinCap API for {symbol}")
                result['error'] = "Invalid asset data structure"
                
            # Handle historical data
            if historical_data:
                if 'data' in historical_data:
                    result['historical_data'] = historical_data['data']
                else:
                    logger.warning(f"Unexpected historical data structure from CoinCap API for {symbol}")
                    result['error'] = "Invalid historical data structure"
            
            return result
            
        except Exception as e:
            logger.error(f"Error fetching CoinCap data for {symbol}: {e}")
            return {
                'source': 'coincap',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'data': None
            }
    
    def _get_cached_data(self, source: str, symbol: str, **kwargs) -> Optional[Dict]:
        """Try to get data from cache."""
        if not self.use_cache or not self.cache:
            return None
        
        # Generate cache key based on source, symbol and relevant kwargs
        cache_key = f"{source}_{symbol}"
        
        # Add relevant kwargs to cache key
        if source == 'coindesk':
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            days = kwargs.get('days', 30)
            
            if start_date and end_date:
                # Handle both datetime and string date formats
                if isinstance(start_date, datetime):
                    start_str = start_date.strftime('%Y%m%d')
                else:
                    start_str = start_date.replace('-', '')
                
                if isinstance(end_date, datetime):
                    end_str = end_date.strftime('%Y%m%d')
                else:
                    end_str = end_date.replace('-', '')
                
                cache_key += f"_{start_str}_{end_str}"
            else:
                cache_key += f"_{days}days"
        
        elif source == 'binance':
            for param in ['include_order_book', 'include_trades']:
                if param in kwargs:
                    cache_key += f"_{param}_{kwargs[param]}"
        
        elif source == 'mempool':
            for param in ['include_tx_volume', 'include_fees']:
                if param in kwargs:
                    cache_key += f"_{param}_{kwargs[param]}"
        
        return self.cache.get(cache_key)
    
    def _cache_data(self, source: str, symbol: str, data: Dict, **kwargs) -> None:
        """Cache data for future use."""
        if not self.use_cache or not self.cache:
            return
        
        # Generate cache key based on source, symbol and relevant kwargs
        cache_key = f"{source}_{symbol}"
        
        # Add relevant kwargs to cache key
        if source == 'coindesk':
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')
            days = kwargs.get('days', 30)
            
            if start_date and end_date:
                # Handle both datetime and string date formats
                if isinstance(start_date, datetime):
                    start_str = start_date.strftime('%Y%m%d')
                else:
                    start_str = start_date.replace('-', '')
                
                if isinstance(end_date, datetime):
                    end_str = end_date.strftime('%Y%m%d')
                else:
                    end_str = end_date.replace('-', '')
                
                cache_key += f"_{start_str}_{end_str}"
            else:
                cache_key += f"_{days}days"
        
        elif source == 'binance':
            for param in ['include_order_book', 'include_trades']:
                if param in kwargs:
                    cache_key += f"_{param}_{kwargs[param]}"
        
        elif source == 'mempool':
            for param in ['include_tx_volume', 'include_fees']:
                if param in kwargs:
                    cache_key += f"_{param}_{kwargs[param]}"
        
        self.cache.set(cache_key, data)
    
    def get_market_data(self, symbol: str, sources: List[str] = [], **kwargs) -> Dict[str, Any]:
        """
        Get market data from specified sources for a symbol.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            sources: List of data sources to query, or None for all available
            **kwargs: Additional parameters for specific data sources
            
        Returns:
            Dictionary containing data from all requested sources
        """
        if sources is None:
            sources = list(self.data_handlers.keys())
        
        results = {}
        
        # Process each requested source
        for source in sources:
            if source not in self.data_handlers:
                logger.warning(f"Unknown data source: {source}")
                continue
            
            # Try to get from cache first
            cached_data = self._get_cached_data(source, symbol, **kwargs)
            if cached_data is not None:
                results[source] = cached_data
                logger.info(f"Using cached data for {source}_{symbol}")
                continue
            
            # Fetch fresh data
            logger.info(f"Fetching fresh data for {source}_{symbol}")
            data = self.data_handlers[source](symbol, **kwargs)
            results[source] = data
            
            # Cache the fresh data
            self._cache_data(source, symbol, data, **kwargs)
        
        # Add unified timestamp
        results['timestamp'] = datetime.now().isoformat()
        results['symbol'] = symbol
        
        return results
    
    def get_data_as_dataframe(self, symbol: str, sources: List[str] = [], **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Get market data as pandas DataFrames for easier analysis.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            sources: List of data sources to query, or None for all available
            **kwargs: Additional parameters for specific data sources
            
        Returns:
            Dictionary mapping source names to pandas DataFrames
        """
        raw_data = self.get_market_data(symbol, sources, **kwargs)
        dataframes = {}
        
        # Convert each source's data to appropriate DataFrame format
        for source, data in raw_data.items():
            if source in ['timestamp', 'symbol']:
                continue
                
            if source == 'coindesk':
                if 'historical_prices' in data and data['historical_prices']:
                    dataframes[f'{source}_historical'] = pd.DataFrame(data['historical_prices'])
                
            elif source == 'binance':
                if 'market_data' in data and data['market_data']:
                    dataframes[f'{source}_market'] = pd.DataFrame([data['market_data']])
                
                if 'order_book' in data and data['order_book']:
                    bids_df = pd.DataFrame(data['order_book'].get('bids', []), columns=['price', 'quantity'])
                    bids_df['side'] = 'bid'
                    
                    asks_df = pd.DataFrame(data['order_book'].get('asks', []), columns=['price', 'quantity'])
                    asks_df['side'] = 'ask'
                    
                    dataframes[f'{source}_orderbook'] = pd.concat([bids_df, asks_df])
                
                if 'recent_trades' in data and data['recent_trades']:
                    dataframes[f'{source}_trades'] = pd.DataFrame(data['recent_trades'])
            
            elif source == 'mempool':
                if 'mempool_info' in data and data['mempool_info']:
                    dataframes[f'{source}_info'] = pd.DataFrame([data['mempool_info']])
                
                if 'transaction_volume' in data and data['transaction_volume']:
                    dataframes[f'{source}_volume'] = pd.DataFrame(data['transaction_volume'])
                
                if 'fee_estimates' in data and data['fee_estimates']:
                    dataframes[f'{source}_fees'] = pd.DataFrame([data['fee_estimates']])
        
        return dataframes
    
    def get_current_prices(self, symbols: List[str], prioritize_source: str = 'binance') -> Dict[str, float]:
        """
        Get current prices for multiple symbols.
        
        Args:
            symbols: List of cryptocurrency symbols
            prioritize_source: Preferred data source for prices
            
        Returns:
            Dictionary mapping symbols to current prices
        """
        prices = {}
        sources = ['binance', 'coindesk']
        
        # Reorder sources to prioritize the preferred one
        if prioritize_source in sources:
            sources.remove(prioritize_source)
            sources.insert(0, prioritize_source)
        
        # Get prices for each symbol
        for symbol in symbols:
            for source in sources:
                try:
                    data = self.get_market_data(symbol, sources=[source])
                    
                    if source == 'binance' and source in data:
                        if 'market_data' in data[source] and 'lastPrice' in data[source]['market_data']:
                            prices[symbol] = float(data[source]['market_data']['lastPrice'])
                            break
                    
                    elif source == 'coindesk' and source in data:
                        if 'current_price' in data[source] and 'bpi' in data[source]['current_price']:
                            # CoinDesk only supports BTC
                            if symbol.upper() == 'BTC':
                                prices[symbol] = float(data[source]['current_price']['bpi']['USD']['rate_float'])
                                break
                
                except Exception as e:
                    logger.warning(f"Error getting price for {symbol} from {source}: {e}")
        
        return prices
    
    def clear_cache(self, source: Optional[str] = None, symbol: Optional[str] = None) -> None:
        """
        Clear cache entries.
        
        Args:
            source: Specific source to clear, or None for all sources
            symbol: Specific symbol to clear, or None for all symbols
        """
        if not self.use_cache or not self.cache:
            return
        
        if source is None and symbol is None:
            # Clear all cache
            self.cache.clear()
            logger.info("Cleared all cache entries")
        
        elif source is not None and symbol is None:
            # Clear all entries for a specific source
            self.cache.clear(f"{source}_")
            logger.info(f"Cleared cache entries for source {source}")
        
        elif source is None and symbol is not None:
            # Clear all entries for a specific symbol
            for src in self.data_handlers.keys():
                self.cache.clear(f"{src}_{symbol}")
            logger.info(f"Cleared cache entries for symbol {symbol}")
        
        else:
            # Clear specific source and symbol
            self.cache.clear(f"{source}_{symbol}")
            logger.info(f"Cleared cache entry for {source}_{symbol}")


# Example usage
if __name__ == "__main__":
    # Load environment variables if needed (e.g., for API keys)
    load_dotenv()
    API_KEY = os.getenv("BINANCE_API_KEY")  # Example of using env var
    
    # Create unified data pipeline
    pipeline = UnifiedDataPipeline(api_key=API_KEY)
    
    # Get BTC data from all sources
    btc_data = pipeline.get_market_data("BTC")
    print(f"Retrieved data for BTC from {len(btc_data)-2} sources")
    
    # Get current prices for multiple symbols
    symbols = ["BTC", "ETH", "SOL"]
    prices = pipeline.get_current_prices(symbols)
    print("Current prices:")
    for symbol, price in prices.items():
        print(f"  {symbol}: ${price:,.2f}")
    
    # Get data as DataFrames
    btc_dfs = pipeline.get_data_as_dataframe("BTC")
    print(f"Created {len(btc_dfs)} DataFrames for BTC data")
    for name, df in btc_dfs.items():
        print(f"  {name}: {len(df)} rows") 