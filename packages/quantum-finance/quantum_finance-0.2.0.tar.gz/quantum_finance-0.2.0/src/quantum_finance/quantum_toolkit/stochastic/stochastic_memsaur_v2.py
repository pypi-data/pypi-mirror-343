"""
Stochastic-Memsaur Quantum Error Analysis Module - V2 API Compatible
Implements stochastic methods for error analysis in quantum financial simulations.
Compatible with IBM Quantum Runtime V2 API (post-August 2024)
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

# Import our adapter to handle V1/V2 API differences
# Use absolute path from toolkit root
from quantum_toolkit.utils.qiskit_adapter import QiskitRuntimeAdapter

# Setup logging
logger = logging.getLogger(__name__)

class StochasticMemsaurAnalyzer:
    """
    Stochastic Memory-efficient Sampling and Analysis for Uncertainty Resolution (Memsaur)
    
    Provides methods for analyzing quantum circuit error characteristics
    using stochastic sampling techniques that are memory-efficient.
    
    Compatible with IBM Quantum Runtime V2 API.
    """
    
    def __init__(self, service, backend_name: Optional[str] = None):
        """
        Initialize the analyzer with IBM Quantum service and backend.
        
        Args:
            service: IBM Quantum service instance
            backend_name: Name of the backend to use (if None, will use least busy)
        """
        self.service = service
        self.backend_name = backend_name
        self.backend = None
        
        # Initialize the backend
        self._init_backend()
        
    def _init_backend(self):
        """Initialize the quantum backend"""
        if self.backend_name:
            self.backend = self.service.backend(self.backend_name)
        else:
            # Get least busy backend with sufficient qubits
            try:
                from qiskit_ibm_provider import least_busy
            except ImportError:
                raise ImportError("Could not import 'least_busy'. Please ensure you have qiskit-ibm-provider >=0.5.0 installed.")
            available_backends = self.service.backends(
                simulator=False, 
                operational=True,
                min_num_qubits=5
            )
            if available_backends:
                self.backend = least_busy(available_backends)
                logger.info(f"Selected least busy backend: {getattr(self.backend, 'name', 'unknown')}")
            else:
                # Fallback to simulator
                logger.warning("No available quantum backends, falling back to simulator")
                self.backend = self.service.backend("ibmq_qasm_simulator")
                
        logger.info(f"Using backend: {getattr(self.backend, 'name', 'unknown')}")
        if self.backend is None:
            raise RuntimeError("Failed to initialize a valid quantum backend. Please check your IBM Quantum service configuration and backend availability.")
    
    def analyze_circuit_errors(
        self, 
        circuit: QuantumCircuit,
        shots: int = 4000,
        resilience_level: int = 1,
        optimization_level: int = 1,
        use_session: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze error characteristics of a quantum circuit.
        
        Args:
            circuit: The quantum circuit to analyze
            shots: Number of shots for sampling
            resilience_level: Error mitigation level (0-3)
            optimization_level: Circuit optimization level (0-3)
            use_session: Whether to use session mode
            
        Returns:
            Dict containing error analysis results
        """
        # Ensure circuit is in ISA format required by V2 API
        isa_circuit = QiskitRuntimeAdapter.ensure_isa_circuits(circuit, self.backend)
        
        # Configure options using our adapter
        options = QiskitRuntimeAdapter.configure_options(
            resilience_level=resilience_level,
            optimization_level=optimization_level,
            max_execution_time=300,  # 5-minute timeout
            transpilation={"skip_transpilation": False}  # Ensure proper transpilation
        )
        
        # Create the sampler using our adapter
        sampler = QiskitRuntimeAdapter.get_sampler(
            self.service,
            self.backend,
            options=options,
            use_session=use_session
        )
        
        # Run the circuit
        logger.info(f"Running circuit with {shots} shots at resilience level {resilience_level}")
        job = sampler.run(isa_circuit, shots=shots)
        result = job.result()
        
        # Process results using our adapter
        counts_or_quasi = QiskitRuntimeAdapter.process_sampler_result(result)
        
        # Calculate ideal distribution for comparison
        ideal_statevector = Statevector.from_instruction(circuit)
        ideal_probs = self._get_ideal_probabilities(ideal_statevector, circuit)
        
        # Calculate error metrics
        error_analysis = self._calculate_error_metrics(counts_or_quasi, ideal_probs)
        
        # Add metadata
        error_analysis['backend'] = getattr(self.backend, 'name', 'unknown')
        error_analysis['shots'] = shots
        error_analysis['resilience_level'] = resilience_level
        error_analysis['circuit_depth'] = circuit.depth()
        error_analysis['circuit_width'] = circuit.num_qubits
        
        return error_analysis
    
    def _get_ideal_probabilities(
        self, 
        statevector: Statevector, 
        circuit: QuantumCircuit
    ) -> Dict[str, float]:
        """
        Get ideal probabilities from a statevector.
        
        Args:
            statevector: The ideal statevector
            circuit: The original circuit
            
        Returns:
            Dict mapping bitstrings to probabilities
        """
        # Get measurement qubits
        measured_qubits = []
        for inst, qargs, _ in circuit.data:
            if inst.name == "measure":
                if qargs[0].index not in measured_qubits:
                    measured_qubits.append(qargs[0].index)
        
        if not measured_qubits:
            # If no measurements, assume all qubits are measured
            measured_qubits = list(range(circuit.num_qubits))
        
        # Get probabilities
        probs = statevector.probabilities(measured_qubits)
        
        # Convert to dict mapping bitstrings to probabilities
        result = {}
        for i, prob in enumerate(probs):
            if prob > 0:
                bitstr = format(i, f"0{len(measured_qubits)}b")
                result[bitstr] = prob
                
        return result
    
    def _calculate_error_metrics(
        self, 
        experimental_result: Dict[str, float], 
        ideal_probs: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate error metrics by comparing experimental and ideal results.
        
        Args:
            experimental_result: Dict mapping bitstrings to counts or quasi-probabilities
            ideal_probs: Dict mapping bitstrings to ideal probabilities
            
        Returns:
            Dict containing error metrics
        """
        # Normalize experimental results if they're counts
        total = sum(experimental_result.values())
        exp_probs = {k: v / total for k, v in experimental_result.items()}
        
        # Calculate cross entropy
        cross_entropy = 0
        for bitstr, ideal_prob in ideal_probs.items():
            exp_prob = exp_probs.get(bitstr, 0)
            if exp_prob > 0:
                cross_entropy -= ideal_prob * np.log2(exp_prob)
            else:
                cross_entropy = float('inf')
                break
                
        # Calculate total variation distance
        tvd = 0
        all_bitstrs = set(list(ideal_probs.keys()) + list(exp_probs.keys()))
        for bitstr in all_bitstrs:
            ideal_p = ideal_probs.get(bitstr, 0)
            exp_p = exp_probs.get(bitstr, 0)
            tvd += abs(ideal_p - exp_p)
        tvd *= 0.5  # Normalize
        
        # Calculate hellinger distance
        hellinger = 0
        for bitstr in all_bitstrs:
            ideal_p = ideal_probs.get(bitstr, 0)
            exp_p = exp_probs.get(bitstr, 0)
            hellinger += (np.sqrt(ideal_p) - np.sqrt(exp_p))**2
        hellinger = np.sqrt(hellinger / 2)
        
        return {
            "cross_entropy": cross_entropy,
            "total_variation_distance": tvd,
            "hellinger_distance": hellinger,
            "fidelity": 1 - tvd  # Simple fidelity estimate
        }
    
    def compare_resilience_levels(
        self, 
        circuit: QuantumCircuit,
        shots: int = 4000,
        levels: List[int] = [0, 1, 2, 3]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compare error metrics across different resilience levels.
        
        Args:
            circuit: The quantum circuit to analyze
            shots: Number of shots for sampling
            levels: List of resilience levels to test
            
        Returns:
            Dict mapping resilience levels to their analysis results
        """
        results = {}
        for level in levels:
            logger.info(f"Analyzing with resilience level {level}")
            results[f"level_{level}"] = self.analyze_circuit_errors(
                circuit=circuit,
                shots=shots,
                resilience_level=level
            )
            
        return results
    
    def stochastic_uncertainty_estimation(
        self, 
        circuit: QuantumCircuit,
        num_samples: int = 5,
        shots_per_sample: int = 1000,
        resilience_level: int = 1
    ) -> Dict[str, Any]:
        """
        Estimate uncertainty in circuit execution using stochastic sampling.
        
        Args:
            circuit: The quantum circuit to analyze
            num_samples: Number of independent samples to take
            shots_per_sample: Shots per sample
            resilience_level: Error mitigation level
            
        Returns:
            Dict containing uncertainty metrics
        """
        # Collect multiple samples
        samples = []
        for i in range(num_samples):
            logger.info(f"Running stochastic sample {i+1}/{num_samples}")
            result = self.analyze_circuit_errors(
                circuit=circuit,
                shots=shots_per_sample,
                resilience_level=resilience_level
            )
            samples.append(result)
            
        # Calculate statistics across samples
        metrics = ['cross_entropy', 'total_variation_distance', 'hellinger_distance', 'fidelity']
        stats = {}
        
        for metric in metrics:
            values = [sample[metric] for sample in samples]
            stats[metric] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'samples': values
            }
            
        return {
            'statistics': stats,
            'num_samples': num_samples,
            'shots_per_sample': shots_per_sample,
            'backend': getattr(self.backend, 'name', 'unknown'),
            'resilience_level': resilience_level
        } 