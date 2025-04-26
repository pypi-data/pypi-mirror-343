"""
Intelligent Backend Selection for IBM Quantum Integration

This module provides an intelligent backend selection system that considers
multiple factors when selecting the optimal IBM Quantum backend:
- Qubit count requirements
- Circuit depth and width
- Gate set compatibility 
- Qubit connectivity/topology
- Error rates (gate errors, readout errors)
- Queue length and expected wait time
- Backend availability and status

The system uses a weighted scoring approach that can be customized based on
application priorities.

Usage:
    from quantum_toolkit.integration.backend_selection import IntelligentBackendSelector
    
    # Initialize the selector
    selector = IntelligentBackendSelector()
    
    # Get backend recommendations for a circuit
    recommended_backends = selector.select_backend(circuit)
    
    # Use top recommendation
    best_backend = recommended_backends[0]['backend']
"""

import logging
import time
import os
from typing import Dict, List, Tuple, Optional, Union, Any, Set
import numpy as np

# Import Qiskit - Guarded Approach
HAS_IBM_RUNTIME = False
try:
    from qiskit import QuantumCircuit
    from qiskit.transpiler import CouplingMap
    from qiskit.providers import Backend
    from qiskit_ibm_runtime import QiskitRuntimeService
    HAS_IBM_RUNTIME = True
except ImportError:
    # Imports failed, HAS_IBM_RUNTIME remains False.
    # We will guard usage below. No dummy types needed.
    logging.warning("qiskit or qiskit_ibm_runtime not found. Backend selection features will be disabled.")
    # Define placeholders *only if* needed for syntax, prefer guarding
    QuantumCircuit, CouplingMap, Backend, QiskitRuntimeService = Any, Any, Any, Any

# Configure logging
logger = logging.getLogger(__name__)

class SelectionCriteria:
    """Class defining criteria for backend selection."""
    
    # Default weights for different factors
    DEFAULT_WEIGHTS = {
        'qubit_count': 1.0,      # Weight for having sufficient qubits
        'connectivity': 0.8,     # Weight for topology/connectivity match
        'error_rates': 0.9,      # Weight for low error rates
        'queue_length': 0.5,     # Weight for short queue
        'gate_set': 0.7,         # Weight for supporting required gates
        'uptime': 0.6,           # Weight for backend reliability
    }
    
    def __init__(self, 
                custom_weights: Optional[Dict[str, float]] = None,
                min_qubits: Optional[int] = None,
                max_queue_length: Optional[int] = None,
                required_gates: Optional[List[str]] = None):
        """
        Initialize selection criteria.
        
        Args:
            custom_weights: Custom weights for different factors
            min_qubits: Minimum required qubits
            max_queue_length: Maximum acceptable queue length
            required_gates: List of gates that must be supported
        """
        self.weights = self.DEFAULT_WEIGHTS.copy()
        if custom_weights:
            for factor, weight in custom_weights.items():
                if factor in self.weights:
                    self.weights[factor] = weight
        
        self.min_qubits = min_qubits
        self.max_queue_length = max_queue_length
        self.required_gates = required_gates


class IntelligentBackendSelector:
    """
    Intelligent backend selection system that recommends the optimal backend
    based on circuit requirements and backend capabilities.
    """
    # Use Any for potentially unimported types
    service: Optional[Any]
    _backends_cache: Dict[str, Any]

    def __init__(self, service: Optional[Any] = None):
        """
        Initialize the intelligent backend selector.

        Args:
            service: QiskitRuntimeService instance. If None, will attempt to create one.
        """
        self.service = service
        self._backends_cache = {} # Initialize as empty dict
        self._backends_cache_time = 0
        self._cache_timeout = 300  # Cache backends for 5 minutes

        # Default weights for different factors (can be customized)
        self.weights = SelectionCriteria.DEFAULT_WEIGHTS.copy()

        # Initialize the service if not provided and runtime is available
        if self.service is None and HAS_IBM_RUNTIME:
            try:
                # Use standard initialization - relies on env vars or saved credentials
                # Ensure QiskitRuntimeService is the actual class here if HAS_IBM_RUNTIME is True
                if HAS_IBM_RUNTIME:
                     self.service = QiskitRuntimeService()
                     logger.info("Initialized QiskitRuntimeService using default credentials.")
            except Exception as e:
                logger.error(f"Failed to initialize QiskitRuntimeService automatically: {str(e)}", exc_info=True)
                self.service = None # Set to None on failure
        elif not HAS_IBM_RUNTIME:
             logger.debug("Qiskit IBM Runtime not available. Cannot initialize service.")
             self.service = None

    def get_backends(self, refresh: bool = False) -> List[Any]: # Return List[Any]
        """
        Get a list of available backends, with caching.

        Args:
            refresh: Force refresh the backends cache

        Returns:
            List of available backend objects (typed as Any)
        """
        current_time = time.time()

        # Check if we need to refresh the cache
        if (refresh or
            not self._backends_cache or
            (current_time - self._backends_cache_time) > self._cache_timeout):

            if not self.service or not HAS_IBM_RUNTIME:
                if HAS_IBM_RUNTIME and self.service is None:
                    logger.warning("QiskitRuntimeService not initialized. Cannot fetch backends.")
                return []

            try:
                # TODO: Verify the correct method to list backends in the current qiskit-ibm-runtime version.
                backends_list: List[Any] = []
                backends_method = getattr(self.service, 'backends', None)
                if callable(backends_method):
                    try:
                         backends_list = backends_method(operational=True)
                         logger.debug("Fetched backends using service.backends(operational=True)")
                    except TypeError:
                         logger.debug("Fetching all backends via service.backends() and filtering manually for operational status.")
                         all_backends = backends_method()
                         temp_list = []
                         for b in all_backends:
                              if not HAS_IBM_RUNTIME: break # Should not happen here, but safety
                              status_method = getattr(b, 'status', None)
                              status = status_method() if callable(status_method) else status_method
                              if status and getattr(status, 'operational', False):
                                   temp_list.append(b)
                         backends_list = temp_list
                else:
                    logger.warning("QiskitRuntimeService instance does not have a callable 'backends' method. Cannot fetch backends.")
                    return []

                # Filter out simulators
                real_backends_dict: Dict[str, Any] = {}
                for b in backends_list:
                    if not HAS_IBM_RUNTIME: break # Safety check
                    config_method = getattr(b, 'configuration', None)
                    config = config_method() if callable(config_method) else config_method
                    is_simulator = getattr(config, 'simulator', False) if config else False
                    if not is_simulator:
                        backend_name = getattr(b, 'name', f'unknown_backend_{id(b)}')
                        real_backends_dict[backend_name] = b

                self._backends_cache = real_backends_dict
                self._backends_cache_time = current_time

                logger.info(f"Refreshed backends cache, found {len(real_backends_dict)} operational real backends")
            except Exception as e:
                logger.error(f"Error fetching/processing backends: {str(e)}", exc_info=True)
                if not self._backends_cache:
                    return []

        return list(self._backends_cache.values())

    def _analyze_circuit(self, circuit: Any) -> Dict[str, Any]: # Use Any
        """
        Analyze a quantum circuit to determine its requirements.
        
        Args:
            circuit: The quantum circuit to analyze
            
        Returns:
            Dictionary with circuit requirements
        """
        if not HAS_IBM_RUNTIME:
             logger.error("Cannot analyze circuit: Qiskit is not available.")
             return {}

        # Now HAS_IBM_RUNTIME is True, circuit should be a QuantumCircuit
        # Use isinstance check for runtime verification if needed, though type hint is Any
        # if not isinstance(circuit, QuantumCircuit): ...

        num_qubits = getattr(circuit, 'num_qubits', 0)
        depth_val = 0
        depth_method = getattr(circuit, 'depth', None)
        if callable(depth_method):
            try:
                depth_val = depth_method()
            except Exception as e:
                 logger.warning(f"Could not determine circuit depth: {e}")
        
        # Analyze gate types used in the circuit
        gate_counts = {}
        gate_set = set()
        circuit_data = getattr(circuit, 'data', [])
        
        for instruction_tuple in circuit_data:
             if len(instruction_tuple) < 1: continue
             instruction = instruction_tuple[0]
             qargs = instruction_tuple[1] if len(instruction_tuple) > 1 else []

             gate_name = getattr(instruction, 'name', None)
             if not gate_name: continue

             gate_set.add(gate_name)
             gate_counts[gate_name] = gate_counts.get(gate_name, 0) + 1
        
        # Analyze qubit connectivity requirements
        connectivity_requirements = set()
        circuit_qubits = getattr(circuit, 'qubits', [])
        find_bit_method = getattr(circuit, 'find_bit', None)

        for instruction_tuple in circuit_data:
             if len(instruction_tuple) < 2: continue
             instruction = instruction_tuple[0]
             qargs = instruction_tuple[1]

             if len(qargs) == 2:  # 2-qubit gate
                q1, q2 = qargs[0], qargs[1]
                q1_idx, q2_idx = -1, -1

                # Try different methods to get qubit indices robustly
                try:
                     if not circuit_qubits: raise ValueError("circuit.qubits not available")
                     q1_idx = circuit_qubits.index(q1)
                     q2_idx = circuit_qubits.index(q2)
                except (AttributeError, ValueError, TypeError):
                    try:
                         q1_idx = q1.index
                         q2_idx = q2.index
                    except (AttributeError, TypeError):
                         try:
                              if not callable(find_bit_method): raise AttributeError("find_bit not available or not callable")
                              q1_result = find_bit_method(q1)
                              q2_result = find_bit_method(q2)
                              if q1_result and isinstance(q1_result, list) and q1_result[0]: q1_idx = q1_result[0][1]
                              if q2_result and isinstance(q2_result, list) and q2_result[0]: q2_idx = q2_result[0][1]
                         except (AttributeError, TypeError, IndexError):
                               q1_idx = 0
                               q2_idx = 1
                               logger.debug("Falling back to arbitrary qubit indices (0, 1) for connectivity analysis.")

                if isinstance(q1_idx, int) and isinstance(q2_idx, int) and q1_idx >= 0 and q2_idx >= 0:
                    sorted_indices = tuple(sorted([q1_idx, q2_idx]))
                    connectivity_requirements.add(sorted_indices)
                else:
                     logger.warning(f"Could not reliably determine qubit indices for gate {getattr(instruction, 'name', '?')} acting on {qargs}. Connectivity requirement ignored.")

        return {
            'num_qubits': num_qubits,
            'depth': depth_val,
            'gate_counts': gate_counts,
            'gate_set': gate_set,
            'connectivity_requirements': connectivity_requirements
        }
    
    def _evaluate_backend(self, backend: Any, requirements: Dict[str, Any]) -> Dict[str, Union[float, str]]: # Use Any
        """
        Evaluate a backend against the circuit requirements.
        
        Args:
            backend: The backend to evaluate
            requirements: Dictionary with circuit requirements
            
        Returns:
            Dictionary with scores for different factors or an error string.
        """
        scores: Dict[str, Union[float, str]] = {}
        backend_name = getattr(backend, 'name', 'Unknown Backend') # Get name safely
        
        try:
            # Get backend properties and configuration safely
            config_method = getattr(backend, 'configuration', None)
            status_method = getattr(backend, 'status', None)
            properties_method = getattr(backend, 'properties', None)

            config = config_method() if callable(config_method) else config_method
            status = status_method() if callable(status_method) else status_method
            
            properties = None
            has_properties = False
            if properties_method:
                 try:
                      properties = properties_method() if callable(properties_method) else properties_method
                      has_properties = properties is not None
                 except Exception as prop_exc:
                      logger.warning(f"Could not retrieve properties for {backend_name}: {prop_exc}")
                      properties = None
                      has_properties = False
            
            if not config or not status:
                 raise RuntimeError(f"Could not retrieve configuration or status for backend {backend_name}")

            # 1. Qubit count score (binary - either has enough or doesn't)
            required_qubits = requirements['num_qubits']
            available_qubits = getattr(config, 'n_qubits', 0) # Default to 0 if missing
            
            if available_qubits >= required_qubits:
                scores['qubit_count'] = 1.0
            else:
                # Not enough qubits, this is a hard requirement
                scores['qubit_count'] = 0.0
                # Early return as this backend can't run the circuit
                return scores
            
            # 2. Connectivity score
            coupling_map_list = getattr(config, 'coupling_map', None)
            if coupling_map_list:
                try:
                    # Initialize CouplingMap only if Qiskit is available
                    coupling_map_instance = None
                    if HAS_IBM_RUNTIME:
                         coupling_map_instance = CouplingMap(coupling_map_list)

                    # Check if all required connections are available
                    if coupling_map_instance:
                         connectivity_requirements = requirements['connectivity_requirements']
                         missing_connections = 0
                         
                         # Safely check graph edges
                         graph = getattr(coupling_map_instance, 'graph', None)
                         has_edge_method = getattr(graph, 'has_edge', None) if graph else None

                         for q1, q2 in connectivity_requirements:
                             # Adjust for potentially different qubit count between 
                             # the circuit and the actual backend layout
                             if q1 >= available_qubits or q2 >= available_qubits:
                                 missing_connections += 1
                                 continue
                             
                             edge_exists = False
                             if has_edge_method and callable(has_edge_method):
                                 edge_exists = has_edge_method(q1, q2) or has_edge_method(q2, q1)

                             if not edge_exists:
                                 missing_connections += 1
                         
                         if connectivity_requirements:
                             connectivity_score = 1.0 - (missing_connections / len(connectivity_requirements))
                         else:
                             connectivity_score = 1.0  # No connectivity requirements
                             
                         scores['connectivity'] = connectivity_score
                except Exception as e:
                    logger.warning(f"Failed to initialize CouplingMap for backend {backend_name}: {e}. Assuming no connectivity info.")
                    scores['connectivity'] = 1.0 # Or potentially a lower score like 0.5? Depends on desired behavior.
            else:
                # No coupling map information, assume full connectivity (or penalize if needed)
                scores['connectivity'] = 1.0 # Or potentially a lower score like 0.5? Depends on desired behavior.
            
            # 3. Error rates score
            if has_properties and properties: # Check properties is not None
                # Calculate average gate error rates
                gate_errors = []
                backend_gates = getattr(properties, 'gates', []) # Safe access
                for gate_name in requirements['gate_set']:
                     # Handle specific gates we care about
                     if gate_name in ['cx', 'cz', 'cp', 'swap']:  # Two-qubit gates
                         for gate_info in backend_gates:
                             if getattr(gate_info, 'gate', '') == gate_name: # Safe access
                                 params = getattr(gate_info, 'parameters', [])
                                 if params and len(params) > 0:
                                     error_value = getattr(params[0], 'value', None)
                                     if isinstance(error_value, (float, int)):
                                         gate_errors.append(error_value)
                     elif gate_name in ['x', 'y', 'z', 'h', 's', 't', 'rx', 'ry', 'rz', 'id']:  # Single-qubit gates
                         for gate_info in backend_gates:
                             if getattr(gate_info, 'gate', '') == gate_name: # Safe access
                                 params = getattr(gate_info, 'parameters', [])
                                 if params and len(params) > 0:
                                     error_value = getattr(params[0], 'value', None)
                                     if isinstance(error_value, (float, int)):
                                          gate_errors.append(error_value)
                
                # Calculate readout error rates
                readout_errors = []
                readout_error_method = getattr(properties, 'readout_error', None)
                if callable(readout_error_method):
                     for qubit in range(min(required_qubits, available_qubits)):
                         try:
                             error = readout_error_method(qubit)
                             if isinstance(error, (float, int)):
                                  readout_errors.append(error)
                         except Exception:
                             # Log warning or ignore if specific qubit readout error is unavailable
                             # logger.debug(f"Could not get readout error for qubit {qubit} on {backend_name}")
                             pass
                
                # Combine error metrics (lower is better)
                gate_error_score = 0.5 # Default neutral score
                if gate_errors:
                    avg_gate_error = sum(gate_errors) / len(gate_errors)
                    # Normalize to [0, 1] where 1 is best (lowest error)
                    # Assuming 0.1 (10%) as a "high" error rate threshold for normalization
                    gate_error_score = max(0, 1 - (avg_gate_error / 0.1)) 
                
                readout_error_score = 0.5 # Default neutral score
                if readout_errors:
                    avg_readout_error = sum(readout_errors) / len(readout_errors)
                    # Normalize to [0, 1] where 1 is best (lowest error)
                    # Assuming 0.1 (10%) as a "high" error rate threshold
                    readout_error_score = max(0, 1 - (avg_readout_error / 0.1))
                
                # Combine gate and readout errors (weighted)
                scores['error_rates'] = 0.7 * gate_error_score + 0.3 * readout_error_score
            else:
                # No properties available, use a neutral score
                scores['error_rates'] = 0.5
            
            # 4. Queue length score
            pending_jobs = getattr(status, 'pending_jobs', 10) # Default to moderate queue if missing
            # Ensure pending_jobs is a number
            if not isinstance(pending_jobs, (int, float)):
                 pending_jobs = 10 # Fallback default
            # Normalize to [0, 1] where 1 is best (shortest queue)
            # Assuming 20 as a "long" queue threshold for normalization
            queue_score = max(0, 1 - (pending_jobs / 20.0)) # Use float division
            scores['queue_length'] = queue_score
            
            # 5. Gate set support score
            required_gates = requirements['gate_set']
            supported_gates_list = getattr(config, 'basis_gates', []) # Safe access
            supported_gates = set(supported_gates_list)
            
            gate_set_score = 1.0 # Default optimistic score
            if required_gates: # Avoid division by zero if no gates required
                 # Calculate how many required gates are directly supported
                 directly_supported = required_gates.intersection(supported_gates)
                 gate_set_score = len(directly_supported) / len(required_gates)
            
            # Improve score if essential universal gates are supported (can build others)
            essential_gates = {'cx', 'id', 'rz', 'sx', 'x'} # Common modern basis gate set elements
            # Or use Qiskit's standard equivalence library if more advanced check needed
            if essential_gates.issubset(supported_gates):
                 gate_set_score = max(gate_set_score, 0.9) # High score if universal set likely available
            elif 'u' in supported_gates or ('u1' in supported_gates and 'u2' in supported_gates and 'u3' in supported_gates):
                 gate_set_score = max(gate_set_score, 0.85) # Also good if U gates supported

            scores['gate_set'] = gate_set_score
            
            # 6. Uptime/stability score
            is_operational = getattr(status, 'operational', False) # Default to False if missing
            scores['uptime'] = 1.0 if is_operational else 0.0
            
            return scores
            
        except Exception as e:
            logger.error(f"Error evaluating backend {backend_name}: {str(e)}")
            # Return minimal scoring information including error string
            # Ensure keys match expected structure even on error, with error flag
            return {'qubit_count': 0.0, 'error': str(e)}
    
    def _calculate_overall_score(self, scores: Dict[str, Union[float, str]]) -> float: # Accept updated type
        """
        Calculate an overall score from individual factor scores, using weights.
        
        Args:
            scores: Dictionary with scores for different factors (can include 'error')
            
        Returns:
            Overall weighted score
        """
        # Check for error flag or insufficient qubits
        if 'error' in scores or scores.get('qubit_count', 0.0) == 0.0:
            return 0.0
            
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for factor, score in scores.items():
            # Only include factors that are in weights AND have a numeric score
            if factor in self.weights and isinstance(score, (int, float)):
                weight = self.weights[factor]
                weighted_sum += score * weight
                weight_sum += weight
        
        if weight_sum == 0:
            return 0.0 # Avoid division by zero if no weighted factors found/scored
            
        # Normalize score
        return weighted_sum / weight_sum
    
    def select_backend(self, 
                      circuit: Union[Any, List[Any]], # Use Any
                      refresh_backends: bool = False,
                      backend_filters: Optional[Dict[str, Any]] = None,
                      custom_weights: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        """
        Select the optimal backend for the given circuit(s).
        
        Args:
            circuit: Quantum circuit or list of circuits to run
            refresh_backends: Force refresh the backends cache
            backend_filters: Additional filters for backends (e.g., {'name': 'ibm_sherbrooke'})
            custom_weights: Custom weights for different factors
            
        Returns:
            List of recommended backends with scores, sorted by overall score (best first)
        """
        if not HAS_IBM_RUNTIME:
             logger.error("Cannot select backend: Qiskit Runtime is not available.")
             return []

        circuit_requirements: Optional[Dict[str, Any]] = None
        # Use isinstance with the actual class when HAS_IBM_RUNTIME is True
        if isinstance(circuit, QuantumCircuit):
            circuit_requirements = self._analyze_circuit(circuit)
        elif isinstance(circuit, list):
             valid_circuits = [c for c in circuit if isinstance(c, QuantumCircuit)]
             if not valid_circuits:
                  logger.error("Input list does not contain valid QuantumCircuit objects.")
                  return []

             all_requirements = [self._analyze_circuit(c) for c in valid_circuits]
             if not all_requirements: return []

             circuit_requirements = {
                 'num_qubits': 0,
                 'depth': 0,
                 'gate_counts': {},
                 'gate_set': set(),
                 'connectivity_requirements': set()
             }
             # Aggregate requirements
             for r in all_requirements:
                  circuit_requirements['num_qubits'] = max(circuit_requirements['num_qubits'], r.get('num_qubits', 0))
                  circuit_requirements['depth'] = max(circuit_requirements['depth'], r.get('depth', 0))
                  circuit_requirements['gate_set'].update(r.get('gate_set', set()))
                  circuit_requirements['connectivity_requirements'].update(r.get('connectivity_requirements', set()))
                
                  # Sum gate counts (handle potential missing key)
                  for gate, count in r.get('gate_counts', {}).items():
                      circuit_requirements['gate_counts'][gate] = circuit_requirements['gate_counts'].get(gate, 0) + count
        else:
            logger.error(f"Invalid input type for 'circuit': {type(circuit)}. Expected QuantumCircuit or List[QuantumCircuit].")
            return []
        
        if circuit_requirements is None:
             logger.error("Could not determine circuit requirements.")
             return []

        # Apply custom weights if provided
        original_weights = None
        if custom_weights:
            original_weights = self.weights.copy()
            for factor, weight in custom_weights.items():
                if factor in self.weights:
                    self.weights[factor] = weight
        
        try:
            # Get available backends (already returns List[AnyBackend])
            all_available_backends = self.get_backends(refresh=refresh_backends) 
            if not all_available_backends:
                logger.warning("No backends available for selection")
                return []
            
            # Apply additional filters if provided
            backends_to_evaluate = all_available_backends
            if backend_filters:
                filtered_backends = []
                for backend in all_available_backends:
                    match = True
                    config_method = getattr(backend, 'configuration', None)
                    config = config_method() if callable(config_method) else config_method

                    for key, expected_value in backend_filters.items():
                        actual_value = None
                        # Handle special case for name
                        if key == 'name':
                            actual_value = getattr(backend, 'name', None)
                        # Handle other properties through configuration
                        elif config and hasattr(config, key):
                             actual_value = getattr(config, key, None)
                        # Could add checks for status attributes too if needed
                        
                        # Perform comparison
                        if actual_value != expected_value:
                             match = False
                             break # Stop checking filters for this backend
                    
                    if match:
                        filtered_backends.append(backend)
                
                backends_to_evaluate = filtered_backends
                if not backends_to_evaluate:
                     logger.warning(f"No backends matched the provided filters: {backend_filters}")
                     return []

            # Evaluate each backend
            recommendations = []
            for backend in backends_to_evaluate:
                backend_name = getattr(backend, 'name', 'Unknown')
                # Evaluate backend against circuit requirements
                scores = self._evaluate_backend(backend, circuit_requirements) # Returns Dict[str, Union[float, str]]
                
                # Calculate overall score (handles error cases internally)
                overall_score = self._calculate_overall_score(scores)
                
                # Add to recommendations if it meets minimum requirements (score > 0)
                if overall_score > 0:
                    # Safely get pending jobs from status
                    pending_jobs = None
                    status_method = getattr(backend, 'status', None)
                    status = status_method() if callable(status_method) else status_method
                    if status:
                        pending_jobs = getattr(status, 'pending_jobs', None)

                    recommendations.append({
                        'backend': backend, # The actual backend object
                        'name': backend_name,
                        'overall_score': overall_score,
                        'detail_scores': scores, # Include the raw scores dictionary (might contain 'error')
                        'pending_jobs': pending_jobs if isinstance(pending_jobs, (int, float)) else None # Ensure it's a number or None
                    })
            
            # Sort recommendations by overall score (descending)
            recommendations.sort(key=lambda x: x['overall_score'], reverse=True)
            
            # Log the recommendations
            if recommendations:
                # Log top 1-3 recommendations
                top_n = min(len(recommendations), 3)
                log_msg = f"Backend recommendations (top {top_n}):\n"
                for i, rec in enumerate(recommendations[:top_n]):
                     log_msg += f"  {i+1}. {rec['name']} (Score: {rec['overall_score']:.4f}, Jobs: {rec['pending_jobs']})\n"
                logger.info(log_msg.strip())
                # logger.debug(f"Full recommendations: {recommendations}") # Optionally log all details at debug level
            else:
                logger.warning("No suitable backends found matching the criteria and requirements.")
                
            return recommendations
            
        except Exception as e:
            logger.error(f"Error during backend selection process: {str(e)}", exc_info=True) # Log traceback
            return []
        finally:
            # Restore original weights if modified
            if original_weights:
                self.weights = original_weights

    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """
        Update the weights used for backend selection.
        
        Args:
            new_weights: Dictionary mapping factors to their new weights
        """
        for factor, weight in new_weights.items():
            if factor in self.weights:
                self.weights[factor] = weight
                
    def get_backend_details(self, backend_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific backend.
        
        Args:
            backend_name: Name of the backend
            
        Returns:
            Dictionary with backend details or an error message.
        """
        if not self.service or not HAS_IBM_RUNTIME:
             if HAS_IBM_RUNTIME and self.service is None:
                  logger.warning("QiskitRuntimeService not initialized. Cannot get backend details.")
             else:
                  logger.warning("Qiskit Runtime not available. Cannot get backend details.")
             return {'error': 'QiskitRuntimeService not available or not initialized.'}

        try:
            backend_instance: Optional[Any] = None # Use Any
            get_backend_method = getattr(self.service, 'get_backend', None)
            if callable(get_backend_method):
                 try:
                     backend_instance = get_backend_method(backend_name)
                 except Exception as get_be_exc:
                      logger.error(f"Error calling get_backend for {backend_name}: {get_be_exc}", exc_info=True)
                      return {'error': f'Failed to retrieve backend {backend_name}: {get_be_exc}'}
            else:
                 logger.error("QiskitRuntimeService instance does not have a callable 'get_backend' method.")
                 return {'error': 'Service object configuration error: get_backend not found.'}

            if not backend_instance:
                 logger.warning(f"Backend '{backend_name}' not found by service.get_backend.")
                 return {'error': f'Backend {backend_name} not found by service.'}

            # Get basic information safely using getattr and checking callables
            config_method = getattr(backend_instance, 'configuration', None)
            status_method = getattr(backend_instance, 'status', None)
            properties_method = getattr(backend_instance, 'properties', None)

            config = config_method() if callable(config_method) else config_method
            status = status_method() if callable(status_method) else status_method
            
            properties = None
            has_properties = False
            if properties_method:
                 try:
                      properties = properties_method() if callable(properties_method) else properties_method
                      has_properties = properties is not None
                 except Exception as prop_exc:
                      logger.warning(f"Could not retrieve properties for {backend_name} in get_backend_details: {prop_exc}")
                      properties = None
                      has_properties = False

            if not config or not status:
                 return {'error': f'Could not retrieve configuration or status for {backend_name}.'}
                
            # Collect basic information safely
            details = {
                'name': getattr(backend_instance, 'name', backend_name), # Use backend_instance
                'qubits': getattr(config, 'n_qubits', None),
                'operational': getattr(status, 'operational', None), # Keep None if unknown
                'status_msg': getattr(status, 'status_msg', 'Unknown'),
                'pending_jobs': getattr(status, 'pending_jobs', None),
                'basis_gates': getattr(config, 'basis_gates', None),
                'simulator': getattr(config, 'simulator', None), # Keep None if unknown
                'version': getattr(config, 'backend_version', None), # Example: add version if available
                'description': getattr(backend_instance, 'description', None), # Use backend_instance
            }
            
            # Add coupling map if available
            coupling_map_list = getattr(config, 'coupling_map', None)
            if coupling_map_list:
                # Optionally convert to CouplingMap object or keep as list
                details['coupling_map'] = coupling_map_list # Keep raw list for simplicity
                # Or: details['coupling_map_obj'] = CouplingMap(coupling_map_list) 
                
            # Add properties if available and properties object exists
            if has_properties and properties: # Check properties object again
                # Get average gate errors safely
                avg_gate_errors = {}
                backend_gates = getattr(properties, 'gates', [])
                gate_errors_temp: Dict[str, List[float]] = {}
                if backend_gates:
                     for gate_info in backend_gates:
                        gate_name = getattr(gate_info, 'gate', None)
                        gate_params = getattr(gate_info, 'parameters', [])
                        if gate_name and gate_params:
                            error_value = getattr(gate_params[0], 'value', None)
                            if isinstance(error_value, (float, int)):
                                if gate_name not in gate_errors_temp:
                                     gate_errors_temp[gate_name] = []
                                gate_errors_temp[gate_name].append(error_value)
                
                # Calculate averages
                for gate, errors in gate_errors_temp.items():
                    if errors:
                        avg_gate_errors[gate] = sum(errors) / len(errors)
                if avg_gate_errors:
                    details['avg_gate_errors'] = avg_gate_errors
                
                # Get readout errors safely
                readout_errors = {}
                num_qubits = details.get('qubits') # Use already fetched qubit count
                readout_error_method = getattr(properties, 'readout_error', None)
                if isinstance(num_qubits, int) and callable(readout_error_method):
                    for qubit in range(num_qubits):
                        try:
                            error = readout_error_method(qubit)
                            if isinstance(error, (float, int)):
                                 readout_errors[qubit] = error
                        except Exception:
                            pass # Ignore if specific qubit data is missing
                if readout_errors:
                    details['readout_errors'] = readout_errors
                
                # Add T1/T2 times if available safely
                t1_times = {}
                t2_times = {}
                t1_method = getattr(properties, 't1', None)
                t2_method = getattr(properties, 't2', None)
                if isinstance(num_qubits, int) and callable(t1_method) and callable(t2_method):
                    for qubit in range(num_qubits):
                        try:
                             t1 = t1_method(qubit)
                             t2 = t2_method(qubit)
                             if isinstance(t1, (float, int)): t1_times[qubit] = t1
                             if isinstance(t2, (float, int)): t2_times[qubit] = t2
                        except Exception:
                            pass # Ignore if specific qubit data is missing
                
                if t1_times: details['t1_times'] = t1_times
                if t2_times: details['t2_times'] = t2_times

                # Add calibration date if available
                last_update_date = getattr(properties, 'last_update_date', None)
                if last_update_date:
                    # Attempt to convert to string, handling potential datetime object
                    try:
                        details['last_calibration_time'] = str(last_update_date)
                    except:
                         details['last_calibration_time'] = repr(last_update_date) # Fallback representation

            # Remove keys with None values for cleaner output, if desired
            details = {k: v for k, v in details.items() if v is not None}

            return details
            
        except Exception as e:
            logger.error(f"Error fetching backend details for {backend_name}: {str(e)}", exc_info=True) # Log traceback
            return {'error': f"Failed to get details for {backend_name}: {str(e)}"}


# Create a simple demo function for testing the module
def demo():
    """Simple demo of backend selection."""
    if not HAS_IBM_RUNTIME:
        print("Qiskit or Qiskit Runtime not installed. Cannot run demo.")
        return

    import os
    import sys
    from dotenv import load_dotenv
    # These imports are safe now due to the HAS_IBM_RUNTIME check above
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime import QiskitRuntimeService

    # Load environment variables
    load_dotenv()
    token = os.environ.get("IBM_QUANTUM_TOKEN")

    # Check if token exists OR rely on default loading mechanism
    # The service initialization below will handle missing token/credentials
    # if token or QiskitRuntimeService.saved_accounts(): # Check if default loading might work
    
    try:
        # Initialize the QiskitRuntimeService (will try default loading)
        service: Optional[QiskitRuntimeService] = None
        try:
             service = QiskitRuntimeService()
             logger.info("Demo: Initialized QiskitRuntimeService using default credentials.")
        except Exception as service_exc:
             print(f"Demo: Failed to initialize QiskitRuntimeService: {service_exc}", file=sys.stderr)
             print("Demo: Please ensure IBM Quantum token is set via IBM_QUANTUM_TOKEN env var or Qiskit config.", file=sys.stderr)
             return # Exit demo if service cannot be initialized

        # Create the backend selector
        # Pass the potentially initialized service object
        selector = IntelligentBackendSelector(service=service) 

        # Check if service was actually set (it should be unless exception above)
        if not selector.service:
             print("Demo: Selector could not use the initialized service. Aborting demo.", file=sys.stderr)
             return

        # Create a simple test circuit
        circuit = QuantumCircuit(4)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.cx(0, 2)
        circuit.cx(0, 3)
        circuit.measure_all()
        
        # Get backend recommendations
        print("Finding optimal backends for a GHZ state circuit...")
        recommendations = selector.select_backend(circuit)
        
        if recommendations:
            print("\nTop 3 recommended backends:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"{i}. {rec['name']} (Score: {rec['overall_score']:.4f}, " 
                      f"Pending jobs: {rec['pending_jobs']})")
                print("   Detail scores:")
                for factor, score in rec['detail_scores'].items():
                    print(f"   - {factor}: {score:.4f}")
                print()
            
            # Get detailed information about the top backend
            top_backend = recommendations[0]['backend']
            details = selector.get_backend_details(top_backend.name)
            
            print(f"Detailed information for {top_backend.name}:")
            for key, value in details.items():
                if key in ['coupling_map', 'avg_gate_errors', 'readout_errors', 't1_times', 't2_times']:
                    print(f"  {key}: [Complex data, length: {len(value)}]")
                else:
                    print(f"  {key}: {value}")
        else:
            print("No suitable backends found.")
            
    except Exception as e:
        print(f"Error in demo: {str(e)}", file=sys.stderr) # Print errors to stderr


if __name__ == "__main__":
    # No need to import sys here anymore as it's in demo()
    demo() 