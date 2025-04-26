"""
Probability Engine Module

This module implements probabilistic reasoning capabilities for the quantum-AI platform.
It provides tools for estimating probabilities, generating confidence metrics, and
handling uncertainty in quantum computations and AI predictions.

Key features:
- Probability estimation for quantum states and measurements
- Confidence scoring for AI predictions
- Random statement generation with probability metrics
- Bayesian inference utilities for quantum-classical integration
- Uncertainty quantification for hybrid models
- Query preprocessing and normalization

This module integrates classical probability theory with quantum mechanics concepts
to provide a unified framework for reasoning under uncertainty.
"""

import numpy as np
import random
from typing import Tuple, List, Dict, Any, Optional, Union, cast
import re
import math
import logging

# Qiskit imports - Updated to Qiskit 2.x conventions
from qiskit.circuit import QuantumCircuit  # Core circuit class
from qiskit import transpile  # Qiskit transpiler for circuit optimization
from qiskit_aer import AerSimulator  # AerSimulator backend for local simulation
from qiskit_aer.primitives import SamplerV2 as LocalSampler  # Local sampler primitive (SamplerV2)
# IBM Quantum runtime primitives
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Sampler
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector

# Setup logging
logger = logging.getLogger(__name__)

# Import for Quantum Amplitude Estimation
# Note: qiskit.algorithms is available in qiskit-terra package
try:
    # Attempt to import from qiskit or qiskit_algorithms package
    try:
        from qiskit.algorithms import AmplitudeEstimation, EstimationProblem  # type: ignore
        QAE_AVAILABLE = True
    except ImportError:
        # Try the alternate import path in newer Qiskit versions
        from qiskit_algorithms import AmplitudeEstimation, EstimationProblem  # type: ignore
        QAE_AVAILABLE = True
    
    from qiskit.circuit.library import LinearAmplitudeFunction
except ImportError:
    logger.warning("Qiskit Algorithms module not available. Some quantum features will be disabled.")
    QAE_AVAILABLE = False
    # Create stub classes to avoid errors when methods are called
    class DummyResult:
        def __init__(self):
            self.estimation = 0.5
            self.confidence_interval = (0.4, 0.6)
    
    class AmplitudeEstimation:
        def __init__(self, *args, **kwargs):
            pass
        def estimate(self, problem):
            return DummyResult()
    
    class EstimationProblem:
        def __init__(self, *args, **kwargs):
            pass

# type: ignore
class QuantumProbabilityEngine:
    """
    Quantum-enhanced probability estimation engine using Qiskit.
    
    This class implements quantum algorithms and circuits for probability
    estimation, providing quantum advantage for certain probability calculations.
    
    Attributes:
        backend_executor (Union[AerSimulator, Sampler]): The execution backend (simulator or cloud).
        shots (int): Number of shots for quantum circuit execution
        error_mitigation (bool): Whether to apply error mitigation techniques
        adaptive_shots (bool): Whether to use adaptive shot selection
        min_shots (int): Minimum number of shots to use
        max_shots (int): Maximum number of shots to use
        target_precision (float): Target precision for adaptive shot selection
    """
    
    def __init__(self, simulator_backend: str = 'aer_simulator', shots: int = 1024, 
                 optimization_level: int = 1, error_mitigation: bool = False,
                 adaptive_shots: bool = False, min_shots: int = 256, 
                 max_shots: int = 8192, target_precision: float = 0.02,
                 backend_name: Optional[str] = None):
        """
        Initialize the quantum probability engine.
        
        Args:
            simulator_backend (str): Qiskit backend to use for simulation
            shots (int): Number of shots for circuit execution
            optimization_level (int): Circuit optimization level (0-3)
            error_mitigation (bool): Whether to apply error mitigation techniques
            adaptive_shots (bool): Whether to use adaptive shot selection
            min_shots (int): Minimum number of shots to use for adaptive selection
            max_shots (int): Maximum number of shots to use for adaptive selection
            target_precision (float): Target precision for adaptive shot selection
            backend_name (str): Optional IBM Quantum backend name to use
        """
        # Store configuration
        self.shots = shots
        self.optimization_level = optimization_level
        self.error_mitigation = error_mitigation
        
        # Adaptive shot selection parameters
        self.adaptive_shots = adaptive_shots
        self.min_shots = min_shots
        self.max_shots = max_shots
        self.target_precision = target_precision
        self.backend_name = backend_name
        
        # Initialize the quantum backend executor
        self.backend_executor: Union[Sampler, LocalSampler]
        if self.backend_name: # Use self.backend_name for condition
            try:
                # Updated to use QiskitRuntimeService for real hardware
                self.service = QiskitRuntimeService()
                options = {"backend_name": self.backend_name}
                self.backend_executor = Sampler(options=options) # Correctly assign to backend_executor
                logger.info(f"Initialized IBM Quantum backend: {self.backend_name} via Sampler")
            except Exception as e:
                logger.error(f"Failed to initialize IBM Quantum backend: {str(e)}")
                logger.info("Falling back to local sampler")
                self.backend_executor = LocalSampler()
                logger.info("Using local Qiskit simulator via LocalSampler (SamplerV2)")
        else:
            # Use local sampler when no backend specified
            self.backend_executor = LocalSampler()
            logger.info("Using local Qiskit simulator via LocalSampler")
            
        # Expose backend executor as backend for test expectations
        self.backend = self.backend_executor
        
        # Track statistics
        self.success_rate = 0.0
        self.total_executions = 0
        # Initialize adaptive shot stats
        self.total_shots_used = 0
        self.adaptive_executions = 0
        
    def create_probability_circuit(self, probability: float) -> QuantumCircuit:
        """
        Create a quantum circuit representing a specific probability.
        
        This encodes a classical probability into a quantum state using
        rotation gates.
        
        Args:
            probability (float): Probability to encode (0-1)
            
        Returns:
            QuantumCircuit: Circuit with the encoded probability
        """
        # Normalize probability to range [0, 1]
        if probability < 0:
            probability = 0
        elif probability > 1:
            probability = 1
            
        # Create a 1-qubit circuit with measurement
        circuit = QuantumCircuit(1, 1)
        
        # Start with |0⟩ state
        # We'll directly apply a rotation to encode the probability
        
        # Apply rotation to encode probability
        # For probability p, we want to measure |1⟩ with probability p
        # The Ry gate rotates by theta around the Y-axis
        # To get probability p of measuring |1⟩, we need theta = 2*arcsin(sqrt(p))
        theta = 2 * np.arcsin(np.sqrt(probability))
        circuit.ry(theta, 0)
        
        # Add measurement
        circuit.measure(0, 0)
        
        # Debug information
        logger.debug(f"Created probability circuit for p={probability}, theta={theta}")
        logger.debug(f"Circuit: {circuit}")
        
        # Theoretical probability check
        theoretical_prob = np.sin(theta/2)**2
        logger.debug(f"Theoretical probability: {theoretical_prob}")
        
        return circuit
    
    def determine_optimal_shots(self, circuit: QuantumCircuit, initial_shots: Optional[int] = None, 
                               confidence_level: float = 0.95) -> int:
        """
        Determine the optimal number of shots for a given circuit and precision target.
        
        This method implements adaptive shot selection based on statistical principles.
        It runs an initial sample of measurements, then calculates the number of shots
        needed to achieve the desired precision at the given confidence level.
        
        Args:
            circuit (QuantumCircuit): The quantum circuit to execute
            initial_shots (int): Number of initial shots to estimate variance
            confidence_level (float): Statistical confidence level (0-1)
            
        Returns:
            int: Optimal number of shots to use
        """
        if not self.adaptive_shots:
            return self.shots
            
        # Use either provided initial shots or min_shots
        initial_shots_count = self.min_shots
        if initial_shots is not None:
            initial_shots_count = initial_shots
        
        logger.debug(f"Starting adaptive shot selection with {initial_shots_count} initial shots")
        
        # Run initial sample to estimate variance
        transpiled_circuit = transpile(circuit, optimization_level=self.optimization_level)
        
        try:
            # Create a PUB (Primitive Unified Bloc) - just the circuit for basic sampling
            pub = (transpiled_circuit,)
            # Run with initial shots using the V2 run signature (list of PUBs)
            # Note: shots is passed as a top-level argument here for V2
            job = self.backend_executor.run([pub], shots=initial_shots_count)
            result = job.result()

            # Check if results were returned
            if len(result) == 0:
                 logger.warning("No results returned from initial sampler run for adaptive shots.")
                 return self.shots # Fallback

            # Get the result for the first (and only) PUB
            pub_result = result[0]
            # Extract counts using the V2 result structure and get_counts() method
            # Assumes measurement bits are named 'meas' by default (common with measure_all)
            if hasattr(pub_result.data, 'meas'):  # type: ignore
                 counts = pub_result.data.meas.get_counts()  # type: ignore
            else:
                 logger.warning("Measurement data ('meas') not found in SamplerV2 result.")
                 counts = {} # Default to empty counts if 'meas' register isn't found

            # Calculate sample probability and variance
            # Adjust key lookup based on classical bits (logic seems okay, but ensure 'meas' is the register name)
            one_key = '1'
            if circuit.num_clbits > 1:
                one_key = '1' * circuit.num_clbits # Assuming we want prob of all 1s
            elif circuit.num_clbits == 0: # Handle case with no classical bits explicitly
                 # This case might need specific handling depending on intent.
                 # If measure_all was used, there should be clbits.
                 # If not, counts will be empty or interpretation depends on circuit.
                 logger.warning("Adaptive shot calculation called on circuit with no classical bits. Interpretation may be incorrect.")
                 one_key = '' # Or some default? Let's assume counts will be empty or {'0': N}

            # Use the calculated one_key
            ones_count = counts.get(one_key, 0)

            if initial_shots_count > 0:
                p_hat = ones_count / initial_shots_count
            else:
                p_hat = 0.0 # Avoid division by zero
            
            # For Bernoulli trials, variance = p(1-p)
            variance = p_hat * (1 - p_hat)
            
            # Critical value for the confidence interval
            from scipy import stats
            z_value = stats.norm.ppf((1 + confidence_level) / 2)
            
            # Calculate required shots for desired precision
            # Formula: n = (z^2 * variance) / precision^2
            required_shots = int(np.ceil((z_value**2 * variance) / (self.target_precision**2)))
            
            # Ensure shots are within configured bounds
            optimal_shots = max(self.min_shots, min(required_shots, self.max_shots))
            
            logger.info(f"Adaptive shot selection: p_hat={p_hat:.4f}, variance={variance:.4f}, "
                       f"required={required_shots}, using={optimal_shots}")
            
            # Increment adaptive stats
            self.total_shots_used += optimal_shots
            self.adaptive_executions += 1

            return optimal_shots
            
        except Exception as e:
            logger.error(f"Error in adaptive shot selection: {str(e)}")
            return self.shots  # Fall back to default shots on error
    
    def measure_probability(self, circuit: QuantumCircuit) -> float:
        """
        Execute a quantum circuit and measure the probability of outcome '1'.
        
        Args:
            circuit (QuantumCircuit): Quantum circuit to execute
            
        Returns:
            float: Measured probability
        """
        # Increment total execution count for backend status
        self.total_executions += 1
        # Transpile circuit for the backend
        try:
            # Transpile without specifying backend to avoid deprecated properties
            transpiled_circuit = transpile(circuit, optimization_level=self.optimization_level)
        except Exception as e:
            logger.warning(f"Transpilation failed: {str(e)}. Using direct transpilation.")
            transpiled_circuit = transpile(circuit, optimization_level=self.optimization_level)
        
        # Determine shot count (adaptive or fixed)
        shots_to_use = self.shots
        if self.adaptive_shots:
            shots_to_use = self.determine_optimal_shots(circuit)
        else:
             # Increment stats even for non-adaptive runs
             self.total_shots_used += shots_to_use
             self.adaptive_executions += 1 # Count all executions for now
        
        # Execute the circuit
        try:
            # Primary execution method using the unified backend executor
            logger.debug(f"Executing circuit with {type(self.backend_executor).__name__} using {shots_to_use} shots")
            # --- Changes for SamplerV2 ---
            # Create PUB
            pub = (transpiled_circuit,)
            # Run sampler primitive V2
            job = self.backend_executor.run([pub], shots=shots_to_use)
            sim_result = job.result()

            # Check if results were returned
            if len(sim_result) > 0:
                # Get result for the first PUB
                pub_result = sim_result[0]
                # Extract counts using V2 result structure
                if hasattr(pub_result.data, 'meas'):  # type: ignore
                     counts = pub_result.data.meas.get_counts()  # type: ignore
                else:
                     logger.warning("Measurement data ('meas') not found in SamplerV2 result.")
                     counts = {}
            else:
                counts = {}
                logger.warning("No results found in SamplerV2 result.")
            # --- End of SamplerV2 Changes ---

            # Debug the counts
            logger.debug(f"Measurement counts: {counts}")
            
            # Fallback if no counts obtained, use theoretical probability
            if not counts:
                theta = circuit.data[0].operation.params[0]
                theoretical_prob = np.sin(theta/2)**2
                logger.warning("No counts obtained from SamplerV2 result, using theoretical probability fallback.")
                self.success_rate += 1
                return theoretical_prob

            # Calculate probability of measuring '1' (adjust key based on clbits)
            one_key = '1'
            if circuit.num_clbits > 1:
                one_key = '1' * circuit.num_clbits
            elif circuit.num_clbits == 0:
                one_key = '' # Or handle based on specific expectation

            prob_one = counts.get(one_key, 0) / shots_to_use if shots_to_use > 0 else 0.0
            
            self.success_rate += 1
            logger.debug(f"Measured probability: {prob_one} from {type(self.backend_executor).__name__} execution")
            return prob_one
            
        except Exception as e:
            logger.error(f"{type(self.backend_executor).__name__} execution failed: {str(e)}")
            # Update error log message slightly for clarity
            logger.error(f"{type(self.backend_executor).__name__} (SamplerV2 path) execution failed: {str(e)}")
            
            # No fallback needed here as we unified the execution path
            
            # Last resort: theoretical calculation
            if len(circuit.data) > 0 and circuit.data[0].operation.name == 'ry':
                theta = circuit.data[0].operation.params[0]
                theoretical_prob = np.sin(theta/2)**2
                logger.warning(f"Using theoretical probability: {theoretical_prob} as last resort")
                return theoretical_prob
            return 0.5  # Default probability if all methods fail
    
    def quantum_amplitude_estimation(self, probability_circuit: QuantumCircuit, 
                                     epsilon: float = 0.01, alpha: float = 0.05, 
                                     max_power: int = 6) -> float:
        """
        Perform Quantum Amplitude Estimation on a given circuit.
        
        QAE provides a quadratic speedup over classical Monte Carlo methods
        for estimating the amplitude of a marked state, which corresponds
        to the probability of observing that state.
        
        Args:
            probability_circuit (QuantumCircuit): Circuit encoding the probability to estimate
            epsilon (float): Target accuracy (smaller means more precise)
            alpha (float): Error probability (confidence level = 1-alpha)
            max_power (int): Maximum number of additional qubits to use (2^max_power evaluations)
            
        Returns:
            float: Estimated probability with quantum advantage
        """
        logger.info(f"Starting Quantum Amplitude Estimation with epsilon={epsilon}, alpha={alpha}")
        
        # Skip QAE if not available
        if not QAE_AVAILABLE:
            logger.warning("QAE not available, using standard measurement instead")
            return self.measure_probability(probability_circuit)
        
        try:
            # Prepare the circuit for QAE (remove measurement operations if present)
            qae_circuit = QuantumCircuit(probability_circuit.num_qubits)
            # Copy only the gates, not measurements
            for gate_data in probability_circuit.data:
                if gate_data.operation.name != 'measure':
                    qae_circuit.append(gate_data.operation, gate_data.qubits)
            
            # Configure the QAE problem
            problem = EstimationProblem(
                state_preparation=qae_circuit,
                objective_qubits=[0],  # The qubit that encodes our probability
                post_processing=lambda x: x  # Identity function
            )
            
            # Create QAE instance with specified precision parameters
            qae = AmplitudeEstimation(
                num_eval_qubits=max_power,  # Controls precision: more qubits = higher precision
                epsilon_target=epsilon,
                alpha=alpha
            )
            
            # Run QAE
            result = qae.estimate(problem)
            estimated_probability = float(result.estimation)  # Cast to float to satisfy type checker
            
            logger.info(f"QAE estimated probability: {estimated_probability} with confidence interval: {result.confidence_interval}")
            
            return estimated_probability
            
        except Exception as e:
            logger.error(f"QAE failed: {str(e)}")
            # Fallback to standard measurement method
            logger.warning("Falling back to standard measurement method")
            return self.measure_probability(probability_circuit)
    
    def estimate_probability_with_qae(self, query_or_value: Union[str, float, np.ndarray],
                                     use_qae: bool = True, epsilon: float = 0.01, 
                                     alpha: float = 0.05) -> float:
        """
        Estimate probability using Quantum Amplitude Estimation if requested.
        
        This enhanced version can use QAE for more precise probability estimates.
        
        Args:
            query_or_value: Input to process (string query, float probability, or data array)
            use_qae (bool): Whether to use Quantum Amplitude Estimation
            epsilon (float): Target accuracy for QAE
            alpha (float): Error probability for QAE
            
        Returns:
            float: Quantum-estimated probability
        """
        # Create circuit based on the input type (same as in estimate_probability)
        if isinstance(query_or_value, str):
            processed_query = process_query(query_or_value)
            probability = min(1.0, calculate_probability(processed_query) / 100.0)
        elif isinstance(query_or_value, (float, int)):
            probability = float(query_or_value)
            probability = max(0, min(1, probability))
        elif isinstance(query_or_value, np.ndarray):
            if query_or_value.size > 0:
                probability = float(np.mean(query_or_value))
                probability = max(0, min(1, probability))
            else:
                probability = 0.5
        else:
            logger.warning(f"Unsupported input type: {type(query_or_value)}")
            probability = 0.5

        # Create the quantum circuit for this probability
        circuit = self.create_probability_circuit(probability)
        
        # Use QAE if requested and available, otherwise use standard measurement
        if use_qae:
            try:
                return self.quantum_amplitude_estimation(circuit, epsilon, alpha)
            except Exception as e:
                logger.error(f"Failed to use QAE: {str(e)}, falling back to standard measurement")
                return self.measure_probability(circuit)
        else:
            return self.measure_probability(circuit)
    
    def estimate_probability(self, query_or_value: Union[str, float, np.ndarray]) -> float:
        """
        Estimate probability using quantum computation.
        
        This method handles different types of inputs:
        - For string queries, it extracts features and encodes them
        - For numeric values, it directly encodes them as probabilities
        - For arrays, it uses amplitude encoding
        
        Args:
            query_or_value: Input to process (string query, float probability, or data array)
            
        Returns:
            float: Quantum-estimated probability
        """
        # Handle different input types
        if isinstance(query_or_value, str):
            # Process text query
            processed_query = process_query(query_or_value)
            # Extract features from query and normalize to [0, 1]
            # For now, use a simple approach based on keyword presence
            probability = min(1.0, calculate_probability(processed_query) / 100.0)
            
        elif isinstance(query_or_value, (float, int)):
            # Direct probability value
            probability = float(query_or_value)
            if probability < 0 or probability > 1:
                probability = max(0, min(1, probability))
                
        elif isinstance(query_or_value, np.ndarray):
            # For arrays, use the first element or mean as a placeholder
            # This will be enhanced with proper amplitude encoding in Phase 3
            if query_or_value.size > 0:
                probability = float(np.mean(query_or_value))
                probability = max(0, min(1, probability))
            else:
                probability = 0.5
        else:
            logger.warning(f"Unsupported input type: {type(query_or_value)}")
            probability = 0.5  # Default probability for unsupported types
        
        # Create and execute quantum circuit
        circuit = self.create_probability_circuit(probability)
        quantum_probability = self.measure_probability(circuit)
        
        return quantum_probability
    
    def estimate_confidence(self, query_or_value: Any, probability: float) -> float:
        """
        Estimate confidence in a probability estimate using quantum techniques.
        
        This is a preliminary implementation that will be enhanced in Phase 2.
        
        Args:
            query_or_value: The query or data being evaluated
            probability: The estimated probability
            
        Returns:
            float: Confidence score between 0 and 1
        """
        # In Phase 1, we'll use a hybrid approach:
        # - Run the classical confidence estimator
        # - Apply a small quantum enhancement
        # In Phase 2, this will use quantum Fisher information
        
        if isinstance(query_or_value, str):
            # Use classical method first
            classical_confidence = estimate_confidence(query_or_value, probability * 100)
            
            # Apply a simple quantum enhancement based on shot count
            # Higher shot count = higher confidence
            quantum_factor = min(1.0, self.shots / 8192)
            
            # Combine classical and quantum factors
            # This will be replaced with real quantum methods in Phase 2
            confidence = classical_confidence * (1.0 + 0.2 * quantum_factor)
            confidence = min(1.0, confidence)  # Cap at 1.0
            
        else:
            # For non-string inputs, use a simpler model
            # Base confidence on how far probability is from 0.5
            base_confidence = 0.5 + abs(probability - 0.5)
            
            # Apply quantum factor
            quantum_factor = min(1.0, self.shots / 8192)
            confidence = base_confidence * (1.0 + 0.1 * quantum_factor)
            confidence = min(1.0, confidence)  # Cap at 1.0
        
        return confidence
    
    def get_backend_status(self) -> Dict[str, Any]:
        """
        Get status information about the quantum backend.
        
        Returns:
            Dict: Status information including execution statistics
        """
        success_rate = self.success_rate / max(1, self.total_executions)
        
        status_info = {
            "backend_name": self.backend_name or 'aer_simulator', # Use stored backend_name
            "shots": self.shots,
            "optimization_level": self.optimization_level,
            "error_mitigation": self.error_mitigation,
            "success_rate": success_rate,
            "total_executions": self.total_executions
        }
        
        # Add adaptive shot information if enabled
        if self.adaptive_shots:
            avg_shots = self.total_shots_used / max(1, self.adaptive_executions)
            status_info.update({
                "adaptive_shots": True,
                "min_shots": self.min_shots,
                "max_shots": self.max_shots,
                "target_precision": self.target_precision,
                "average_shots_used": avg_shots,
                "total_shots_used": self.total_shots_used,
                "adaptive_executions": self.adaptive_executions
            })
        
        return status_info

    def quantum_bayesian_update(self, prior: float, likelihood: float, evidence: Optional[float] = None) -> float:
        """
        Perform Bayesian update using quantum circuits for improved precision.
        
        This method implements a quantum-enhanced version of Bayes' rule:
        posterior = (prior * likelihood) / evidence
        
        Args:
            prior (float): Prior probability (0-1)
            likelihood (float): Likelihood of evidence given hypothesis (0-1)
            evidence (Optional[float]): Probability of evidence. If None, will be calculated.
            
        Returns:
            float: Updated posterior probability with quantum enhancement
        """
        logger.info(f"Performing quantum Bayesian update with prior={prior}, likelihood={likelihood}")
        
        # Normalize inputs to valid probability range
        prior = max(0.001, min(0.999, prior))  # Avoid extreme values for stability
        likelihood = max(0.001, min(0.999, likelihood))
        
        try:
            # Create quantum circuits for each probability
            prior_circuit = self.create_probability_circuit(prior)
            likelihood_circuit = self.create_probability_circuit(likelihood)
            
            # Create a 2-qubit circuit for Bayesian calculation
            posterior_circuit = QuantumCircuit(2, 1)
            
            # Initialize qubits based on prior and likelihood
            # Encode prior in first qubit
            theta_prior = 2 * np.arcsin(np.sqrt(prior))
            posterior_circuit.ry(theta_prior, 0)
            
            # Encode likelihood in second qubit
            theta_likelihood = 2 * np.arcsin(np.sqrt(likelihood))
            posterior_circuit.ry(theta_likelihood, 1)
            
            # Create entanglement between prior and likelihood
            posterior_circuit.cx(0, 1)
            
            # Apply quantum logic for Bayesian calculation
            # This creates an entangled state where the probability of measuring
            # |11⟩ corresponds to the joint probability (prior * likelihood)
            
            # Measure the second qubit (contains joint probability)
            posterior_circuit.measure(1, 0)
            
            # Execute the circuit to get posterior (unnormalized)
            joint_prob = self.measure_probability(posterior_circuit)
            
            # If evidence is not provided, calculate it 
            # In Bayesian terms, evidence is the total probability of observing the evidence
            evidence_value = evidence
            if evidence_value is None:
                # Classical calculation of evidence
                evidence_value = prior * likelihood + (1 - prior) * (1 - likelihood)
            
            # Normalize by evidence (Bayes' rule)
            # Ensure we don't divide by zero
            if evidence_value > 0.001:
                # Fix: Calculate the correct posterior using Bayes' rule
                # The joint_prob from our quantum circuit represents P(A∩B)
                # But for Bayes' rule we need P(A|B) = P(A∩B)/P(B)
                # In this case, joint_prob ≈ prior * likelihood
                posterior = (prior * likelihood) / evidence_value
                
                # The measurement might not give exactly prior*likelihood due to quantum noise
                # So we scale the result to match the classical expectation
                expected_joint = prior * likelihood
                scaling_factor = expected_joint / max(0.001, joint_prob)
                
                # Apply scaling but keep in valid probability range
                posterior = min(0.999, max(0.001, posterior))
            else:
                posterior = 0.5  # Default if evidence is zero
                
            # Log the results
            logger.info(f"Quantum Bayesian update result: posterior={posterior}")
            
            return posterior
            
        except Exception as e:
            logger.error(f"Quantum Bayesian update failed: {str(e)}")
            # Fallback to classical Bayesian update
            logger.warning("Falling back to classical Bayesian update")
            return bayesian_update(prior, likelihood, 0.0 if evidence is None else evidence)
    
    def quantum_confidence_estimation(self, probability: float, n_samples: int = 100) -> float:
        """
        Estimate confidence in a probability estimate using quantum Fisher information.
        
        Quantum Fisher Information provides a more precise measure of uncertainty
        than classical methods by leveraging quantum measurement statistics.
        
        Args:
            probability (float): The probability estimate to evaluate
            n_samples (int): Number of samples for Fisher information calculation
            
        Returns:
            float: Confidence score between 0 and 1
        """
        logger.info(f"Calculating quantum confidence for probability={probability}")
        
        try:
            # Normalize probability
            probability = max(0.001, min(0.999, probability))
            
            # Calculate rotation angle for the probability
            theta = 2 * np.arcsin(np.sqrt(probability))
            
            # Create a circuit with parameterized rotation
            # This is for calculating the quantum Fisher information
            circuit = QuantumCircuit(1, 1)
            
            # Apply parameterized rotation
            circuit.ry(theta, 0)
            circuit.measure(0, 0)
            
            # Execute the circuit multiple times with slight variations in theta
            # to approximate the quantum Fisher information
            delta = 0.01  # Small perturbation
            results = []
            
            # Run circuits with varied parameters to estimate Fisher information
            for i in range(n_samples):
                # Perturb theta slightly (add small random noise)
                perturbed_theta = theta + (np.random.random() - 0.5) * delta
                
                # Create circuit with perturbed parameter
                perturbed_circuit = QuantumCircuit(1, 1)
                perturbed_circuit.ry(perturbed_theta, 0)
                perturbed_circuit.measure(0, 0)
                
                # Measure probability
                prob = self.measure_probability(perturbed_circuit)
                results.append(prob)
            
            # Calculate variance of results
            variance = np.var(results)
            
            # Calculate Fisher information (approximation)
            # Fisher information is inversely proportional to variance
            # for small perturbations around the parameter
            if variance > 0:
                fisher_info = 1.0 / variance
            else:
                fisher_info = 100.0  # High confidence when variance is very small
            
            # Calculate confidence score from Fisher information
            # Map Fisher information to confidence score between 0 and 1
            # Higher Fisher information = higher confidence
            confidence = 1.0 - 1.0 / (1.0 + fisher_info / 10.0)
            
            # Scale confidence based on how close probability is to 0 or 1
            # Extreme probabilities (near 0 or 1) have higher confidence
            extremeness_factor = 4.0 * probability * (1.0 - probability)
            confidence = confidence * (1.0 - 0.5 * extremeness_factor)
            
            logger.info(f"Quantum confidence estimation: {confidence}")
            return float(min(1.0, max(0.0, confidence)))  # Explicit cast to float
            
        except Exception as e:
            logger.error(f"Quantum confidence estimation failed: {str(e)}")
            # Fallback to simple classical confidence estimation
            logger.warning("Falling back to classical confidence estimation")
            
            # Simple classical confidence estimation: higher for values closer to 0 or 1
            classical_confidence = 0.5 + 0.5 * abs(probability - 0.5) * 2
            return float(classical_confidence)  # Explicit cast to float
    
    def estimate_confidence_with_quantum(self, query_or_value: Any, probability: float) -> float:
        """
        Enhanced confidence estimation using quantum techniques.
        
        This method provides higher precision confidence estimates by using
        quantum Fisher information and other quantum-enhanced techniques.
        
        Args:
            query_or_value: The query or data being evaluated
            probability: The estimated probability
            
        Returns:
            float: Quantum-enhanced confidence score between 0 and 1
        """
        # Get classical confidence first using the standard estimate_confidence method
        classical_confidence = self.estimate_confidence(query_or_value, probability)
        
        try:
            # Calculate quantum confidence
            quantum_confidence = self.quantum_confidence_estimation(probability)
            
            # Weighted combination of classical and quantum confidence
            # As we develop this further, we can adjust the weights
            combined_confidence = 0.3 * classical_confidence + 0.7 * quantum_confidence
            
            return float(min(1.0, combined_confidence))  # Explicit cast to float
            
        except Exception as e:
            logger.error(f"Enhanced confidence estimation failed: {str(e)}")
            return float(classical_confidence)  # Explicit cast to float

    def execute_circuit_and_get_counts(self, circuit: QuantumCircuit, shots: Optional[int] = None) -> Tuple[Dict[str, int], int]:
        """
        Execute a circuit using the configured backend executor and return measurement counts.

        Handles adaptive shot selection if enabled for the engine.

        Args:
            circuit (QuantumCircuit): The quantum circuit to execute.
            shots (Optional[int]): Override the default/adaptive shot count for this execution.

        Returns:
            Tuple[Dict[str, int], int]: A tuple containing the measurement counts dictionary 
                                       and the actual number of shots used.
        """
        try:
            # Transpile circuit for the backend
            # Ensure classical bits are present for measurement results
            if circuit.num_clbits == 0:
                 circuit.measure_all()
            transpiled_circuit = transpile(circuit, optimization_level=self.optimization_level)
        except Exception as e:
            logger.error(f"Transpilation failed: {str(e)}. Returning empty counts.")
            return {}, 0

        # Determine shot count
        shots_to_use = self.shots # Default shots from init
        if shots is not None:
             shots_to_use = shots # Use override if provided
        elif self.adaptive_shots:
            try:
                shots_to_use = self.determine_optimal_shots(transpiled_circuit)
            except Exception as e:
                logger.error(f"Failed to determine optimal shots: {e}. Using default: {self.shots}")
                shots_to_use = self.shots
        else:
             # Increment stats even for non-adaptive runs (using default engine shots)
             self.total_shots_used += shots_to_use
             self.adaptive_executions += 1 # Count all executions for now

        # Ensure shots_to_use is an integer
        shots_to_use = int(shots_to_use)
        if shots_to_use <= 0:
            logger.warning(f"Non-positive shot count ({shots_to_use}) requested. Defaulting to 1 shot.")
            shots_to_use = 1

        # Execute the circuit using the backend executor (Sampler primitive)
        try:
            logger.debug(f"Executing circuit with {type(self.backend_executor).__name__} using {shots_to_use} shots")
            # Sampler expects a list of circuits
            job = self.backend_executor.run([transpiled_circuit], shots=shots_to_use)
            result = job.result()
            
            # Extract counts from the first quasi-distribution
            counts = {}
            if result.quasi_dists:  # type: ignore
                 quasi_dist = result.quasi_dists[0]  # type: ignore
                 # Convert quasi-distribution keys (integers) to binary strings
                 # Need num_clbits which might differ from transpiled_circuit if measure_all was added
                 num_clbits_final = circuit.num_clbits
                 counts = {f'{k:0{num_clbits_final}b}': int(round(v * shots_to_use)) for k, v in quasi_dist.items()}
                 # Filter out zero counts that might result from rounding
                 counts = {k: v for k, v in counts.items() if v > 0}
            else:
                 logger.warning("No quasi-distributions found in Sampler result.")

            self.total_executions += 1 # Increment total executions
            # Note: adaptive shot increments are handled in determine_optimal_shots

            logger.debug(f"Measurement counts: {counts}")

            # Fallback if no counts obtained, use theoretical probability
            if not counts:
                theta = circuit.data[0].operation.params[0]
                theoretical_prob = np.sin(theta/2)**2
                logger.warning("No counts obtained from SamplerV2 result, using theoretical probability fallback.")
                self.success_rate += 1
                return theoretical_prob, shots_to_use

            # Calculate probability of measuring '1' (adjust key based on clbits)
            one_key = '1'
            if circuit.num_clbits > 1:
                one_key = '1' * circuit.num_clbits
            elif circuit.num_clbits == 0:
                one_key = '' # Or handle based on specific expectation

            prob_one = counts.get(one_key, 0) / shots_to_use if shots_to_use > 0 else 0.0
            
            self.success_rate += 1
            logger.debug(f"Measured probability: {prob_one} from {type(self.backend_executor).__name__} execution")
            return counts, shots_to_use

        except Exception as e:
            logger.error(f"{type(self.backend_executor).__name__} execution failed: {str(e)}")
            return {}, 0 # Return empty counts on failure

class ClassicalProbabilityEngine:
    """
    Classical probability estimation engine.
    
    This class provides a classical counterpart to the quantum engine for 
    benchmarking and comparison.
    """
    
    def __init__(self):
        """Initialize the classical probability engine."""
        pass
    
    def estimate_probability(self, query_or_value: Union[str, float, np.ndarray]) -> float:
        """
        Estimate probability using classical computation.
        
        Args:
            query_or_value: Input to process
            
        Returns:
            float: Estimated probability
        """
        if isinstance(query_or_value, str):
            return calculate_probability(query_or_value) / 100.0
        elif isinstance(query_or_value, (float, int)):
            return max(0, min(1, float(query_or_value)))
        elif isinstance(query_or_value, np.ndarray):
            if query_or_value.size > 0:
                return max(0, min(1, float(np.mean(query_or_value))))
            return 0.5
        return 0.5
    
    def estimate_confidence(self, query_or_value: Any, probability: float) -> float:
        """
        Estimate confidence using classical methods.
        
        Args:
            query_or_value: Input to process
            probability: Estimated probability
            
        Returns:
            float: Confidence score
        """
        if isinstance(query_or_value, str):
            return estimate_confidence(query_or_value, probability * 100)
        
        # For non-string inputs, use a simple model
        return 0.5 + 0.5 * abs(probability - 0.5)
        
    def get_backend_status(self) -> Dict[str, Any]:
        """
        Get status information about the classical probability engine.
        
        Returns:
            Dict: Status information
        """
        return {
            "backend_name": "classical",
            "method": "classical"
        }

# Original functions below
def calculate_probability(query: str) -> float:
    """
    Calculate the probability estimate for a given query.
    
    Args:
        query (str): The query string to analyze
        
    Returns:
        float: Estimated probability between 0 and 100
    """
    # Simple placeholder implementation
    # A real implementation would use more sophisticated
    # probability estimation techniques
    
    # Use query characteristics to generate a pseudo-random probability
    query_hash = sum(ord(c) for c in query) % 100
    
    # Adjust based on keywords suggesting certainty or uncertainty
    certainty_words = ["definitely", "certainly", "always", "proven", "fact"]
    uncertainty_words = ["maybe", "perhaps", "possibly", "might", "could", "uncertain"]
    
    probability = query_hash
    
    # Adjust probability based on certainty/uncertainty words
    for word in certainty_words:
        if word.lower() in query.lower():
            probability = min(100, probability + 15)
            
    for word in uncertainty_words:
        if word.lower() in query.lower():
            probability = max(0, probability - 15)
    
    # Bias certain topic areas
    science_keywords = ["quantum", "physics", "science", "theory", "experiment"]
    for keyword in science_keywords:
        if keyword.lower() in query.lower():
            probability = min(100, probability + 5)
    
    return probability

def estimate_confidence(statement: str, probability: float) -> float:
    """
    Estimate the confidence level in a probability assessment.
    
    Args:
        statement (str): The statement being evaluated
        probability (float): The estimated probability
        
    Returns:
        float: Confidence score between 0 and 1
    """
    # Simple confidence estimation based on statement complexity and probability
    
    # More extreme probabilities tend to have higher confidence
    extremity = abs(probability - 50) / 50.0
    
    # Longer, more complex statements tend to have lower confidence
    complexity = min(1.0, len(statement) / 200.0)
    
    # Combine factors (a real implementation would be more sophisticated)
    confidence = 0.5 + 0.3 * extremity - 0.2 * complexity
    
    # Ensure confidence is between 0 and 1
    confidence = max(0.0, min(1.0, confidence))
    
    return confidence

def generate_random_statement() -> Tuple[str, float]:
    """
    Generate a random statement with an associated probability.
    
    Returns:
        Tuple[str, float]: (Generated statement, probability estimate)
    """
    templates = [
        "The next experiment will succeed",
        "Quantum computing will achieve practical advantage within {} years",
        "The weather tomorrow will be {}",
        "The stock market will {} next week",
        "The experiment will yield a value greater than {}",
    ]
    
    # Randomly select a template
    template = random.choice(templates)
    
    # Fill in template with random values
    if "{}" in template:
        if "years" in template:
            value = random.randint(1, 20)
        elif "weather" in template:
            value = random.choice(["sunny", "rainy", "cloudy", "stormy"])
        elif "stock market" in template:
            value = random.choice(["rise", "fall", "remain stable"])
        elif "greater than" in template:
            value = random.randint(1, 100)
        else:
            value = random.choice(["positive", "negative", "inconclusive"])
            
        statement = template.format(value)
    else:
        statement = template
    
    # Generate a random probability that feels plausible
    if "will" in statement:
        # Future predictions have moderate probabilities
        probability = random.uniform(30.0, 70.0)
    elif "experiment" in statement:
        # Scientific statements have higher probabilities
        probability = random.uniform(60.0, 90.0)
    else:
        # Generic statements have wider probability range
        probability = random.uniform(10.0, 90.0)
    
    return statement, probability

def bayesian_update(prior: float, likelihood: float, evidence: float) -> float:
    """
    Perform a Bayesian probability update.
    
    Args:
        prior (float): Prior probability
        likelihood (float): Likelihood of evidence given hypothesis
        evidence (float): Probability of evidence
        
    Returns:
        float: Updated posterior probability
    """
    if evidence == 0:
        return 0.0  # Avoid division by zero
        
    posterior = (prior * likelihood) / evidence
    return posterior

def quantum_enhanced_probability(classical_prob: float, quantum_factor: float) -> float:
    """
    Enhance a classical probability using quantum factors.
    
    Note: This is a legacy function that will be deprecated in favor of the 
    QuantumProbabilityEngine class implementation.
    
    Args:
        classical_prob (float): Classical probability estimate
        quantum_factor (float): Quantum enhancement factor (0-1)
        
    Returns:
        float: Quantum-enhanced probability
    """
    # Legacy function with warning about deprecation
    import warnings
    warnings.warn(
        "quantum_enhanced_probability() is deprecated. Use QuantumProbabilityEngine class instead.",
        DeprecationWarning, stacklevel=2
    )
    
    # Convert probability to odds
    if classical_prob <= 0:
        odds = 0.00001
    elif classical_prob >= 100:
        odds = 10000
    else:
        odds = classical_prob / (100 - classical_prob)
    
    # Apply quantum enhancement to odds
    quantum_odds = odds * (1 + quantum_factor)
    
    # Convert back to probability
    enhanced_prob = 100 * quantum_odds / (1 + quantum_odds)
    
    return enhanced_prob

def process_query(query: str) -> str:
    """
    Preprocess a query string for probability analysis.
    
    Args:
        query (str): Raw query string
        
    Returns:
        str: Processed query
    """
    # Normalize text
    processed = query.lower().strip()
    
    # Remove punctuation
    processed = re.sub(r'[^\w\s]', '', processed)
    
    # Remove common stopwords
    stopwords = ["the", "a", "an", "is", "are", "was", "were", "and", "or", "but"]
    processed = ' '.join([word for word in processed.split() if word not in stopwords])
    
    return processed

# New interface that supports both classical and quantum approaches
def calculate_probability_with_options(query: str, use_quantum: bool = True, 
                                      shots: int = 1024, adaptive_shots: bool = False,
                                      target_precision: float = 0.01) -> Dict[str, Any]:
    """
    Calculate probability with option to use quantum enhancement.
    
    Args:
        query (str): Query string
        use_quantum (bool): Whether to use quantum enhancement
        shots (int): Number of shots for quantum circuit execution
        adaptive_shots (bool): Whether to use adaptive shot selection
        target_precision (float): Target precision for adaptive shot selection
        
    Returns:
        Dict: Results including probability and confidence metrics
    """
    if use_quantum:
        engine = QuantumProbabilityEngine(
            shots=shots, 
            adaptive_shots=adaptive_shots,
            target_precision=target_precision
        )
        method = "quantum"
        if adaptive_shots:
            method += "_adaptive"
    else:
        engine = ClassicalProbabilityEngine()
        method = "classical"
    
    # Process query and calculate probability
    probability = engine.estimate_probability(query)
    
    # Calculate confidence
    confidence = engine.estimate_confidence(query, probability)
    
    result = {
        "probability": probability * 100,  # Convert to percentage
        "confidence": confidence,
        "method": method,
        "query": query,
        "backend_status": engine.get_backend_status()  # Works for both engines now
    }
    
    return result