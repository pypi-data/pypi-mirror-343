#!/usr/bin/env python3

"""
Mempool API Client

This module provides a client for interacting with the mempool.space API,
which offers real-time Bitcoin mempool data, fee estimates, and transaction information.

This data can be used to enhance cryptocurrency market predictions by providing
insights into network congestion, transaction costs, and network activity levels.

References:
- mempool.space API documentation: https://mempool.space/api
"""

import os
import sys
import logging
import json
import time
import random
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
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


class MempoolNetwork(Enum):
    """Bitcoin network types supported by the mempool.space API."""
    MAINNET = "mainnet"
    TESTNET = "testnet"
    SIGNET = "signet"


@dataclass
class MempoolConfig:
    """Configuration options for the MempoolClient."""
    base_url: str = "https://mempool.space/api"
    network: MempoolNetwork = MempoolNetwork.MAINNET
    request_timeout: int = 30  # seconds
    max_retries: int = 3
    retry_delay: int = 2  # seconds
    cache_ttl: int = 60  # seconds
    user_agent: str = "Quantum-Financial-API/1.0"
    
    def get_api_url(self) -> str:
        """Get the full API URL with network path if needed."""
        if self.network == MempoolNetwork.MAINNET:
            return self.base_url
        else:
            return f"{self.base_url}/{self.network.value}"


class MempoolClient:
    """
    Client for interacting with the mempool.space API.
    
    This client provides methods to retrieve Bitcoin mempool data including:
    - Fee estimates for different confirmation targets
    - Mempool statistics (size, transaction count, fee ranges)
    - Recent transactions
    - Block information
    
    The data is useful for predicting transaction costs, network congestion,
    and blockchain activity levels - all of which can inform cryptocurrency
    market predictions.
    """
    
    def __init__(self, config: Optional[MempoolConfig] = None):
        """Initialize the mempool client with the given configuration."""
        self.config = config or MempoolConfig()
        self.api_url = self.config.get_api_url()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.config.user_agent
        })
        
        # Simple in-memory cache
        self._cache = {}
        
        # Track rate limit status
        self._rate_limit_remaining = None
        self._rate_limit_reset = None
        self._request_count = 0
        self._last_error_time = 0
        self._consecutive_errors = 0
        
        logger.info(f"Initialized MempoolClient with API URL: {self.api_url}")

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a request to the mempool.space API with retry logic and exponential backoff.
        
        Args:
            endpoint: API endpoint (without leading slash)
            params: Optional query parameters
            
        Returns:
            JSON response (dict or list)
            
        Raises:
            requests.RequestException: If the request fails after retries
        """
        url = f"{self.api_url}/{endpoint}"
        cache_key = f"{url}_{json.dumps(params or {})}"
        
        # Check cache first
        cache_entry = self._cache.get(cache_key)
        if cache_entry and (time.time() - cache_entry['timestamp'] < self.config.cache_ttl):
            logger.debug(f"Cache hit for {url}")
            return cache_entry['data']
        
        # Track request count
        self._request_count += 1
        
        # Check if we've recently encountered rate limits and should delay requests
        current_time = time.time()
        if self._rate_limit_reset and current_time < self._rate_limit_reset:
            wait_time = self._rate_limit_reset - current_time
            logger.warning(f"Preemptively waiting {wait_time:.2f}s for rate limit reset")
            time.sleep(wait_time)
            # Reset rate limit tracking after waiting
            self._rate_limit_reset = None
        
        # Not in cache or expired, make the request
        retries = 0
        base_delay = self.config.retry_delay
        
        while retries <= self.config.max_retries:
            try:
                logger.debug(f"Making request to {url} with params {params}")
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=self.config.request_timeout
                )
                
                # Check for and store rate limit headers if they exist
                if 'X-Ratelimit-Remaining' in response.headers:
                    self._rate_limit_remaining = int(response.headers['X-Ratelimit-Remaining'])
                    
                if 'X-Ratelimit-Reset' in response.headers:
                    self._rate_limit_reset = float(response.headers['X-Ratelimit-Reset'])
                
                # Handle HTTP 429 rate limiting with improved exponential backoff
                if response.status_code == 429:
                    # Use Retry-After header if present, otherwise use exponential backoff
                    if 'Retry-After' in response.headers:
                        retry_after = int(response.headers['Retry-After'])
                    else:
                        # Calculate exponential backoff with jitter
                        jitter = random.uniform(0.75, 1.25)
                        retry_after = min(300, base_delay * (2 ** retries)) * jitter
                    
                    # Update consecutive errors
                    self._consecutive_errors += 1
                    
                    # Log detailed rate limit info
                    logger.warning(
                        f"Rate limited by API (429). Retrying after {retry_after:.2f}s. "
                        f"Consecutive errors: {self._consecutive_errors}"
                    )
                    
                    time.sleep(retry_after)
                    retries += 1
                    continue
                
                # Handle server errors (5xx) with exponential backoff
                if response.status_code >= 500:
                    # Calculate exponential backoff with jitter
                    jitter = random.uniform(0.8, 1.2)
                    retry_after = min(300, base_delay * (2 ** retries)) * jitter
                    
                    # Update consecutive errors
                    self._consecutive_errors += 1
                    
                    logger.warning(
                        f"Server error: {response.status_code}. Retrying after {retry_after:.2f}s. "
                        f"Consecutive errors: {self._consecutive_errors}"
                    )
                    
                    time.sleep(retry_after)
                    retries += 1
                    continue
                
                # Handle other errors
                response.raise_for_status()
                
                # If we get here, the request succeeded, reset error counter
                self._consecutive_errors = 0
                self._last_error_time = 0
                
                # Parse JSON response
                try:
                    data = response.json()
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON from response: {str(e)}")
                    logger.debug(f"Response content: {response.text[:200]}...")
                    raise
                
                # Cache the result
                self._cache[cache_key] = {
                    'timestamp': time.time(),
                    'data': data
                }
                
                # If we're getting low on rate limit, delay future requests
                if self._rate_limit_remaining is not None and self._rate_limit_remaining < 5:
                    logger.warning(f"Rate limit running low ({self._rate_limit_remaining} remaining). Slowing down requests.")
                    
                return data
                
            except (requests.RequestException, json.JSONDecodeError) as e:
                retries += 1
                self._consecutive_errors += 1
                
                # Record error time
                self._last_error_time = time.time()
                
                if retries > self.config.max_retries:
                    logger.error(f"Failed to make request to {url} after {self.config.max_retries} retries: {str(e)}")
                    raise
                
                # Calculate exponential backoff delay with added jitter
                # Base is multiplied by 2^retry_number, with randomization to prevent synchronized retries
                # More aggressive backoff for more consecutive errors
                backoff_factor = min(5, 1 + (self._consecutive_errors / 10))
                max_delay = 120  # Cap at 2 minutes
                backoff_delay = min(
                    max_delay, 
                    base_delay * (2 ** (retries - 1)) * backoff_factor
                )
                
                # Add jitter (±25%)
                jitter = random.uniform(0.75, 1.25)
                backoff_delay *= jitter
                
                logger.warning(
                    f"Request to {url} failed (attempt {retries}/{self.config.max_retries}): {str(e)}. "
                    f"Retrying in {backoff_delay:.2f}s. Consecutive errors: {self._consecutive_errors}"
                )
                time.sleep(backoff_delay)
        
        # This should never happen because of the raise in the exception handler above,
        # but adding this to satisfy the linter
        raise requests.RequestException(f"Failed to make request to {url} after exhausting retries")
    
    def get_fees_recommended(self) -> Dict[str, int]:
        """
        Get recommended fee rates for different confirmation targets.
        
        Returns:
            Dictionary with fee rate recommendations in sat/vB:
            {
                "fastestFee": int,  # For confirmation within 1 block
                "halfHourFee": int, # For confirmation within 3 blocks
                "hourFee": int,     # For confirmation within 6 blocks
                "economyFee": int,  # For confirmation within 144 blocks (1 day)
                "minimumFee": int   # Minimum relay fee
            }
        """
        return self._make_request("v1/fees/recommended")
    
    def get_fee_estimate(self, target_blocks: int) -> int:
        """
        Get fee estimate for a specific confirmation target.
        
        Args:
            target_blocks: Number of blocks to target for confirmation
            
        Returns:
            Estimated fee rate in sat/vB
            
        Raises:
            ValueError: If target_blocks is not a positive integer
            requests.RequestException: If the API request fails
        """
        if not isinstance(target_blocks, int) or target_blocks <= 0:
            raise ValueError("target_blocks must be a positive integer")
            
        try:
            # The mempool API has a direct endpoint for fee estimates by target block
            endpoint = f"v1/fees/block-target/{target_blocks}"
            try:
                # First try the direct endpoint if available
                fee_data = self._make_request(endpoint)
                
                # The response should be a simple number representing the fee rate
                if isinstance(fee_data, (int, float)):
                    return int(fee_data)
            except requests.RequestException as e:
                logger.warning(f"Failed to get direct fee estimate for target {target_blocks} blocks: {e}")
                # Fall back to recommended fees mapping
            
            # Fall back to recommended fees
            recommended = self.get_fees_recommended()
            
            # Map target blocks to recommended fee categories
            if target_blocks == 1:
                return recommended.get("fastestFee", 5)  # Default to 5 sat/vB if API fails
            elif target_blocks <= 3:
                return recommended.get("halfHourFee", 3)
            elif target_blocks <= 6:
                return recommended.get("hourFee", 2)
            elif target_blocks <= 144:  # 1 day
                return recommended.get("economyFee", 1)
            else:
                return recommended.get("minimumFee", 1)
                
        except requests.RequestException as e:
            logger.error(f"Failed to get fee estimate for target {target_blocks} blocks: {e}")
            # Return more intelligent default based on target_blocks
            if target_blocks == 1:
                return 5  # Conservative default for fastest
            elif target_blocks <= 3:
                return 3  # Conservative default for half hour
            elif target_blocks <= 6:
                return 2  # Conservative default for hour
            else:
                return 1  # Minimum fee for longer timeframes
    
    def estimate_transaction_fee(self, tx_size_vbytes: int, confirmation_target: int = 3) -> Dict[str, Any]:
        """
        Estimate the fee for a transaction of given size with desired confirmation target.
        
        Args:
            tx_size_vbytes: Transaction size in virtual bytes
            confirmation_target: Target number of blocks for confirmation
            
        Returns:
            Dictionary with fee information:
            {
                "fee_rate": float,        # Fee rate in sat/vB
                "total_fee": int,         # Total fee in satoshis
                "confirmation_target": int,  # Target blocks for confirmation
                "estimated_time": int,    # Estimated time in minutes
                "tx_size_vbytes": int,    # Transaction size in vBytes
                "confidence": float,      # Confidence level in the estimate (0-1)
                "fee_range": {            # Range of possible fees
                    "min": int,           # Minimum recommended fee
                    "max": int            # Maximum recommended fee
                }
            }
        """
        if not isinstance(tx_size_vbytes, int) or tx_size_vbytes <= 0:
            raise ValueError("tx_size_vbytes must be a positive integer")
            
        # Get fee rate for the target confirmation time with retry
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                fee_rate = self.get_fee_estimate(confirmation_target)
                break
            except Exception as e:
                if attempt == max_attempts - 1:
                    logger.error(f"Failed to get fee estimate after {max_attempts} attempts: {e}")
                    # Use a conservative default
                    fee_rate = max(2, confirmation_target * 2)
                else:
                    logger.warning(f"Fee estimation attempt {attempt+1} failed: {e}. Retrying...")
                    time.sleep(1)
        
        # Calculate total fee
        total_fee = int(tx_size_vbytes * fee_rate)
        
        # Get mempool state for better time estimation
        try:
            mempool_stats = self.get_mempool_stats()
            blocks_in_mempool = mempool_stats.get('blocks', 1)
            
            # Better estimate confirmation time based on current mempool state
            if blocks_in_mempool > confirmation_target:
                # If mempool is congested, estimate might be optimistic
                estimated_time = confirmation_target * 12  # 12 min per block instead of 10 min
                confidence = 0.7
            else:
                # Normal conditions
                estimated_time = confirmation_target * 10  # 10 min per block on average
                confidence = 0.9
            
        except Exception as e:
            logger.warning(f"Failed to get mempool stats for better time estimation: {e}")
            # Fall back to simple estimation
            estimated_time = confirmation_target * 10  # 10 min per block on average
            confidence = 0.8
        
        # Get fee recommendations for fee range
        try:
            fee_recommendations = self.get_fees_recommended()
            
            # Determine fee range based on confirmation target
            if confirmation_target == 1:
                fee_min = fee_recommendations.get('fastestFee', fee_rate * 0.8)
                fee_max = fee_rate * 1.2  # 20% buffer
            elif confirmation_target <= 3:
                fee_min = fee_recommendations.get('hourFee', fee_rate * 0.7)
                fee_max = fee_recommendations.get('fastestFee', fee_rate * 1.3)
            else:
                fee_min = fee_recommendations.get('economyFee', fee_rate * 0.6)
                fee_max = fee_recommendations.get('halfHourFee', fee_rate * 1.2)
        except Exception as e:
            logger.warning(f"Failed to get fee recommendations for fee range: {e}")
            # Fall back to simple range
            fee_min = int(fee_rate * 0.7)
            fee_max = int(fee_rate * 1.3)
        
        return {
            "fee_rate": fee_rate,
            "total_fee": total_fee,
            "confirmation_target": confirmation_target,
            "estimated_time": estimated_time,
            "tx_size_vbytes": tx_size_vbytes,
            "confidence": confidence,
            "fee_range": {
                "min": int(fee_min),
                "max": int(fee_max)
            }
        }
    
    def get_mempool_blocks(self) -> List[Dict[str, Any]]:
        """
        Get current mempool as projected blocks.
        
        Returns:
            List of projected blocks with their transactions and fee rates
        """
        result = self._make_request("v1/fees/mempool-blocks")
        if not isinstance(result, list):
            logger.warning(f"Expected list response from mempool-blocks endpoint, got {type(result)}")
            return []
        return result
    
    def get_mempool_stats(self) -> Dict[str, Any]:
        """
        Get current mempool statistics.
        
        Returns:
            Dictionary with mempool statistics including:
            - Count of transactions
            - Virtual size in bytes
            - Total fee in sats
        """
        return self._make_request("mempool")
    
    def get_recent_transactions(self) -> List[Dict[str, Any]]:
        """
        Get a list of the last 10 transactions to enter the mempool.
        
        Returns:
            List of recent transactions with basic information
        """
        result = self._make_request("mempool/recent")
        if not isinstance(result, list):
            logger.warning(f"Expected list response from mempool/recent endpoint, got {type(result)}")
            return []
        return result
    
    def get_blocks(self, start_height: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get recent blocks.
        
        Args:
            start_height: Optional starting height (if omitted, returns latest blocks)
            
        Returns:
            List of blocks with basic information
        """
        endpoint = f"v1/blocks/{start_height}" if start_height else "v1/blocks"
        result = self._make_request(endpoint)
        if not isinstance(result, list):
            logger.warning(f"Expected list response from blocks endpoint, got {type(result)}")
            return []
        return result
    
    def get_transaction(self, txid: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific transaction.
        
        Args:
            txid: Transaction ID (hash)
            
        Returns:
            Dictionary with transaction details
        """
        return self._make_request(f"tx/{txid}")
    
    def get_transaction_status(self, txid: str) -> Dict[str, Any]:
        """
        Get the status of a transaction.
        
        Args:
            txid: Transaction ID (hex)
            
        Returns:
            Dictionary with transaction status information
        """
        return self._make_request(f"tx/{txid}/status")
    
    def validate_transaction(self, txid: str) -> Dict[str, Any]:
        """
        Validate a transaction and get its details.
        
        This method performs a comprehensive validation of a transaction,
        checking its status, confirmation count, and validity.
        
        Args:
            txid: Transaction ID to validate
            
        Returns:
            Dictionary with validation results:
            {
                "valid": bool,                  # Whether the transaction is valid
                "status": str,                  # Status of the transaction
                "confirmed": bool,              # Whether the transaction is confirmed
                "confirmation_count": int,      # Number of confirmations
                "included_in_block": str,       # Block hash or null
                "timestamp": int,               # Transaction timestamp
                "fee_rate": float,              # Fee rate in sat/vB
                "total_fee": int,               # Total fee in satoshis
                "inputs_count": int,            # Number of inputs
                "outputs_count": int,           # Number of outputs
                "total_input_value": int,       # Total input value in satoshis
                "total_output_value": int,      # Total output value in satoshis
                "validation_errors": list,      # List of validation errors if any
                "replacement_risk": float       # Risk of replacement by fee (0-1)
            }
        """
        if not txid or not isinstance(txid, str) or len(txid) != 64:
            raise ValueError("Invalid transaction ID format")
        
        result = {
            "valid": False,
            "status": "unknown",
            "confirmed": False,
            "confirmation_count": 0,
            "included_in_block": None,
            "timestamp": 0,
            "fee_rate": 0.0,
            "total_fee": 0,
            "inputs_count": 0,
            "outputs_count": 0,
            "total_input_value": 0,
            "total_output_value": 0,
            "validation_errors": [],
            "replacement_risk": 0.0
        }
        
        # Get transaction data
        try:
            tx_data = self.get_transaction(txid)
            
            # Basic info
            result["status"] = tx_data.get("status", "unknown")
            result["confirmed"] = tx_data.get("status", {}).get("confirmed", False)
            result["confirmation_count"] = tx_data.get("status", {}).get("block_height", 0)
            result["included_in_block"] = tx_data.get("status", {}).get("block_hash")
            result["timestamp"] = tx_data.get("status", {}).get("block_time", 0)
            
            # Extract transaction details
            if "fee" in tx_data and "vsize" in tx_data:
                result["fee_rate"] = tx_data["fee"] / tx_data["vsize"]
                result["total_fee"] = tx_data["fee"]
            
            result["inputs_count"] = len(tx_data.get("vin", []))
            result["outputs_count"] = len(tx_data.get("vout", []))
            
            # Calculate total input and output values
            total_input = 0
            for vin in tx_data.get("vin", []):
                if "prevout" in vin and "value" in vin["prevout"]:
                    total_input += vin["prevout"]["value"]
            
            total_output = 0
            for vout in tx_data.get("vout", []):
                if "value" in vout:
                    total_output += vout["value"]
            
            result["total_input_value"] = total_input
            result["total_output_value"] = total_output
            
            # Additional validation checks
            validation_errors = []
            
            # Check if all inputs have valid references
            for i, vin in enumerate(tx_data.get("vin", [])):
                if "prevout" not in vin:
                    validation_errors.append(f"Input #{i} has no prevout reference")
            
            # Check if fee is reasonable
            if "fee" in tx_data and tx_data["fee"] > 0:
                # Check for extremely high fees (potential mistake)
                if result["fee_rate"] > 1000:  # More than 1000 sat/vB is suspicious
                    validation_errors.append("Extremely high fee rate detected")
                
                # Check for extremely low fees (might not confirm)
                if result["fee_rate"] < 1:  # Less than 1 sat/vB might not confirm
                    validation_errors.append("Extremely low fee rate may prevent confirmation")
            
            # Check for RBF (Replace-By-Fee) signaling
            rbf_signaled = False
            for vin in tx_data.get("vin", []):
                if "sequence" in vin and vin["sequence"] < 0xffffffff - 1:
                    rbf_signaled = True
                    break
            
            # Calculate replacement risk
            if not result["confirmed"]:
                if rbf_signaled:
                    # High risk if unconfirmed and signals RBF
                    result["replacement_risk"] = 0.8
                elif result["fee_rate"] < 5:
                    # Medium-high risk if low fee rate
                    result["replacement_risk"] = 0.6
                else:
                    # Lower risk otherwise
                    result["replacement_risk"] = 0.3
            else:
                # Confirmed transactions have very low replacement risk
                result["replacement_risk"] = 0.0
            
            # Set validation errors
            result["validation_errors"] = validation_errors
            
            # Set overall validity
            result["valid"] = (len(validation_errors) == 0)
            
            # Adjust validity based on confirmation status
            if result["confirmed"] and result["confirmation_count"] >= 6:
                # Transactions with 6+ confirmations are highly reliable
                result["valid"] = True
                
        except Exception as e:
            logger.error(f"Error validating transaction {txid}: {str(e)}")
            result["validation_errors"].append(f"Validation failed: {str(e)}")
        
        return result
    
    def get_transaction_fees(self, txid: str) -> Dict[str, Any]:
        """
        Get fee-related information for a transaction, including CPFP (Child Pays for Parent).
        
        Args:
            txid: Transaction ID (hash)
            
        Returns:
            Dictionary with fee and CPFP information
        """
        return self._make_request(f"v1/tx/{txid}/cpfp")
    
    def get_mempool_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of current mempool data.
        
        Returns:
            Dictionary with combined mempool statistics and fee recommendations
        """
        try:
            # Get fee recommendations
            fees = self.get_fees_recommended()
            
            # Get mempool statistics
            mempool_stats = self.get_mempool_stats()
            
            # Get current projected mempool blocks
            mempool_blocks = self.get_mempool_blocks()
            
            # Combine the data
            return {
                "timestamp": datetime.now().isoformat(),
                "fee_recommendations": fees,
                "mempool_statistics": mempool_stats,
                "projected_blocks": mempool_blocks[:3]  # Include first 3 projected blocks
            }
        except Exception as e:
            logger.error(f"Error getting mempool summary: {e}")
            return {"error": str(e)}
    
    def get_fee_history(self, blocks: int = 10) -> Dict[str, Any]:
        """
        Compile fee history data by analyzing recent blocks.
        
        Args:
            blocks: Number of recent blocks to analyze
            
        Returns:
            Dictionary with fee history data
        """
        try:
            # Get recent blocks
            recent_blocks = self.get_blocks()[:blocks]
            
            # Extract median fees from each block
            fees = []
            timestamps = []
            
            for block in recent_blocks:
                if 'medianFee' in block:
                    fees.append(block['medianFee'])
                    timestamps.append(block.get('timestamp', 0))
            
            # Create a simple DataFrame for analysis
            if fees:
                df = pd.DataFrame({
                    'timestamp': timestamps,
                    'median_fee': fees
                })
                
                # Calculate basic stats
                stats = {
                    'min': float(df['median_fee'].min()),
                    'max': float(df['median_fee'].max()),
                    'mean': float(df['median_fee'].mean()),
                    'median': float(df['median_fee'].median()),
                    'std': float(df['median_fee'].std())
                }
                
                return {
                    'fees': fees,
                    'timestamps': timestamps,
                    'statistics': stats
                }
            else:
                return {'error': 'No fee data available'}
                
        except Exception as e:
            logger.error(f"Error getting fee history: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    # Simple test if run directly
    client = MempoolClient()
    
    print("Testing mempool.space API client...")
    print("\nFee Recommendations:")
    print(json.dumps(client.get_fees_recommended(), indent=2))
    
    print("\nMempool Summary:")
    summary = client.get_mempool_summary()
    # Print a cleaner version of the summary
    clean_summary = {
        "timestamp": summary["timestamp"],
        "fee_recommendations": summary["fee_recommendations"],
        "mempool_statistics": {
            k: v for k, v in summary.get("mempool_statistics", {}).items()
            if k in ["count", "vsize", "total_fee"]
        }
    }
    print(json.dumps(clean_summary, indent=2)) 