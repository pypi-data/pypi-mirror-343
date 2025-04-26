#!/usr/bin/env python3

"""
IBM Quantum Enhanced Interface

This module provides a unified interface that combines three advanced quantum computing features:
1. Intelligent Backend Selection
2. Job Monitoring and Alerting
3. Circuit Cutting for Larger Circuits

It offers a simplified API for executing quantum circuits on IBM Quantum hardware with
advanced features for optimizing performance, monitoring execution, and handling larger circuits.

Usage:
    from ibm_quantum_enhanced import IBMQuantumEnhanced
    
    # Initialize the enhanced interface
    quantum = IBMQuantumEnhanced()
    
    # Create a quantum circuit
    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(5, 5)
    # ... add gates to your circuit ...
    circuit.measure_all()
    
    # Execute with all advanced features
    result = quantum.run_circuit(circuit)
    
    # Access the results
    counts = result.get_counts()

Author: Quantum-AI Team
"""

import os
import sys
import time
import logging
import tempfile
from typing import Dict, List, Union, Optional, Any, Tuple, Callable

# Import Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options
from qiskit_ibm_runtime.exceptions import IBMBackendApiError
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.result import Counts

# Import our advanced feature modules
from .quantum_toolkit.integration.backend_selection import IntelligentBackendSelector, SelectionCriteria
from .quantum_toolkit.integration.ibm_quantum_job_monitor import IBMQuantumJobMonitor, AlertConfiguration, JobStatus
from .quantum_toolkit.circuits.ibm_quantum_circuit_cutting import QuantumCircuitCutter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ibm_quantum_enhanced')


class EnhancedResult:
    """
    Enhanced result class that wraps the IBM Quantum result and provides additional information.
    """
    
    def __init__(self, 
                original_result: Any = None, 
                job_id: Optional[str] = None,
                backend_name: Optional[str] = None,
                circuit_cut: bool = False,
                subcircuit_count: int = 0,
                execution_time: float = 0.0,
                metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize the enhanced result.
        
        Args:
            original_result: Original result from IBM Quantum
            job_id: ID of the job
            backend_name: Name of the backend used
            circuit_cut: Whether circuit cutting was applied
            subcircuit_count: Number of subcircuits (if circuit cutting was applied)
            execution_time: Total execution time
            metadata: Additional metadata
        """
        self.original_result = original_result
        self.job_id = job_id
        self.backend_name = backend_name
        self.circuit_cut = circuit_cut
        self.subcircuit_count = subcircuit_count
        self.execution_time = execution_time
        self.metadata = metadata or {}
        
    def get_counts(self) -> Dict[str, int]:
        """
        Get the counts from the result.
        Handles V2 SamplerResult, older Result types, and dicts, prioritizing direct get_counts if available.
        
        Returns:
            Dictionary of bitstrings and their counts
        """
        logger.debug(f"Starting get_counts for result type: {type(self.original_result)}")
        
        # --- Attempt 1: Direct get_counts() method on the result object itself ---
        # This often works for various Qiskit result types, including potentially PrimitiveResult
        logger.debug("Checking for direct get_counts() method on the result object...")
        if hasattr(self.original_result, 'get_counts'):
            try:
                logger.info("Found direct get_counts() method. Calling it.")
                counts_data = self.original_result.get_counts()
                # PrimitiveResult.get_counts() might return a Counts object or list thereof
                # Handle potential list (though unlikely for single circuit run)
                if isinstance(counts_data, list):
                    if counts_data:
                        logger.debug("Direct get_counts() returned a list, taking first element.")
                        counts_data = counts_data[0]
                    else:
                        logger.warning("Direct get_counts() returned an empty list.")
                        return {}
                        
                if isinstance(counts_data, dict) or isinstance(counts_data, Counts):
                    logger.debug(f"Successfully extracted counts via direct get_counts(): {counts_data}")
                    return dict(counts_data)
                else:
                    logger.warning(f"Direct get_counts() returned unexpected type after list check: {type(counts_data)}")
            except Exception as e:
                logger.warning(f"Exception during direct get_counts() call: {e}", exc_info=True)
        else:
             logger.debug("No direct get_counts() method found on result object.")

        # --- Attempt 2: V2 Path (via Pubs) - If direct get_counts failed ---
        # This is the expected path for runtime results
        logger.debug("Checking for V2 structure via 'pubs' attribute...")
        try:
            if hasattr(self.original_result, 'pubs') and self.original_result.pubs:
                logger.debug("Found 'pubs' attribute. Proceeding with nested V2 logic.")
                first_pub_result = self.original_result.pubs[0]
                
                if hasattr(first_pub_result, 'data') and first_pub_result.data is not None:
                    logger.debug(f"Accessing PubResult.data object: {first_pub_result.data}")
                    data_bin_like = first_pub_result.data
                    try:
                        for reg_name in data_bin_like:
                            try:
                                register_data = getattr(data_bin_like, reg_name)
                                if hasattr(register_data, 'get_counts'):
                                    logger.info(f"Found get_counts() in nested register '{reg_name}'. Calling it.")
                                    counts_obj = register_data.get_counts()
                                    if isinstance(counts_obj, dict) or isinstance(counts_obj, Counts):
                                        logger.debug(f"Successfully extracted nested V2 counts: {counts_obj}")
                                        return dict(counts_obj)
                                    else:
                                        logger.warning(f"Nested get_counts() on '{reg_name}' returned unexpected type: {type(counts_obj)}")
                            except Exception as nested_reg_err:
                                logger.warning(f"Error processing nested register '{reg_name}': {nested_reg_err}")
                        logger.warning("V2/Pubs Path: No register with a valid get_counts() found.")
                    except TypeError:
                        logger.warning(f"V2/Pubs Path: PubResult.data object (type: {type(data_bin_like)}) is not iterable.")
                else:
                    logger.warning("V2/Pubs Path: First PubResult missing 'data' attribute or it is None.")
            else:
                logger.debug("No 'pubs' attribute found.")

        except Exception as e:
            logger.warning(f"Exception during V2/Pubs path processing: {e}", exc_info=True)

        # --- Attempt 3: V1 Path (Quasi Dists) ---
        logger.debug("Checking for V1 structure (quasi_dists attribute)...")
        try:
            if hasattr(self.original_result, 'quasi_dists'):
                logger.info("Found 'quasi_dists'. Attempting V1 conversion.")
                return self._convert_quasi_dists_to_counts()
        except Exception as e:
            logger.warning(f"Exception during V1 path processing: {e}", exc_info=True)
            
        # --- Attempt 4: Dictionary access ---
        logger.debug("Checking for fallback: dictionary access for 'counts' key...")
        if isinstance(self.original_result, dict) and 'counts' in self.original_result:
            logger.info("Found 'counts' key in dictionary result. Accessing it.")
            return self.original_result['counts']
            
        # --- Final Failure ---
        logger.error("Could not extract counts from result object of type %s after all attempts", type(self.original_result))
        return {}
            
    def _convert_quasi_dists_to_counts(self) -> Dict[str, int]:
        """
        Convert quasi-distributions to counts.
        
        Returns:
            Dictionary of bitstrings and their counts
        """
        try:
            shots = self.metadata.get('shots', 1024)
            counts = {}
            
            for quasi_dist in self.original_result.quasi_dists:
                for bitstring, probability in quasi_dist.items():
                    # Convert binary int to bitstring
                    bit_str = format(bitstring, f'0{self.metadata.get("num_qubits", 1)}b')
                    counts[bit_str] = int(round(probability * shots))
            
            return counts
            
        except Exception as e:
            logger.error(f"Error converting quasi-distributions to counts: {e}")
            return {}
    
    def get_memory(self) -> List[str]:
        """
        Get the memory (individual measurement results) from the result.
        
        Returns:
            List of measurement results as bitstrings
        """
        if hasattr(self.original_result, 'get_memory'):
            return self.original_result.get_memory()
        else:
            logger.warning("Memory not available in result")
            return []
    
    def get_statevector(self) -> Any:
        """
        Get the statevector from the result, if available.
        
        Returns:
            Statevector or None if not available
        """
        if hasattr(self.original_result, 'get_statevector'):
            return self.original_result.get_statevector()
        else:
            logger.warning("Statevector not available in result")
            return None
    
    def __str__(self) -> str:
        """String representation of the result."""
        return (
            f"EnhancedResult(job_id={self.job_id}, "
            f"backend={self.backend_name}, "
            f"circuit_cut={self.circuit_cut}, "
            f"subcircuit_count={self.subcircuit_count}, "
            f"execution_time={self.execution_time:.2f}s)"
        )


class IBMQuantumEnhanced:
    """
    Enhanced interface for IBM Quantum with advanced features.
    """
    
    def __init__(self, 
                token: Optional[str] = None,
                backend_selector: Optional[IntelligentBackendSelector] = None,
                job_monitor: Optional[IBMQuantumJobMonitor] = None,
                circuit_cutter: Optional[QuantumCircuitCutter] = None,
                service: Optional[QiskitRuntimeService] = None):
        """
        Initialize the enhanced IBM Quantum interface.
        
        Args:
            token: IBM Quantum API token (if None, will try to use token from environment or disk)
            backend_selector: Custom backend selector instance
            job_monitor: Custom job monitor instance
            circuit_cutter: Custom circuit cutter instance
            service: Existing QiskitRuntimeService instance
        """
        # Set up IBM Quantum service
        self.token = token or os.environ.get('IBM_QUANTUM_TOKEN')
        
        if service is not None:
            self.service = service
        else:
            self.service = self._initialize_service()
        
        # Initialize components
        self.backend_selector = backend_selector or IntelligentBackendSelector(service=self.service)
        
        # Corrected AlertConfiguration initialization
        alert_config = AlertConfiguration(
            long_queue_threshold=600,  # Map from max_queue_time
            long_execution_threshold=1800,  # Map from max_execution_time
            alert_on_failure=True, # Assume alert_on_status=['ERROR', 'CANCELLED'] implies this
            result_quality_threshold=0.8 # Map from min_result_quality
            # status_check_interval and alert_on_status_change use defaults
        )
        self.job_monitor = job_monitor or IBMQuantumJobMonitor(alert_config=alert_config)
    
        self.circuit_cutter = circuit_cutter or QuantumCircuitCutter(max_subcircuit_width=16)
    
    def _initialize_service(self) -> QiskitRuntimeService:
        """
        Initialize the IBM Quantum service.
        
        Returns:
            QiskitRuntimeService instance
        """
        try:
            # First try with the token if provided
            if self.token:
                return QiskitRuntimeService(channel="ibm_quantum", token=self.token)
            
            # Otherwise try with saved credentials
            return QiskitRuntimeService()
        except Exception as e:
            logger.error(f"Error initializing IBM Quantum service: {e}")
            raise RuntimeError(f"Failed to initialize IBM Quantum service: {e}")
    
    def run_circuit(self, 
                   circuit: QuantumCircuit,
                   backend_name: Optional[str] = None,
                   shots: int = 1024,
                   selection_criteria: Optional[SelectionCriteria] = None,
                   use_circuit_cutting: bool = True,
                   max_subcircuit_width: Optional[int] = None,
                   cutting_method: str = 'graph_partition',
                   optimization_level: int = 1,
                   session: Optional[Session] = None,
                   callback: Optional[Callable[[str, Any], None]] = None) -> EnhancedResult:
        """
        Run a quantum circuit with enhanced features.
        
        Args:
            circuit: The quantum circuit to execute
            backend_name: Name of the backend to use (if None, will select automatically)
            shots: Number of shots for the execution
            selection_criteria: Criteria for backend selection
            use_circuit_cutting: Whether to use circuit cutting for large circuits
            max_subcircuit_width: Maximum width of subcircuits (if None, uses default)
            cutting_method: Method to use for circuit cutting
            optimization_level: Transpiler optimization level
            session: IBM Quantum session to use
            callback: Callback function for status updates
            
        Returns:
            EnhancedResult: Result with additional information
        """
        start_time = time.time()
        # Explicitly type hint metadata
        metadata: Dict[str, Any] = {
            'shots': int(shots) if shots is not None else 1024,
            'optimization_level': int(optimization_level) if optimization_level is not None else 1,
            'num_qubits': circuit.num_qubits,
            'depth': circuit.depth(),
            'num_gates': len(circuit.data)
        }
        
        # Step 1: Select the best backend if not specified
        if backend_name is None:
            # Extract relevant info from SelectionCriteria for select_backend call
            sel_custom_weights = getattr(selection_criteria, 'weights', None)
            sel_required_gates = getattr(selection_criteria, 'required_gates', None)
            sel_min_qubits = getattr(selection_criteria, 'min_qubits', None)
            sel_max_queue = getattr(selection_criteria, 'max_queue_length', None)
            
            # Build filters (Note: required_gates and max_queue are not direct filters here)
            sel_backend_filters = {}
            if sel_min_qubits is not None:
                # This filter isn't directly supported by IntelligentBackendSelector, 
                # but qubit count is checked during evaluation.
                pass 

            # Call select_backend with appropriate args
            recommended_backends = self.backend_selector.select_backend(
                circuit,
                custom_weights=sel_custom_weights,
                backend_filters=sel_backend_filters
            )
            
            # Check if any recommendations were found
            if not recommended_backends:
                raise RuntimeError("No suitable backend found by IntelligentBackendSelector.")
            
            # Get the best backend (first in the sorted list)
            best_backend_info = recommended_backends[0]
            backend = best_backend_info['backend'] # Get the actual backend object
            backend_name = backend.name
            logger.info(f"Selected backend: {backend_name} (Score: {best_backend_info['overall_score']:.4f})")
        else:
            backend = self.service.backend(backend_name)
            logger.info(f"Using specified backend: {backend_name}")
        
        # Add backend name to metadata (as str)
        metadata['backend_name'] = str(backend_name)
        
        # Step 2: Apply circuit cutting if necessary and enabled
        circuit_cut = False
        subcircuit_count = 0
        
        if use_circuit_cutting and circuit.num_qubits > backend.num_qubits:
            logger.info(f"Circuit requires {circuit.num_qubits} qubits but backend only has "
                       f"{backend.num_qubits}. Applying circuit cutting.")
            
            if max_subcircuit_width is not None:
                self.circuit_cutter.max_subcircuit_width = max_subcircuit_width
            else:
                self.circuit_cutter.max_subcircuit_width = backend.num_qubits
                
            # Cut the circuit
            subcircuits = self.circuit_cutter.cut_circuit(
                circuit, method=cutting_method
            )
            subcircuit_count = len(subcircuits)
            
            # Execute subcircuits
            executed_subcircuits = self.circuit_cutter.execute_subcircuits(
                subcircuits, backend=backend
            )
            
            # Reconstruct results
            result_data = self.circuit_cutter.reconstruct_results(executed_subcircuits)
            
            circuit_cut = True
            metadata['circuit_cut'] = True
            metadata['subcircuit_count'] = int(subcircuit_count) # Ensure int
            metadata['cutting_method'] = str(cutting_method) # Ensure str
            
            # Create a job ID for the composite execution
            job_id = f"cut-{int(time.time())}-{subcircuit_count}"
            
            execution_time = time.time() - start_time
            
            # Return the reconstructed result
            return EnhancedResult(
                original_result=result_data,
                job_id=job_id,
                backend_name=backend_name,
                circuit_cut=True,
                subcircuit_count=subcircuit_count,
                execution_time=execution_time,
                metadata=metadata
            )
        
        # Step 3: Transpile the circuit (if not cut) for the target backend
        logger.info(f"Transpiling circuit for {backend_name} with optimization level {optimization_level}")
        try:
            # Use the selected backend object for transpilation
            isa_circuit = transpile(circuit, backend=backend, optimization_level=optimization_level)
            logger.info("Transpilation successful.")
        except Exception as transpile_err:
            logger.error(f"Failed to transpile circuit for {backend_name}: {transpile_err}", exc_info=True)
            raise RuntimeError(f"Circuit transpilation failed: {transpile_err}")

        # Step 4: Execute the transpiled circuit
        logger.info(f"Executing transpiled circuit on {backend_name} with {shots} shots")
        
        # Use local variable to avoid obscuring parameter
        active_session: Optional[Session] = session 
        close_session: bool = False 
        
        try:
            # --- Session Management ---
            if active_session is None: 
                assert backend_name is not None, "Backend name must be specified or selected before creating a session."
                logger.debug(f"Creating Session for backend: {backend_name}")
                # Ensure the backend object is available
                if backend is None: 
                     backend = self.service.backend(backend_name) # Fetch the object if needed
                # Initialize Session with the BackendV2 object
                active_session = Session(backend=backend)
                close_session = True 
            
            # --- Sampler Initialization with Minimal Options --- 
            from qiskit_ibm_runtime import Sampler
            try:
                # Initialize Sampler with mode and only default_shots in options dict
                options_dict = {"default_shots": shots}
                sampler = Sampler(mode=active_session, options=options_dict)
                logger.info(f"Initialized Sampler with options: {options_dict}")
                
            except Exception as e:
                 logger.error(f"Failed to initialize Sampler: {e}", exc_info=True)
                 raise RuntimeError(f"Failed to initialize Sampler: {e}")
            
            # --- Job Execution --- 
            job = sampler.run([isa_circuit], shots=shots) 
            logger.info(f"Submitted job {job.job_id()} to {backend_name}")
            
            # Start monitoring the job AFTER submission
            # --- Define Callbacks Dictionary (needed if callback provided) --- 
            job_callbacks = None
            if callback:
                job_callbacks = {
                    'status_change': lambda job_id, status, old_status: callback(
                        "status", {"job_id": job_id, "status": status, "old_status": old_status}
                    ),
                    'completion': lambda job_id, metrics: callback(
                        "completion", {"job_id": job_id, "metrics": metrics}
                    ),
                    'failure': lambda job_id, metrics: callback(
                        "failure", {"job_id": job_id, "metrics": metrics}
                    )
                }
            
            # Start monitoring if callbacks are defined
            if job_callbacks: 
                self.job_monitor.monitor_job(
                    job_id=job.job_id(), 
                    job=job,             
                    callbacks=job_callbacks # Pass the dictionary, not the raw callback
                )
                # Wait for result with timeout
                logger.info(f"Monitoring started for {job.job_id()}. Waiting for result...")
                try:
                    timeout = self.job_monitor.alert_config.long_execution_threshold + 120 
                    result = job.result(timeout=timeout)
                    logger.info(f"Received result for job {job.job_id()}")
                except Exception as res_err:
                    logger.error(f"Failed to get result for job {job.job_id()} within timeout: {res_err}")
                    metadata['error'] = f"Result retrieval failed: {str(res_err)}" 
            else: 
                logger.info(f"Waiting for job {job.job_id()} to complete synchronously...")
                result = job.result() 
                logger.info(f"Job {job.job_id()} completed synchronously.")

            # Calculate execution time (outside session block)
            execution_time = time.time() - start_time
            
            # Return the enhanced result
            # Ensure job_id is accessed only if job exists
            final_job_id = job.job_id() if job else None
            return EnhancedResult(
                original_result=result, 
                job_id=final_job_id,
                backend_name=backend_name,
                circuit_cut=circuit_cut,
                subcircuit_count=subcircuit_count,
                execution_time=execution_time,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error executing circuit: {e}")
            
            # Calculate execution time even for failed executions
            execution_time = time.time() - start_time
            
            # Return a result with error information
            metadata['error'] = str(e)
            return EnhancedResult(
                original_result=None,
                job_id=None,
                backend_name=backend_name,
                circuit_cut=circuit_cut,
                subcircuit_count=subcircuit_count,
                execution_time=execution_time,
                metadata=metadata
            )
        finally:
            # Close session only if it was created locally 
            if close_session and active_session: 
                try:
                    active_session.close()
                    logger.debug(f"Closed locally created session for backend {backend_name}")
                except Exception as sess_close_err:
                    logger.warning(f"Failed to close session: {sess_close_err}")
    
    def run_circuits(self, 
                    circuits: List[QuantumCircuit],
                    backend_name: Optional[str] = None,
                    shots: int = 1024,
                    selection_criteria: Optional[SelectionCriteria] = None,
                    use_circuit_cutting: bool = True,
                    max_subcircuit_width: Optional[int] = None,
                    optimization_level: int = 1,
                    session: Optional[Session] = None,
                    callback: Optional[Callable[[str, Any], None]] = None) -> List[EnhancedResult]:
        """
        Run multiple quantum circuits with enhanced features.
        
        Args:
            circuits: List of quantum circuits to execute
            backend_name: Name of the backend to use (if None, will select automatically)
            shots: Number of shots for the execution
            selection_criteria: Criteria for backend selection
            use_circuit_cutting: Whether to use circuit cutting for large circuits
            max_subcircuit_width: Maximum width of subcircuits (if None, uses default)
            optimization_level: Transpiler optimization level
            session: IBM Quantum session to use (Currently ignored in this implementation)
            callback: Callback function for status updates
            
        Returns:
            List of EnhancedResult objects
        """
        start_time = time.time()
        results: List[EnhancedResult] = []
        job: Optional[Any] = None
        selected_backend_name: Optional[str] = backend_name
        job_id_err: Optional[str] = None 
        # Use local variable to avoid obscuring parameter
        active_session: Optional[Session] = session 
        close_session: bool = False
        
        try:
            # Ensure service is initialized 
            assert self.service is not None, "IBM Quantum service is not initialized."
            service = self.service

            # --- Backend Selection --- 
            if selected_backend_name is None:
                if not circuits: # Check if circuits list is empty
                    raise ValueError("Circuit list cannot be empty if backend_name is not specified.")
                # Extract relevant info from SelectionCriteria for select_backend call
                sel_custom_weights = getattr(selection_criteria, 'weights', None)
                sel_required_gates = getattr(selection_criteria, 'required_gates', None)
                sel_min_qubits = getattr(selection_criteria, 'min_qubits', None)
                sel_max_queue = getattr(selection_criteria, 'max_queue_length', None)
                
                # Build filters 
                sel_backend_filters = {}
                # TODO: Implement filter creation based on criteria (e.g., sel_min_qubits)
                # if sel_min_qubits is not None:
                #    sel_backend_filters['min_num_qubits'] = sel_min_qubits 

                # Call select_backend with appropriate args, using the first circuit
                recommended_backends = self.backend_selector.select_backend(
                    circuits[0], # Use the first circuit for selection
                    custom_weights=sel_custom_weights,
                    backend_filters=sel_backend_filters
                )
                
                # Check if any recommendations were found
                if not recommended_backends:
                    raise RuntimeError("No suitable backend found by IntelligentBackendSelector for the first circuit.")
                
                # Get the best backend (first in the sorted list)
                best_backend_info = recommended_backends[0]
                # backend = best_backend_info['backend'] # Don't need the full backend object here
                selected_backend_name = best_backend_info['backend'].name # Just need the name
                logger.info(f"Selected backend based on first circuit: {selected_backend_name} (Score: {best_backend_info['overall_score']:.4f})")
            else:
                 # Verify backend exists using self.backend_selector.service
                 if not self.backend_selector.service: # Check service via backend_selector
                      raise RuntimeError("IBM Quantum service is not initialized (via backend selector).")
                 try:
                     # Use the local service variable to check existence
                     _ = service.backend(selected_backend_name) # Check if backend exists
                     logger.info(f"Using specified backend: {selected_backend_name}")
                 except Exception as e:
                     logger.error(f"Failed to get specified backend {selected_backend_name}: {e}")
                     raise

            # Ensure a backend name is selected
            if selected_backend_name is None:
                raise RuntimeError("Backend name could not be determined.")

            # --- Session Management --- 
            if active_session is None: 
                assert selected_backend_name is not None, "Selected backend name cannot be None here."
                logger.debug(f"Creating Session for backend: {selected_backend_name} for multiple circuits")
                # Need the actual backend object here
                backend_object = self.service.backend(selected_backend_name)
                # Initialize Session with the BackendV2 object
                active_session = Session(backend=backend_object)
                close_session = True
            else:
                 pass # Assume provided session is correctly configured

            # --- Sampler Initialization with Minimal Options --- 
            from qiskit_ibm_runtime import Sampler
            try:
                # Initialize Sampler with mode and only default_shots in options dict
                options_dict = {"default_shots": shots}
                sampler = Sampler(mode=active_session, options=options_dict)
                logger.info(f"Initialized Sampler for batch with options: {options_dict}")

            except Exception as e:
                 logger.error(f"Failed to initialize Sampler for batch: {e}", exc_info=True)
                 raise RuntimeError(f"Failed to initialize Sampler for batch: {e}")

            # Step 2: Transpile all circuits for the target backend
            logger.info(f"Transpiling {len(circuits)} circuits for {selected_backend_name} with optimization level {optimization_level}")
            transpiled_circuits = []
            try:
                # Transpile each circuit individually
                # TODO: Consider using PassManager for potentially better batch transpilation if performance is an issue
                for i, circ in enumerate(circuits):
                    logger.debug(f"Transpiling circuit {i+1}/{len(circuits)}...")
                    # Corrected: Ensure we use the backend *object* (backend_object)
                    isa_circuit = transpile(circ, backend=backend_object, optimization_level=optimization_level)
                    transpiled_circuits.append(isa_circuit)
                logger.info(f"Transpilation successful for all {len(transpiled_circuits)} circuits.")
            except Exception as transpile_err:
                logger.error(f"Failed to transpile one or more circuits for {selected_backend_name}: {transpile_err}", exc_info=True)
                raise RuntimeError(f"Circuit transpilation failed: {transpile_err}")

            # Step 3: Execute the transpiled circuits
            logger.info(f"Executing {len(transpiled_circuits)} transpiled circuits on {selected_backend_name} with {shots} shots")
            
            # Use local variable to avoid obscuring parameter
            active_session: Optional[Session] = session 
            close_session: bool = False
            
            try:
                # --- Job Execution --- 
                # Pass the *transpiled* circuit list and shots for this specific batch run
                # Note: optimization_level and resilience_level are implicitly default here
                job = sampler.run(transpiled_circuits, shots=shots)
                logger.info(f"Submitted batch job {job.job_id()} to {selected_backend_name}")
                
                # --- Define Callbacks Dictionary --- 
                job_callbacks = None
                if callback:
                    # Reconstruct the dictionary expected by monitor_job
                    job_callbacks = {
                        'status_change': lambda jid, status, old_status: callback(
                            "status", {"job_id": jid, "status": status, "old_status": old_status}
                        ),
                        'completion': lambda jid, metrics: callback(
                            "completion", {"job_id": jid, "metrics": metrics}
                        ),
                        'failure': lambda jid, metrics: callback(
                            "failure", {"job_id": jid, "metrics": metrics}
                        )
                        # Add other callbacks if the main callback function handles them
                    }

                # Start monitoring the job AFTER submission
                result: Optional[Any] = None # Initialize result
                if job_callbacks: # Check if we have a valid callbacks dict
                    self.job_monitor.monitor_job(
                        job_id=job.job_id(), 
                        job=job,             
                        callbacks=job_callbacks # Pass the dictionary
                    )
                    # Wait for result with timeout
                    logger.info(f"Monitoring started for {job.job_id()}. Waiting for result...")
                    try:
                        timeout = self.job_monitor.alert_config.long_execution_threshold + 120 
                        result = job.result(timeout=timeout)
                        logger.info(f"Received result for job {job.job_id()}")
                    except Exception as res_err:
                        logger.error(f"Failed to get result for job {job.job_id()} within timeout: {res_err}")
                        # Create error metadata for the failed result retrieval
                        error_metadata = {
                            'error': f'Result retrieval failed: {str(res_err)}', 
                            'backend_name': str(selected_backend_name),
                            'job_id': job.job_id() 
                        }
                        # Create EnhancedResult with error info
                        results = [EnhancedResult(
                            original_result=None, 
                            job_id=job.job_id(),
                            backend_name=selected_backend_name,
                            circuit_cut=False, 
                            subcircuit_count=0,
                            execution_time=time.time() - start_time, 
                            metadata=error_metadata
                        )] * len(circuits) # Apply error to all circuits in the batch
                        return results # Return immediately on result retrieval failure

                else: 
                    logger.info(f"Waiting for job {job.job_id()} to complete synchronously...")
                    result = job.result() 
                    logger.info(f"Job {job.job_id()} completed synchronously.")

                # Calculate execution time 
                execution_time = time.time() - start_time
                
                # Return the enhanced result(s) - result contains results for all circuits
                # Ensure job_id is accessed only if job exists (it does here)
                final_job_id = job.job_id()
                
                # Check if the result object is a V2 SamplerResult with pubs
                if result is not None and hasattr(result, 'pubs') and isinstance(result.pubs, list):
                     num_pubs = len(result.pubs)
                     if num_pubs != len(transpiled_circuits):
                          logger.warning(f"Number of PubResults ({num_pubs}) doesn't match number of submitted circuits ({len(transpiled_circuits)}) for job {final_job_id}.")
                          # Handle mismatch - maybe create error results or one result with warning
                          for i in range(len(transpiled_circuits)):
                              error_metadata = {
                                  'error': 'Mismatch between submitted circuit count and result pub count.',
                                  'shots': shots,
                                  'optimization_level': optimization_level,
                                  'backend_name': str(selected_backend_name),
                                  'job_id': final_job_id,
                                  'circuit_index': i
                              }
                              results.append(EnhancedResult(
                                  original_result=None, # No specific pub result to associate
                                  job_id=final_job_id,
                                  backend_name=selected_backend_name,
                                  circuit_cut=False,
                                  subcircuit_count=0,
                                  execution_time=execution_time / len(transpiled_circuits) if transpiled_circuits else execution_time,
                                  metadata=error_metadata
                              ))
                     else:
                          # Create an EnhancedResult for each PubResult
                          for i, pub_result in enumerate(result.pubs):
                               # Extract shots possibly specific to this PUB from metadata if available
                               pub_metadata_shots = pub_result.metadata.get('shots', shots) 
                               result_metadata = {
                                   'shots': pub_metadata_shots,
                                   'optimization_level': optimization_level,
                                   'backend_name': str(selected_backend_name),
                                   'job_id': final_job_id,
                                   'circuit_index': i
                                   # Add other relevant metadata from pub_result.metadata if needed
                               }
                               # Pass the individual PubResult as original_result
                               results.append(EnhancedResult(
                                   original_result=pub_result, 
                                   job_id=final_job_id,
                                   backend_name=selected_backend_name,
                                   circuit_cut=False, # Assuming no cutting within batch for now
                                   subcircuit_count=0,
                                   execution_time=execution_time / num_pubs, # Approximate time per pub
                                   metadata=result_metadata
                               ))
                elif result is None: # Handle case where result is None (job failed/timeout)
                     logger.error(f"Job {final_job_id} completed but result object is None. Creating error results.")
                     for i, circuit in enumerate(transpiled_circuits): # Use transpiled_circuits length
                          error_metadata = { 
                              'error': 'Job completed but no result object was returned.', 
                              'backend_name': str(selected_backend_name),
                              'job_id': final_job_id,
                              'circuit_index': i
                          }
                          results.append(EnhancedResult(
                             original_result=None, 
                             job_id=final_job_id,
                             backend_name=str(selected_backend_name),
                             circuit_cut=False, 
                             subcircuit_count=0,
                             execution_time=execution_time, # Use total time 
                             metadata=error_metadata
                          ))
                
            except Exception as e:
                logger.error(f"Error executing batch job: {e}", exc_info=True)
                execution_time = time.time() - start_time
                # Safely get job_id if job exists, otherwise use None
                job_id_err = job.job_id() if job else None 
                
                # Ensure results list is clear if error happened before loop (already initialized as empty)
                # results = [] # Not needed, initialized above
                for circuit_index, circuit in enumerate(circuits):
                     # Define error metadata dictionary inside the loop
                     error_metadata = { 
                         'error': f'Execution failed: {str(e)}', 
                         'backend_name': str(selected_backend_name), # Use selected_backend_name
                         'job_id': job_id_err, # Use the potentially None job_id_err
                         'circuit_index': circuit_index
                     }
                     
                     # Create EnhancedResult inside the loop, passing metadata inline
                     results.append(EnhancedResult(
                        original_result=None, 
                        job_id=job_id_err,
                        backend_name=str(selected_backend_name), # Use selected_backend_name
                        circuit_cut=False, 
                        subcircuit_count=0,
                        execution_time=execution_time / len(circuits) if circuits else execution_time, 
                        metadata=error_metadata
                     ))
        except Exception as e:
            logger.error(f"Error running multiple circuits: {e}", exc_info=True)
            execution_time = time.time() - start_time
            # Safely get job_id if job exists, otherwise use None
            job_id_err = job.job_id() if job else None 
            
            # Ensure results list is clear if error happened before loop (already initialized as empty)
            # results = [] # Not needed, initialized above
            for circuit_index, circuit in enumerate(circuits):
                 # Define error metadata dictionary inside the loop
                 error_metadata = { 
                     'error': f'Execution failed: {str(e)}', 
                     'backend_name': str(selected_backend_name), # Use selected_backend_name
                     'job_id': job_id_err, # Use the potentially None job_id_err
                     'circuit_index': circuit_index
                 }
                 
                 # Create EnhancedResult inside the loop, passing metadata inline
                 results.append(EnhancedResult(
                    original_result=None, 
                    job_id=job_id_err,
                    backend_name=str(selected_backend_name), # Use selected_backend_name
                    circuit_cut=False, 
                    subcircuit_count=0,
                    execution_time=execution_time / len(circuits) if circuits else execution_time, 
                    metadata=error_metadata
                 ))
        finally:
            # Close session only if it was created locally
            if close_session and active_session: # Check local variable
                try:
                    active_session.close() # Close the local variable
                    logger.debug(f"Closed locally created session for backend {selected_backend_name}")
                except Exception as sess_close_err:
                    logger.warning(f"Failed to close session: {sess_close_err}")
            
        return results # Return the list of results (or error results)
    
    def list_backends(self, 
                     min_qubits: Optional[int] = None, 
                     simulator: Optional[bool] = None,
                     operational: bool = True) -> List[str]:
        """
        List available backends with optional filtering.
        
        Args:
            min_qubits: Minimum number of qubits required
            simulator: If True, return only simulators; if False, return only real hardware
            operational: If True, return only operational backends
            
        Returns:
            List of backend names meeting the criteria
        """
        backends = self.service.backends()
        
        filtered_backends = []
        for backend in backends:
            # Skip non-operational backends if requested
            if operational:
                # In Qiskit 1.0+, operational status is accessed through status().operational
                # rather than directly as an attribute
                try:
                    is_operational = False
                    # Try different approaches for backward/forward compatibility
                    if hasattr(backend, 'status') and callable(backend.status):
                        status = backend.status()
                        is_operational = getattr(status, 'operational', False)
                    elif hasattr(backend, 'operational'):
                        # Fallback for older versions
                        is_operational = backend.operational
                    
                    if not is_operational:
                        continue
                except Exception as e:
                    logger.warning(f"Could not determine operational status for {backend.name}: {e}")
                    # Skip backends with undeterminable operational status
                    continue
                
            # Filter by simulator status if specified
            if simulator is not None:
                is_simulator = getattr(backend, 'simulator', None)
                if is_simulator is None and hasattr(backend, 'configuration'):
                    # Try to get from configuration if available
                    config = backend.configuration()
                    is_simulator = getattr(config, 'simulator', False)
                
                if simulator != is_simulator:
                    continue
            
            # Filter by minimum qubits if specified
            if min_qubits is not None:
                num_qubits = getattr(backend, 'num_qubits', 0)
                if num_qubits < min_qubits:
                    continue
                
            filtered_backends.append(backend.name)
        
        return filtered_backends
    
    def get_backend_properties(self, backend_name: str) -> Dict[str, Any]:
        """
        Get detailed properties of a specific backend using BackendV2 interface.
        
        Args:
            backend_name: Name of the backend
            
        Returns:
            Dictionary with backend details or an error message.
        """
        try:
            # Use the service object stored in the class
            backend = self.service.backend(backend_name)
            if not backend:
                 return {'error': f'Backend {backend_name} not found.'}

            # --- Use BackendV2 API with getattr for safety --- 
            properties: Dict[str, Any] = {
                'name': getattr(backend, 'name', backend_name),
                'version': getattr(backend, 'backend_version', None),
                'num_qubits': getattr(backend, 'num_qubits', None),
                'operational': getattr(backend, 'operational', None),
                'status_msg': getattr(backend, 'status_msg', None),
                'pending_jobs': getattr(backend, 'pending_jobs', None),
                'simulator': getattr(backend, 'simulator', None),
                'basis_gates': getattr(backend, 'basis_gates', None),
                'coupling_map': list(backend.coupling_map.get_edges()) if getattr(backend, 'coupling_map', None) else None,
                'max_shots': getattr(backend, 'max_shots', None),
                'max_circuits': getattr(backend, 'max_experiments', None), 
                'avg_cx_error': None,
                'avg_readout_error': None,
                'qubit_properties': None 
            }
            
            # Access target properties for more details if available
            target = getattr(backend, 'target', None)
            if target:
                 if getattr(target, 'basis_gates', None):
                      properties['basis_gates'] = target.basis_gates
                 coupling_map_target = getattr(target, 'coupling_map', None)
                 if coupling_map_target:
                      properties['coupling_map'] = list(coupling_map_target.get_edges())
                 
                 # Calculate average error rates from target.instruction_properties
                 cx_errors = []
                 readout_errors = {} # qubit -> error
                 # Attempt to access instruction_properties as an attribute (dictionary)
                 instruction_props = getattr(target, 'instruction_properties', None)
                 
                 # Process the data ONLY if it's a dictionary
                 if isinstance(instruction_props, dict):
                      for qargs, props in instruction_props.items(): 
                           cx_prop = props.get('cx') 
                           if cx_prop and hasattr(cx_prop, 'error') and cx_prop.error is not None:
                                cx_errors.append(cx_prop.error)
                          
                           measure_prop = props.get('measure')
                           if measure_prop and hasattr(measure_prop, 'error') and measure_prop.error is not None:
                                if len(qargs) == 1: 
                                    readout_errors[qargs[0]] = measure_prop.error
                 else:
                      logger.warning(f"Could not retrieve instruction properties as a dictionary for {backend_name}. Average errors not calculated.")
                                  
                 if cx_errors:
                      properties['avg_cx_error'] = sum(cx_errors) / len(cx_errors)
                 if readout_errors:
                      avg_ro_error = sum(readout_errors.values()) / len(readout_errors)
                      properties['avg_readout_error'] = avg_ro_error

                 # Extract qubit properties (T1, T2, Freq) from target.qubit_properties
                 # Initialize qubit_props_dict to None for safety
                 qubit_props_dict = None 
                 qubit_props_list = getattr(target, 'qubit_properties', None)
                 if qubit_props_list:
                     # Create dict only if processing is successful
                     temp_qubit_props_dict = {}
                     for q_prop in qubit_props_list:
                         q_idx = getattr(q_prop, 'qubit', None) 
                         if q_idx is not None:
                              q_data = {
                                   't1': getattr(q_prop, 't1', None),
                                   't2': getattr(q_prop, 't2', None),
                                   'frequency': getattr(q_prop, 'frequency', None),
                                   'readout_error': readout_errors.get(q_idx) # Uses readout_errors calculated above
                              }
                              if any(v is not None for v in q_data.values()): 
                                   temp_qubit_props_dict[f'Q{q_idx}'] = {k:v for k,v in q_data.items() if v is not None}
                              
                     # Assign only if the dictionary is not empty
                     if temp_qubit_props_dict:
                          qubit_props_dict = temp_qubit_props_dict
                          
                 # Assign to final properties dict (will be None if extraction failed)
                 properties['qubit_properties'] = qubit_props_dict
                      
            else: 
                 logger.warning(f"Backend {backend_name} does not have a Target defined. Detailed error/qubit properties might be missing.")
                 pass 
                
        except Exception as e: 
            logger.error(f"Error retrieving properties for backend {backend_name}: {e}", exc_info=True)
            return {'error': f'Failed to retrieve properties for {backend_name}: {str(e)}'}
        
        return properties
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a running job.
        
        Args:
            job_id: ID of the job to cancel
            
        Returns:
            True if cancellation was successful, False otherwise
        """
        try:
            # Get the job
            job = self.service.job(job_id)
            
            # Cancel the job
            job.cancel()
            logger.info(f"Successfully cancelled job {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling job {job_id}: {e}")
            return False


def create_enhanced_ibm_quantum(token: Optional[str] = None) -> IBMQuantumEnhanced:
    """
    Create an instance of the enhanced IBM Quantum interface.
    
    Args:
        token: IBM Quantum API token (optional)
        
    Returns:
        IBMQuantumEnhanced instance
    """
    return IBMQuantumEnhanced(token=token)


if __name__ == "__main__":
    """
    Example usage of the enhanced IBM Quantum interface.
    """
    # Create an enhanced interface
    quantum = create_enhanced_ibm_quantum()
    
    # List available backends
    print("Available backends:")
    backends = quantum.list_backends(simulator=False, operational=True)
    for backend in backends:
        print(f"  - {backend}")
    
    # Create a simple quantum circuit (Bell state)
    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    
    # Execute the circuit using the enhanced interface
    result = quantum.run_circuit(
        circuit=circuit,
        shots=1024,
        use_circuit_cutting=False,  # Not needed for this small circuit
        optimization_level=1
    )
    
    # Print the results
    print(f"\nExecution result: {result}")
    print(f"Counts: {result.get_counts()}")
    print(f"Execution time: {result.execution_time:.2f} seconds") 