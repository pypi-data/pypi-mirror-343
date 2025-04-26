#!/usr/bin/env python3

"""
Fixed IBM Quantum Integration Layer

This module provides a comprehensive integration layer for running quantum circuits 
on IBM Quantum hardware, with fixes for Qiskit 1.0+ compatibility.

Features:
- Intelligent backend selection based on job requirements
- Circuit optimization for IBM quantum hardware
- Error mitigation strategies
- Result processing and interpretation
- Robust error handling and retry mechanisms
- Topology-aware circuit optimization
- Mock implementation for testing and development

Usage:
    from ibm_quantum_integration_fixed import IBMQuantumIntegration
    
    # Initialize the integration layer
    ibm = IBMQuantumIntegration()
    
    # Run circuit on IBM hardware
    results = ibm.run_circuit(circuit)

Author: Quantum-AI Team
"""

import os
import json
import logging
import time
import threading
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union, Any, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ibm_quantum_integration')

# Load environment variables for API access
from dotenv import load_dotenv
load_dotenv()

# Import Qiskit and IBM Quantum components
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import ZGate
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Optimize1qGates, CXCancellation
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Define custom exception classes that may not be available in all versions
class RuntimeJobMaxTimeoutError(Exception): pass
class RuntimeInternalError(Exception): pass
class IBMQJobApiError(Exception): pass

# Force IBM runtime imports - try to find the package in the venv path
# This helps ensure we're using the real implementation, not the mock
runtime_import_successful = False

try:
    # Try direct import first
    from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options
    
    # Try to import SamplerV2 (preferred) or fall back to Sampler
    try:
        from qiskit_ibm_runtime import SamplerV2 as Sampler
        logger.info("Using SamplerV2 as Sampler")
    except ImportError:
        from qiskit_ibm_runtime import Sampler
        logger.info("Using Sampler directly")
    
    # Import exception classes
    from qiskit_ibm_runtime.exceptions import (
        IBMRuntimeError, 
        RuntimeJobFailureError, 
        RuntimeJobTimeoutError
    )
    
    # Try to import advanced exceptions if available
    try:
        from qiskit_ibm_runtime.exceptions import (
            RuntimeJobMaxTimeoutError,
            RuntimeInternalError
        )
        logger.info("Imported advanced exception classes")
    except ImportError:
        logger.info("Using custom fallback exception classes for advanced error types")
    
    # Import noise model
    from qiskit_aer.noise import NoiseModel
    
    runtime_import_successful = True
    logger.info("Successfully imported qiskit_ibm_runtime")
    
except ImportError as e:
    logger.error(f"Error importing qiskit_ibm_runtime: {str(e)}")
    
    # Try an alternative approach - look for the package in the virtual environment
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        logger.info(f"Trying to find qiskit_ibm_runtime in virtual environment: {venv_path}")
        site_packages = os.path.join(venv_path, 'lib', 'python3*', 'site-packages')
        import glob
        for path in glob.glob(site_packages):
            if os.path.exists(os.path.join(path, 'qiskit_ibm_runtime')):
                logger.info(f"Found qiskit_ibm_runtime in {path}")
                if path not in sys.path:
                    sys.path.insert(0, path)
                    logger.info(f"Added {path} to sys.path")
                try:
                    from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options
                    
                    # Try to import SamplerV2 (preferred) or fall back to Sampler
                    try:
                        from qiskit_ibm_runtime import SamplerV2 as Sampler
                        logger.info("Using SamplerV2 as Sampler")
                    except ImportError:
                        from qiskit_ibm_runtime import Sampler
                        logger.info("Using Sampler directly")
                    
                    # Import exception classes
                    from qiskit_ibm_runtime.exceptions import (
                        IBMRuntimeError, 
                        RuntimeJobFailureError, 
                        RuntimeJobTimeoutError
                    )
                    
                    # Try to import advanced exceptions if available
                    try:
                        from qiskit_ibm_runtime.exceptions import (
                            RuntimeJobMaxTimeoutError,
                            RuntimeInternalError
                        )
                        logger.info("Imported advanced exception classes")
                    except ImportError:
                        logger.info("Using custom fallback exception classes for advanced error types")
                    
                    # Import noise model
                    from qiskit_aer.noise import NoiseModel
                    
                    runtime_import_successful = True
                    logger.info("Successfully imported qiskit_ibm_runtime from virtual environment")
                    break
                except ImportError as e2:
                    logger.error(f"Error importing from site-packages: {str(e2)}")

if not runtime_import_successful:
    # Mock classes for testing/development when qiskit_ibm_runtime is not available
    logger.warning("qiskit_ibm_runtime not available - using mock classes for testing")
    
    class QiskitRuntimeService:
        def __init__(self, *args, **kwargs):
            pass
        
        def backends(self, filters=None):
            """Return a list of backends that match the filters"""
            # This is a mock implementation for testing
            backend_configs = [
                {"name": "mock_5q", "n_qubits": 5, "operational": True, "pending_jobs": 2, "simulator": False},
                {"name": "mock_7q", "n_qubits": 7, "operational": True, "pending_jobs": 5, "simulator": False},
                {"name": "mock_sim", "n_qubits": 32, "operational": True, "pending_jobs": 0, "simulator": True}
            ]
            
            # Create mock backend objects
            backends = []
            for config in backend_configs:
                backend = type('MockBackend', (), {
                    'name': config["name"],
                    'configuration': lambda n_qubits=config["n_qubits"], simulator=config["simulator"]: 
                        type('Config', (), {'n_qubits': n_qubits, 'simulator': simulator}),
                    'status': lambda operational=config["operational"], pending_jobs=config["pending_jobs"]: 
                        type('Status', (), {'operational': operational, 'pending_jobs': pending_jobs}),
                    'properties': lambda: None,
                    'provider': lambda: type('MockProvider', (), {'name': 'ibm-mock'})
                })
                
                if filters is None or filters(backend):
                    backends.append(backend)
            
            return backends
        
        def backend(self, name):
            """Return a specific backend by name"""
            for backend in self.backends():
                if backend.name == name:
                    return backend
            
            # Return a default backend if name not found
            return self.backends()[0]
            
    class Sampler:
        def __init__(self, *args, **kwargs):
            self.options = type('Options', (), {'default_shots': 1024, 'resilience_level': 1})
            # Track if we should simulate an error condition
            self._simulate_error = random.random() < 0.1  # 10% chance of error for testing error handling
            
        def run(self, circuits):
            """Run circuits on the mock sampler"""
            logger.info("Running circuits on MOCK sampler")
            
            # Create a mock job
            class MockJob:
                def __init__(self, simulate_error=False):
                    self._job_id = f"mock-job-{random.randint(10000, 99999)}"
                    self._result = None
                    self._simulate_error = simulate_error
                    self._start_time = time.time()
                    
                    # Record job submission in log
                    logger.info(f"Submitted mock job {self._job_id}")
                
                def job_id(self):
                    """Return the mock job ID"""
                    return self._job_id
                
                def result(self):
                    """Return a mock result with improved error handling"""
                    # Simulate processing time
                    elapsed = time.time() - self._start_time
                    if elapsed < 1.0:
                        remaining = 1.0 - elapsed
                        time.sleep(remaining)
                    
                    # Simulate potential errors
                    if self._simulate_error:
                        error_type = random.choice([
                            "timeout", "failure", "runtime", "internal"
                        ])
                        
                        if error_type == "timeout":
                            logger.error(f"Mock job {self._job_id} timed out")
                            raise RuntimeJobTimeoutError(f"Mock job {self._job_id} timed out")
                        elif error_type == "failure":
                            logger.error(f"Mock job {self._job_id} failed")
                            raise RuntimeJobFailureError(f"Mock job {self._job_id} failed due to mock backend error")
                        elif error_type == "runtime":
                            logger.error(f"Mock job {self._job_id} experienced a runtime error")
                            raise IBMRuntimeError(f"Mock runtime error in job {self._job_id}")
                        elif error_type == "internal":
                            logger.error(f"Mock job {self._job_id} experienced an internal error")
                            raise RuntimeInternalError(f"Mock internal error in job {self._job_id}")
                    
                    if not self._result:
                        # Generate mock results
                        self._result = []
                        
                        for i in range(len(circuits) if isinstance(circuits, list) else 1):
                            # Get the actual circuit to determine properties
                            if isinstance(circuits, list):
                                circuit = circuits[i]
                            else:
                                circuit = circuits
                            
                            # Determine number of qubits from the circuit
                            n_qubits = circuit.num_qubits if hasattr(circuit, 'num_qubits') else 3
                            
                            # Create more realistic mock counts that vary between runs
                            shots = 1024  # Default shots value
                            
                            # Generate a distribution of measurement outcomes
                            mock_counts = {}
                            remaining_shots = shots
                            
                            # Ensure at least the 0 and 1 states for the first qubit are represented
                            mock_counts["0" * n_qubits] = random.randint(shots // 4, shots // 2)
                            remaining_shots -= mock_counts["0" * n_qubits]
                            
                            mock_counts["1" + "0" * (n_qubits-1)] = random.randint(shots // 4, remaining_shots)
                            remaining_shots -= mock_counts["1" + "0" * (n_qubits-1)]
                            
                            # Add some random states if needed
                            if remaining_shots > 0 and n_qubits > 1:
                                # Add a few more random states
                                for _ in range(min(3, 2**n_qubits - 2)):  # At most 3 more states
                                    if remaining_shots <= 0:
                                        break
                                        
                                    # Generate a random bitstring that we haven't used yet
                                    while True:
                                        bitstring = ''.join(random.choice(['0', '1']) for _ in range(n_qubits))
                                        if bitstring not in mock_counts:
                                            break
                                    
                                    mock_counts[bitstring] = random.randint(1, remaining_shots)
                                    remaining_shots -= mock_counts[bitstring]
                            
                            # Create a PubResult-like structure for compatibility with real API
                            # This now mimics the result structure in the IBM Quantum guide
                            class MockRegister:
                                def __init__(self, counts):
                                    self._counts = counts
                                
                                def get_counts(self):
                                    return self._counts
                            
                            class MockData:
                                def __init__(self, counts):
                                    self.c = MockRegister(counts)
                                    self.meas = MockRegister(counts)
                                    # Make it accessible via __dict__ for dynamic access
                                    self.__dict__['c'] = self.c
                                    self.__dict__['meas'] = self.meas
                            
                            class MockPubResult:
                                def __init__(self, counts):
                                    self.data = MockData(counts)
                                    self.metadata = {
                                        "circuit_depth": random.randint(5, 15),
                                        "gate_counts": {"h": random.randint(1, n_qubits), 
                                                      "cx": random.randint(0, n_qubits-1 if n_qubits > 1 else 0)},
                                    }
                            
                            self._result.append(MockPubResult(mock_counts))
                    
                    logger.info(f"Mock job {self._job_id} completed successfully")
                    return self._result
            
            return MockJob(simulate_error=self._simulate_error)
            
    class Session:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
            
    class Options:
        pass
        
    class IBMRuntimeError(Exception): pass
    class RuntimeJobFailureError(Exception): pass
    class RuntimeJobTimeoutError(Exception): pass
    
    class NoiseModel:
        """Mock implementation of NoiseModel that provides basic interface compatibility"""
        def __init__(self, basis_gates=None):
            self.basis_gates = basis_gates or ['u1', 'u2', 'u3', 'cx']
            
        def from_backend(self, backend):
            """Create a noise model from a backend"""
            return self
            
        def add_all_qubit_quantum_error(self, error, op_name):
            """Add error to all qubits for a particular operation"""
            pass
            
        def add_quantum_error(self, error, op_name, qubits):
            """Add error to specific qubits for a particular operation"""
            pass

# Constants for retry mechanisms
MAX_RETRIES = 3
RETRY_DELAY_BASE = 5  # seconds
MAX_RETRY_DELAY = 60  # seconds

class IBMQuantumIntegration:
    """
    Integration layer for running quantum circuits on IBM Quantum hardware.
    
    This class handles:
    - IBM Quantum service initialization
    - Backend selection based on circuit requirements
    - Circuit optimization and transpilation
    - Error mitigation strategies
    - Result processing and interpretation
    - Robust error handling and retry mechanisms
    - Mock implementation for testing when real hardware not available
    """
    
    def __init__(self, token: Optional[str] = None, channel: str = "ibm_quantum"):
        """
        Initialize the integration layer.
        
        Args:
            token: IBM Quantum API token. If None, will try to read from environment.
            channel: IBM Quantum channel ('ibm_quantum' or 'ibm_cloud')
        """
        # Get token from environment if not provided
        if token is None:
            token = os.environ.get("IBM_QUANTUM_TOKEN")
            if not token:
                logger.warning("IBM Quantum token not found in environment variables, using mock implementation")
                self.service = QiskitRuntimeService()
                self.using_mock = True
                return
        
        try:
            # Initialize the Qiskit Runtime service
            logger.info("Initializing Qiskit Runtime service...")
            self.service = QiskitRuntimeService(channel=channel, token=token)
            logger.info("Service initialized successfully")
            self.using_mock = False
        except Exception as e:
            logger.error(f"Failed to initialize QiskitRuntimeService: {str(e)}")
            logger.warning("Falling back to mock implementation")
            self.service = QiskitRuntimeService()
            self.using_mock = True
    
    def run_circuit(self, 
                   circuit: Union[QuantumCircuit, List[QuantumCircuit]],
                   backend_name: Optional[str] = None,
                   shots: int = 1024,
                   optimization_level: int = 1,
                   resilience_level: Optional[int] = None,
                   max_retries: int = MAX_RETRIES) -> Dict[str, Any]:
        """
        Run a quantum circuit or list of circuits on IBM Quantum hardware with robust error handling.
        
        Args:
            circuit: The quantum circuit or list of circuits to run
            backend_name: Specific backend to use (optional)
            shots: Number of shots for the execution
            optimization_level: Transpiler optimization level (0-3)
            resilience_level: Error mitigation level (0-3), None for default
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary containing execution results and metadata
        """
        # Convert single circuit to list
        circuits = circuit if isinstance(circuit, list) else [circuit]
        
        # Determine required qubits
        max_qubits = max(circuit.num_qubits for circuit in circuits)
        logger.info(f"Circuit requires {max_qubits} qubits")
        
        # Get backend
        if backend_name:
            backend = self.service.backend(backend_name)
        else:
            # Find backend with sufficient qubits and lowest pending jobs
            backends = self.service.backends(
                filters=lambda b: b.configuration().n_qubits >= max_qubits
            )
            backend = min(backends, key=lambda b: b.status().pending_jobs)
        
        backend_name = backend.name
        logger.info(f"Using backend: {backend_name}")
        
        # Retry loop
        retry_count = 0
        last_exception = None
        
        while retry_count <= max_retries:
            try:
                if retry_count > 0:
                    delay = min(RETRY_DELAY_BASE * (2 ** retry_count), MAX_RETRY_DELAY)
                    logger.warning(f"Retry {retry_count}/{max_retries} after delay of {delay}s")
                    time.sleep(delay)
                
                # Transpile circuits for the backend
                logger.info(f"Transpiling circuits for {backend_name}...")
                transpiled_circuits = [
                    transpile(c, backend=backend, optimization_level=optimization_level)
                    for c in circuits
                ]
                
                # Execute circuits
                start_time = time.time()
                logger.info(f"Executing circuit(s) on {backend_name} with {shots} shots...")
                
                with Session(backend=backend) as session:
                    sampler = Sampler(mode=session)
                    sampler.options.default_shots = shots
                    
                    # Set resilience level if specified
                    if resilience_level is not None:
                        try:
                            sampler.options.resilience_level = resilience_level
                            logger.info(f"Resilience level set to {resilience_level}")
                        except Exception as e:
                            logger.warning(f"Could not set resilience_level: {str(e)}")
                    
                    job = sampler.run(transpiled_circuits)
                    job_id = job.job_id()
                    logger.info(f"Job ID: {job_id}")
                    
                    # Wait for results
                    logger.info("Waiting for job to complete...")
                    result = job.result()
                
                execution_time = time.time() - start_time
                logger.info(f"Circuit executed successfully in {execution_time:.2f} seconds")
                
                # Process results
                processed_results = []
                for i, res in enumerate(result):
                    # Try different ways to access the counts based on register naming conventions
                    try:
                        counts = res.data.c.get_counts()
                    except (AttributeError, KeyError):
                        try:
                            counts = res.data.meas.get_counts()
                        except (AttributeError, KeyError):
                            # Find what register name is available
                            reg_name = list(res.data.__dict__.keys())[0]
                            logger.info(f"Using register name: {reg_name} for result {i}")
                            counts = getattr(res.data, reg_name).get_counts()
                    
                    # Store processed result
                    processed_results.append({
                        "counts": counts,
                        "metadata": res.metadata if hasattr(res, 'metadata') else {}
                    })
                
                # Return a dictionary with results and metadata
                return {
                    "results": processed_results,
                    "execution_time": execution_time,
                    "backend_name": backend_name,
                    "job_id": job_id,
                    "shots": shots,
                    "optimization_level": optimization_level,
                    "resilience_level": resilience_level,
                    "retry_count": retry_count,
                    "status": "success"
                }
                
            except (RuntimeJobTimeoutError, RuntimeJobMaxTimeoutError) as e:
                logger.error(f"Job timed out: {str(e)}")
                last_exception = e
                retry_count += 1
                
            except (IBMRuntimeError, RuntimeJobFailureError, IBMQJobApiError) as e:
                logger.error(f"IBM Quantum error: {str(e)}")
                last_exception = e
                retry_count += 1
                
            except RuntimeInternalError as e:
                logger.error(f"IBM Quantum internal error: {str(e)}")
                last_exception = e
                retry_count += 1
                
            except Exception as e:
                logger.error(f"Unexpected error executing circuit: {str(e)}")
                last_exception = e
                retry_count += 1
        
        # If we get here, all retries have failed
        logger.error(f"All {max_retries} retry attempts failed")
        
        # Return error information
        return {
            "status": "error",
            "error_message": str(last_exception),
            "error_type": type(last_exception).__name__,
            "backend_name": backend_name,
            "retry_count": retry_count - 1
        }

# Example usage
if __name__ == "__main__":
    print("=== IBM Quantum Integration Layer (Fixed) ===")
    
    try:
        # Initialize with token from environment
        ibm = IBMQuantumIntegration()
        
        if ibm.using_mock:
            print("Using mock implementation")
        else:
            print("Connected to IBM Quantum service")
            
        # Create a simple Bell circuit
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        
        # Run the circuit
        result = ibm.run_circuit(qc, shots=1024)
        
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Counts: {result['results'][0]['counts']}")
        else:
            print(f"Error: {result['error_message']}")
        
    except Exception as e:
        print(f"Error: {str(e)}") 