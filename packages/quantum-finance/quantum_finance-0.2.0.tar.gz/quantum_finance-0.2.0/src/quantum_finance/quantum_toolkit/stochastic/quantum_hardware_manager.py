"""
Quantum Hardware Resource Manager

This module manages access to quantum hardware providers, tracks usage quotas,
and optimizes resource allocation to ensure efficient use of limited quantum
computing time.

Notes:
- Current implementation supports IBM Quantum hardware via Qiskit
- Monthly quota of 10 minutes (600 seconds) is tracked and enforced
- Provides intelligent fallback to classical methods when appropriate
- Maintains usage logs to inform optimization decisions
"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional, List, Tuple, Union, Type
from datetime import datetime
from dotenv import load_dotenv

# Conditional imports for quantum providers
try:
    # Updated imports for newer Qiskit versions
    from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, SamplerV2
    # Import base classes and local primitives for type hinting and fallback
    from qiskit.primitives import ( # Qiskit SDK 1.0+
        BaseEstimatorV2,
        BaseSamplerV2,
        StatevectorEstimator, 
        StatevectorSampler
    )
    # Aer might still be useful for direct simulation if needed, but primitives are preferred
    from qiskit_aer import Aer
    # Standard Qiskit error
    from qiskit.exceptions import QiskitError
    HAS_IBMQ = True
except ImportError:
    HAS_IBMQ = False
    # Define placeholders if imports fail
    QiskitRuntimeService = None # type: ignore
    EstimatorV2 = None # type: ignore
    SamplerV2 = None # type: ignore
    BaseEstimatorV2 = None # type: ignore
    BaseSamplerV2 = None # type: ignore
    StatevectorEstimator = None # type: ignore
    StatevectorSampler = None # type: ignore
    Aer = None # type: ignore
    QiskitError = Exception # type: ignore
    logging.warning("qiskit-ibm-runtime or qiskit not fully available. Quantum hardware access disabled.")

logger = logging.getLogger(__name__)

class QuantumHardwareManager:
    """
    Manages access to quantum hardware resources and tracks usage quotas.
    
    This class handles:
    1. Loading and managing API keys from .env file
    2. Tracking monthly usage against quotas
    3. Selecting appropriate backends based on problem characteristics
    4. Providing fallback to classical methods when appropriate
    5. Logging usage for optimization decisions
    """
    
    def __init__(self, 
                 usage_log_file: str = "quantum_usage_log.json",
                 monthly_quota_seconds: int = 600,  # 10 minutes default
                 min_problem_size: int = 10,        # Min assets for quantum
                 max_problem_size: int = 50,        # Max assets for quantum
                 enforce_quota: bool = True):       # Whether to enforce quota limits
        """
        Initialize the quantum hardware manager.
        
        Args:
            usage_log_file: Path to the JSON file tracking usage
            monthly_quota_seconds: Monthly quota in seconds (default: 600s = 10min)
            min_problem_size: Minimum problem size for quantum optimization
            max_problem_size: Maximum problem size for quantum optimization
            enforce_quota: Whether to enforce quota limits
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize IBM Quantum settings
        self.ibmq_api_key = os.getenv("IBMQ_API_KEY", "")
        
        # Get additional configuration variables
        self.ibmq_hub = os.getenv("IBMQ_HUB", "ibm-q")
        self.ibmq_group = os.getenv("IBMQ_GROUP", "open")
        self.ibmq_project = os.getenv("IBMQ_PROJECT", "main")
        
        # Build the channel string
        self.ibmq_channel = f"{self.ibmq_hub}/{self.ibmq_group}/{self.ibmq_project}"
        
        # Initialize usage tracking
        self.usage_log_file = usage_log_file
        self.monthly_quota_seconds = monthly_quota_seconds
        self.min_problem_size = min_problem_size
        self.max_problem_size = max_problem_size
        self.enforce_quota = enforce_quota
        self.usage_stats = self._load_usage_stats()
        
        # Initialize provider and backend info
        self.service = None
        self.available_backends = []
        self._initialize_provider()
        
        # Optimization parameters
        self.optimization_methods = {
            "small": "classical",           # Up to min_problem_size assets
            "medium": "hybrid",             # Between min and max problem size
            "large": "classical_advanced"   # Above max_problem_size assets
        }
        
        logger.info("QuantumHardwareManager initialized")
        
    def _initialize_provider(self) -> None:
        """Initialize the quantum provider if API key is available."""
        if not HAS_IBMQ or QiskitRuntimeService is None:
            logger.warning("IBM Quantum provider package not available, cannot initialize service.")
            self.service = None
            return
            
        try:
            # Try using existing credentials first
            # Check if QiskitRuntimeService is callable (not None)
            if QiskitRuntimeService:
                self.service = QiskitRuntimeService()
                logger.info("Successfully connected to IBM Quantum service using existing credentials")
                self.available_backends = self._get_available_backends()
                logger.info(f"Available backends: {len(self.available_backends)}")
                return # Success
            else:
                 raise QiskitError("QiskitRuntimeService not available despite HAS_IBMQ being True.")

        except Exception as e1:
            logger.warning(f"Could not load existing credentials or initialize service: {str(e1)}")
            # Proceed to try with API key from .env

        if not self.ibmq_api_key or self.ibmq_api_key == "your_api_key_here":
            logger.warning("No valid IBMQ API key found in environment, cannot initialize service.")
            self.service = None
            return
            
        try:
            # Initialize with API key if QiskitRuntimeService is callable
            if QiskitRuntimeService:
                self.service = QiskitRuntimeService(
                    channel="ibm_quantum", 
                    token=self.ibmq_api_key,
                )
                self.available_backends = self._get_available_backends()
                logger.info(f"Successfully connected to IBM Quantum service with API key")
                logger.info(f"Available backends: {len(self.available_backends)}")
            else:
                logger.error("QiskitRuntimeService not available to initialize with API key.")
                self.service = None
                
        except QiskitError as e:
            logger.error(f"Failed to initialize IBM Quantum service with API key: {str(e)}")
            self.service = None
        except Exception as e:
            logger.error(f"Unexpected error initializing quantum provider with API key: {str(e)}")
            self.service = None
    
    def _get_available_backends(self) -> List[str]:
        """Get list of available backends from the provider."""
        if not self.service:
            return []
            
        try:
            backends = self.service.backends()
            return [backend.name for backend in backends]
        except Exception as e:
            logger.error(f"Error getting available backends: {str(e)}")
            return []
    
    def _load_usage_stats(self) -> Dict[str, Any]:
        """Load usage statistics from the log file."""
        if not os.path.exists(self.usage_log_file):
            return {"jobs": []}
            
        try:
            with open(self.usage_log_file, 'r') as f:
                data = json.load(f)
                # Ensure jobs key exists
                if "jobs" not in data:
                    data["jobs"] = []
                return data
        except json.JSONDecodeError:
            logger.error(f"Error parsing usage log file {self.usage_log_file}")
            return {"jobs": []}
        except IOError:
            logger.error(f"Error reading usage log file {self.usage_log_file}")
            return {"jobs": []}
    
    def _save_usage_stats(self) -> None:
        """Save usage statistics to the log file."""
        try:
            with open(self.usage_log_file, 'w') as f:
                json.dump(self.usage_stats, f, indent=2)
        except IOError:
            logger.error(f"Error writing to usage log file {self.usage_log_file}")
    
    def check_quota_available(self) -> bool:
        """Check if there's quantum computing time left in the current month's quota."""
        if not self.enforce_quota:
            return True
            
        current_month = datetime.now().strftime("%Y-%m")
        
        if current_month not in self.usage_stats:
            self.usage_stats[current_month] = 0.0
            
        return self.usage_stats[current_month] < self.monthly_quota_seconds
    
    def get_remaining_quota(self) -> float:
        """Get remaining quantum computing time in seconds for the current month."""
        current_month = datetime.now().strftime("%Y-%m")
        
        if current_month not in self.usage_stats:
            return self.monthly_quota_seconds
            
        return max(0, self.monthly_quota_seconds - self.usage_stats[current_month])
    
    def log_usage(self, execution_time: float, job_metadata: Dict[str, Any]) -> None:
        """
        Log quantum hardware usage.
        
        Args:
            execution_time: Execution time in seconds
            job_metadata: Dictionary with job metadata
        """
        current_month = datetime.now().strftime("%Y-%m")
        
        if current_month not in self.usage_stats:
            self.usage_stats[current_month] = 0.0
            
        self.usage_stats[current_month] += execution_time
        
        # Log the job details
        job_info = {
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "metadata": job_metadata
        }
        
        self.usage_stats.setdefault("jobs", []).append(job_info)
        self._save_usage_stats()
        
        logger.info(f"Logged quantum usage: {execution_time:.2f}s, " +
                   f"remaining: {self.get_remaining_quota():.2f}s")
    
    def get_optimization_method(self, problem_size: int) -> str:
        """
        Determine the appropriate optimization method based on problem size and quota.
        
        Args:
            problem_size: Size of the problem (e.g., number of assets)
            
        Returns:
            Optimization method to use ('quantum', 'hybrid', or 'classical')
        """
        # Check if we have quantum availability (Service initialized and quota available)
        has_quantum = HAS_IBMQ and self.service is not None and self.check_quota_available()
        
        if not has_quantum:
            logger.info("No quantum resources available (provider/quota), using classical optimization")
            return "classical"
            
        # Determine method based on problem size
        if problem_size < self.min_problem_size:
            logger.info(f"Problem size {problem_size} too small for quantum advantage, using classical")
            return "classical"
        elif problem_size > self.max_problem_size:
            logger.info(f"Problem size {problem_size} too large for current quantum hardware, using advanced classical")
            return "classical_advanced"
        else:
            # For medium size problems, check remaining quota
            remaining_quota = self.get_remaining_quota()
            if remaining_quota < 60:  # Less than 1 minute left
                logger.info(f"Limited quota remaining ({remaining_quota:.2f}s), using hybrid optimization")
                return "hybrid"
            else:
                logger.info(f"Using full quantum optimization for problem size {problem_size}")
                return "quantum"
    
    def get_estimator_primitive(self, 
                                options: Optional[Dict] = None, 
                                use_simulator: bool = False) -> Optional[Any]: # Revert to Any if type hints fail
        """
        Get a Qiskit Estimator primitive (V2 API).
        Returns a runtime Estimator if service and quota are available,
        otherwise returns a local StatevectorEstimator simulator.
        
        Args:
            options: Optional dictionary of runtime options for the Estimator.
            use_simulator: Force use of simulator regardless of service/quota.
            
        Returns:
            An instance implementing BaseEstimatorV2, or None if imports failed.
        """
        if not HAS_IBMQ or StatevectorEstimator is None or BaseEstimatorV2 is None:
            logger.warning("Qiskit packages/Estimator classes not available. Cannot provide Estimator.")
            return None

        # Determine if we should use the simulator
        should_use_simulator = use_simulator or not self.service or not self.check_quota_available()

        if should_use_simulator:
            if not self.service:
                 reason = "no quantum service available"
            elif not self.check_quota_available():
                 reason = "quota exceeded"
            else:
                 reason = "explicitly requested"
            logger.info(f"Using local StatevectorEstimator ({reason}).")
            if StatevectorEstimator is None:
                logger.error("StatevectorEstimator class is not available due to import error.")
                return None
            try:
                # StatevectorEstimator V2 might take options, but often defaults are fine.
                # Pass options cautiously or not at all if unsure.
                return StatevectorEstimator()
            except Exception as e:
                logger.error(f"Failed to initialize StatevectorEstimator: {e}")
                return None
        else:
            # Use the runtime EstimatorV2
            logger.info(f"Attempting to use IBM Quantum EstimatorV2.")
            if EstimatorV2 is None:
                logger.error("EstimatorV2 class is not available.")
                # Attempt fallback even if runtime class isn't found, maybe service exists
                # Fallback handled below
            elif self.service:
                try:
                    # Pass options dict directly. Backend selection can be inside options.
                    # Ex: options={"backend": "ibm_simulator", "resilience_level": 1}
                    # If no backend in options, service default is used.
                    runtime_options = options or {}
                    estimator = EstimatorV2(options=runtime_options)
                    logger.info(f"Initialized runtime EstimatorV2 with options: {runtime_options}")
                    return estimator
                except Exception as e:
                    logger.error(f"Failed to initialize runtime EstimatorV2: {e}")
                    # Fallback handled below
            
            # Fallback to local simulator if runtime init failed or service was None initially
            logger.warning("Falling back to local StatevectorEstimator.")
            if StatevectorEstimator:
                try:
                    return StatevectorEstimator()
                except Exception as e_sim:
                     logger.error(f"Failed to initialize fallback StatevectorEstimator: {e_sim}")
                     return None
            else:
                logger.error("StatevectorEstimator not available for fallback.")
                return None # No fallback available

    def get_sampler_primitive(self, 
                              options: Optional[Dict] = None, 
                              use_simulator: bool = False) -> Optional[Any]: # Revert to Any if type hints fail
        """
        Get a Qiskit Sampler primitive (V2 API).
        Returns a runtime Sampler if service and quota are available,
        otherwise returns a local StatevectorSampler simulator.
        
        Args:
            options: Optional dictionary of runtime options for the Sampler.
            use_simulator: Force use of simulator regardless of service/quota.
            
        Returns:
            An instance implementing BaseSamplerV2, or None if imports failed.
        """
        if not HAS_IBMQ or StatevectorSampler is None or BaseSamplerV2 is None:
            logger.warning("Qiskit packages/Sampler classes not available. Cannot provide Sampler.")
            return None

        # Determine if we should use the simulator
        should_use_simulator = use_simulator or not self.service or not self.check_quota_available()

        if should_use_simulator:
            if not self.service:
                 reason = "no quantum service available"
            elif not self.check_quota_available():
                 reason = "quota exceeded"
            else:
                 reason = "explicitly requested"
            logger.info(f"Using local StatevectorSampler ({reason}).")
            if StatevectorSampler is None:
                logger.error("StatevectorSampler class is not available due to import error.")
                return None
            try:
                # Local StatevectorSampler takes options like seed, but try without to appease linter
                # local_options = {k: v for k, v in (options or {}).items() if k == 'seed_simulator'}
                # if 'seed_simulator' in local_options:
                #     local_options['seed'] = local_options.pop('seed_simulator')
                # Try initializing WITH options first
                return StatevectorSampler()
            except Exception as e:
                logger.error(f"Failed to initialize StatevectorSampler: {e}")
                return None
        else:
            # Use the runtime SamplerV2
            logger.info(f"Attempting to use IBM Quantum SamplerV2.")
            if SamplerV2 is None:
                logger.error("SamplerV2 class is not available.")
                # Fallback handled below
            elif self.service:
                try:
                    runtime_options = options or {}
                    # Pass options dict. Backend selection via options or service default.
                    sampler = SamplerV2(options=runtime_options)
                    logger.info(f"Initialized runtime SamplerV2 with options: {runtime_options}")
                    return sampler
                except Exception as e:
                    logger.error(f"Failed to initialize runtime SamplerV2: {e}")
                    # Fallback handled below

            # Fallback to local simulator
            logger.warning("Falling back to local StatevectorSampler.")
            if StatevectorSampler:
                try:
                    # Try initializing fallback Sampler WITHOUT options first to appease linter
                    local_options = {k: v for k, v in (options or {}).items() if k == 'seed_simulator'}
                    if 'seed_simulator' in local_options:
                         local_options['seed'] = local_options.pop('seed_simulator')
                    # If options are needed, pass them: StatevectorSampler(options=local_options)
                    return StatevectorSampler() 
                except Exception as e_sim:
                     logger.error(f"Failed to initialize fallback StatevectorSampler: {e_sim}")
                     return None # Fallback init failed
            else:
                logger.error("StatevectorSampler not available for fallback.")
                return None # No fallback available
    
    def estimate_execution_time(self, 
                              num_qubits: int, 
                              circuit_depth: int, 
                              shots: int = 1024) -> float:
        """
        Estimate execution time for quantum circuits.
        
        Args:
            num_qubits: Number of qubits in the circuit
            circuit_depth: Depth of the circuit
            shots: Number of shots for circuit execution
            
        Returns:
            Estimated execution time in seconds
        """
        # Simple heuristic model - can be refined with actual benchmarks
        # Base time for circuit initialization
        base_time = 1.0
        
        # Time proportional to circuit complexity (qubits * depth)
        complexity_factor = 0.01
        complexity_time = complexity_factor * num_qubits * circuit_depth
        
        # Time proportional to number of shots
        shot_factor = 0.001
        shot_time = shot_factor * shots
        
        # Add overhead for real hardware vs simulator
        hardware_overhead = 5.0 if self.service else 1.0
        
        # Total estimated time
        total_time = (base_time + complexity_time + shot_time) * hardware_overhead
        
        return total_time
    
    def get_optimal_batch_size(self, 
                             num_qubits: int, 
                             circuit_depth: int,
                             total_circuits: int) -> int:
        """
        Determine optimal batch size for circuit execution.
        
        Args:
            num_qubits: Number of qubits in each circuit
            circuit_depth: Depth of each circuit
            total_circuits: Total number of circuits to execute
            
        Returns:
            Optimal batch size
        """
        # Simple heuristic for batch sizing - can be refined
        if not self.service:
            # For simulator, larger batches are generally better
            return min(50, total_circuits)
            
        # For real hardware, consider circuit complexity
        complexity = num_qubits * circuit_depth
        
        if complexity < 100:
            return min(20, total_circuits)
        elif complexity < 500:
            return min(10, total_circuits)
        else:
            return min(5, total_circuits) 