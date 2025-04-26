#!/usr/bin/env python3

"""
CoinCap API Client

This module provides a client for interacting with the CoinCap API v2,
which offers cryptocurrency market data including prices, market caps,
supply information, and trading volume across multiple cryptocurrencies.

The CoinCap API provides real-time cryptocurrency market data for over 
1,000 cryptocurrencies with data aggregated from thousands of exchanges.

References:
- CoinCap API: https://api.coincap.io/v2/
"""

import os
import sys
import logging
import json
import time
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import requests
from enum import Enum
from dataclasses import dataclass, field
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Interval(Enum):
    """Time intervals for historical data."""
    MINUTE_1 = "m1"
    MINUTE_5 = "m5"
    MINUTE_15 = "m15"
    MINUTE_30 = "m30"
    HOUR_1 = "h1"
    HOUR_2 = "h2"
    HOUR_4 = "h4"
    HOUR_8 = "h8"
    HOUR_12 = "h12"
    DAY_1 = "d1"
    WEEK_1 = "w1"


@dataclass
class CoinCapConfig:
    """Configuration options for the CoinCapClient."""
    base_url: str = "https://api.coincap.io/v2"  # Using v2 API (v3 requires API key)
    request_timeout: int = 30  # seconds
    max_retries: int = 3
    retry_delay: int = 2  # seconds
    cache_ttl: int = 60  # seconds
    user_agent: str = "Quantum-Financial-API/1.0"
    api_key: Optional[str] = None


class CoinCapClient:
    """
    A client for interacting with the CoinCap API.
    
    This client provides methods to retrieve cryptocurrency market data
    including current and historical prices, market caps, and other metrics.
    """
    
    def __init__(self, config: Optional[CoinCapConfig] = None, api_key: Optional[str] = None):
        """
        Initialize the CoinCap API client.
        
        Args:
            config: Optional configuration settings for the client
            api_key: API key for authentication (overrides config.api_key if provided)
        """
        self.config = config or CoinCapConfig()
        if api_key:
            self.config.api_key = api_key
            
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.config.user_agent,
            "Accept": "application/json"
        })
        
        if self.config.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.config.api_key}"
            })
            
        self._cache = {}
        logger.info("CoinCap client initialized")
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a request to the CoinCap API.
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            Response data as Python object
            
        Raises:
            Exception: If the request fails after max_retries
        """
        # Check cache
        cache_key = f"{endpoint}:{json.dumps(params or {})}"
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self.config.cache_ttl:
                logger.debug(f"Using cached data for {endpoint}")
                return cached_data
        
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"
        
        # Initialize parameters dict if None
        if params is None:
            params = {}
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.config.request_timeout
                )
                
                if response.status_code == 429:
                    logger.warning(f"Rate limit hit, retrying in {self.config.retry_delay} seconds...")
                    time.sleep(self.config.retry_delay)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                # Cache the response
                self._cache[cache_key] = (data, time.time())
                
                return data
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.config.max_retries}): {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay)
                else:
                    logger.error(f"Failed to make request to {url} after {self.config.max_retries} attempts")
                    raise Exception(f"Failed to make request to {url}: {e}")
    
    def get_assets(self, limit: int = 100, offset: int = 0, search: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a list of all cryptocurrencies with latest market data.
        
        Args:
            limit: Number of results to return (default 100, max 2000)
            offset: Number of results to skip (default 0)
            search: Search by asset id or symbol
            
        Returns:
            Dictionary containing cryptocurrency data
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if search:
            params["search"] = search
            
        return self._make_request("assets", params)
    
    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        Get data for a specific cryptocurrency.
        
        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            
        Returns:
            Dictionary containing cryptocurrency data
        """
        return self._make_request(f"assets/{asset_id}")
    
    def get_asset_history(
        self,
        asset_id: str,
        interval: Union[str, Interval] = Interval.DAY_1,
        start: Optional[Union[int, datetime]] = None,
        end: Optional[Union[int, datetime]] = None
    ) -> Dict[str, Any]:
        """
        Get historical price and market data for a cryptocurrency.
        
        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            interval: Time interval for data points
            start: Start time (Unix timestamp or datetime, defaults to 1 day ago)
            end: End time (Unix timestamp or datetime, defaults to now)
            
        Returns:
            Dictionary containing historical price and market data
        """
        # Convert interval to string if it's an Enum
        if isinstance(interval, Interval):
            interval = interval.value
            
        # Default start/end times if not provided
        if end is None:
            end = datetime.now()
        if start is None:
            start = end - timedelta(days=1)
            
        # Convert datetime to timestamps if needed
        if isinstance(start, datetime):
            start = int(start.timestamp() * 1000)
        if isinstance(end, datetime):
            end = int(end.timestamp() * 1000)
            
        params = {
            "interval": interval,
            "start": start,
            "end": end
        }
        
        return self._make_request(f"assets/{asset_id}/history", params)
    
    def get_asset_markets(self, asset_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Get all markets for a specific cryptocurrency.
        
        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            limit: Number of results to return (default 100, max 2000)
            offset: Number of results to skip (default 0)
            
        Returns:
            Dictionary containing market data
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        return self._make_request(f"assets/{asset_id}/markets", params)
    
    def get_markets(
        self,
        limit: int = 100,
        offset: int = 0,
        baseSymbol: Optional[str] = None,
        quoteSymbol: Optional[str] = None,
        exchange_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get data for all markets.
        
        Args:
            limit: Number of results to return (default 100, max 2000)
            offset: Number of results to skip (default 0)
            baseSymbol: Filter by base symbol (e.g., "BTC")
            quoteSymbol: Filter by quote symbol (e.g., "USD")
            exchange_id: Filter by exchange ID
            
        Returns:
            Dictionary containing market data
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if baseSymbol:
            params["baseSymbol"] = baseSymbol
        if quoteSymbol:
            params["quoteSymbol"] = quoteSymbol
        if exchange_id:
            params["exchangeId"] = exchange_id
            
        return self._make_request("markets", params)
    
    def get_exchanges(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Get data for all exchanges.
        
        Args:
            limit: Number of results to return (default 100, max 2000)
            offset: Number of results to skip (default 0)
            
        Returns:
            Dictionary containing exchange data
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        return self._make_request("exchanges", params)
    
    def get_exchange(self, exchange_id: str) -> Dict[str, Any]:
        """
        Get data for a specific exchange.
        
        Args:
            exchange_id: Exchange identifier
            
        Returns:
            Dictionary containing exchange data
        """
        return self._make_request(f"exchanges/{exchange_id}")
    
    def get_rates(self) -> Dict[str, Any]:
        """
        Get exchange rates for all assets against USD.
        
        Returns:
            Dictionary containing exchange rate data
        """
        return self._make_request("rates")
    
    def get_rate(self, asset_id: str) -> Dict[str, Any]:
        """
        Get exchange rate for a specific asset against USD.
        
        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            
        Returns:
            Dictionary containing exchange rate data
        """
        return self._make_request(f"rates/{asset_id}")
    
    def get_candles(
        self,
        exchange: str,
        interval: Union[str, Interval],
        base_id: str,
        quote_id: str,
        start: Optional[Union[int, datetime]] = None,
        end: Optional[Union[int, datetime]] = None
    ) -> Dict[str, Any]:
        """
        Get OHLCV (Open, High, Low, Close, Volume) candle data for a market.
        
        Args:
            exchange: Exchange identifier
            interval: Time interval for candles
            base_id: Base asset identifier
            quote_id: Quote asset identifier
            start: Start time (Unix timestamp or datetime)
            end: End time (Unix timestamp or datetime)
            
        Returns:
            Dictionary containing OHLCV data
        """
        # Convert interval to string if it's an Enum
        if isinstance(interval, Interval):
            interval = interval.value
            
        # Convert datetime to timestamps if needed
        if isinstance(start, datetime):
            start = int(start.timestamp() * 1000)
        if isinstance(end, datetime):
            end = int(end.timestamp() * 1000)
            
        params = {
            "exchange": exchange,
            "interval": interval,
            "baseId": base_id,
            "quoteId": quote_id
        }
        
        if start:
            params["start"] = start
        if end:
            params["end"] = end
            
        return self._make_request("candles", params)
    
    def get_asset_prices_as_dataframe(
        self,
        asset_id: str,
        interval: Union[str, Interval] = Interval.DAY_1,
        start: Optional[Union[int, datetime]] = None,
        end: Optional[Union[int, datetime]] = None
    ) -> pd.DataFrame:
        """
        Get historical price data for an asset as a pandas DataFrame.
        
        Args:
            asset_id: Asset identifier (e.g., "bitcoin")
            interval: Time interval for data points
            start: Start time (Unix timestamp or datetime, defaults to 1 day ago)
            end: End time (Unix timestamp or datetime, defaults to now)
            
        Returns:
            DataFrame with price data
        """
        response = self.get_asset_history(asset_id, interval, start, end)
        
        if not response.get("data"):
            return pd.DataFrame()
            
        data = response["data"]
        df = pd.DataFrame(data)
        
        # Convert timestamp to datetime
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"], unit="ms")
            df = df.set_index("time")
            
        # Convert numeric columns
        for col in df.columns:
            if col != "time":
                df[col] = pd.to_numeric(df[col], errors="coerce")
                
        return df
    
    def get_candles_as_dataframe(
        self,
        exchange: str,
        interval: Union[str, Interval],
        base_id: str,
        quote_id: str,
        start: Optional[Union[int, datetime]] = None,
        end: Optional[Union[int, datetime]] = None
    ) -> pd.DataFrame:
        """
        Get OHLCV candle data for a market as a pandas DataFrame.
        
        Args:
            exchange: Exchange identifier
            interval: Time interval for candles
            base_id: Base asset identifier
            quote_id: Quote asset identifier
            start: Start time (Unix timestamp or datetime)
            end: End time (Unix timestamp or datetime)
            
        Returns:
            DataFrame with OHLCV data
        """
        response = self.get_candles(exchange, interval, base_id, quote_id, start, end)
        
        if not response.get("data"):
            return pd.DataFrame()
            
        data = response["data"]
        df = pd.DataFrame(data)
        
        # Convert timestamp to datetime
        if "period" in df.columns:
            df["time"] = pd.to_datetime(df["period"], unit="ms")
            df = df.set_index("time")
            df = df.drop(columns=["period"])
            
        # Convert numeric columns
        for col in ["open", "high", "low", "close", "volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                
        return df
    
    def clear_cache(self):
        """Clear the client's cache."""
        self._cache = {}
        logger.info("Cache cleared")


# Example usage
if __name__ == "__main__":
    client = CoinCapClient()
    assets = client.get_assets(limit=10)
    print(json.dumps(assets, indent=2)) 