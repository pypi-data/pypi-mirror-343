"""
Development Insights Module

This module provides tools for tracking, analyzing, and learning from the development
process. It captures information about:

1. Common errors and their resolutions
2. Development patterns and anti-patterns
3. Performance bottlenecks and optimizations
4. Code quality metrics and improvements

The system uses this information to provide insights and recommendations for
improving development workflows and preventing recurring issues.

Usage:
    from development_insights import DevelopmentTracker
    
    # Create a tracker
    tracker = DevelopmentTracker()
    
    # Record an error and its resolution
    tracker.record_error(
        error_type="ImportError",
        message="Module not found",
        resolution="Fixed import statement",
        code_context="app.py:10"
    )
    
    # Get recommendations for current task
    recommendations = tracker.get_recommendations(task="api_development")
"""

import os
import json
import logging
import datetime
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from collections import Counter, defaultdict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('development_insights')

class DevelopmentTracker:
    """Tracks development activities and provides insights and recommendations."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize the development tracker.
        
        Args:
            data_dir: Directory to store tracking data. If None, uses default.
        """
        if data_dir is None:
            self.data_dir = Path(__file__).parent / 'dev_insights_data'
        else:
            self.data_dir = Path(data_dir)
            
        # Ensure the data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Paths for different types of data
        self.errors_path = self.data_dir / 'errors.json'
        self.patterns_path = self.data_dir / 'patterns.json'
        self.metrics_path = self.data_dir / 'metrics.json'
        self.recommendations_path = self.data_dir / 'recommendations.json'
        
        # Load existing data or create new
        self._load_data()
    
    def _load_data(self) -> None:
        """Load tracking data from files."""
        # Load errors data
        if self.errors_path.exists():
            try:
                with open(self.errors_path, 'r') as f:
                    self.errors_data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in {self.errors_path}, creating new data")
                self.errors_data = {"errors": []}
        else:
            self.errors_data = {"errors": []}
        
        # Load patterns data
        if self.patterns_path.exists():
            try:
                with open(self.patterns_path, 'r') as f:
                    self.patterns_data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in {self.patterns_path}, creating new data")
                self.patterns_data = {"patterns": [], "anti_patterns": []}
        else:
            self.patterns_data = {"patterns": [], "anti_patterns": []}
        
        # Load metrics data
        if self.metrics_path.exists():
            try:
                with open(self.metrics_path, 'r') as f:
                    self.metrics_data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in {self.metrics_path}, creating new data")
                self.metrics_data = {"code_metrics": [], "performance_metrics": []}
        else:
            self.metrics_data = {"code_metrics": [], "performance_metrics": []}
        
        # Load recommendations data
        if self.recommendations_path.exists():
            try:
                with open(self.recommendations_path, 'r') as f:
                    self.recommendations_data = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in {self.recommendations_path}, creating new data")
                self.recommendations_data = {"recommendations": []}
        else:
            self.recommendations_data = {"recommendations": []}
    
    def _save_data(self, data_type: str) -> None:
        """Save tracking data to file.
        
        Args:
            data_type: Type of data to save ('errors', 'patterns', 'metrics', or 'recommendations').
        """
        try:
            path_map = {
                'errors': self.errors_path,
                'patterns': self.patterns_path,
                'metrics': self.metrics_path,
                'recommendations': self.recommendations_path
            }
            data_map = {
                'errors': self.errors_data,
                'patterns': self.patterns_data,
                'metrics': self.metrics_data,
                'recommendations': self.recommendations_data
            }
            
            path = path_map.get(data_type)
            data = data_map.get(data_type)
            
            if path and data:
                with open(path, 'w') as f:
                    json.dump(data, f, indent=2)
                    logger.info(f"Saved {data_type} data to {path}")
            else:
                logger.error(f"Invalid data type: {data_type}")
        except Exception as e:
            logger.error(f"Failed to save {data_type} data: {e}")
    
    def record_error(self, error_type: str, message: str, resolution: Optional[str] = None,
                     code_context: Optional[str] = None, tags: Optional[List[str]] = None) -> None:
        """Record an error and its resolution.
        
        Args:
            error_type: Type of error (e.g., 'ImportError', 'TypeError').
            message: Error message.
            resolution: How the error was resolved, if applicable.
            code_context: File and line number where the error occurred.
            tags: List of tags for categorizing the error.
        """
        # Create a unique ID for the error based on its properties
        error_id = hashlib.md5(f"{error_type}:{message}:{code_context}".encode()).hexdigest()
        
        # Check if this exact error has been recorded before
        for error in self.errors_data["errors"]:
            if error.get("id") == error_id:
                # Update existing error with new resolution if provided
                if resolution and not error.get("resolution"):
                    error["resolution"] = resolution
                    error["resolved_at"] = datetime.datetime.now().isoformat()
                
                # Update occurrence count and last seen
                error["occurrences"] = error.get("occurrences", 1) + 1
                error["last_seen"] = datetime.datetime.now().isoformat()
                
                self._save_data('errors')
                return
        
        # Record new error
        error_record = {
            "id": error_id,
            "type": error_type,
            "message": message,
            "resolution": resolution,
            "code_context": code_context,
            "tags": tags or [],
            "created_at": datetime.datetime.now().isoformat(),
            "last_seen": datetime.datetime.now().isoformat(),
            "occurrences": 1,
            "resolved_at": datetime.datetime.now().isoformat() if resolution else None
        }
        
        self.errors_data["errors"].append(error_record)
        self._save_data('errors')
        
        # Generate a recommendation based on this error
        if resolution:
            self._generate_recommendation_from_error(error_record)
    
    def record_pattern(self, pattern_type: str, name: str, description: str,
                       code_example: Optional[str] = None, is_anti_pattern: bool = False,
                       tags: Optional[List[str]] = None) -> None:
        """Record a development pattern or anti-pattern.
        
        Args:
            pattern_type: Category of pattern (e.g., 'design', 'code', 'workflow').
            name: Name of the pattern.
            description: Description of the pattern.
            code_example: Example code demonstrating the pattern.
            is_anti_pattern: Whether this is an anti-pattern to avoid.
            tags: List of tags for categorizing the pattern.
        """
        # Create pattern record
        pattern_record = {
            "type": pattern_type,
            "name": name,
            "description": description,
            "code_example": code_example,
            "tags": tags or [],
            "created_at": datetime.datetime.now().isoformat(),
            "occurrences": 1
        }
        
        # Add to appropriate list
        if is_anti_pattern:
            self.patterns_data["anti_patterns"].append(pattern_record)
        else:
            self.patterns_data["patterns"].append(pattern_record)
        
        self._save_data('patterns')
    
    def record_code_metric(self, file_path: str, metrics: Dict[str, Any]) -> None:
        """Record code quality metrics for a file.
        
        Args:
            file_path: Path to the file being measured.
            metrics: Dictionary of metrics (e.g., {'complexity': 10, 'lines': 100}).
        """
        # Create metric record
        metric_record = {
            "file_path": file_path,
            "metrics": metrics,
            "recorded_at": datetime.datetime.now().isoformat()
        }
        
        self.metrics_data["code_metrics"].append(metric_record)
        self._save_data('metrics')
    
    def record_performance_metric(self, component: str, operation: str, 
                                 duration_ms: float, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record a performance metric.
        
        Args:
            component: Component being measured (e.g., 'database', 'api').
            operation: Operation being measured (e.g., 'query', 'request').
            duration_ms: Duration in milliseconds.
            metadata: Additional metadata about the operation.
        """
        # Create performance record
        performance_record = {
            "component": component,
            "operation": operation,
            "duration_ms": duration_ms,
            "metadata": metadata or {},
            "recorded_at": datetime.datetime.now().isoformat()
        }
        
        self.metrics_data["performance_metrics"].append(performance_record)
        self._save_data('metrics')
    
    def add_recommendation(self, title: str, description: str, contexts: Optional[List[str]] = None,
                          priority: int = 3, link: Optional[str] = None, tags: Optional[List[str]] = None) -> None:
        """Add a recommendation for improving development.
        
        Args:
            title: Short title for the recommendation.
            description: Detailed description of the recommendation.
            contexts: List of contexts where this recommendation applies (e.g., 'api_development').
            priority: Priority level (1-5, where 1 is highest).
            link: Link to additional information.
            tags: List of tags for categorizing the recommendation.
        """
        # Create recommendation record
        recommendation_record = {
            "title": title,
            "description": description,
            "contexts": contexts or [],
            "priority": priority,
            "link": link,
            "tags": tags or [],
            "created_at": datetime.datetime.now().isoformat(),
            "implemented": False
        }
        
        self.recommendations_data["recommendations"].append(recommendation_record)
        self._save_data('recommendations')
    
    def _generate_recommendation_from_error(self, error_record: Dict[str, Any]) -> None:
        """Generate a recommendation based on an error.
        
        Args:
            error_record: Error record to generate recommendation from.
        """
        if not error_record.get("resolution"):
            return
        
        title = f"Prevent '{error_record['type']}' errors"
        description = f"We've seen this error: '{error_record['message']}' "
        
        if error_record.get("code_context"):
            description += f"in {error_record['code_context']}. "
        else:
            description += ". "
        
        description += f"Resolution: {error_record['resolution']}"
        
        contexts = []
        if error_record.get("code_context"):
            # Extract file extension to determine context
            match = re.search(r'\.([a-zA-Z0-9]+):', error_record["code_context"])
            if match:
                ext = match.group(1)
                if ext == 'py':
                    contexts.append('python_development')
                elif ext in ('js', 'jsx', 'ts', 'tsx'):
                    contexts.append('javascript_development')
                elif ext in ('html', 'css'):
                    contexts.append('frontend_development')
        
        # Determine priority based on occurrences
        priority = max(1, 6 - min(error_record.get("occurrences", 1), 5))
        
        self.add_recommendation(
            title=title,
            description=description,
            contexts=contexts,
            priority=priority,
            tags=error_record.get("tags", []) + [error_record["type"]]
        )
    
    def get_recommendations(self, task: Optional[str] = None, tags: Optional[List[str]] = None,
                           limit: int = 5) -> List[Dict[str, Any]]:
        """Get recommendations for a specific task or with specific tags.
        
        Args:
            task: Task context to get recommendations for.
            tags: List of tags to filter recommendations by.
            limit: Maximum number of recommendations to return.
            
        Returns:
            List of recommendation records.
        """
        # Filter recommendations
        filtered = self.recommendations_data["recommendations"]
        
        if task:
            filtered = [r for r in filtered if not r.get("contexts") or task in r.get("contexts", [])]
        
        if tags:
            filtered = [r for r in filtered if any(tag in r.get("tags", []) for tag in tags)]
        
        # Sort by priority (lower number = higher priority)
        filtered.sort(key=lambda r: r.get("priority", 5))
        
        return filtered[:limit]
    
    def analyze_errors(self) -> Dict[str, Any]:
        """Analyze recorded errors to identify patterns.
        
        Returns:
            Dictionary with analysis results.
        """
        if not self.errors_data["errors"]:
            return {"message": "No errors recorded yet"}
        
        # Count errors by type
        error_types = Counter(error["type"] for error in self.errors_data["errors"])
        
        # Find most common error messages
        error_messages = Counter(error["message"] for error in self.errors_data["errors"])
        
        # Calculate resolution rate
        total_errors = len(self.errors_data["errors"])
        resolved_errors = sum(1 for error in self.errors_data["errors"] if error.get("resolution"))
        resolution_rate = resolved_errors / total_errors if total_errors > 0 else 0
        
        # Find recurring errors (errors that have occurred multiple times)
        recurring_errors = [error for error in self.errors_data["errors"] 
                           if error.get("occurrences", 1) > 1]
        
        return {
            "total_errors": total_errors,
            "resolved_errors": resolved_errors,
            "resolution_rate": resolution_rate,
            "error_types": dict(error_types.most_common(5)),
            "common_messages": dict(error_messages.most_common(5)),
            "recurring_errors_count": len(recurring_errors),
            "most_frequent_errors": sorted(recurring_errors, 
                                        key=lambda e: e.get("occurrences", 1), 
                                        reverse=True)[:5] if recurring_errors else []
        }
    
    def analyze_project_health(self) -> Dict[str, Any]:
        """Analyze overall project health based on all collected data.
        
        Returns:
            Dictionary with health metrics and recommendations.
        """
        # Analyze errors
        error_analysis = self.analyze_errors()
        
        # Calculate "health score" (simplistic example - would be more sophisticated in practice)
        health_score = 100
        
        # Deduct points for unresolved errors
        if error_analysis.get("total_errors", 0) > 0:
            unresolved_rate = 1 - error_analysis.get("resolution_rate", 0)
            health_score -= min(40, unresolved_rate * 50)
        
        # Deduct points for recurring errors
        recurring_error_count = error_analysis.get("recurring_errors_count", 0)
        health_score -= min(30, recurring_error_count * 5)
        
        # Get top recommendations
        top_recommendations = self.get_recommendations(limit=3)
        
        return {
            "health_score": max(0, health_score),
            "error_analysis": error_analysis,
            "top_recommendations": top_recommendations,
            "generated_at": datetime.datetime.now().isoformat()
        }

    def scan_codebase(self, root_dir: Optional[str] = None) -> Dict[str, Any]:
        """Scan the codebase for common issues and patterns.
        
        Args:
            root_dir: Root directory of the codebase. If None, uses the current directory.
            
        Returns:
            Dictionary with scan results.
        """
        if root_dir is None:
            root_dir = os.getcwd()
        
        root_path = Path(root_dir)
        
        # Initialize scan results
        results = {
            "scanned_files": 0,
            "issues_found": 0,
            "patterns_found": 0,
            "issues_by_type": defaultdict(int),
            "patterns_by_type": defaultdict(int),
            "file_issues": []
        }
        
        # Common anti-patterns to look for (simplified examples)
        anti_patterns = {
            "hardcoded_port": re.compile(r'port\s*=\s*\d{4}'),
            "disconnected_error_handling": re.compile(r'except.*?:(\s*pass|\s*print)'),
            "print_debugging": re.compile(r'print\([\'"]DEBUG'),
        }
        
        # Scan files
        for file_path in root_path.glob('**/*.py'):
            results["scanned_files"] += 1
            file_issues = []
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Check for anti-patterns
                    for pattern_name, pattern_regex in anti_patterns.items():
                        matches = pattern_regex.findall(content)
                        if matches:
                            results["issues_found"] += len(matches)
                            results["issues_by_type"][pattern_name] += len(matches)
                            file_issues.append({
                                "type": pattern_name,
                                "count": len(matches)
                            })
                            
                            # Record as anti-pattern
                            description = f"Found {pattern_name} in {file_path.relative_to(root_path)}"
                            self.record_pattern(
                                pattern_type="code",
                                name=pattern_name,
                                description=description,
                                is_anti_pattern=True,
                                tags=["code_quality", "static_analysis"]
                            )
                            
                    # If issues were found, add to results
                    if file_issues:
                        results["file_issues"].append({
                            "file": str(file_path.relative_to(root_path)),
                            "issues": file_issues
                        })
            except Exception as e:
                logger.error(f"Error scanning file {file_path}: {e}")
        
        return results

    def track_performance(self, component: str, operation: str, duration_ms: float) -> None:
        """Alias for record_performance_metric so FlaskInsights can log performance."""
        # Delegate to existing performance recording method (metadata defaults to None)
        self.record_performance_metric(
            component=component,
            operation=operation,
            duration_ms=duration_ms
        )

# Decorator to track performance of functions
def track_performance(component: str, operation: Optional[str] = None):
    """Decorator to track the performance of a function.
    
    Args:
        component: Component being measured.
        operation: Operation being measured. If None, uses function name.
    
    Returns:
        Decorated function.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            
            duration_ms = (end_time - start_time).total_seconds() * 1000
            
            # Get or create tracker
            try:
                tracker = DevelopmentTracker()
                tracker.record_performance_metric(
                    component=component,
                    operation=operation or func.__name__,
                    duration_ms=duration_ms,
                    metadata={"args_count": len(args), "kwargs_count": len(kwargs)}
                )
            except Exception as e:
                logger.error(f"Error tracking performance: {e}")
            
            return result
        return wrapper
    return decorator

# Function to handle errors and record them
def record_error(func):
    """Decorator to record errors that occur in a function.
    
    Args:
        func: Function to decorate.
    
    Returns:
        Decorated function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Record the error
            try:
                import traceback
                tb = traceback.extract_tb(e.__traceback__)
                last_frame = tb[-1]
                code_context = f"{last_frame.filename}:{last_frame.lineno}"
                
                tracker = DevelopmentTracker()
                tracker.record_error(
                    error_type=type(e).__name__,
                    message=str(e),
                    code_context=code_context
                )
            except Exception as tracking_error:
                logger.error(f"Error recording error: {tracking_error}")
            
            # Re-raise the original exception
            raise
    return wrapper 