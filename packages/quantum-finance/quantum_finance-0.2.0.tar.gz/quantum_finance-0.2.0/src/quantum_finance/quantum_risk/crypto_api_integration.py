#!/usr/bin/env python3

"""
Cryptocurrency API Integration Module for Quantum Risk Package

This module provides the integration layer between the Quantum Risk assessment
package and various cryptocurrency exchange APIs, including Binance Futures
Leaderboard and KuCoin Market Data.

It enables quantum-enhanced risk analysis of cryptocurrency markets by combining
market microstructure data with quantum computing algorithms.

Author: Quantum-AI Team
"""

import os
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime

# Use relative imports for internal quantum_risk modules to maintain consistency
from .data_fetcher import CryptoDataFetcher
from .analyzer import QuantumEnhancedCryptoRiskAnalyzer as QuantumRiskAnalyzer
from .report_generator import ReportGenerator
from .utils.logging_util import setup_logger

logger = setup_logger(__name__)


class CryptoApiIntegration:
    """
    Integration class that connects the Quantum Risk package with
    cryptocurrency exchange APIs for enhanced risk assessment.

    This class provides methods to:
    - Configure different risk assessment profiles
    - Fetch data from multiple exchanges
    - Process market data through quantum risk algorithms
    - Generate comprehensive risk reports
    """

    def __init__(self, config_profile: str = "default", api_key: Optional[str] = None):
        """
        Initialize the cryptocurrency API integration.

        Args:
            config_profile: The configuration profile to use
            api_key: Optional API key for exchanges (if not in environment variables)
        """
        self.api_key = api_key or os.environ.get("RAPIDAPI_KEY")
        if not self.api_key:
            logger.warning("No API key provided. Some functionality may be limited.")

        # Load the configuration profile
        self.config = self._load_config_profile(config_profile)

        # Initialize the data fetcher from the quantum risk package
        self.data_fetcher = CryptoDataFetcher(api_key=self.api_key)

        # Initialize exchange API clients
        self.exchange_clients = {}
        self._initialize_exchange_clients()

        # Initialize the quantum risk analyzer
        self.risk_analyzer = QuantumRiskAnalyzer()

        # Initialize the report generator
        self.report_generator = ReportGenerator()

        logger.info(f"Initialized CryptoApiIntegration with profile: {config_profile}")

    def _load_config_profile(self, profile_name: str) -> Dict[str, Any]:
        """
        Load a configuration profile for risk assessment.

        Args:
            profile_name: Name of the configuration profile

        Returns:
            Configuration dictionary
        """
        # Default configuration
        default_config = {
            "exchanges": ["kucoin"],  # Removed Binance Futures as deprecated
            "symbols": ["BTC", "ETH"],
            "risk_parameters": {
                "quantum_circuit_depth": 3,
                "shots": 1024,
                "optimization_level": 1,
                "bayesian_priors": "auto",
                "risk_threshold": 0.7,
            },
            "data_parameters": {
                "historical_days": 30,
                "order_book_depth": 20,
                "trade_limit": 100,
            },
            "report_parameters": {
                "generate_charts": True,
                "include_raw_data": False,
                "output_format": "json",
            },
        }

        # TODO: Load custom profiles from a configuration file
        # For now, just return the default configuration
        logger.info(f"Using {profile_name} configuration profile")
        return default_config

    def _initialize_exchange_clients(self):
        """Initialize the API clients for each configured exchange"""
        exchanges = self.config.get("exchanges", [])

        for exchange in exchanges:
            try:
                if exchange == "kucoin":
                    # Import and initialize the KuCoin Market Data client
                    from examples.kucoin_market_data import KuCoinMarketData

                    self.exchange_clients["kucoin"] = KuCoinMarketData()
                    logger.info("Initialized KuCoin Market Data client")
                # Add more exchanges as needed

            except Exception as e:
                logger.error(f"Failed to initialize client for {exchange}: {e}")

    def analyze_market_risk(
        self,
        symbol: str,
        exchange: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Perform quantum-enhanced risk analysis on a cryptocurrency market.

        Args:
            symbol: The cryptocurrency symbol (e.g., 'BTC')
            exchange: Optional exchange to use (if None, uses all configured exchanges)

        Returns:
            Dictionary containing risk analysis results
        """
        logger.info(f"Analyzing market risk for {symbol}")

        # Perform the quantum-enhanced risk analysis
        analysis_results = self.risk_analyzer.analyze_with_quantum(symbol)

        # Generate a markdown report from the analysis results
        report_file = self.risk_analyzer.generate_analysis_report(analysis_results)

        # Attach report file path to the results
        analysis_results["report_file"] = report_file

        return analysis_results

    def _collect_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Collect market data from all configured exchanges.

        Args:
            symbol: The cryptocurrency symbol (e.g., 'BTC')

        Returns:
            Dictionary containing market data from all exchanges
        """
        market_data = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "exchanges": {},
        }

        # Collect data from each exchange
        for exch in self.exchange_clients.keys():
            try:
                # Currently only KuCoin is supported
                if exch == "kucoin":
                    market_data["exchanges"][exch] = self._collect_kucoin_data(symbol)
                # Add more exchanges as needed

            except Exception as e:
                logger.error(f"Error collecting data from {exch} for {symbol}: {e}")
                market_data["exchanges"][exch] = {"error": str(e)}

        return market_data

    def _collect_kucoin_data(self, symbol: str) -> Dict[str, Any]:
        """
        Collect data from KuCoin Market Data API.

        Args:
            symbol: The cryptocurrency symbol (e.g., 'BTC')

        Returns:
            Dictionary containing KuCoin data
        """
        client = self.exchange_clients.get("kucoin")
        if not client:
            return {"error": "KuCoin client not initialized"}

        # Data dictionary to collect all KuCoin data
        data = {}

        # Get ticker information
        try:
            ticker = client.get_ticker(symbol)
            data["ticker"] = ticker
        except Exception as e:
            logger.error(f"Error fetching KuCoin ticker for {symbol}: {e}")
            data["ticker"] = {"error": str(e)}

        # Get order book
        try:
            order_book = client.get_order_book(
                symbol,
                depth=self.config["data_parameters"]["order_book_depth"],
            )
            data["order_book"] = order_book
        except Exception as e:
            logger.error(f"Error fetching KuCoin order book for {symbol}: {e}")
            data["order_book"] = {"error": str(e)}

        # Get market statistics
        try:
            market_stats = client.get_market_stats(symbol)
            data["market_stats"] = market_stats
        except Exception as e:
            logger.error(f"Error fetching KuCoin market stats for {symbol}: {e}")
            data["market_stats"] = {"error": str(e)}

        # Get recent trades
        try:
            recent_trades = client.get_recent_trades(
                symbol,
                limit=self.config["data_parameters"]["trade_limit"],
            )
            if isinstance(recent_trades, pd.DataFrame):
                data["recent_trades"] = recent_trades.to_dict(orient="records")
            else:
                data["recent_trades"] = recent_trades
        except Exception as e:
            logger.error(f"Error fetching KuCoin recent trades for {symbol}: {e}")
            data["recent_trades"] = {"error": str(e)}

        # Get historical klines data
        try:
            klines = client.get_klines(
                symbol,
                interval="1day",
                limit=self.config["data_parameters"]["historical_days"],
            )
            if isinstance(klines, pd.DataFrame):
                data["klines"] = klines.to_dict(orient="records")
            else:
                data["klines"] = klines
        except Exception as e:
            logger.error(f"Error fetching KuCoin klines for {symbol}: {e}")
            data["klines"] = {"error": str(e)}

        return data

    def get_available_exchanges(self) -> List[str]:
        """
        Get the list of available exchanges.

        Returns:
            List of available exchange names
        """
        return list(self.exchange_clients.keys())

    def get_configuration_profiles(self) -> List[str]:
        """
        Get the list of available configuration profiles.

        Returns:
            List of available configuration profile names
        """
        # TODO: Implement profile discovery
        return ["default", "high_frequency", "conservative", "aggressive"]

    def set_configuration_profile(self, profile_name: str):
        """
        Set the active configuration profile.

        Args:
            profile_name: Name of the configuration profile to use
        """
        self.config = self._load_config_profile(profile_name)
        logger.info(f"Switched to configuration profile: {profile_name}")


if __name__ == "__main__":
    # Simple test code
    import dotenv

    # Load environment variables from .env file if it exists
    dotenv.load_dotenv()

    # Create an instance of the integration class
    integration = CryptoApiIntegration()

    # List available exchanges
    print("Available exchanges:", integration.get_available_exchanges())

    # Test with BTC
    try:
        print("\nAnalyzing market risk for BTC...")
        results = integration.analyze_market_risk("BTC")

        print("\nRisk analysis completed for BTC")
        print(f"Risk Score: {results['risk_results'].get('risk_score', 'N/A')}")
        print(f"Report: {results['report']['summary']}")

    except Exception as e:
        print("Error in test: {}".format(e))
