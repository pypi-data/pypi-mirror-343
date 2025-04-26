"""
Unified Quantum API

This module implements the unified API layer for integrating the four quantum
technology pillars:
1. Stochastic Quantum Methods
2. Memsaur Technology
3. Backend Selection Optimization
4. Circuit Cutting and Distribution

The QuantumAPI class provides a simplified, unified interface to these technologies,
allowing them to be used individually or in combination through a consistent API.
"""

import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, Literal
import uuid

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Define a simple BaseModel if pydantic is not available
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

# Import the necessary quantum components
try:
    from qiskit import QuantumCircuit
except ImportError:
    # Create a minimal QuantumCircuit class for type hints if qiskit is not available
    class QuantumCircuit:
        """Placeholder for QuantumCircuit when qiskit is not available."""
        pass

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Data Models for Configuration
class StochasticConfig(BaseModel):
    """Configuration for stochastic quantum methods."""
    precision: float = 0.01
    max_iterations: int = 1000
    default_shots: int = 1024
    api_key: Optional[str] = None
    api_host: Optional[str] = None

class MemoryConfig(BaseModel):
    """Configuration for quantum memory management."""
    network_size: int = 4
    coherence_extension_factor: float = 2.0
    memory_timeout: int = 3600  # seconds

class BackendConfig(BaseModel):
    """Configuration for backend selection."""
    weights: Dict[str, float] = {
        'qubit_count': 1.0,
        'connectivity': 0.8,
        'error_rates': 0.9,
        'queue_length': 0.5,
        'gate_set': 0.7,
        'uptime': 0.6,
        'memory': 0.8
    }
    refresh_interval: int = 300  # seconds

class CircuitCuttingConfig(BaseModel):
    """Configuration for circuit cutting."""
    max_subcircuit_width: int = 20
    max_cuts: int = 5
    default_method: str = 'graph_partition'

class GeneralConfig(BaseModel):
    """General configuration for the unified API."""
    log_level: str = 'INFO'
    cache_timeout: int = 300  # seconds

class QuantumAPIConfig(BaseModel):
    """Configuration for the unified quantum API."""
    stochastic_methods: StochasticConfig = StochasticConfig()
    memory_management: MemoryConfig = MemoryConfig()
    backend_selection: BackendConfig = BackendConfig()
    circuit_cutting: CircuitCuttingConfig = CircuitCuttingConfig()
    general: GeneralConfig = GeneralConfig()
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'QuantumAPIConfig':
        """Create config from dictionary."""
        # Extract section configs
        stochastic_dict = config_dict.get('stochastic_methods', {})
        memory_dict = config_dict.get('memory_management', {})
        backend_dict = config_dict.get('backend_selection', {})
        circuit_dict = config_dict.get('circuit_cutting', {})
        general_dict = config_dict.get('general', {})
        
        # Create config objects
        return cls(
            stochastic_methods=StochasticConfig(**stochastic_dict),
            memory_management=MemoryConfig(**memory_dict),
            backend_selection=BackendConfig(**backend_dict),
            circuit_cutting=CircuitCuttingConfig(**circuit_dict),
            general=GeneralConfig(**general_dict)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'stochastic_methods': vars(self.stochastic_methods),
            'memory_management': vars(self.memory_management),
            'backend_selection': vars(self.backend_selection),
            'circuit_cutting': vars(self.circuit_cutting),
            'general': vars(self.general)
        }

# Result Data Models
class StochasticResult(BaseModel):
    """Result from stochastic quantum methods."""
    final_state: List[float]
    trajectory: List[List[float]]
    expectation_values: Dict[str, float]
    execution_time: float
    shots_used: int
    backend_used: str
    success: bool
    error_message: Optional[str] = None

class MemoryHandle(BaseModel):
    """Handle for quantum memory allocation."""
    id: str
    allocation_time: str
    size: int
    expiration_time: Optional[str] = None

class MemoryResult(BaseModel):
    """Result from memory operations."""
    success: bool
    memory_handle: Optional[MemoryHandle] = None
    data: Optional[Any] = None
    coherence_metrics: Optional[Dict[str, float]] = None
    error_message: Optional[str] = None

class BackendSelection(BaseModel):
    """Result from backend selection."""
    recommended_backends: List[Dict[str, Any]]
    best_match: Dict[str, Any]
    score_details: Dict[str, float]

class CircuitExecutionResult(BaseModel):
    """Result from circuit cutting and execution."""
    original_circuit_properties: Dict[str, Any]
    subcircuit_count: int
    cut_count: int
    execution_results: Dict[str, Any]
    reconstructed_results: Dict[str, Any]
    execution_time: float
    success: bool
    error_message: Optional[str] = None

class WorkflowResult(BaseModel):
    """Result from a combined workflow."""
    workflow_id: str
    execution_time: float
    steps: List[Dict[str, Any]]
    results: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

# Exception classes
class QuantumAPIError(Exception):
    """Base class for all Quantum API errors."""
    pass

class StochasticMethodsError(QuantumAPIError):
    """Errors in stochastic quantum methods."""
    pass

class MemoryError(QuantumAPIError):
    """Errors in quantum memory operations."""
    pass

class BackendSelectionError(QuantumAPIError):
    """Errors in backend selection."""
    pass

class CircuitCuttingError(QuantumAPIError):
    """Errors in circuit cutting operations."""
    pass

class WorkflowError(QuantumAPIError):
    """Errors in workflow execution."""
    pass

# Technology Interfaces
class StochasticQuantumMethods:
    """Interface for stochastic quantum methods."""
    
    def simulate_qsde(self, parameters: Dict[str, Any]) -> StochasticResult:
        """Run a quantum stochastic differential equation simulation."""
        raise NotImplementedError("Method not implemented")
    
    def propagate_bayesian_risk(self, initial_probabilities: List[float],
                             market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Propagate risk through a quantum Bayesian network."""
        raise NotImplementedError("Method not implemented")

class QuantumMemoryManager:
    """Interface for quantum memory management."""
    
    def allocate(self, state_description: Dict[str, Any]) -> MemoryHandle:
        """Allocate quantum memory."""
        raise NotImplementedError("Method not implemented")
    
    def store(self, memory_handle: MemoryHandle, quantum_data: Any) -> bool:
        """Store quantum data in memory."""
        raise NotImplementedError("Method not implemented")
    
    def retrieve(self, memory_handle: MemoryHandle) -> Any:
        """Retrieve quantum data from memory."""
        raise NotImplementedError("Method not implemented")
    
    def release(self, memory_handle: MemoryHandle) -> bool:
        """Release quantum memory."""
        raise NotImplementedError("Method not implemented")

class BackendSelector:
    """Interface for backend selection."""
    
    def select(self, circuit: QuantumCircuit, 
              requirements: Dict[str, Any]) -> BackendSelection:
        """Select optimal backend."""
        raise NotImplementedError("Method not implemented")
    
    def predict_performance(self, circuit: QuantumCircuit,
                           backend: Any) -> Dict[str, Any]:
        """Predict performance of circuit on backend."""
        raise NotImplementedError("Method not implemented")

class CircuitCutter:
    """Interface for circuit cutting."""
    
    def cut(self, circuit: QuantumCircuit, 
           strategy: Dict[str, Any]) -> List[Any]:
        """Cut circuit into smaller subcircuits."""
        raise NotImplementedError("Method not implemented")
    
    def execute(self, subcircuits: List[Any],
               backend: Any) -> List[Any]:
        """Execute subcircuits."""
        raise NotImplementedError("Method not implemented")
    
    def reconstruct(self, results: List[Any]) -> Dict[str, Any]:
        """Reconstruct full circuit result."""
        raise NotImplementedError("Method not implemented")

# Import adapters 
# These will be implemented in separate files
try:
    from .adapters.stochastic_adapter import StochasticMethodsAdapter
    from .adapters.memsaur_adapter import MemsaurAdapter
    from .adapters.backend_adapter import BackendSelectorAdapter
    from .adapters.circuit_adapter import CircuitCutterAdapter
    HAS_ADAPTERS = True
except ImportError:
    HAS_ADAPTERS = False
    logger.warning("Adapters not found, will use placeholder implementations")

# Main API class
class QuantumAPI:
    """Unified API for quantum technology pillars."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Quantum API.
        
        Args:
            config: Optional configuration dictionary for customizing behavior
        """
        logger.info("Initializing Quantum API")
        start_time = time.time()
        
        # Load configuration
        self.config = QuantumAPIConfig.from_dict(config or {})
        
        # Set up logging based on configuration
        log_level = getattr(logging, self.config.general.log_level, logging.INFO)
        logger.setLevel(log_level)
        
        # Initialize technology components (lazy loading)
        self._stochastic_methods = None
        self._memory_manager = None
        self._backend_selector = None
        self._circuit_cutter = None
        
        # Cache for storing frequent results
        self._cache = {}
        
        logger.info(f"Quantum API initialized in {time.time() - start_time:.2f} seconds")
    
    def _get_stochastic_methods(self) -> StochasticQuantumMethods:
        """Get or initialize stochastic methods component."""
        if self._stochastic_methods is None:
            logger.info("Initializing stochastic quantum methods")
            try:
                if HAS_ADAPTERS:
                    self._stochastic_methods = StochasticMethodsAdapter(self.config.stochastic_methods)
                else:
                    # Use a placeholder for now
                    self._stochastic_methods = StochasticQuantumMethods()
            except Exception as e:
                logger.error(f"Failed to initialize stochastic methods: {str(e)}")
                raise StochasticMethodsError(f"Initialization error: {str(e)}")
                
        return self._stochastic_methods
    
    def _get_memory_manager(self) -> QuantumMemoryManager:
        """Get or initialize memory manager component."""
        if self._memory_manager is None:
            logger.info("Initializing quantum memory manager")
            try:
                if HAS_ADAPTERS:
                    self._memory_manager = MemsaurAdapter(self.config.memory_management)
                else:
                    # Use a placeholder for now
                    self._memory_manager = QuantumMemoryManager()
            except Exception as e:
                logger.error(f"Failed to initialize memory manager: {str(e)}")
                raise MemoryError(f"Initialization error: {str(e)}")
                
        return self._memory_manager
    
    def _get_backend_selector(self) -> BackendSelector:
        """Get or initialize backend selector component."""
        if self._backend_selector is None:
            logger.info("Initializing backend selector")
            try:
                if HAS_ADAPTERS:
                    self._backend_selector = BackendSelectorAdapter(self.config.backend_selection)
                else:
                    # Use a placeholder for now
                    self._backend_selector = BackendSelector()
            except Exception as e:
                logger.error(f"Failed to initialize backend selector: {str(e)}")
                raise BackendSelectionError(f"Initialization error: {str(e)}")
                
        return self._backend_selector
    
    def _get_circuit_cutter(self) -> CircuitCutter:
        """Get or initialize circuit cutter component."""
        if self._circuit_cutter is None:
            logger.info("Initializing circuit cutter")
            try:
                # Import adapters here to avoid circular imports
                from .adapters import HAS_ADAPTERS
                from .adapters.circuit_adapter import CircuitCutterAdapter
                
                if HAS_ADAPTERS:
                    self._circuit_cutter = CircuitCutterAdapter(self.config.circuit_cutting)
                else:
                    # Use a placeholder implementation
                    self._circuit_cutter = CircuitCutter()
                    logger.warning("No circuit cutter adapter available, using placeholder")
            except Exception as e:
                logger.error(f"Failed to initialize circuit cutter: {str(e)}")
                raise CircuitCuttingError(f"Initialization error: {str(e)}")
                
        return self._circuit_cutter
    
    def run_stochastic_simulation(self, 
                               parameters: Dict[str, Any],
                               **kwargs) -> StochasticResult:
        """
        Run a stochastic quantum simulation.
        
        Args:
            parameters: Parameters for the stochastic simulation
            **kwargs: Additional options
            
        Returns:
            StochasticResult object with simulation results
        """
        logger.info("Running stochastic quantum simulation")
        start_time = time.time()
        
        try:
            stochastic = self._get_stochastic_methods()
            
            # Determine which stochastic method to use
            method = parameters.get('method', 'qsde')
            
            if method == 'qsde':
                result = stochastic.simulate_qsde(parameters)
            elif method == 'bayesian':
                # Extract parameters
                initial_probabilities = parameters.get('initial_probabilities', [0.5] * 5)
                market_data = parameters.get('market_data', {})
                
                # Run Bayesian propagation
                raw_result = stochastic.propagate_bayesian_risk(
                    initial_probabilities=initial_probabilities,
                    market_data=market_data
                )
                
                # Convert to standardized result format
                result = StochasticResult(
                    final_state=raw_result.get('updated_probabilities', []),
                    trajectory=raw_result.get('probability_trajectory', [[]]),
                    expectation_values=raw_result.get('expectation_values', {}),
                    execution_time=raw_result.get('execution_time', time.time() - start_time),
                    shots_used=raw_result.get('shots', 0),
                    backend_used=raw_result.get('backend', 'unknown'),
                    success=True,
                    error_message=None
                )
            else:
                raise StochasticMethodsError(f"Unknown stochastic method: {method}")
            
            # Add execution time
            result.execution_time = time.time() - start_time
            logger.info(f"Stochastic simulation completed in {result.execution_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Stochastic simulation failed: {str(e)}")
            
            # Return error result
            return StochasticResult(
                final_state=[],
                trajectory=[[]],
                expectation_values={},
                execution_time=execution_time,
                shots_used=0,
                backend_used='none',
                success=False,
                error_message=str(e)
            )
    
    def hybrid_predict(self, market_data, stochastic_weight=None, neural_weight=None):
        """
        Generate a hybrid prediction using the StochasticNeuralBridge.

        Args:
            market_data: Input market data (e.g., pandas DataFrame)
            stochastic_weight: Optional override for stochastic component weight
            neural_weight: Optional override for neural component weight

        Returns:
            Combined prediction dictionary with 'predicted_price', 'confidence', and components breakdown
        """
        logger.info("Running hybrid_predict with hybrid bridge")

        # Lazy initialization of stochastic simulator
        if not hasattr(self, '_stochastic_simulator') or self._stochastic_simulator is None:
            from quantum_finance.quantum_toolkit.stochastic.stochastic_quantum_simulator import StochasticQuantumSimulator
            # Determine configuration space dimension from market_data
            try:
                dim = market_data.shape[1]
            except Exception:
                dim = 1
            self._stochastic_simulator = StochasticQuantumSimulator(config_space_dim=dim)

        # Lazy initialization of neural network
        if not hasattr(self, '_neural_network') or self._neural_network is None:
            from quantum_finance.quantum_toolkit.hybrid.neural import TrajectoryConditionedNetwork
            try:
                input_dim = market_data.shape[1]
            except Exception:
                input_dim = 1
            self._neural_network = TrajectoryConditionedNetwork(
                input_dim=input_dim,
                hidden_dims=[20, 10],
                output_dim=1
            )

        # Lazy initialization of bridge
        if not hasattr(self, '_bridge') or self._bridge is None:
            from quantum_finance.quantum_toolkit.hybrid.stochastic_neural import StochasticNeuralBridge
            config = {
                'stochastic_weight': stochastic_weight or 0.5,
                'neural_weight': neural_weight or 0.5,
                'adaptive_weighting': True,
                'uncertainty_threshold': 0.2
            }
            self._bridge = StochasticNeuralBridge(
                self._stochastic_simulator,
                self._neural_network,
                config
            )
        else:
            if stochastic_weight is not None:
                self._bridge.config['stochastic_weight'] = stochastic_weight
            if neural_weight is not None:
                self._bridge.config['neural_weight'] = neural_weight

        # Generate and return prediction
        return self._bridge.predict(market_data)
    
    def manage_quantum_memory(self,
                           memory_operation: str,
                           quantum_data: Any = None,
                           memory_handle: Optional[MemoryHandle] = None,
                           **kwargs) -> MemoryResult:
        """
        Perform quantum memory operations.
        
        Args:
            memory_operation: Operation to perform ('allocate', 'store', 'retrieve', 'release')
            quantum_data: Data for store operations
            memory_handle: Handle for retrieve/release operations
            **kwargs: Additional options
            
        Returns:
            MemoryResult object with operation results
        """
        logger.info(f"Performing quantum memory operation: {memory_operation}")
        start_time = time.time()
        
        try:
            memory_manager = self._get_memory_manager()
            
            if memory_operation == 'allocate':
                # Create a state description from quantum_data
                state_description = quantum_data if isinstance(quantum_data, dict) else {'data': quantum_data}
                handle = memory_manager.allocate(state_description)
                
                return MemoryResult(
                    success=True,
                    memory_handle=handle,
                    execution_time=time.time() - start_time
                )
                
            elif memory_operation == 'store':
                if not memory_handle:
                    raise MemoryError("Memory handle required for store operation")
                
                success = memory_manager.store(memory_handle, quantum_data)
                
                return MemoryResult(
                    success=success,
                    memory_handle=memory_handle,
                    execution_time=time.time() - start_time
                )
                
            elif memory_operation == 'retrieve':
                if not memory_handle:
                    raise MemoryError("Memory handle required for retrieve operation")
                
                data = memory_manager.retrieve(memory_handle)
                
                return MemoryResult(
                    success=True,
                    memory_handle=memory_handle,
                    data=data,
                    execution_time=time.time() - start_time
                )
                
            elif memory_operation == 'release':
                if not memory_handle:
                    raise MemoryError("Memory handle required for release operation")
                
                success = memory_manager.release(memory_handle)
                
                return MemoryResult(
                    success=success,
                    memory_handle=memory_handle,
                    execution_time=time.time() - start_time
                )
                
            else:
                raise MemoryError(f"Unknown memory operation: {memory_operation}")
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Memory operation failed: {str(e)}")
            
            return MemoryResult(
                success=False,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def select_optimal_backend(self,
                            circuit: QuantumCircuit,
                            requirements: Dict[str, Any] = None,
                            **kwargs) -> BackendSelection:
        """
        Select the optimal backend for the given circuit.
        
        Args:
            circuit: The quantum circuit to execute
            requirements: Requirements for backend selection
            **kwargs: Additional options
            
        Returns:
            BackendSelection object with backend recommendations
        """
        logger.info("Selecting optimal backend")
        start_time = time.time()
        
        try:
            selector = self._get_backend_selector()
            
            # Use default requirements if none provided
            if requirements is None:
                requirements = {
                    'min_qubits': getattr(circuit, 'num_qubits', 2),
                }
            
            # Check cache before performing selection
            cache_key = f"backend_selection_{hash(str(circuit))}"
            if cache_key in self._cache:
                cache_entry = self._cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.config.general.cache_timeout:
                    logger.info("Using cached backend selection")
                    return cache_entry['result']
            
            # Perform backend selection
            result = selector.select(circuit, requirements)
            
            # Cache the result
            self._cache[cache_key] = {
                'timestamp': time.time(),
                'result': result
            }
            
            logger.info(f"Backend selection completed in {time.time() - start_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Backend selection failed: {str(e)}")
            raise BackendSelectionError(f"Selection error: {str(e)}")
    
    def cut_and_execute_circuit(self,
                             circuit: QuantumCircuit,
                             cutting_strategy: Dict[str, Any] = None,
                             backend: Any = None,
                             **kwargs) -> CircuitExecutionResult:
        """
        Cut, distribute, and execute a large quantum circuit.
        
        Args:
            circuit: The quantum circuit to execute
            cutting_strategy: Strategy for circuit cutting
            backend: Backend to execute on (or None to select automatically)
            **kwargs: Additional options
            
        Returns:
            CircuitExecutionResult object with execution results
        """
        logger.info("Cutting and executing circuit")
        start_time = time.time()
        
        try:
            cutter = self._get_circuit_cutter()
            
            # Use default strategy if none provided
            if cutting_strategy is None:
                cutting_strategy = {
                    'method': self.config.circuit_cutting.default_method,
                    'max_subcircuit_width': self.config.circuit_cutting.max_subcircuit_width,
                    'max_cuts': self.config.circuit_cutting.max_cuts
                }
            
            # Analyze original circuit
            original_properties = {
                'num_qubits': getattr(circuit, 'num_qubits', 0),
                'depth': getattr(circuit, 'depth', lambda: 0)(),
                'operations': getattr(circuit, 'count_ops', lambda: {})()
            }
            
            # Select backend if not provided
            if backend is None and kwargs.get('use_optimal_backend', True):
                backend_selection = self.select_optimal_backend(
                    circuit, 
                    kwargs.get('backend_requirements', {})
                )
                backend = backend_selection.best_match.get('backend')
            
            # Cut the circuit
            subcircuits = cutter.cut(circuit, cutting_strategy)
            
            # Execute subcircuits
            subcircuit_results = cutter.execute(subcircuits, backend)
            
            # Reconstruct the results
            reconstructed_results = cutter.reconstruct(subcircuit_results)
            
            result = CircuitExecutionResult(
                original_circuit_properties=original_properties,
                subcircuit_count=len(subcircuits),
                cut_count=len(subcircuits) - 1,
                execution_results={'subcircuit_results': subcircuit_results},
                reconstructed_results=reconstructed_results,
                execution_time=time.time() - start_time,
                success=True,
                error_message=None
            )
            
            logger.info(f"Circuit execution completed in {result.execution_time:.2f} seconds")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Circuit execution failed: {str(e)}")
            
            return CircuitExecutionResult(
                original_circuit_properties={},
                subcircuit_count=0,
                cut_count=0,
                execution_results={},
                reconstructed_results={},
                execution_time=execution_time,
                success=False,
                error_message=str(e)
            )
    
    def execute_workflow(self,
                      workflow_definition: Dict[str, Any],
                      **kwargs) -> WorkflowResult:
        """
        Execute a workflow combining multiple technologies.
        
        Args:
            workflow_definition: Definition of the workflow steps
            **kwargs: Additional options
            
        Returns:
            WorkflowResult object with workflow results
        """
        logger.info("Executing quantum workflow")
        start_time = time.time()
        
        workflow_id = workflow_definition.get('id', str(uuid.uuid4()))
        steps = workflow_definition.get('steps', [])
        workflow_results = {}
        executed_steps = []
        
        try:
            for i, step in enumerate(steps):
                step_type = step.get('type')
                step_params = step.get('parameters', {})
                step_id = step.get('id', f"step_{i}")
                
                logger.info(f"Executing workflow step {i+1}/{len(steps)}: {step_type}")
                step_start_time = time.time()
                
                # Execute the appropriate operation based on step type
                if step_type == 'stochastic_simulation':
                    result = self.run_stochastic_simulation(step_params)
                    
                elif step_type == 'memory_operation':
                    # Get memory operation details
                    memory_op = step_params.get('operation')
                    memory_data = step_params.get('data')
                    memory_handle = step_params.get('handle')
                    
                    # If handle is a reference to previous step, resolve it
                    if isinstance(memory_handle, str) and memory_handle.startswith('$'):
                        ref_step = memory_handle[1:]
                        if ref_step in workflow_results:
                            memory_result = workflow_results[ref_step]
                            memory_handle = memory_result.memory_handle
                    
                    result = self.manage_quantum_memory(memory_op, memory_data, memory_handle)
                    
                elif step_type == 'backend_selection':
                    # Get circuit from parameters or from a previous step
                    circuit_ref = step_params.get('circuit_reference')
                    circuit = step_params.get('circuit')
                    
                    if circuit_ref and circuit_ref.startswith('$'):
                        ref_step = circuit_ref[1:]
                        if ref_step in workflow_results:
                            circuit = workflow_results[ref_step].get('circuit')
                    
                    requirements = step_params.get('requirements', {})
                    result = self.select_optimal_backend(circuit, requirements)
                    
                elif step_type == 'circuit_execution':
                    # Get circuit from parameters or from a previous step
                    circuit_ref = step_params.get('circuit_reference')
                    circuit = step_params.get('circuit')
                    
                    if circuit_ref and circuit_ref.startswith('$'):
                        ref_step = circuit_ref[1:]
                        if ref_step in workflow_results:
                            circuit = workflow_results[ref_step].get('circuit')
                    
                    cutting_strategy = step_params.get('cutting_strategy')
                    backend = step_params.get('backend')
                    
                    # If backend is a reference to a previous step, resolve it
                    if isinstance(backend, str) and backend.startswith('$'):
                        ref_step = backend[1:]
                        if ref_step in workflow_results:
                            backend_result = workflow_results[ref_step]
                            backend = backend_result.best_match.get('backend')
                    
                    result = self.cut_and_execute_circuit(circuit, cutting_strategy, backend)
                    
                else:
                    raise WorkflowError(f"Unknown step type: {step_type}")
                
                # Store the result
                workflow_results[step_id] = result
                
                # Record the executed step
                executed_steps.append({
                    'id': step_id,
                    'type': step_type,
                    'execution_time': time.time() - step_start_time,
                    'success': getattr(result, 'success', True)
                })
            
            # Create the workflow result
            result = WorkflowResult(
                workflow_id=workflow_id,
                execution_time=time.time() - start_time,
                steps=executed_steps,
                results=workflow_results,
                success=True,
                error_message=None
            )
            
            logger.info(f"Workflow execution completed in {result.execution_time:.2f} seconds")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Workflow execution failed: {str(e)}")
            
            return WorkflowResult(
                workflow_id=workflow_id,
                execution_time=execution_time,
                steps=executed_steps,
                results=workflow_results,
                success=False,
                error_message=str(e)
            ) 