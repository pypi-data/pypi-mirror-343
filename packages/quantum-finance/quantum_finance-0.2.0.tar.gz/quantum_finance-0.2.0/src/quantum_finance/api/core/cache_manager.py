#!/usr/bin/env python3

"""
Quantum Financial API - Cache Manager

Implements a comprehensive caching system for the Quantum Financial API
with support for component results, lazy loading, and memory optimization.

This module provides:
- In-memory LRU cache for component results
- Configurable time-to-live (TTL) for cached items
- Memory usage monitoring and automatic cache eviction
- Statistics for cache performance monitoring
"""

import os
import time
import logging
import json
import numpy as np
import threading
from typing import Dict, List, Tuple, Optional, Union, Any, Callable
from enum import Enum
from collections import OrderedDict
from dataclasses import dataclass
import psutil
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CacheItemType(Enum):
    """Types of items that can be cached."""
    MARKET_ENCODING = "market_encoding"
    PHASE_TRACKING = "phase_tracking"
    ADAPTIVE_LEARNING = "adaptive_learning"
    QUANTUM_DIFFUSION = "quantum_diffusion"
    STOCHASTIC_SIMULATION = "stochastic_simulation"
    QUANTUM_STATE = "quantum_state"
    CIRCUIT_RESULT = "circuit_result"
    ANALYSIS_RESULT = "analysis_result"
    ENSEMBLE_PREDICTION = "ensemble_prediction"


@dataclass
class CacheItem:
    """Represents an item in the cache with metadata."""
    key: str
    value: Any
    item_type: CacheItemType
    created_at: float
    last_accessed: float
    access_count: int = 0
    ttl: Optional[float] = None  # Time-to-live in seconds, None means no expiration
    size_bytes: int = 0
    
    def is_expired(self) -> bool:
        """Check if this cache item has expired."""
        if self.ttl is None:
            return False
        return time.time() > (self.created_at + self.ttl)
    
    def update_last_accessed(self) -> None:
        """Update the last accessed timestamp and increment access count."""
        self.last_accessed = time.time()
        self.access_count += 1


class LRUCache:
    """
    Thread-safe LRU (Least Recently Used) cache implementation with TTL support
    and memory usage tracking.
    """
    
    def __init__(
        self,
        max_size: int = 1000,
        max_memory_mb: float = 1024,  # 1GB default max memory
        default_ttl: Optional[float] = 3600,  # 1 hour default TTL
        enable_stats: bool = True
    ):
        """
        Initialize the LRU cache.
        
        Args:
            max_size: Maximum number of items in the cache
            max_memory_mb: Maximum memory usage in MB
            default_ttl: Default time-to-live for items in seconds (None for no expiration)
            enable_stats: Whether to collect and track cache statistics
        """
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._max_memory_bytes = int(max_memory_mb * 1024 * 1024)
        self._default_ttl = default_ttl
        self._current_memory_usage = 0
        self._lock = threading.RLock()
        self._enable_stats = enable_stats
        
        # Statistics
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0
        self._memory_evictions = 0
        
        # Start periodic cleanup task
        self._cleanup_interval = 300  # 5 minutes
        self._stop_cleanup = threading.Event()
        self._cleanup_thread = threading.Thread(target=self._periodic_cleanup, daemon=True)
        self._cleanup_thread.start()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get an item from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        with self._lock:
            if key not in self._cache:
                if self._enable_stats:
                    self._misses += 1
                return None
            
            item = self._cache[key]
            
            # Check if expired
            if item.is_expired():
                self._remove_item(key)
                if self._enable_stats:
                    self._expirations += 1
                    self._misses += 1
                return None
            
            # Update access information and move to end (most recently used)
            item.update_last_accessed()
            self._cache.move_to_end(key)
            
            if self._enable_stats:
                self._hits += 1
                
            return item.value
    
    def put(
        self,
        key: str,
        value: Any,
        item_type: CacheItemType,
        ttl: Optional[float] = None,
        size_bytes: Optional[int] = None
    ) -> None:
        """
        Add an item to the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            item_type: Type of item being cached
            ttl: Time-to-live in seconds, overrides default if provided
            size_bytes: Size of the item in bytes, will be estimated if not provided
        """
        if ttl is None:
            ttl = self._default_ttl
            
        # Estimate size if not provided
        if size_bytes is None:
            try:
                if isinstance(value, np.ndarray):
                    size_bytes = value.nbytes
                elif isinstance(value, (str, bytes)):
                    size_bytes = len(value)
                elif hasattr(value, '__sizeof__'):
                    size_bytes = value.__sizeof__()
                else:
                    # Approximate size using JSON serialization as fallback
                    size_bytes = len(json.dumps(value, default=str).encode('utf-8'))
            except Exception as e:
                logger.warning(f"Error estimating cache item size: {e}")
                size_bytes = 1024  # Default 1KB if estimation fails
        
        with self._lock:
            # If key already exists, remove it first to update size tracking
            if key in self._cache:
                old_item = self._cache[key]
                self._current_memory_usage -= old_item.size_bytes
            
            # Create new cache item
            item = CacheItem(
                key=key,
                value=value,
                item_type=item_type,
                created_at=time.time(),
                last_accessed=time.time(),
                ttl=ttl,
                size_bytes=size_bytes
            )
            
            # Add to cache and update memory usage
            self._cache[key] = item
            self._cache.move_to_end(key)  # Move to end (most recently used)
            self._current_memory_usage += size_bytes
            
            # Enforce cache size limits
            self._enforce_limits()
    
    def _remove_item(self, key: str) -> None:
        """Remove an item from the cache and update memory usage."""
        if key in self._cache:
            item = self._cache[key]
            self._current_memory_usage -= item.size_bytes
            del self._cache[key]
    
    def _enforce_limits(self) -> None:
        """Enforce cache size and memory limits by evicting items if necessary."""
        # First, enforce max items limit
        while len(self._cache) > self._max_size:
            oldest_key, _ = self._cache.popitem(last=False)  # Remove oldest item
            if self._enable_stats:
                self._evictions += 1
        
        # Then, enforce memory limit
        while self._current_memory_usage > self._max_memory_bytes and self._cache:
            oldest_key, _ = self._cache.popitem(last=False)  # Remove oldest item
            if self._enable_stats:
                self._memory_evictions += 1
    
    def remove(self, key: str) -> bool:
        """
        Explicitly remove an item from the cache.
        
        Args:
            key: Cache key to remove
            
        Returns:
            True if the key was in the cache, False otherwise
        """
        with self._lock:
            if key in self._cache:
                self._remove_item(key)
                return True
            return False
    
    def clear(self) -> None:
        """Clear all items from the cache."""
        with self._lock:
            self._cache.clear()
            self._current_memory_usage = 0
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired items from the cache.
        
        Returns:
            Number of items removed
        """
        removed_count = 0
        with self._lock:
            expired_keys = [key for key, item in self._cache.items() if item.is_expired()]
            for key in expired_keys:
                self._remove_item(key)
                removed_count += 1
                if self._enable_stats:
                    self._expirations += 1
            return removed_count
    
    def _periodic_cleanup(self) -> None:
        """Periodically clean up expired items."""
        while not self._stop_cleanup.is_set():
            time.sleep(self._cleanup_interval)
            try:
                removed = self.cleanup_expired()
                if removed > 0:
                    logger.debug(f"Periodic cleanup removed {removed} expired cache items")
            except Exception as e:
                logger.error(f"Error during periodic cache cleanup: {e}")
    
    def stop(self) -> None:
        """Stop the periodic cleanup thread."""
        self._stop_cleanup.set()
        self._cleanup_thread.join(timeout=1.0)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary of cache statistics
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests) if total_requests > 0 else 0
            
            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "memory_usage_mb": self._current_memory_usage / (1024 * 1024),
                "max_memory_mb": self._max_memory_bytes / (1024 * 1024),
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "evictions": self._evictions,
                "memory_evictions": self._memory_evictions,
                "expirations": self._expirations
            }
    
    def get_items_by_type(self) -> Dict[CacheItemType, int]:
        """
        Get count of cached items by type.
        
        Returns:
            Dictionary mapping item types to counts
        """
        with self._lock:
            result = {}
            for item in self._cache.values():
                if item.item_type not in result:
                    result[item.item_type] = 0
                result[item.item_type] += 1
            return result


class CacheManager:
    """
    Centralized cache manager for the Quantum Financial API.
    
    Manages different caches for different types of data with appropriate
    configuration for each.
    """
    
    def __init__(
        self,
        max_results_size: int = 1000,
        max_results_memory_mb: float = 512,
        max_states_size: int = 100,
        max_states_memory_mb: float = 1024,
        results_ttl: float = 3600,  # 1 hour
        states_ttl: float = 1800    # 30 minutes
    ):
        """
        Initialize the cache manager.
        
        Args:
            max_results_size: Maximum number of result items
            max_results_memory_mb: Maximum memory for results in MB
            max_states_size: Maximum number of state items
            max_states_memory_mb: Maximum memory for states in MB
            results_ttl: TTL for result items in seconds
            states_ttl: TTL for state items in seconds
        """
        # Create separate caches for different types of data
        self.results_cache = LRUCache(
            max_size=max_results_size,
            max_memory_mb=max_results_memory_mb,
            default_ttl=results_ttl
        )
        
        self.states_cache = LRUCache(
            max_size=max_states_size,
            max_memory_mb=max_states_memory_mb,
            default_ttl=states_ttl
        )
        
        logger.info(
            f"Initialized CacheManager with results cache: {max_results_size} items, "
            f"{max_results_memory_mb}MB and states cache: {max_states_size} items, "
            f"{max_states_memory_mb}MB"
        )
    
    def get_result(self, key: str) -> Optional[Any]:
        """Get a result from the results cache."""
        return self.results_cache.get(key)
    
    def put_result(
        self,
        key: str,
        value: Any,
        item_type: CacheItemType,
        ttl: Optional[float] = None
    ) -> None:
        """Add a result to the results cache."""
        self.results_cache.put(key, value, item_type, ttl)
    
    def get_state(self, key: str) -> Optional[Any]:
        """Get a state from the states cache."""
        return self.states_cache.get(key)
    
    def put_state(
        self,
        key: str,
        value: Any,
        item_type: CacheItemType,
        ttl: Optional[float] = None
    ) -> None:
        """Add a state to the states cache."""
        self.states_cache.put(key, value, item_type, ttl)
    
    def clear_all(self) -> None:
        """Clear all caches."""
        self.results_cache.clear()
        self.states_cache.clear()
        logger.info("All caches cleared")
    
    def clear(self) -> None:
        """Clear all caches (alias for clear_all)."""
        self.clear_all()
    
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all caches."""
        return {
            "results": self.results_cache.get_stats(),
            "states": self.states_cache.get_stats()
        }
    
    def shutdown(self) -> None:
        """Shut down the cache manager and stop all background tasks."""
        self.results_cache.stop()
        self.states_cache.stop()
        logger.info("Cache manager shutdown complete")


# Singleton instance
_cache_manager = None
_cache_manager_lock = threading.Lock()


def get_cache_manager() -> CacheManager:
    """
    Get the global cache manager instance.
    
    Returns:
        Singleton CacheManager instance
    """
    global _cache_manager
    
    if _cache_manager is None:
        with _cache_manager_lock:
            if _cache_manager is None:
                _cache_manager = CacheManager()
    
    return _cache_manager 