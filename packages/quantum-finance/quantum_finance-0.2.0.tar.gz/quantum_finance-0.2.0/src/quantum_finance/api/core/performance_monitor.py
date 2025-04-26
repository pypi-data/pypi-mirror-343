#!/usr/bin/env python3

"""
Quantum Financial API - Performance Monitor

Provides comprehensive performance monitoring and profiling capabilities
for the Quantum Financial API, tracking execution times, memory usage,
and resource utilization across components.

This module enables:
- Function execution time tracking
- Memory usage monitoring
- Component-level performance insights
- Visualization of performance bottlenecks
- Historical performance trend analysis
"""

import os
import time
import logging
import threading
import functools
import json
import numpy as np
import psutil
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, TypeVar, cast
from dataclasses import dataclass, field, asdict
import uuid
from datetime import datetime, timedelta
from collections import deque
from enum import Enum
import traceback
import gc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type variables for generics
F = TypeVar('F', bound=Callable[..., Any])


class PerformanceMetricType(Enum):
    """Types of performance metrics tracked."""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    CACHE_HITS = "cache_hits"
    CACHE_MISSES = "cache_misses"
    TASK_COUNT = "task_count"


class ComponentType(Enum):
    """Components in the Quantum Financial API."""
    ADAPTIVE_LEARNING = "adaptive_learning"
    MARKET_ENCODING = "market_encoding"
    PHASE_TRACKING = "phase_tracking"
    QUANTUM_DIFFUSION = "quantum_diffusion"
    STOCHASTIC_SIMULATION = "stochastic_simulation"
    API_CORE = "api_core"
    CACHE_MANAGER = "cache_manager"
    PARALLEL_MANAGER = "parallel_manager"
    

@dataclass
class PerformanceMetric:
    """
    Represents a single performance measurement with metadata.
    """
    metric_id: str
    metric_type: PerformanceMetricType
    component: ComponentType
    function_name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result['metric_type'] = self.metric_type.value
        result['component'] = self.component.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PerformanceMetric':
        """Create from dictionary."""
        # Convert string enums back to enum objects
        data['metric_type'] = PerformanceMetricType(data['metric_type'])
        data['component'] = ComponentType(data['component'])
        return cls(**data)


class PerformanceMonitor:
    """
    Monitors and records performance metrics for the Quantum Financial API.
    
    Provides decorators and context managers for tracking performance of
    functions and code blocks, as well as methods for analyzing and
    visualizing performance data.
    """
    
    def __init__(
        self,
        enabled: bool = True,
        max_history_size: int = 10000,
        log_threshold_ms: float = 1000.0,  # Log slow functions (>1000ms)
        memory_check_interval: float = 5.0  # Check memory every 5 seconds
    ):
        """
        Initialize the performance monitor.
        
        Args:
            enabled: Whether monitoring is enabled
            max_history_size: Maximum number of metrics to keep in memory
            log_threshold_ms: Threshold in ms for logging slow function calls
            memory_check_interval: How often to check memory usage (seconds)
        """
        self.enabled = enabled
        self.max_history_size = max_history_size
        self.log_threshold_ms = log_threshold_ms
        self.memory_check_interval = memory_check_interval
        
        # Store metrics in a thread-safe way
        self._metrics: deque = deque(maxlen=max_history_size)
        self._metrics_lock = threading.RLock()
        
        # Memory monitoring
        self._memory_monitor_thread = None
        self._stop_memory_monitor = threading.Event()
        self._baseline_memory = None
        
        # Start memory monitoring if enabled
        if self.enabled:
            self._start_memory_monitor()
            self._record_baseline_memory()
        
        logger.info(f"Performance monitoring {'enabled' if enabled else 'disabled'}")
    
    def _record_baseline_memory(self):
        """Record baseline memory usage."""
        # Force garbage collection to get accurate reading
        gc.collect()
        self._baseline_memory = psutil.Process().memory_info().rss
        logger.debug(f"Baseline memory: {self._baseline_memory / (1024*1024):.2f}MB")
    
    def _start_memory_monitor(self):
        """Start the memory monitoring thread."""
        if self._memory_monitor_thread is None:
            self._stop_memory_monitor.clear()
            self._memory_monitor_thread = threading.Thread(
                target=self._monitor_memory,
                daemon=True
            )
            self._memory_monitor_thread.start()
            logger.debug("Memory monitoring thread started")
    
    def _monitor_memory(self):
        """Periodically monitor memory usage."""
        while not self._stop_memory_monitor.is_set():
            try:
                process = psutil.Process()
                memory_info = process.memory_info()
                
                # Record memory usage for the process
                self.record_metric(
                    metric_type=PerformanceMetricType.MEMORY_USAGE,
                    component=ComponentType.API_CORE,
                    function_name="process_total",
                    value=memory_info.rss / (1024 * 1024),  # Convert to MB
                    metadata={
                        "vms": memory_info.vms / (1024 * 1024),
                        "percent": process.memory_percent()
                    }
                )
                
                # Record CPU usage
                self.record_metric(
                    metric_type=PerformanceMetricType.CPU_USAGE,
                    component=ComponentType.API_CORE,
                    function_name="process_total",
                    value=process.cpu_percent(),
                    metadata={
                        "system_cpu": psutil.cpu_percent(),
                        "num_threads": process.num_threads()
                    }
                )
                
            except Exception as e:
                logger.error(f"Error in memory monitoring: {e}")
            
            # Wait for next interval
            self._stop_memory_monitor.wait(self.memory_check_interval)
    
    def record_metric(
        self,
        metric_type: PerformanceMetricType,
        component: ComponentType,
        function_name: str,
        value: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record a performance metric.
        
        Args:
            metric_type: Type of metric
            component: Component being measured
            function_name: Function or operation name
            value: Metric value
            metadata: Additional contextual information
        """
        if not self.enabled:
            return
            
        metric = PerformanceMetric(
            metric_id=str(uuid.uuid4()),
            metric_type=metric_type,
            component=component,
            function_name=function_name,
            value=value,
            metadata=metadata or {}
        )
        
        with self._metrics_lock:
            self._metrics.append(metric)
        
        # Log slow function calls
        if (metric_type == PerformanceMetricType.EXECUTION_TIME and 
                value * 1000 >= self.log_threshold_ms):
            logger.warning(
                f"Slow function: {component.value}.{function_name} "
                f"took {value:.2f}s to execute"
            )
    
    def function_timer(
        self, 
        component: ComponentType
    ) -> Callable[[F], F]:
        """
        Decorator to measure function execution time.
        
        Args:
            component: Component the function belongs to
            
        Returns:
            Decorator function
        """
        def decorator(func: F) -> F:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)
                
                start_time = time.time()
                try:
                    # Record memory before
                    process = psutil.Process()
                    memory_before = process.memory_info().rss
                    
                    # Execute function
                    result = func(*args, **kwargs)
                    
                    # Calculate execution time
                    execution_time = time.time() - start_time
                    
                    # Record memory after and calculate difference
                    memory_after = process.memory_info().rss
                    memory_diff = memory_after - memory_before
                    
                    # Record execution time metric
                    self.record_metric(
                        metric_type=PerformanceMetricType.EXECUTION_TIME,
                        component=component,
                        function_name=func.__name__,
                        value=execution_time,
                        metadata={
                            "memory_diff_bytes": memory_diff,
                            "memory_diff_mb": memory_diff / (1024 * 1024),
                            "args_count": len(args),
                            "kwargs_count": len(kwargs)
                        }
                    )
                    
                    return result
                except Exception as e:
                    # Calculate execution time even for failures
                    execution_time = time.time() - start_time
                    
                    # Record execution time for failed operation
                    self.record_metric(
                        metric_type=PerformanceMetricType.EXECUTION_TIME,
                        component=component,
                        function_name=func.__name__,
                        value=execution_time,
                        metadata={
                            "error": str(e),
                            "error_type": type(e).__name__,
                            "traceback": traceback.format_exc()
                        }
                    )
                    
                    # Re-raise the exception
                    raise
                    
            return cast(F, wrapper)
        return decorator
    
    def get_metrics(
        self,
        metric_type: Optional[PerformanceMetricType] = None,
        component: Optional[ComponentType] = None,
        function_name: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        limit: Optional[int] = None
    ) -> List[PerformanceMetric]:
        """
        Get filtered performance metrics.
        
        Args:
            metric_type: Filter by metric type
            component: Filter by component
            function_name: Filter by function name
            start_time: Filter by start time (timestamp)
            end_time: Filter by end time (timestamp)
            limit: Maximum number of metrics to return
            
        Returns:
            List of matching performance metrics
        """
        with self._metrics_lock:
            # Create a copy of metrics to avoid modification during iteration
            metrics = list(self._metrics)
        
        # Apply filters
        if metric_type is not None:
            metrics = [m for m in metrics if m.metric_type == metric_type]
            
        if component is not None:
            metrics = [m for m in metrics if m.component == component]
            
        if function_name is not None:
            metrics = [m for m in metrics if m.function_name == function_name]
            
        if start_time is not None:
            metrics = [m for m in metrics if m.timestamp >= start_time]
            
        if end_time is not None:
            metrics = [m for m in metrics if m.timestamp <= end_time]
        
        # Sort by timestamp (newest first)
        metrics.sort(key=lambda m: m.timestamp, reverse=True)
        
        # Apply limit
        if limit is not None:
            metrics = metrics[:limit]
            
        return metrics
    
    def get_function_stats(
        self,
        component: Optional[ComponentType] = None,
        function_name: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get execution time statistics for functions.
        
        Args:
            component: Filter by component
            function_name: Filter by function name
            start_time: Filter by start time (timestamp)
            end_time: Filter by end time (timestamp)
            
        Returns:
            Dictionary mapping function identifiers to statistics
        """
        # Get execution time metrics
        metrics = self.get_metrics(
            metric_type=PerformanceMetricType.EXECUTION_TIME,
            component=component,
            function_name=function_name,
            start_time=start_time,
            end_time=end_time
        )
        
        # Group by component and function name
        stats: Dict[str, Dict[str, Any]] = {}
        
        for metric in metrics:
            key = f"{metric.component.value}.{metric.function_name}"
            
            if key not in stats:
                stats[key] = {
                    "component": metric.component.value,
                    "function_name": metric.function_name,
                    "count": 0,
                    "total_time": 0.0,
                    "min_time": float('inf'),
                    "max_time": 0.0,
                    "times": []
                }
            
            # Update statistics
            stats[key]["count"] += 1
            stats[key]["total_time"] += metric.value
            stats[key]["min_time"] = min(stats[key]["min_time"], metric.value)
            stats[key]["max_time"] = max(stats[key]["max_time"], metric.value)
            stats[key]["times"].append(metric.value)
        
        # Calculate averages and standard deviations
        for key, stat in stats.items():
            stat["avg_time"] = stat["total_time"] / stat["count"] if stat["count"] > 0 else 0
            
            if len(stat["times"]) > 1:
                stat["std_dev"] = np.std(stat["times"])
            else:
                stat["std_dev"] = 0
                
            # Convert to ms for better readability
            stat["avg_time_ms"] = stat["avg_time"] * 1000
            stat["min_time_ms"] = stat["min_time"] * 1000
            stat["max_time_ms"] = stat["max_time"] * 1000
            stat["std_dev_ms"] = stat["std_dev"] * 1000
            
            # Remove raw times to save memory
            del stat["times"]
            
        return stats
    
    def get_memory_usage_trend(
        self,
        interval_seconds: float = 60.0,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Get memory usage trend over time.
        
        Args:
            interval_seconds: Time interval for grouping measurements
            start_time: Filter by start time (timestamp)
            end_time: Filter by end time (timestamp)
            
        Returns:
            Dictionary with timestamps and memory usage values
        """
        # Get memory usage metrics
        metrics = self.get_metrics(
            metric_type=PerformanceMetricType.MEMORY_USAGE,
            start_time=start_time,
            end_time=end_time
        )
        
        # Sort by timestamp
        metrics.sort(key=lambda m: m.timestamp)
        
        if not metrics:
            return {"timestamps": [], "values": []}
        
        # Group by time intervals
        result = {"timestamps": [], "values": []}
        current_interval = metrics[0].timestamp
        current_values = []
        
        for metric in metrics:
            if metric.timestamp - current_interval > interval_seconds:
                # Move to next interval
                if current_values:
                    # Record average for the interval
                    result["timestamps"].append(current_interval)
                    result["values"].append(np.mean(current_values))
                    
                    # Reset for next interval
                    current_interval = metric.timestamp
                    current_values = []
            
            current_values.append(metric.value)
        
        # Add the last interval if there's data
        if current_values:
            result["timestamps"].append(current_interval)
            result["values"].append(np.mean(current_values))
        
        # Convert timestamps to datetime strings for easier reading
        result["datetime_labels"] = [
            datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            for ts in result["timestamps"]
        ]
        
        return result
    
    def plot_function_performance(
        self,
        top_n: int = 10,
        component: Optional[ComponentType] = None,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot performance of the slowest functions.
        
        Args:
            top_n: Number of slowest functions to show
            component: Filter by component
            save_path: Path to save the plot (None = show plot)
        """
        # Get function statistics
        stats = self.get_function_stats(component=component)
        
        # Sort by average time (descending)
        sorted_stats = sorted(
            stats.items(), 
            key=lambda x: x[1]["avg_time"], 
            reverse=True
        )
        
        # Take top N slowest functions
        top_funcs = sorted_stats[:top_n]
        
        if not top_funcs:
            logger.warning("No function performance data available to plot")
            return
        
        # Prepare data for plotting
        func_names = [f"{s[1]['function_name']}" for s in top_funcs]
        avg_times = [s[1]["avg_time"] * 1000 for s in top_funcs]  # Convert to ms
        max_times = [s[1]["max_time"] * 1000 for s in top_funcs]
        call_counts = [s[1]["count"] for s in top_funcs]
        
        # Create figure with two subplots (execution time and call count)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
        
        # Plot average and max times
        x = np.arange(len(func_names))
        width = 0.35
        
        ax1.bar(x - width/2, avg_times, width, label='Avg Time (ms)')
        ax1.bar(x + width/2, max_times, width, label='Max Time (ms)')
        
        # Add function names and styling
        ax1.set_ylabel('Time (ms)')
        ax1.set_title('Function Performance')
        ax1.set_xticks(x)
        ax1.set_xticklabels(func_names, rotation=45, ha='right')
        ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax1.legend()
        
        # Plot call counts
        ax2.bar(x, call_counts, color='green', alpha=0.7)
        ax2.set_ylabel('Call Count')
        ax2.set_xticks(x)
        ax2.set_xticklabels(func_names, rotation=45, ha='right')
        ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Performance plot saved to {save_path}")
        else:
            plt.show()
    
    def plot_memory_usage(
        self,
        hours: float = 1.0,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot memory usage over time.
        
        Args:
            hours: Number of hours of history to include
            save_path: Path to save the plot (None = show plot)
        """
        # Calculate start time
        end_time = time.time()
        start_time = end_time - (hours * 3600)
        
        # Get memory trend data
        memory_data = self.get_memory_usage_trend(
            interval_seconds=60.0,  # 1-minute intervals
            start_time=start_time,
            end_time=end_time
        )
        
        if not memory_data["timestamps"]:
            logger.warning("No memory usage data available to plot")
            return
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(memory_data["timestamps"], memory_data["values"], marker='o', linestyle='-')
        
        # Add styling
        plt.ylabel('Memory Usage (MB)')
        plt.title(f'Memory Usage Over Last {hours:.1f} Hour(s)')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Format x-axis with datetime labels
        plt.xticks(
            memory_data["timestamps"][::max(1, len(memory_data["timestamps"])//10)],
            [datetime.fromtimestamp(ts).strftime('%H:%M:%S') for ts in 
             memory_data["timestamps"][::max(1, len(memory_data["timestamps"])//10)]],
            rotation=45
        )
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            logger.info(f"Memory usage plot saved to {save_path}")
        else:
            plt.show()
    
    def export_metrics(self, filepath: str) -> None:
        """
        Export metrics to a JSON file.
        
        Args:
            filepath: Path to save the metrics
        """
        with self._metrics_lock:
            # Create a copy of metrics to avoid modification during serialization
            metrics = list(self._metrics)
        
        # Convert metrics to dictionaries
        metrics_dict = [m.to_dict() for m in metrics]
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump({
                "metadata": {
                    "exported_at": time.time(),
                    "exported_at_str": datetime.now().isoformat(),
                    "metric_count": len(metrics)
                },
                "metrics": metrics_dict
            }, f, indent=2)
        
        logger.info(f"Exported {len(metrics)} metrics to {filepath}")
    
    def generate_performance_report(
        self,
        filepath: str,
        hours: float = 24.0
    ) -> None:
        """
        Generate a comprehensive performance report.
        
        Args:
            filepath: Path to save the report
            hours: Number of hours of history to include
        """
        # Calculate start time
        end_time = time.time()
        start_time = end_time - (hours * 3600)
        
        # Get function statistics
        func_stats = self.get_function_stats(start_time=start_time, end_time=end_time)
        
        # Sort by total time (descending)
        sorted_stats = sorted(
            func_stats.items(), 
            key=lambda x: x[1]["total_time"], 
            reverse=True
        )
        
        # Get memory trend
        memory_data = self.get_memory_usage_trend(
            interval_seconds=300.0,  # 5-minute intervals
            start_time=start_time,
            end_time=end_time
        )
        
        # Generate plots
        plots_dir = os.path.join(os.path.dirname(filepath), "plots")
        os.makedirs(plots_dir, exist_ok=True)
        
        func_plot_path = os.path.join(plots_dir, "function_performance.png")
        memory_plot_path = os.path.join(plots_dir, "memory_usage.png")
        
        self.plot_function_performance(top_n=20, save_path=func_plot_path)
        self.plot_memory_usage(hours=hours, save_path=memory_plot_path)
        
        # Create report HTML
        with open(filepath, 'w') as f:
            f.write(f"""
            <html>
                <head>
                    <title>Quantum Financial API Performance Report</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        h1, h2, h3 {{ color: #333366; }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
                        th {{ background-color: #f2f2f2; }}
                        tr:nth-child(even) {{ background-color: #f9f9f9; }}
                        .summary {{ background-color: #eef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                        .warning {{ color: #990000; }}
                    </style>
                </head>
                <body>
                    <h1>Quantum Financial API Performance Report</h1>
                    <div class="summary">
                        <h2>Summary</h2>
                        <p>Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>Time period: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')} to {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')} ({hours:.1f} hours)</p>
                        <p>Total functions monitored: {len(func_stats)}</p>
                        <p>Total memory measurements: {len(memory_data['timestamps'])}</p>
                    </div>
                    
                    <h2>Performance Visualizations</h2>
                    <div>
                        <h3>Function Performance</h3>
                        <img src="plots/function_performance.png" alt="Function Performance" style="max-width: 100%;">
                        
                        <h3>Memory Usage</h3>
                        <img src="plots/memory_usage.png" alt="Memory Usage" style="max-width: 100%;">
                    </div>
                    
                    <h2>Slowest Functions</h2>
                    <table>
                        <tr>
                            <th>Function</th>
                            <th>Component</th>
                            <th>Calls</th>
                            <th>Total Time (s)</th>
                            <th>Avg Time (ms)</th>
                            <th>Max Time (ms)</th>
                        </tr>
            """)
            
            # Add top 20 slowest functions
            for key, stats in sorted_stats[:20]:
                # Highlight slow functions (avg > 100ms)
                row_class = ' class="warning"' if stats["avg_time"] > 0.1 else ''
                
                f.write(f"""
                        <tr{row_class}>
                            <td>{stats['function_name']}</td>
                            <td>{stats['component']}</td>
                            <td>{stats['count']}</td>
                            <td>{stats['total_time']:.2f}</td>
                            <td>{stats['avg_time_ms']:.2f}</td>
                            <td>{stats['max_time_ms']:.2f}</td>
                        </tr>
                """)
            
            f.write("""
                    </table>
                    
                    <h2>Memory Usage Statistics</h2>
            """)
            
            # Add memory statistics
            if memory_data["values"]:
                current_memory = memory_data["values"][-1]
                peak_memory = max(memory_data["values"])
                avg_memory = sum(memory_data["values"]) / len(memory_data["values"])
                
                f.write(f"""
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value (MB)</th>
                        </tr>
                        <tr>
                            <td>Current Memory Usage</td>
                            <td>{current_memory:.2f}</td>
                        </tr>
                        <tr>
                            <td>Peak Memory Usage</td>
                            <td>{peak_memory:.2f}</td>
                        </tr>
                        <tr>
                            <td>Average Memory Usage</td>
                            <td>{avg_memory:.2f}</td>
                        </tr>
                    </table>
                """)
            else:
                f.write("<p>No memory usage data available.</p>")
            
            f.write("""
                </body>
            </html>
            """)
        
        logger.info(f"Performance report generated at {filepath}")
    
    def shutdown(self) -> None:
        """Shut down the performance monitor."""
        if self._memory_monitor_thread is not None:
            self._stop_memory_monitor.set()
            self._memory_monitor_thread.join(timeout=2.0)
            self._memory_monitor_thread = None
        
        logger.info("Performance monitor shutdown complete")


# Singleton instance
_performance_monitor = None
_monitor_lock = threading.Lock()


def get_performance_monitor() -> PerformanceMonitor:
    """
    Get the global performance monitor instance.
    
    Returns:
        Singleton PerformanceMonitor instance
    """
    global _performance_monitor
    
    if _performance_monitor is None:
        with _monitor_lock:
            if _performance_monitor is None:
                _performance_monitor = PerformanceMonitor()
    
    return _performance_monitor


# Convenience decorators
def monitor_function(component: ComponentType) -> Callable[[F], F]:
    """
    Decorator to monitor function performance.
    
    Args:
        component: Component the function belongs to
        
    Returns:
        Decorated function
    """
    return get_performance_monitor().function_timer(component) 