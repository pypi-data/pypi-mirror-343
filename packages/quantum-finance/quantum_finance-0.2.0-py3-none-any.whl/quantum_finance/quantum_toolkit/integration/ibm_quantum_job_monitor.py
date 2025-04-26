#!/usr/bin/env python3

"""
IBM Quantum Job Monitoring and Alerting System

This module provides a comprehensive job monitoring system for IBM Quantum jobs:
- Real-time job status tracking
- Execution time monitoring
- Job failure alerts and notifications
- Result quality assessment
- Customizable alerting thresholds and callbacks

Usage:
    from ibm_quantum_job_monitor import IBMQuantumJobMonitor
    
    # Initialize the monitor
    monitor = IBMQuantumJobMonitor()
    
    # Monitor a job
    monitor.monitor_job(job_id, callbacks={
        'status_change': on_status_change,
        'completion': on_completion,
        'failure': on_failure
    })
    
    # Check job status
    status = monitor.get_job_status(job_id)

Author: Quantum-AI Team
"""

import os
import sys
import time
import logging
import threading
import json
import datetime
from typing import Dict, List, Tuple, Optional, Union, Any, Callable
from enum import Enum
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ibm_quantum_job_monitor')

# Custom Exception
class JobMonitorError(Exception):
    """Custom exception for job monitor errors."""
    pass

# Try to import IBM Quantum Runtime
try:
    from qiskit_ibm_runtime import QiskitRuntimeService
    from qiskit_ibm_runtime.runtime_job import RuntimeJob
    HAS_IBM_RUNTIME = True
except ImportError:
    HAS_IBM_RUNTIME = False
    logger.warning("qiskit_ibm_runtime not found. Using mock implementation.")

# Job status enum
class JobStatus(str, Enum):
    """Enum representing possible job statuses."""
    INITIALIZING = 'initializing'
    QUEUED = 'queued'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    UNKNOWN = 'unknown'

class JobMetrics:
    """Class to store and analyze job metrics."""
    
    def __init__(self):
        """Initialize the job metrics."""
        self.queue_time = None
        self.execution_time = None
        self.total_time = None
        self.result_quality = None
        self.error_messages = []
        self.status_history = []
        
    def add_status(self, status: str, timestamp: float):
        """Add a status update to the history."""
        self.status_history.append((status, timestamp))
        
    def calculate_times(self):
        """Calculate queue and execution times from status history."""
        if len(self.status_history) < 2:
            return
            
        # Find timestamps for status transitions
        init_time = None
        queue_start = None
        execution_start = None
        completion_time = None
        
        for status, timestamp in self.status_history:
            if status == JobStatus.INITIALIZING and init_time is None:
                init_time = timestamp
            elif status == JobStatus.QUEUED and queue_start is None:
                queue_start = timestamp
            elif status == JobStatus.RUNNING and execution_start is None:
                execution_start = timestamp
            elif status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED] and completion_time is None:
                completion_time = timestamp
        
        # Calculate times
        if queue_start is not None and execution_start is not None:
            self.queue_time = execution_start - queue_start
            
        if execution_start is not None and completion_time is not None:
            self.execution_time = completion_time - execution_start
            
        if init_time is not None and completion_time is not None:
            self.total_time = completion_time - init_time
    
    def assess_result_quality(self, result: Dict[str, Any]) -> float:
        """
        Assess the quality of a job result.
        
        Args:
            result: The job result
            
        Returns:
            float: Quality score between 0.0 and 1.0
        """
        # This is a placeholder for a more sophisticated assessment
        # Real implementation would analyze results based on multiple factors
        
        if not result:
            self.result_quality = 0.0
            return 0.0
            
        # Check if we have any results
        if 'results' not in result:
            self.result_quality = 0.5  # Neutral if no detailed results
            return 0.5
            
        # Simple quality check based on presence of expected fields
        # and absence of error indicators
        score = 0.8  # Start with a good score
        
        # Check for error indicators
        if 'error' in result:
            score -= 0.5
            
        # Check for warning indicators
        if 'warnings' in result and result['warnings']:
            score -= 0.2
            
        # Ensure score is within range
        self.result_quality = max(0.0, min(1.0, score))
        return self.result_quality

class AlertConfiguration:
    """Configuration for job monitoring alerts."""
    
    def __init__(self, 
                 long_queue_threshold: int = 3600,     # 1 hour
                 long_execution_threshold: int = 1800, # 30 minutes
                 status_check_interval: int = 60,      # 1 minute
                 alert_on_status_change: bool = True,
                 alert_on_completion: bool = True,
                 alert_on_failure: bool = True,
                 result_quality_threshold: float = 0.7):
        """
        Initialize the alert configuration.
        
        Args:
            long_queue_threshold: Threshold for long queue time alerts (seconds)
            long_execution_threshold: Threshold for long execution time alerts (seconds)
            status_check_interval: Interval for status checks (seconds)
            alert_on_status_change: Whether to alert on status changes
            alert_on_completion: Whether to alert on job completion
            alert_on_failure: Whether to alert on job failure
            result_quality_threshold: Threshold for result quality alerts (0.0-1.0)
        """
        self.long_queue_threshold = long_queue_threshold
        self.long_execution_threshold = long_execution_threshold
        self.status_check_interval = status_check_interval
        self.alert_on_status_change = alert_on_status_change
        self.alert_on_completion = alert_on_completion
        self.alert_on_failure = alert_on_failure
        self.result_quality_threshold = result_quality_threshold

class IBMQuantumJobMonitor:
    """
    Monitor and alert system for IBM Quantum jobs.
    """
    
    def __init__(self, service: Optional[Any] = None, 
                alert_config: Optional[AlertConfiguration] = None,
                log_file: Optional[str] = None):
        """
        Initialize the job monitor.
        
        Args:
            service: QiskitRuntimeService instance. If None, will attempt to create one.
            alert_config: AlertConfiguration instance. If None, uses default values.
            log_file: Path to log file for job status changes. If None, no file logging.
        """
        self.service = service
        self.alert_config = alert_config or AlertConfiguration()
        self.log_file = log_file
        
        # Job tracking
        self._monitored_jobs = {}      # job_id -> RuntimeJob
        self._job_metrics = {}         # job_id -> JobMetrics
        self._job_callbacks = {}       # job_id -> callbacks dict
        self._monitoring_threads = {}  # job_id -> thread
        self._stop_events = {}         # job_id -> threading.Event
        
        # Initialize service if not provided
        if self.service is None and HAS_IBM_RUNTIME:
            try:
                self.service = QiskitRuntimeService()
                logger.info("Initialized QiskitRuntimeService")
            except Exception as e:
                logger.error(f"Failed to initialize QiskitRuntimeService: {str(e)}")
                self.service = None
    
    def monitor_job(self, 
                   job_id: str, 
                   job: Optional[Any] = None,
                   callbacks: Optional[Dict[str, Callable]] = None):
        """
        Start monitoring a job.
        
        Args:
            job_id: ID of the job to monitor
            job: RuntimeJob instance. If None, will retrieve using job_id.
            callbacks: Dictionary of callback functions for different events:
                - 'status_change': Called when job status changes
                - 'completion': Called when job completes successfully
                - 'failure': Called when job fails
                - 'long_queue': Called when job is queued for a long time
                - 'long_execution': Called when job execution takes a long time
                - 'result_quality': Called when result quality is below threshold
        """
        # Check if already monitoring this job
        if job_id in self._monitored_jobs:
            logger.info(f"Already monitoring job {job_id}")
            return
            
        # Get the job if not provided
        if job is None and self.service:
            try:
                job = self.service.job(job_id)
                logger.info(f"Retrieved job {job_id}")
            except Exception as e:
                logger.error(f"Error retrieving job {job_id}: {str(e)}")
                return
        
        # Store job and initialize metrics
        self._monitored_jobs[job_id] = job
        self._job_metrics[job_id] = JobMetrics()
        self._job_callbacks[job_id] = callbacks or {}
        
        # Create stop event
        stop_event = threading.Event()
        self._stop_events[job_id] = stop_event
        
        # Start monitoring thread
        monitoring_thread = threading.Thread(
            target=self._monitor_job_status,
            args=(job_id, stop_event),
            daemon=True
        )
        
        self._monitoring_threads[job_id] = monitoring_thread
        monitoring_thread.start()
        
        logger.info(f"Started monitoring job {job_id}")
        
    def _monitor_job_status(self, job_id: str, stop_event: threading.Event):
        """
        Monitor job status in a background thread.
        
        Args:
            job_id: ID of the job to monitor
            stop_event: Event to signal the thread to stop
        """
        job = self._monitored_jobs.get(job_id)
        metrics = self._job_metrics.get(job_id)
        callbacks = self._job_callbacks.get(job_id)
        
        if not job or not metrics:
            logger.error(f"Job {job_id} not found in monitored jobs")
            return
            
        # Initial status check
        try:
            current_status = self._get_job_status_str(job)
            metrics.add_status(current_status, time.time())
            logger.info(f"Job {job_id} initial status: {current_status}")
            
            # Log to file if configured
            self._log_status_change(job_id, current_status)
            
        except Exception as e:
            logger.error(f"Error checking initial status for job {job_id}: {str(e)}")
            current_status = JobStatus.UNKNOWN
        
        # Monitoring loop
        start_time = time.time()
        queue_alert_sent = False
        execution_alert_sent = False
        
        while not stop_event.is_set():
            try:
                # Wait for the configured interval
                stop_event.wait(self.alert_config.status_check_interval)
                if stop_event.is_set():
                    break
                    
                # Check the current status
                new_status = self._get_job_status_str(job)
                current_time = time.time()
                
                # Check for status change
                if new_status != current_status:
                    logger.info(f"Job {job_id} status changed: {current_status} -> {new_status}")
                    
                    # Update metrics
                    metrics.add_status(new_status, current_time)
                    metrics.calculate_times()
                    
                    # Log to file if configured
                    self._log_status_change(job_id, new_status)
                    
                    # Call status change callback if configured
                    if self.alert_config.alert_on_status_change and callbacks and 'status_change' in callbacks:
                        try:
                            callbacks['status_change'](job_id, new_status, current_status)
                        except Exception as e:
                            logger.error(f"Error in status change callback for job {job_id}: {str(e)}")
                    
                    # Update current status
                    current_status = new_status
                    
                    # Check for completion or failure
                    if new_status == JobStatus.COMPLETED and self.alert_config.alert_on_completion:
                        logger.info(f"Job {job_id} completed successfully")
                        
                        # Try to get results and assess quality
                        try:
                            result = job.result()
                            quality = metrics.assess_result_quality(result)
                            
                            # Check result quality
                            if quality is not None and quality < self.alert_config.result_quality_threshold and callbacks and 'result_quality' in callbacks:
                                logger.warning(f"Job {job_id} result quality below threshold: {quality:.2f}")
                                callbacks['result_quality'](job_id, quality, result)
                                
                        except Exception as e:
                            logger.error(f"Error getting result or assessing quality for completed job {job_id}: {str(e)}")
                            metrics.error_messages.append(str(e))
                        
                        # Call completion callback if configured
                        if callbacks and 'completion' in callbacks:
                            try:
                                callbacks['completion'](job_id, metrics)
                            except Exception as e:
                                logger.error(f"Error in completion callback for job {job_id}: {str(e)}")
                        
                        # Exit the monitoring loop
                        break
                        
                    elif new_status == JobStatus.FAILED and self.alert_config.alert_on_failure:
                        logger.warning(f"Job {job_id} failed")
                        
                        # Try to get error information
                        try:
                            error = job.error_message()
                            metrics.error_messages.append(error)
                        except Exception:
                            pass
                        
                        # Call failure callback if configured
                        if callbacks and 'failure' in callbacks:
                            try:
                                callbacks['failure'](job_id, metrics)
                            except Exception as e:
                                logger.error(f"Error in failure callback for job {job_id}: {str(e)}")
                        
                        # Exit the monitoring loop
                        break
                        
                    elif new_status == JobStatus.CANCELLED:
                        logger.info(f"Job {job_id} was cancelled")
                        # Exit the monitoring loop
                        break
                
                # Check for long queue time
                if current_status == JobStatus.QUEUED and not queue_alert_sent:
                    queue_time = current_time - start_time
                    if queue_time > self.alert_config.long_queue_threshold and callbacks and 'long_queue' in callbacks:
                        logger.warning(f"Job {job_id} has been queued for {queue_time:.1f} seconds")
                        try:
                            callbacks['long_queue'](job_id, queue_time)
                        except Exception as e:
                            logger.error(f"Error in long queue callback for job {job_id}: {str(e)}")
                        queue_alert_sent = True
                        
                # Check for long execution time
                if current_status == JobStatus.RUNNING and not execution_alert_sent:
                    # Find when the job started running
                    running_start = None
                    for status, timestamp in metrics.status_history:
                        if status == JobStatus.RUNNING:
                            running_start = timestamp
                            break
                    
                    if running_start:
                        execution_time = current_time - running_start
                        if execution_time > self.alert_config.long_execution_threshold and callbacks and 'long_execution' in callbacks:
                            logger.warning(f"Job {job_id} has been running for {execution_time:.1f} seconds")
                            try:
                                callbacks['long_execution'](job_id, execution_time)
                            except Exception as e:
                                logger.error(f"Error in long execution callback for job {job_id}: {str(e)}")
                            execution_alert_sent = True
                
            except Exception as e:
                logger.error(f"Error monitoring job {job_id}: {str(e)}")
                time.sleep(max(self.alert_config.status_check_interval, 5))
        
        # Cleanup
        logger.info(f"Stopped monitoring job {job_id}")
        self._cleanup_job(job_id)
    
    def _get_job_status_str(self, job) -> str:
        """
        Get the status of a job as a string.
        
        Args:
            job: RuntimeJob instance
            
        Returns:
            str: Status string
        """
        if not job:
            return JobStatus.UNKNOWN
            
        try:
            status = job.status()
            
            # Convert status to string representation
            if hasattr(status, 'name'):
                # Status might be an enum
                return status.name.lower()
            elif hasattr(status, 'value'):
                # Status might be a custom enum-like object
                return status.value.lower()
            else:
                # Status might be a string directly
                return status.lower()
                
        except Exception as e:
            logger.error(f"Error getting job status: {str(e)}")
            return JobStatus.UNKNOWN
    
    def _log_status_change(self, job_id: str, status: str):
        """
        Log a job status change to a file if configured.
        
        Args:
            job_id: ID of the job
            status: New status
        """
        if not self.log_file:
            return
            
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - Job {job_id}: {status}\n"
            
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
                
        except Exception as e:
            logger.error(f"Error logging status change to file: {str(e)}")
    
    def _cleanup_job(self, job_id: str):
        """
        Clean up resources for a job that's no longer being monitored.
        
        Args:
            job_id: ID of the job
        """
        # Remove from monitored jobs
        if job_id in self._monitored_jobs:
            del self._monitored_jobs[job_id]
            
        # Remove stop event
        if job_id in self._stop_events:
            del self._stop_events[job_id]
            
        # Remove monitoring thread
        if job_id in self._monitoring_threads:
            del self._monitoring_threads[job_id]
    
    def stop_monitoring(self, job_id: str):
        """
        Stop monitoring a job.
        
        Args:
            job_id: ID of the job to stop monitoring
        """
        if job_id in self._stop_events:
            self._stop_events[job_id].set()
            logger.info(f"Requested stop monitoring for job {job_id}")
        else:
            logger.warning(f"Job {job_id} is not being monitored")
    
    def get_job_status(self, job_id: str) -> str:
        """
        Get the current status of a job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            str: Job status
        """
        job = self._monitored_jobs.get(job_id)
        if job:
            return self._get_job_status_str(job)
        
        # If job is not being monitored, try to get it from the service
        if self.service:
            try:
                job = self.service.job(job_id)
                return self._get_job_status_str(job)
            except Exception as e:
                logger.error(f"Error retrieving job {job_id}: {str(e)}")
        
        return JobStatus.UNKNOWN
    
    def get_job_metrics(self, job_id: str) -> Optional[JobMetrics]:
        """
        Get metrics for a job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            JobMetrics or None: Job metrics if available
        """
        return self._job_metrics.get(job_id)
    
    def get_monitored_jobs(self) -> List[str]:
        """
        Get a list of jobs currently being monitored.
        
        Returns:
            List[str]: List of job IDs
        """
        return list(self._monitored_jobs.keys())
    
    def update_alert_config(self, new_config: AlertConfiguration):
        """
        Update the alert configuration.
        
        Args:
            new_config: New alert configuration
        """
        self.alert_config = new_config
        logger.info("Updated alert configuration")


class AlertConsole:
    """
    Console-based alert handler for job monitoring.
    
    This class provides default callbacks for job monitoring alerts
    that print alerts to the console.
    """
    
    @staticmethod
    def on_status_change(job_id: str, new_status: str, old_status: str):
        """Status change callback."""
        print(f"[STATUS CHANGE] Job {job_id}: {old_status} -> {new_status}")
    
    @staticmethod
    def on_completion(job_id: str, metrics: JobMetrics):
        """Completion callback."""
        print(f"[COMPLETION] Job {job_id} completed successfully")
        
        if metrics.queue_time:
            print(f"  Queue time: {metrics.queue_time:.1f} seconds")
        if metrics.execution_time:
            print(f"  Execution time: {metrics.execution_time:.1f} seconds")
        if metrics.total_time:
            print(f"  Total time: {metrics.total_time:.1f} seconds")
        if metrics.result_quality is not None:
            print(f"  Result quality: {metrics.result_quality:.2f}")
    
    @staticmethod
    def on_failure(job_id: str, metrics: JobMetrics):
        """Failure callback."""
        print(f"[FAILURE] Job {job_id} failed")
        
        if metrics.error_messages:
            print(f"  Error: {metrics.error_messages[-1]}")
    
    @staticmethod
    def on_long_queue(job_id: str, queue_time: float):
        """Long queue callback."""
        print(f"[LONG QUEUE] Job {job_id} has been queued for {queue_time:.1f} seconds")
    
    @staticmethod
    def on_long_execution(job_id: str, execution_time: float):
        """Long execution callback."""
        print(f"[LONG EXECUTION] Job {job_id} has been running for {execution_time:.1f} seconds")
    
    @staticmethod
    def on_result_quality(job_id: str, quality: float, result: Dict[str, Any]):
        """Result quality callback."""
        print(f"[RESULT QUALITY] Job {job_id} result quality is {quality:.2f}")


if __name__ == "__main__":
    """
    Example usage of the IBMQuantumJobMonitor.
    """
    import os
    from dotenv import load_dotenv
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='IBM Quantum Job Monitor')
    parser.add_argument('--job-id', type=str, help='ID of the job to monitor')
    parser.add_argument('--log-file', type=str, default='ibm_job_monitor.log', help='Path to log file')
    
    args = parser.parse_args()
    
    # Load environment variables (for IBM Quantum token)
    load_dotenv()
    token = os.environ.get("IBM_QUANTUM_TOKEN")
    
    if not token:
        print("IBM_QUANTUM_TOKEN not found in environment variables.")
        print("Please set this variable in your .env file.")
        sys.exit(1)
    
    if HAS_IBM_RUNTIME:
        try:
            # Initialize the QiskitRuntimeService
            service = QiskitRuntimeService(channel="ibm_quantum", token=token)
            
            # Create a job monitor with console alerts
            monitor = IBMQuantumJobMonitor(service=service, log_file=args.log_file)
            
            if args.job_id:
                # Monitor a specific job
                print(f"Starting to monitor job {args.job_id}")
                
                # Set up console alerts
                monitor.monitor_job(args.job_id, callbacks={
                    'status_change': AlertConsole.on_status_change,
                    'completion': AlertConsole.on_completion,
                    'failure': AlertConsole.on_failure,
                    'long_queue': AlertConsole.on_long_queue,
                    'long_execution': AlertConsole.on_long_execution,
                    'result_quality': AlertConsole.on_result_quality
                })
                
                try:
                    # Keep the main thread running
                    while True:
                        # Check if we're still monitoring the job
                        if args.job_id not in monitor.get_monitored_jobs():
                            print("Job monitoring completed.")
                            break
                        time.sleep(5)
                except KeyboardInterrupt:
                    print("Stopping job monitoring...")
                    monitor.stop_monitoring(args.job_id)
            else:
                # List recent jobs
                print("Listing recent jobs:")
                jobs = service.jobs(limit=5)
                
                for i, job in enumerate(jobs, 1):
                    status = monitor._get_job_status_str(job)
                    job_id = job.job_id()
                    creation_date = job.creation_date
                    
                    print(f"{i}. Job ID: {job_id}")
                    print(f"   Status: {status}")
                    print(f"   Created: {creation_date.strftime('%Y-%m-%d %H:%M:%S %Z') if creation_date else 'N/A'}")
                    print()
                
                print("To monitor a specific job, run with --job-id JOB_ID")
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            sys.exit(1)
    else:
        print("qiskit_ibm_runtime not found. Please install it with:")
        print("pip install qiskit-ibm-runtime")
        sys.exit(1) 