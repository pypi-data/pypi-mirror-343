#!/usr/bin/env python3

"""
Data Fetcher Module for Quantum Risk Assessment

This module handles the retrieval of cryptocurrency market data from various sources,
with a focus on Binance API data for market microstructure analysis.

It provides a unified interface for retrieving order book data, 24-hour statistics,
and recent trades, with fallback mechanisms for different data sources.

Author: Quantum-AI Team
"""

import os
# Use relative import for utilities within the same package
from .utils.logging_util import setup_logger
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = setup_logger(__name__)

class CryptoDataFetcher:
    """
    Cryptocurrency data fetcher component that handles retrieving market data
    from various sources with appropriate fallback mechanisms.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the cryptocurrency data fetcher.
        
        Args:
            api_key: Optional RapidAPI key for Binance API access
        """
        self.api_key = api_key or os.environ.get("RAPIDAPI_KEY")
        if not self.api_key:
            logger.error("No RapidAPI key provided. API functionality requires a valid key.")
            raise ValueError("RapidAPI key is required for fetching cryptocurrency data. Please set the RAPIDAPI_KEY environment variable or provide it as an argument.")
        
        self._fetcher = self._initialize_fetcher()
    
    def _initialize_fetcher(self):
        """Initialize and return the appropriate data fetcher based on availability"""
        try:
            # First try to import the enhanced crypto data fetcher if available
            from examples.crypto_data_fetcher_enhanced import EnhancedCryptoDataFetcher  # type: ignore
            fetcher = EnhancedCryptoDataFetcher(api_key=self.api_key)  # type: ignore
            logger.info("Using EnhancedCryptoDataFetcher")
            return fetcher
        except ImportError:
            try:
                # Fall back to the basic crypto data fetcher
                from examples.crypto_data_fetcher import CryptoDataFetcher as BasicCryptoDataFetcher  # type: ignore
                fetcher = BasicCryptoDataFetcher(api_key=self.api_key)  # type: ignore
                logger.info("Using basic CryptoDataFetcher")
                return fetcher
            except ImportError:
                # If neither is available, raise an error
                error_msg = "No crypto data fetcher available. Please ensure either examples.crypto_data_fetcher or examples.crypto_data_fetcher_enhanced is in your PYTHONPATH."
                logger.error(error_msg)
                raise ImportError(error_msg)
    
    def get_binance_order_book(self, symbol: str) -> Dict[str, Any]:
        """
        Get order book data for a cryptocurrency from Binance API.
        
        Args:
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            
        Returns:
            Order book data with bids and asks
        """
        return self._fetcher.get_binance_order_book(symbol)  # type: ignore[attr-defined]
    
    def get_binance_24hr_stats(self, symbol: str) -> Dict[str, Any]:
        """
        Get 24-hour statistics for a cryptocurrency from Binance API.
        
        Args:
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            
        Returns:
            24-hour statistics
        """
        return self._fetcher.get_binance_24hr_stats(symbol)  # type: ignore[attr-defined]
    
    def get_recent_trades(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get recent trades for a cryptocurrency from Binance API.
        
        Args:
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            limit: Number of trades to retrieve (default: 100)
            
        Returns:
            Recent trades data
        """
        if hasattr(self._fetcher, 'get_binance_recent_trades'):
            return self._fetcher.get_binance_recent_trades(symbol, limit)  # type: ignore[attr-defined]
        else:
            error_msg = f"Recent trades functionality not available for {symbol}. The underlying fetcher does not support this method."
            logger.error(error_msg)
            raise NotImplementedError(error_msg)
    
    def get_historical_prices(self, symbol: str, days: int = 90, end_date=None) -> Dict[str, Any]:
        """
        Get historical daily prices for a cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol (e.g. 'BTC', 'ETH')
            days: Number of days of historical data to fetch
            end_date: Optional end date for the data
            
        Returns:
            Historical price data with dates and prices
        """
        if hasattr(self._fetcher, 'get_historical_prices'):
            if hasattr(self._fetcher.get_historical_prices, '__code__') and 'end_date' in self._fetcher.get_historical_prices.__code__.co_varnames:
                return self._fetcher.get_historical_prices(symbol, days, end_date=end_date)  # type: ignore[attr-defined]
            else:
                logger.warning("End date parameter not supported by fetcher, using default end date")
                return self._fetcher.get_historical_prices(symbol, days)  # type: ignore[attr-defined]
        else:
            error_msg = f"Historical prices functionality not available for {symbol}. The underlying fetcher does not support this method."
            logger.error(error_msg)
            raise NotImplementedError(error_msg) 