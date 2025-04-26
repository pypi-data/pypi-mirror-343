#!/usr/bin/env python3

"""
Quantum Financial API - Memory Optimizer

Provides memory optimization strategies for handling large datasets and
quantum states in the Quantum Financial API.

This module enables:
- Lazy loading of large datasets
- Efficient memory pooling
- Data compression techniques
- Automatic garbage collection control
- Smart object lifecycle management
"""

import os
import gc
import sys
import logging
import numpy as np
import weakref
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, TypeVar, Generic, Set
from dataclasses import dataclass, field
from enum import Enum
import threading
import time
import psutil
import zlib
import pickle
import io
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type variables for generics
T = TypeVar('T')  # Input type


class DataCompressionLevel(Enum):
    """Data compression levels for memory optimization."""
    NONE = 0
    LOW = 1
    MEDIUM = 5
    HIGH = 9


class MemoryOptimizationStrategy(Enum):
    """Memory optimization strategies."""
    LAZY_LOADING = "lazy_loading"
    COMPRESSION = "compression"
    MEMORY_POOLING = "memory_pooling"
    CHUNK_PROCESSING = "chunk_processing"
    SELECTIVE_CACHING = "selective_caching"


@dataclass
class CompressionStats:
    """Statistics about compression results."""
    original_size_bytes: int
    compressed_size_bytes: int
    compression_ratio: float
    compression_time_ms: float
    decompression_time_ms: float = 0.0
    method: str = "zlib"
    
    @property
    def size_reduction_percent(self) -> float:
        """Calculate size reduction as a percentage."""
        return (1 - (self.compressed_size_bytes / self.original_size_bytes)) * 100


class MemoryUsageTracker:
    """
    Tracks memory usage changes during operations.
    
    This is useful for measuring memory impact of specific operations
    and optimizing memory-intensive functions.
    """
    
    def __init__(self, label: str = ""):
        """
        Initialize memory usage tracker.
        
        Args:
            label: Label for this tracking session
        """
        self.label = label
        self.start_memory = 0
        self.end_memory = 0
        self.peak_memory = 0
        self.is_tracking = False
        self._monitoring_thread = None
        self._stop_monitoring = threading.Event()
    
    def start(self) -> None:
        """Start tracking memory usage."""
        # Force garbage collection before measuring
        gc.collect()
        
        # Get initial memory usage
        process = psutil.Process()
        self.start_memory = process.memory_info().rss
        self.peak_memory = self.start_memory
        self.is_tracking = True
        
        # Start monitoring thread to track peak memory
        self._stop_monitoring.clear()
        self._monitoring_thread = threading.Thread(
            target=self._monitor_memory,
            daemon=True
        )
        self._monitoring_thread.start()
        
        logger.debug(
            f"Started memory tracking{f' for {self.label}' if self.label else ''} "
            f"from {self.start_memory / (1024 * 1024):.2f}MB"
        )
    
    def stop(self) -> Dict[str, float]:
        """
        Stop tracking memory usage and return statistics.
        
        Returns:
            Dictionary with memory usage statistics
        """
        if not self.is_tracking:
            return {}
        
        # Stop monitoring thread
        self._stop_monitoring.set()
        if self._monitoring_thread:
            self._monitoring_thread.join(timeout=1.0)
        
        # Force garbage collection before measuring final memory
        gc.collect()
        
        # Get final memory usage
        process = psutil.Process()
        self.end_memory = process.memory_info().rss
        
        # Calculate difference
        diff_bytes = self.end_memory - self.start_memory
        diff_mb = diff_bytes / (1024 * 1024)
        peak_diff_bytes = self.peak_memory - self.start_memory
        peak_diff_mb = peak_diff_bytes / (1024 * 1024)
        
        self.is_tracking = False
        
        logger.debug(
            f"Stopped memory tracking{f' for {self.label}' if self.label else ''}: "
            f"change = {diff_mb:+.2f}MB, peak = {peak_diff_mb:+.2f}MB"
        )
        
        return {
            "start_bytes": self.start_memory,
            "end_bytes": self.end_memory,
            "diff_bytes": diff_bytes,
            "peak_bytes": self.peak_memory,
            "peak_diff_bytes": peak_diff_bytes,
            "start_mb": self.start_memory / (1024 * 1024),
            "end_mb": self.end_memory / (1024 * 1024),
            "diff_mb": diff_mb,
            "peak_mb": self.peak_memory / (1024 * 1024),
            "peak_diff_mb": peak_diff_mb
        }
    
    def _monitor_memory(self) -> None:
        """Monitor memory usage in a background thread to track peak memory."""
        process = psutil.Process()
        
        while not self._stop_monitoring.is_set():
            try:
                # Get current memory usage
                current_memory = process.memory_info().rss
                
                # Update peak if higher
                if current_memory > self.peak_memory:
                    self.peak_memory = current_memory
            
            except Exception as e:
                logger.error(f"Error in memory monitoring: {e}")
            
            # Sleep briefly
            time.sleep(0.1)
    
    @contextmanager
    def track(self):
        """Context manager for tracking memory usage during a block of code."""
        self.start()
        try:
            yield
        finally:
            self.stop()


class LazyDataLoader(Generic[T]):
    """
    Enables lazy loading of large datasets to optimize memory usage.
    
    Data is only loaded when needed and can be automatically unloaded
    when memory pressure is high.
    """
    
    def __init__(
        self,
        loader_func: Callable[[], T],
        item_name: str = "",
        auto_unload_threshold_mb: float = 1024  # 1GB default
    ):
        """
        Initialize lazy data loader.
        
        Args:
            loader_func: Function that loads the data
            item_name: Name of the data item for logging
            auto_unload_threshold_mb: Memory threshold in MB for auto-unloading
        """
        self._loader_func = loader_func
        self._item_name = item_name
        self._auto_unload_threshold_mb = auto_unload_threshold_mb
        self._data: Optional[T] = None
        self._data_size_bytes = 0
        self._is_loaded = False
        self._lock = threading.RLock()
        self._last_accessed = 0.0
    
    @property
    def data(self) -> T:
        """
        Get the data, loading it if necessary.
        
        Returns:
            The loaded data
        """
        with self._lock:
            if not self._is_loaded:
                self._load_data()
            
            self._last_accessed = time.time()
            assert self._data is not None, "LazyDataLoader _data should not be None after loading"
            return self._data
    
    @property
    def is_loaded(self) -> bool:
        """Check if data is currently loaded."""
        return self._is_loaded
    
    @property
    def data_size_mb(self) -> float:
        """Get the size of the data in MB."""
        return self._data_size_bytes / (1024 * 1024)
    
    def _load_data(self) -> None:
        """Load the data using the loader function."""
        logger.debug(f"Loading lazy data{f' ({self._item_name})' if self._item_name else ''}...")
        
        # Track memory usage during loading
        memory_tracker = MemoryUsageTracker(f"lazy_load_{self._item_name}")
        memory_tracker.start()
        
        # Load data
        self._data = self._loader_func()
        self._is_loaded = True
        
        # Estimate data size
        stats = memory_tracker.stop()
        self._data_size_bytes = stats["diff_bytes"]
        
        logger.debug(
            f"Loaded lazy data{f' ({self._item_name})' if self._item_name else ''} "
            f"size: {self.data_size_mb:.2f}MB"
        )
    
    def unload(self) -> None:
        """Unload the data to free memory."""
        with self._lock:
            if self._is_loaded:
                logger.debug(
                    f"Unloading lazy data{f' ({self._item_name})' if self._item_name else ''} "
                    f"size: {self.data_size_mb:.2f}MB"
                )
                self._data = None
                self._is_loaded = False
                gc.collect()  # Force garbage collection
    
    def check_memory_pressure(self) -> bool:
        """
        Check if memory pressure is high and unload if necessary.
        
        Returns:
            True if data was unloaded, False otherwise
        """
        with self._lock:
            if not self._is_loaded:
                return False
            
            # Check current memory usage
            memory = psutil.virtual_memory()
            available_mb = memory.available / (1024 * 1024)
            
            # If available memory is less than threshold, unload
            if available_mb < self._auto_unload_threshold_mb:
                logger.info(
                    f"Unloading lazy data due to memory pressure "
                    f"(available: {available_mb:.2f}MB, threshold: {self._auto_unload_threshold_mb:.2f}MB)"
                )
                self.unload()
                return True
            
            return False


class DataCompressor:
    """
    Provides data compression utilities to reduce memory usage.
    
    Supports various compression methods and compression levels
    to balance between memory usage and performance.
    """
    
    def __init__(
        self,
        compression_level: DataCompressionLevel = DataCompressionLevel.MEDIUM
    ):
        """
        Initialize data compressor.
        
        Args:
            compression_level: Compression level to use
        """
        self.compression_level = compression_level
    
    def compress_data(
        self,
        data: Any,
        compression_level: Optional[DataCompressionLevel] = None
    ) -> Tuple[bytes, CompressionStats]:
        """
        Compress data using pickle and zlib.
        
        Args:
            data: Data to compress
            compression_level: Override default compression level
            
        Returns:
            Tuple of (compressed_data, compression_stats)
        """
        level = compression_level.value if compression_level else self.compression_level.value
        
        if level == DataCompressionLevel.NONE.value:
            # Skip compression if level is NONE
            serialized = pickle.dumps(data)
            return serialized, CompressionStats(
                original_size_bytes=len(serialized),
                compressed_size_bytes=len(serialized),
                compression_ratio=1.0,
                compression_time_ms=0.0
            )
        
        # Measure original size and compression time
        start_time = time.time()
        serialized = pickle.dumps(data)
        original_size = len(serialized)
        
        # Compress the serialized data
        compressed = zlib.compress(serialized, level=level)
        compression_time_ms = (time.time() - start_time) * 1000
        
        # Calculate compression ratio
        compressed_size = len(compressed)
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 1.0
        
        stats = CompressionStats(
            original_size_bytes=original_size,
            compressed_size_bytes=compressed_size,
            compression_ratio=compression_ratio,
            compression_time_ms=compression_time_ms
        )
        
        logger.debug(
            f"Compressed data: {stats.original_size_bytes / (1024*1024):.2f}MB -> "
            f"{stats.compressed_size_bytes / (1024*1024):.2f}MB "
            f"(ratio: {stats.compression_ratio:.2f}x, {stats.size_reduction_percent:.1f}% reduction)"
        )
        
        return compressed, stats
    
    def decompress_data(self, compressed_data: bytes) -> Tuple[Any, float]:
        """
        Decompress data that was compressed with compress_data.
        
        Args:
            compressed_data: Compressed data bytes
            
        Returns:
            Tuple of (decompressed_data, decompression_time_ms)
        """
        # Skip decompression if data is not compressed (e.g., NONE level)
        if self.compression_level == DataCompressionLevel.NONE:
            try:
                # Try to unpickle directly
                data = pickle.loads(compressed_data)
                return data, 0.0
            except Exception:
                # If it fails, it's probably compressed
                pass
        
        # Measure decompression time
        start_time = time.time()
        
        try:
            # Decompress
            decompressed = zlib.decompress(compressed_data)
            
            # Deserialize
            data = pickle.loads(decompressed)
            
            decompression_time_ms = (time.time() - start_time) * 1000
            
            return data, decompression_time_ms
        except Exception as e:
            # Handle case where data might not be compressed
            try:
                data = pickle.loads(compressed_data)
                decompression_time_ms = (time.time() - start_time) * 1000
                return data, decompression_time_ms
            except Exception:
                # Re-raise the original exception if both attempts fail
                raise e


class ChunkProcessor(Generic[T]):
    """
    Processes large datasets in manageable chunks to reduce memory usage.
    
    This is useful for operations on large arrays or dataframes that
    would otherwise consume too much memory if processed all at once.
    """
    
    def __init__(
        self, 
        chunk_size: int = 1000, 
        max_workers: int = 4
    ):
        """
        Initialize chunk processor.
        
        Args:
            chunk_size: Number of items in each chunk
            max_workers: Maximum number of parallel workers for chunk processing
        """
        self.chunk_size = chunk_size
        self.max_workers = max_workers
    
    def process_in_chunks(
        self,
        data: List[T],
        process_func: Callable[[List[T]], Any],
        combine_func: Callable[[List[Any]], Any]
    ) -> Any:
        """
        Process a large dataset in chunks.
        
        Args:
            data: Large dataset to process
            process_func: Function to process each chunk of data
            combine_func: Function to combine results from all chunks
            
        Returns:
            Combined result from all chunks
        """
        # Split data into chunks
        chunks = self._split_into_chunks(data)
        
        logger.debug(f"Processing {len(data)} items in {len(chunks)} chunks")
        
        # Process each chunk
        chunk_results = []
        
        if self.max_workers > 1:
            # Process chunks in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                chunk_results = list(executor.map(process_func, chunks))
        else:
            # Process chunks sequentially
            for chunk in chunks:
                chunk_results.append(process_func(chunk))
        
        # Combine results
        result = combine_func(chunk_results)
        
        return result
    
    def _split_into_chunks(self, data: List[T]) -> List[List[T]]:
        """
        Split data into chunks of specified size.
        
        Args:
            data: Data to split into chunks
            
        Returns:
            List of data chunks
        """
        return [data[i:i + self.chunk_size] for i in range(0, len(data), self.chunk_size)]


class MemoryOptimizer:
    """
    Central manager for memory optimization strategies in the Quantum Financial API.
    
    Provides tools for managing memory usage across different components and
    automatically applies optimization techniques based on system state and configuration.
    """
    
    def __init__(
        self,
        enable_compression: bool = True,
        enable_lazy_loading: bool = True,
        enable_chunk_processing: bool = True,
        compression_level: DataCompressionLevel = DataCompressionLevel.MEDIUM,
        chunk_size: int = 1000,
        memory_warning_threshold_percent: float = 75.0,
        memory_critical_threshold_percent: float = 90.0
    ):
        """
        Initialize memory optimizer.
        
        Args:
            enable_compression: Whether to enable data compression
            enable_lazy_loading: Whether to enable lazy loading
            enable_chunk_processing: Whether to enable chunk processing
            compression_level: Default compression level
            chunk_size: Default chunk size for chunk processing
            memory_warning_threshold_percent: Memory usage percentage for warning
            memory_critical_threshold_percent: Memory usage percentage for critical actions
        """
        self.enable_compression = enable_compression
        self.enable_lazy_loading = enable_lazy_loading
        self.enable_chunk_processing = enable_chunk_processing
        self.compression_level = compression_level
        self.chunk_size = chunk_size
        self.memory_warning_threshold_percent = memory_warning_threshold_percent
        self.memory_critical_threshold_percent = memory_critical_threshold_percent
        
        # Initialize components
        self.compressor = DataCompressor(compression_level=compression_level)
        self.chunk_processor = ChunkProcessor(chunk_size=chunk_size)
        
        # Track lazy-loaded objects for memory management
        self.lazy_objects: Dict[str, LazyDataLoader] = {}
        self._lazy_objects_lock = threading.RLock()
        
        # Memory monitoring
        self._memory_monitor_thread = None
        self._stop_memory_monitor = threading.Event()
        
        # Start memory monitoring
        self._start_memory_monitor()
        
        logger.info(
            f"Initialized MemoryOptimizer (compression: {'enabled' if enable_compression else 'disabled'}, "
            f"lazy loading: {'enabled' if enable_lazy_loading else 'disabled'}, "
            f"chunk processing: {'enabled' if enable_chunk_processing else 'disabled'})"
        )
    
    def _start_memory_monitor(self) -> None:
        """Start the memory monitoring thread."""
        if self._memory_monitor_thread is None:
            self._stop_memory_monitor.clear()
            self._memory_monitor_thread = threading.Thread(
                target=self._monitor_memory,
                daemon=True
            )
            self._memory_monitor_thread.start()
            logger.debug("Memory monitoring thread started")
    
    def _monitor_memory(self) -> None:
        """Periodically monitor memory usage and take action if needed."""
        while not self._stop_memory_monitor.is_set():
            try:
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # Take action based on memory usage
                if memory_percent >= self.memory_critical_threshold_percent:
                    try:
                        logger.warning(
                            f"Critical memory usage: {memory_percent:.1f}% - "
                            f"taking aggressive action"
                        )
                    except Exception:
                        pass
                    self._handle_critical_memory()
                elif memory_percent >= self.memory_warning_threshold_percent:
                    try:
                        logger.info(
                            f"High memory usage: {memory_percent:.1f}% - "
                            f"taking preventive action"
                        )
                    except Exception:
                        pass
                    self._handle_high_memory()
            
            except Exception as e:
                try:
                    logger.error(f"Error in memory monitoring: {e}")
                except Exception:
                    pass
            
            # Wait before next check
            self._stop_memory_monitor.wait(10.0)  # Check every 10 seconds
    
    def _handle_high_memory(self) -> None:
        """Handle high memory usage by taking preventive action."""
        # Unload some lazy-loaded objects
        with self._lazy_objects_lock:
            # Sort by last access time (oldest first)
            sorted_objects = sorted(
                self.lazy_objects.items(),
                key=lambda x: x[1]._last_accessed
            )
            
            # Unload up to 25% of objects
            unload_count = max(1, len(sorted_objects) // 4)
            
            for i, (key, obj) in enumerate(sorted_objects):
                if i >= unload_count:
                    break
                    
                if obj.is_loaded:
                    logger.info(f"Unloading lazy object {key} due to high memory usage")
                    obj.unload()
        
        # Force garbage collection
        gc.collect()
    
    def _handle_critical_memory(self) -> None:
        """Handle critical memory usage by taking aggressive action."""
        # Unload all lazy-loaded objects
        with self._lazy_objects_lock:
            for key, obj in self.lazy_objects.items():
                if obj.is_loaded:
                    logger.warning(f"Unloading lazy object {key} due to critical memory usage")
                    obj.unload()
        
        # Force garbage collection
        gc.collect()
        
        # Log memory state
        memory = psutil.virtual_memory()
        logger.info(
            f"Memory state after critical action: {memory.percent:.1f}% used, "
            f"{memory.available / (1024*1024):.2f}MB available"
        )
    
    def register_lazy_object(self, key: str, lazy_loader: LazyDataLoader) -> None:
        """
        Register a lazy-loaded object for memory management.
        
        Args:
            key: Unique key for the object
            lazy_loader: LazyDataLoader instance
        """
        with self._lazy_objects_lock:
            self.lazy_objects[key] = lazy_loader
            logger.debug(f"Registered lazy object: {key}")
    
    def unregister_lazy_object(self, key: str) -> None:
        """
        Unregister a lazy-loaded object.
        
        Args:
            key: Key of the object to unregister
        """
        with self._lazy_objects_lock:
            if key in self.lazy_objects:
                # Unload if loaded
                lazy_obj = self.lazy_objects[key]
                if lazy_obj.is_loaded:
                    lazy_obj.unload()
                
                # Remove from registry
                del self.lazy_objects[key]
                logger.debug(f"Unregistered lazy object: {key}")
    
    def create_lazy_loader(
        self, 
        loader_func: Callable[[], T], 
        item_name: str,
        auto_register: bool = True
    ) -> LazyDataLoader[T]:
        """
        Create a new lazy data loader.
        
        Args:
            loader_func: Function that loads the data
            item_name: Name of the data item for logging and registration
            auto_register: Whether to automatically register the lazy loader
            
        Returns:
            New LazyDataLoader instance
        """
        lazy_loader = LazyDataLoader(loader_func, item_name)
        
        if auto_register and self.enable_lazy_loading:
            self.register_lazy_object(item_name, lazy_loader)
        
        return lazy_loader
    
    def compress_data(
        self, 
        data: Any, 
        compression_level: Optional[DataCompressionLevel] = None
    ) -> Tuple[bytes, CompressionStats]:
        """
        Compress data to reduce memory usage.
        
        Args:
            data: Data to compress
            compression_level: Override default compression level
            
        Returns:
            Tuple of (compressed_data, compression_stats)
        """
        if not self.enable_compression:
            # Skip compression if disabled
            serialized = pickle.dumps(data)
            return serialized, CompressionStats(
                original_size_bytes=len(serialized),
                compressed_size_bytes=len(serialized),
                compression_ratio=1.0,
                compression_time_ms=0.0
            )
        
        return self.compressor.compress_data(data, compression_level)
    
    def decompress_data(self, compressed_data: bytes) -> Any:
        """
        Decompress data that was compressed with compress_data.
        
        Args:
            compressed_data: Compressed data bytes
            
        Returns:
            Decompressed data
        """
        data, _ = self.compressor.decompress_data(compressed_data)
        return data
    
    def process_in_chunks(
        self,
        data: List[T],
        process_func: Callable[[List[T]], Any],
        combine_func: Callable[[List[Any]], Any],
        chunk_size: Optional[int] = None
    ) -> Any:
        """
        Process a large dataset in chunks to reduce memory usage.
        
        Args:
            data: Large dataset to process
            process_func: Function to process each chunk of data
            combine_func: Function to combine results from all chunks
            chunk_size: Override default chunk size
            
        Returns:
            Combined result from all chunks
        """
        if not self.enable_chunk_processing:
            # Process all at once if chunk processing is disabled
            return process_func(data)
        
        # Use custom or default chunk size
        if chunk_size is not None:
            old_chunk_size = self.chunk_processor.chunk_size
            self.chunk_processor.chunk_size = chunk_size
            result = self.chunk_processor.process_in_chunks(data, process_func, combine_func)
            self.chunk_processor.chunk_size = old_chunk_size
            return result
        
        return self.chunk_processor.process_in_chunks(data, process_func, combine_func)
    
    @contextmanager
    def track_memory_usage(self, label: str):
        """
        Context manager for tracking memory usage during a block of code.
        
        Args:
            label: Label for the tracking session
        """
        tracker = MemoryUsageTracker(label)
        tracker.start()
        try:
            yield tracker
        finally:
            tracker.stop()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get current memory statistics.
        
        Returns:
            Dictionary with memory statistics
        """
        memory = psutil.virtual_memory()
        process = psutil.Process()
        process_memory = process.memory_info()
        
        return {
            "system": {
                "total_mb": memory.total / (1024 * 1024),
                "available_mb": memory.available / (1024 * 1024),
                "used_mb": memory.used / (1024 * 1024),
                "percent": memory.percent
            },
            "process": {
                "rss_mb": process_memory.rss / (1024 * 1024),
                "vms_mb": process_memory.vms / (1024 * 1024),
                "percent": process.memory_percent()
            },
            "lazy_objects": {
                "total": len(self.lazy_objects),
                "loaded": sum(1 for obj in self.lazy_objects.values() if obj.is_loaded)
            },
            "thresholds": {
                "warning_percent": self.memory_warning_threshold_percent,
                "critical_percent": self.memory_critical_threshold_percent
            }
        }
    
    def force_garbage_collection(self) -> Dict[str, Any]:
        """
        Force garbage collection and return statistics.
        
        Returns:
            Dictionary with garbage collection statistics
        """
        # Get memory before GC
        memory_before = psutil.Process().memory_info().rss
        
        # Get object counts before GC
        objects_before = len(gc.get_objects())
        
        # Force garbage collection
        gc.collect()
        
        # Get memory after GC
        memory_after = psutil.Process().memory_info().rss
        
        # Get object counts after GC
        objects_after = len(gc.get_objects())
        
        memory_diff = memory_before - memory_after
        objects_diff = objects_before - objects_after
        
        logger.info(
            f"Forced garbage collection: freed {memory_diff / (1024*1024):.2f}MB, "
            f"collected {objects_diff} objects"
        )
        
        return {
            "memory_before_bytes": memory_before,
            "memory_after_bytes": memory_after,
            "memory_diff_bytes": memory_diff,
            "memory_diff_mb": memory_diff / (1024 * 1024),
            "objects_before": objects_before,
            "objects_after": objects_after,
            "objects_diff": objects_diff
        }
    
    def shutdown(self) -> None:
        """Shut down the memory optimizer and release resources."""
        logger.info("Shutting down memory optimizer")
        
        # Stop memory monitoring
        self._stop_memory_monitor.set()
        if self._memory_monitor_thread:
            self._memory_monitor_thread.join(timeout=2.0)
            self._memory_monitor_thread = None
        
        # Unload all lazy objects
        with self._lazy_objects_lock:
            for key, obj in list(self.lazy_objects.items()):
                if obj.is_loaded:
                    obj.unload()
                self.lazy_objects.pop(key, None)
        
        # Force final garbage collection
        gc.collect()
        
        logger.info("Memory optimizer shutdown complete")


# Singleton instance
_memory_optimizer = None
_optimizer_lock = threading.Lock()


def get_memory_optimizer() -> MemoryOptimizer:
    """
    Get the global memory optimizer instance.
    
    Returns:
        Singleton MemoryOptimizer instance
    """
    global _memory_optimizer
    
    if _memory_optimizer is None:
        with _optimizer_lock:
            if _memory_optimizer is None:
                _memory_optimizer = MemoryOptimizer()
    
    return _memory_optimizer 