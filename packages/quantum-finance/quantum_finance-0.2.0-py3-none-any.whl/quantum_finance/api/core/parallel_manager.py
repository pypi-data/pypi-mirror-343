#!/usr/bin/env python3

"""
Quantum Financial API - Parallel Processing Manager

Provides parallel processing capabilities for computationally intensive
operations in the Quantum Financial API.

This module enables:
- Parallel execution of component analyses
- Adaptive thread/process pool management
- Task prioritization and scheduling
- Resource utilization monitoring
"""

import os
import time
import logging
import threading
import multiprocessing
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, Future
from typing import Dict, List, Tuple, Set, Optional, Union, Any, Callable, TypeVar, Generic
from enum import Enum
from dataclasses import dataclass, field
import uuid
import queue
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type variables for generics
T = TypeVar('T')  # Input type
R = TypeVar('R')  # Result type


class TaskPriority(Enum):
    """Priority levels for parallel tasks."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Task(Generic[T, R]):
    """Represents a task to be executed in parallel."""
    task_id: str
    func: Callable[[T], R]
    args: T
    priority: TaskPriority = TaskPriority.NORMAL
    created_at: float = field(default_factory=time.time)
    estimated_complexity: float = 1.0
    
    def __lt__(self, other):
        """Compare tasks based on priority for priority queue."""
        if not isinstance(other, Task):
            return NotImplemented
        # First compare by priority (higher priority first)
        if self.priority != other.priority:
            return self.priority.value > other.priority.value
        # Then by creation time (older first)
        return self.created_at < other.created_at


class ExecutionMode(Enum):
    """Execution modes for parallel processing."""
    THREAD = "thread"
    PROCESS = "process"
    AUTO = "auto"


class ParallelManager:
    """
    Manages parallel execution of tasks with dynamic resource allocation
    and task prioritization.
    """
    
    def __init__(
        self, 
        max_workers: Optional[int] = None,
        execution_mode: ExecutionMode = ExecutionMode.AUTO,
        max_memory_percent: float = 80.0,
        monitor_interval: float = 5.0
    ):
        """
        Initialize the parallel manager.
        
        Args:
            max_workers: Maximum number of worker threads/processes
                        (None = auto-detect based on CPU cores)
            execution_mode: Whether to use threads, processes, or auto-detect
            max_memory_percent: Maximum memory usage as percentage of system memory
            monitor_interval: Interval in seconds for resource monitoring
        """
        # Determine optimal number of workers if not specified
        if max_workers is None:
            max_workers = max(1, cpu_count() - 1)  # Leave one core free for the main thread
        
        self.max_workers = max_workers
        self.execution_mode = execution_mode
        self.max_memory_percent = max_memory_percent
        self.monitor_interval = monitor_interval
        
        # Task queue and results storage
        self.task_queue = queue.PriorityQueue()
        self.results: Dict[str, Any] = {}
        self.tasks_in_progress: Dict[str, Future] = {}
        
        # Synchronization
        self.lock = threading.RLock()
        self.task_completed_events: Dict[str, threading.Event] = {}
        
        # Worker pools - initialize as needed
        self.thread_executor = None
        self.process_executor = None
        
        # Resource monitoring
        self.resource_monitor_thread = None
        self.stop_monitor = threading.Event()
        self.current_workers = 0
        self.adaptive_worker_count = max_workers
        
        # Statistics
        self.stats = {
            "tasks_submitted": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "avg_task_duration": 0.0,
            "total_task_duration": 0.0,
        }
        
        # Initialize executors and start monitoring
        self._init_executors()
        self._start_resource_monitor()
        
        logger.info(
            f"Initialized ParallelManager with {self.max_workers} workers "
            f"using {self.execution_mode.value} mode"
        )
    
    def _init_executors(self):
        """Initialize the appropriate executor based on execution mode."""
        if self.execution_mode in (ExecutionMode.THREAD, ExecutionMode.AUTO):
            self.thread_executor = ThreadPoolExecutor(max_workers=self.max_workers)
        
        if self.execution_mode in (ExecutionMode.PROCESS, ExecutionMode.AUTO):
            # For process pool, limit to fewer workers by default to avoid excessive memory usage
            process_workers = max(1, min(self.max_workers, cpu_count() // 2))
            self.process_executor = ProcessPoolExecutor(max_workers=process_workers)
    
    def _start_resource_monitor(self):
        """Start the resource monitoring thread."""
        if self.resource_monitor_thread is None:
            self.stop_monitor.clear()
            self.resource_monitor_thread = threading.Thread(
                target=self._monitor_resources,
                daemon=True
            )
            self.resource_monitor_thread.start()
            logger.debug("Resource monitoring thread started")
    
    def _monitor_resources(self):
        """Monitor system resources and adjust worker count if needed."""
        while not self.stop_monitor.is_set():
            try:
                # Get current memory usage
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # Adjust worker count based on memory usage
                if memory_percent > self.max_memory_percent:
                    # Reduce worker count if memory usage is too high
                    new_worker_count = max(1, int(self.adaptive_worker_count * 0.75))
                    if new_worker_count < self.adaptive_worker_count:
                        self.adaptive_worker_count = new_worker_count
                        logger.warning(
                            f"Memory usage high ({memory_percent:.1f}%), "
                            f"reducing worker count to {self.adaptive_worker_count}"
                        )
                elif memory_percent < self.max_memory_percent * 0.7 and self.adaptive_worker_count < self.max_workers:
                    # Increase worker count if memory usage is low
                    new_worker_count = min(self.max_workers, self.adaptive_worker_count + 1)
                    if new_worker_count > self.adaptive_worker_count:
                        self.adaptive_worker_count = new_worker_count
                        logger.info(
                            f"Memory usage acceptable ({memory_percent:.1f}%), "
                            f"increasing worker count to {self.adaptive_worker_count}"
                        )
                
                # Log resource usage periodically
                logger.debug(
                    f"System resources: CPU: {psutil.cpu_percent()}%, "
                    f"Memory: {memory_percent:.1f}%, "
                    f"Workers: {self.current_workers}/{self.adaptive_worker_count}"
                )
            
            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")
            
            # Wait for next monitoring interval
            self.stop_monitor.wait(self.monitor_interval)
    
    def submit(
        self, 
        func: Callable[[T], R], 
        args: T, 
        priority: TaskPriority = TaskPriority.NORMAL,
        estimated_complexity: float = 1.0,
        execution_mode: Optional[ExecutionMode] = None
    ) -> str:
        """
        Submit a task for parallel execution.
        
        Args:
            func: Function to execute
            args: Arguments to pass to the function
            priority: Task priority
            estimated_complexity: Estimated computational complexity (higher = more complex)
            execution_mode: Override default execution mode for this task
            
        Returns:
            Task ID that can be used to retrieve the result
        """
        # Generate a unique task ID
        task_id = str(uuid.uuid4())
        
        # Create task and completion event
        task = Task(
            task_id=task_id,
            func=func,
            args=args,
            priority=priority,
            estimated_complexity=estimated_complexity
        )
        
        with self.lock:
            # Create a completion event for this task
            self.task_completed_events[task_id] = threading.Event()
            
            # Add task to the queue
            self.task_queue.put(task)
            self.stats["tasks_submitted"] += 1
            
            # Start task execution
            self._process_queue(execution_mode)
        
        logger.debug(f"Submitted task {task_id} with priority {priority.name}")
        return task_id
    
    def _process_queue(self, preferred_mode: Optional[ExecutionMode] = None):
        """
        Process tasks from the queue.
        
        Args:
            preferred_mode: Preferred execution mode for tasks
        """
        # Determine which executor to use
        mode = preferred_mode or self.execution_mode
        
        # Don't exceed adaptive worker count
        with self.lock:
            while not self.task_queue.empty() and self.current_workers < self.adaptive_worker_count:
                try:
                    # Get the highest priority task
                    task = self.task_queue.get_nowait()
                    
                    # Submit task to appropriate executor
                    if mode == ExecutionMode.PROCESS or (
                        mode == ExecutionMode.AUTO and task.estimated_complexity > 2.0
                    ):
                        # Use process pool for computationally intensive tasks
                        if self.process_executor is None:
                            # Initialize process executor if needed
                            process_workers = max(1, min(self.adaptive_worker_count, cpu_count() // 2))
                            self.process_executor = ProcessPoolExecutor(max_workers=process_workers)
                        
                        future = self.process_executor.submit(
                            self._execute_task_wrapper, task.task_id, task.func, task.args
                        )
                    else:
                        # Use thread pool for I/O bound or less intensive tasks
                        if self.thread_executor is None:
                            # Initialize thread executor if needed
                            self.thread_executor = ThreadPoolExecutor(max_workers=self.adaptive_worker_count)
                        
                        future = self.thread_executor.submit(
                            self._execute_task_wrapper, task.task_id, task.func, task.args
                        )
                    
                    # Register callback to handle task completion
                    future.add_done_callback(
                        lambda f, task_id=task.task_id: self._task_completed(task_id, f)
                    )
                    
                    # Track task
                    self.tasks_in_progress[task.task_id] = future
                    self.current_workers += 1
                    
                except queue.Empty:
                    break
                except Exception as e:
                    logger.error(f"Error processing task from queue: {e}")
                    # Put the task back in the queue
                    self.task_queue.put(task)
    
    def _execute_task_wrapper(self, task_id: str, func: Callable, args: Any) -> Tuple[str, Any, float]:
        """
        Wrapper to execute a task and capture execution time.
        
        Args:
            task_id: Task ID
            func: Function to execute
            args: Arguments to pass to the function
            
        Returns:
            Tuple of (task_id, result, execution_time)
        """
        start_time = time.time()
        try:
            result = func(args)
            execution_time = time.time() - start_time
            return task_id, result, execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Task {task_id} failed: {e}")
            # Re-raise the exception to be caught by the callback
            raise
    
    def _task_completed(self, task_id: str, future: Future):
        """
        Callback for task completion.
        
        Args:
            task_id: ID of the completed task
            future: Future object representing the task
        """
        with self.lock:
            try:
                # Decrement active worker count
                self.current_workers -= 1
                
                if future.exception() is not None:
                    # Task failed
                    self.results[task_id] = {
                        "status": "failed",
                        "error": str(future.exception()),
                        "completed_at": time.time()
                    }
                    self.stats["tasks_failed"] += 1
                else:
                    # Task completed successfully
                    task_id, result, execution_time = future.result()
                    self.results[task_id] = {
                        "status": "completed",
                        "result": result,
                        "execution_time": execution_time,
                        "completed_at": time.time()
                    }
                    self.stats["tasks_completed"] += 1
                    self.stats["total_task_duration"] += execution_time
                    
                    # Update average task duration
                    if self.stats["tasks_completed"] > 0:
                        self.stats["avg_task_duration"] = (
                            self.stats["total_task_duration"] / self.stats["tasks_completed"]
                        )
                
                # Remove from in-progress tasks
                self.tasks_in_progress.pop(task_id, None)
                
                # Set the completion event
                if task_id in self.task_completed_events:
                    self.task_completed_events[task_id].set()
                
            except Exception as e:
                logger.error(f"Error handling task completion: {e}")
            
            # Process more tasks from the queue if available
            self._process_queue()
    
    def get_result(
        self, 
        task_id: str, 
        timeout: Optional[float] = None,
        block: bool = True
    ) -> Optional[Any]:
        """
        Get the result of a task.
        
        Args:
            task_id: Task ID
            timeout: Maximum time to wait for result in seconds (None = wait forever)
            block: Whether to block waiting for the result
            
        Returns:
            Task result or None if not available or timeout occurred
        """
        # Check if result is already available
        if task_id in self.results:
            result_info = self.results[task_id]
            if result_info["status"] == "completed":
                return result_info["result"]
            elif result_info["status"] == "failed":
                raise RuntimeError(f"Task failed: {result_info.get('error', 'Unknown error')}")
        
        # If non-blocking, return None if result not immediately available
        if not block:
            return None
        
        # Wait for the task to complete
        if task_id in self.task_completed_events:
            if self.task_completed_events[task_id].wait(timeout):
                # Result should now be available
                if task_id in self.results:
                    result_info = self.results[task_id]
                    if result_info["status"] == "completed":
                        return result_info["result"]
                    elif result_info["status"] == "failed":
                        raise RuntimeError(f"Task failed: {result_info.get('error', 'Unknown error')}")
        
        # Timeout occurred or event not found
        return None
    
    def wait_for_tasks(self, task_ids: List[str], timeout: Optional[float] = None) -> Dict[str, bool]:
        """
        Wait for multiple tasks to complete.
        
        Args:
            task_ids: List of task IDs to wait for
            timeout: Maximum total time to wait in seconds (None = wait forever)
            
        Returns:
            Dictionary mapping task IDs to completion status (True = completed, False = still running)
        """
        # Find events for all tasks
        events = []
        task_id_to_index = {}
        
        for i, task_id in enumerate(task_ids):
            if task_id in self.task_completed_events:
                events.append(self.task_completed_events[task_id])
                task_id_to_index[task_id] = i
        
        if not events:
            # No events found, all tasks must have completed already or don't exist
            return {task_id: (task_id in self.results) for task_id in task_ids}
        
        # Wait for all events with timeout
        start_time = time.time()
        remaining_timeout = timeout
        
        # Initialize results
        results = {task_id: (task_id in self.results) for task_id in task_ids}
        
        # Wait for incomplete tasks
        incomplete_tasks = [task_id for task_id, completed in results.items() if not completed]
        
        for task_id in incomplete_tasks:
            if task_id in self.task_completed_events:
                event = self.task_completed_events[task_id]
                
                # Calculate remaining timeout
                if timeout is not None:
                    elapsed = time.time() - start_time
                    remaining_timeout = max(0, timeout - elapsed)
                    if remaining_timeout <= 0:
                        break
                
                # Wait for this task
                if event.wait(remaining_timeout):
                    results[task_id] = True
        
        return results
    
    def get_all_results(self, task_ids: List[str], timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Get results for multiple tasks.
        
        Args:
            task_ids: List of task IDs to get results for
            timeout: Maximum total time to wait in seconds (None = wait forever)
            
        Returns:
            Dictionary mapping task IDs to results (None for tasks that aren't complete)
        """
        # Wait for tasks to complete
        completion_status = self.wait_for_tasks(task_ids, timeout)
        
        # Collect results
        results = {}
        for task_id in task_ids:
            try:
                # Non-blocking get_result since we already waited
                results[task_id] = self.get_result(task_id, timeout=0, block=False)
            except Exception as e:
                logger.error(f"Error getting result for task {task_id}: {e}")
                results[task_id] = None
        
        return results
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Attempt to cancel a task.
        
        Args:
            task_id: ID of the task to cancel
            
        Returns:
            True if the task was cancelled, False if it couldn't be cancelled
            (e.g., already completed or running)
        """
        with self.lock:
            # If task is in progress, try to cancel its future
            if task_id in self.tasks_in_progress:
                future = self.tasks_in_progress[task_id]
                cancel_result = future.cancel()
                
                if cancel_result:
                    # Successfully cancelled
                    self.tasks_in_progress.pop(task_id, None)
                    self.current_workers -= 1
                    
                    # Set result to cancelled
                    self.results[task_id] = {
                        "status": "cancelled",
                        "completed_at": time.time()
                    }
                    
                    # Set the completion event
                    if task_id in self.task_completed_events:
                        self.task_completed_events[task_id].set()
                
                return cancel_result
            
            # If in the queue but not started yet, remove from queue
            # This is trickier with priority queue, so we'll mark for removal instead
            for i in range(self.task_queue.qsize()):
                try:
                    task = self.task_queue.get_nowait()
                    
                    if task.task_id == task_id:
                        # Found the task to cancel
                        self.results[task_id] = {
                            "status": "cancelled",
                            "completed_at": time.time()
                        }
                        
                        # Set the completion event
                        if task_id in self.task_completed_events:
                            self.task_completed_events[task_id].set()
                        
                        return True
                    else:
                        # Put the task back in the queue
                        self.task_queue.put(task)
                except queue.Empty:
                    break
        
        # Task not found or already completed
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the parallel manager.
        
        Returns:
            Dictionary of statistics
        """
        with self.lock:
            stats = self.stats.copy()
            stats.update({
                "queue_size": self.task_queue.qsize(),
                "tasks_in_progress": len(self.tasks_in_progress),
                "max_workers": self.max_workers,
                "current_workers": self.current_workers,
                "adaptive_worker_count": self.adaptive_worker_count,
            })
            
            # Add memory usage
            memory = psutil.virtual_memory()
            stats["memory_usage_percent"] = memory.percent
            stats["memory_available_mb"] = memory.available / (1024 * 1024)
            
            return stats
    
    def shutdown(self, wait: bool = True, cancel_pending: bool = False):
        """
        Shut down the parallel manager and release resources.
        
        Args:
            wait: Whether to wait for pending tasks to complete
            cancel_pending: Whether to cancel pending tasks
        """
        logger.info("Shutting down parallel manager")
        
        # Stop the resource monitor
        self.stop_monitor.set()
        if self.resource_monitor_thread is not None:
            self.resource_monitor_thread.join(timeout=2.0)
        
        # Cancel pending tasks if requested
        if cancel_pending:
            with self.lock:
                # Cancel tasks in the queue
                while not self.task_queue.empty():
                    try:
                        task = self.task_queue.get_nowait()
                        self.results[task.task_id] = {
                            "status": "cancelled",
                            "completed_at": time.time()
                        }
                        
                        # Set the completion event
                        if task.task_id in self.task_completed_events:
                            self.task_completed_events[task.task_id].set()
                    except queue.Empty:
                        break
                
                # Cancel in-progress tasks
                for task_id, future in list(self.tasks_in_progress.items()):
                    future.cancel()
                    self.results[task_id] = {
                        "status": "cancelled",
                        "completed_at": time.time()
                    }
                    
                    # Set the completion event
                    if task_id in self.task_completed_events:
                        self.task_completed_events[task_id].set()
        
        # Shut down executors
        if self.thread_executor is not None:
            self.thread_executor.shutdown(wait=wait)
            self.thread_executor = None
        
        if self.process_executor is not None:
            self.process_executor.shutdown(wait=wait)
            self.process_executor = None
        
        logger.info("Parallel manager shutdown complete")


# Singleton instance
_parallel_manager = None
_parallel_manager_lock = threading.Lock()


def get_parallel_manager() -> ParallelManager:
    """
    Get the global parallel manager instance.
    
    Returns:
        Singleton ParallelManager instance
    """
    global _parallel_manager
    
    if _parallel_manager is None:
        with _parallel_manager_lock:
            if _parallel_manager is None:
                _parallel_manager = ParallelManager()
    
    return _parallel_manager 