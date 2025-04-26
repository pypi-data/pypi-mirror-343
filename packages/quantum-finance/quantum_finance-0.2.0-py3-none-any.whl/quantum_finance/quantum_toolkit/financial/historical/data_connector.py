"""
Market Data Connector

This module provides connectors to fetch real market data from various sources.
Currently supports Alpha Vantage as the primary data source.
"""

import os
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import requests
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class MarketDataConnector:
    """
    Real market data connector using Alpha Vantage API.
    
    This class handles fetching and caching of market data from Alpha Vantage,
    providing both historical and real-time data access.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the market data connector.
        
        Args:
            api_key: Alpha Vantage API key (optional, can be set via env var)
        """
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Alpha Vantage API key must be provided either directly "
                "or via ALPHA_VANTAGE_API_KEY environment variable"
            )
            
        self.base_url = 'https://www.alphavantage.co/query'
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = 3600  # 1 hour cache TTL
        self._last_request_time: Dict[str, datetime] = {}
        
    def get_daily_data(self,
                      symbol: str,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get daily historical data for a symbol.
        
        Args:
            symbol: Asset symbol
            start_date: Start date (optional)
            end_date: End date (optional)
            
        Returns:
            DataFrame with daily price data
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',
            'apikey': self.api_key
        }
        
        # Check cache first
        cache_key = f"daily_{symbol}"
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            cache_time = cached_data['timestamp']
            if (datetime.now() - cache_time).total_seconds() < self._cache_ttl:
                df = cached_data['data']
                return self._filter_date_range(df, start_date, end_date)
        
        # Fetch new data
        response = self._make_request(params)
        
        # Parse response
        time_series = response.get('Time Series (Daily)', {})
        data = []
        for date_str, values in time_series.items():
            row = {
                'date': pd.to_datetime(date_str),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            }
            data.append(row)
            
        # Create DataFrame
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        
        # Cache the data
        self._cache[cache_key] = {
            'timestamp': datetime.now(),
            'data': df
        }
        
        return self._filter_date_range(df, start_date, end_date)
    
    def get_intraday_data(self,
                         symbol: str,
                         interval: str = '5min',
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get intraday data for a symbol.
        
        Args:
            symbol: Asset symbol
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            start_date: Start date (optional)
            end_date: End date (optional)
            
        Returns:
            DataFrame with intraday price data
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': 'full',
            'apikey': self.api_key
        }
        
        # Check cache
        cache_key = f"intraday_{symbol}_{interval}"
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            cache_time = cached_data['timestamp']
            if (datetime.now() - cache_time).total_seconds() < self._cache_ttl:
                df = cached_data['data']
                return self._filter_date_range(df, start_date, end_date)
        
        # Fetch new data
        response = self._make_request(params)
        
        # Parse response
        time_series_key = f"Time Series ({interval})"
        time_series = response.get(time_series_key, {})
        data = []
        for timestamp_str, values in time_series.items():
            row = {
                'timestamp': pd.to_datetime(timestamp_str),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            }
            data.append(row)
            
        # Create DataFrame
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        
        # Cache the data
        self._cache[cache_key] = {
            'timestamp': datetime.now(),
            'data': df
        }
        
        return self._filter_date_range(df, start_date, end_date)
    
    def get_fundamental_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get fundamental data for a symbol.
        
        Args:
            symbol: Asset symbol
            
        Returns:
            Dictionary containing fundamental data
        """
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        # Check cache
        cache_key = f"fundamental_{symbol}"
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            cache_time = cached_data['timestamp']
            if (datetime.now() - cache_time).total_seconds() < self._cache_ttl:
                return cached_data['data']
        
        # Fetch new data
        response = self._make_request(params)
        
        # Cache the data
        self._cache[cache_key] = {
            'timestamp': datetime.now(),
            'data': response
        }
        
        return response
    
    def get_market_data(self,
                       symbols: List[str],
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        """
        Get market data for multiple symbols in parallel.
        
        Args:
            symbols: List of asset symbols
            start_date: Start date (optional)
            end_date: End date (optional)
            
        Returns:
            Dictionary mapping symbols to their data DataFrames
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_symbol = {
                executor.submit(self.get_daily_data, symbol, start_date, end_date): symbol
                for symbol in symbols
            }
            
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    data = future.result()
                    results[symbol] = data
                except Exception as e:
                    logger.error(f"Error fetching data for {symbol}: {str(e)}")
                    
        return results
    
    def get_real_time_data(self, symbol: str) -> Dict[str, float]:
        """
        Get real-time quote for a symbol.
        
        Args:
            symbol: Asset symbol
            
        Returns:
            Dictionary containing real-time price data
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        response = self._make_request(params)
        quote = response.get('Global Quote', {})
        
        return {
            'price': float(quote.get('05. price', 0)),
            'volume': int(quote.get('06. volume', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': float(quote.get('10. change percent', '0').strip('%'))
        }
    
    def _make_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Make an API request with rate limiting.
        
        Args:
            params: Request parameters
            
        Returns:
            JSON response
        """
        # Implement rate limiting (5 calls per minute for free API)
        now = datetime.now()
        if params['function'] in self._last_request_time:
            last_request = self._last_request_time[params['function']]
            if (now - last_request).total_seconds() < 12:  # Wait 12 seconds between calls
                wait_time = 12 - (now - last_request).total_seconds()
                if wait_time > 0:
                    logger.info(f"Rate limiting: waiting {wait_time:.2f} seconds")
                    time.sleep(wait_time)
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for API errors
        if "Error Message" in data:
            raise ValueError(f"API Error: {data['Error Message']}")
            
        self._last_request_time[params['function']] = datetime.now()
        return data
    
    def _filter_date_range(self,
                          df: pd.DataFrame,
                          start_date: Optional[datetime],
                          end_date: Optional[datetime]) -> pd.DataFrame:
        """
        Filter DataFrame to specified date range.
        
        Args:
            df: Input DataFrame
            start_date: Start date
            end_date: End date
            
        Returns:
            Filtered DataFrame
        """
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        return df 