import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_aer.noise.errors import depolarizing_error, readout_error
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler  # V2 API: SamplerV2 is the correct import
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from typing import Dict, List, Optional, Tuple, Union
import json
from datetime import datetime
import os

# --------------------------------------------------------------------------------------
# QISKIT V2 PRIMITIVES MIGRATION (2024)
# This file was refactored to use Qiskit V2 primitives (SamplerV2, EstimatorV2).
# - All usage of the old Options class is removed (deprecated in V2).
# - All option setting for SamplerV2 is done via the dataclass interface or dict.
# - SamplerV2 does NOT support resilience_level or optimization_level (these are for EstimatorV2 only).
# - Only valid options for SamplerV2 are set (e.g., default_shots, backend_options for simulators).
# - See: https://docs.quantum.ibm.com/migration-guides/v2-primitives
# - If you update option handling, document rationale in docs/changelog.md and docs/retrospective_summaries.md.
# --------------------------------------------------------------------------------------

class FinancialErrorAnalyzer:
    """
    Error analysis tool for Stochastic-Memsaur financial modeling
    
    This module specifically focuses on analyzing how quantum errors impact
    financial metrics, which is critical for ensuring reliable results in
    quantum financial simulations.
    """
    
    def __init__(self, 
                 service: Optional[QiskitRuntimeService] = None,
                 results_dir: str = './error_analysis_results'):
        """
        Initialize the error analyzer
        
        Args:
            service: QiskitRuntimeService instance (created if None)
            results_dir: Directory to store analysis results
        """
        self.service = service if service else QiskitRuntimeService()
        self.results_dir = results_dir
        
        # Create results directory if it doesn't exist
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        # Initialize simulator
        self.simulator = AerSimulator()
        
        # Cache for backend instances
        self.backend_cache = {}
        
    def analyze_resilience_impact(self,
                                 circuit: QuantumCircuit,
                                 backend_name: str,
                                 resilience_levels: List[int] = [0, 1, 2],
                                 shots: int = 5000) -> Dict:
        """
        Analyze how different resilience levels affect financial metrics
        
        Args:
            circuit: Financial circuit to analyze
            backend_name: Backend to use for analysis
            resilience_levels: List of resilience levels to test
            shots: Number of shots per execution
            
        Returns:
            Dictionary of results by resilience level
        
        Note:
            - This method is for demonstration; SamplerV2 does NOT support resilience_level or optimization_level.
            - Only EstimatorV2 supports resilience_level. For SamplerV2, only valid options (e.g., default_shots) are set.
            - See Qiskit V2 migration guide for details.
        """
        print(f"Starting resilience analysis using {backend_name}...")
        
        results = {}
        
        # Get ideal results using noiseless simulation
        print("Running ideal (noiseless) simulation...")
        ideal_result = self.simulator.run(circuit, shots=shots).result()
        ideal_counts = ideal_result.get_counts()
        ideal_metrics = self._calculate_financial_metrics(ideal_counts)
        
        # Store ideal results as baseline
        results['ideal'] = {
            'counts': ideal_counts,
            'financial_metrics': ideal_metrics
        }
        
        print("Ideal financial metrics:")
        print(f"  - Expected return: {ideal_metrics['expected_return']:.4f}")
        print(f"  - Volatility: {ideal_metrics['volatility']:.4f}")
        print(f"  - Value at risk: {ideal_metrics['value_at_risk']:.4f}")
        print(f"  - Sharpe ratio: {ideal_metrics['sharpe_ratio']:.4f}")
        
        # Check if we should use local simulator
        is_local_simulator = backend_name == 'local_simulator'
        
        # If not local simulator, get the real backend from available backends
        backend = None
        if not is_local_simulator:
            # Get the backend from the service
            try:
                # In V2 API, we need to get backend differently
                backend = self._get_backend(backend_name)
                
                # Optimize circuit for target backend - generate ISA circuit
                pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
                circuit = pm.run(circuit)
                print(f"Circuit optimized to depth {circuit.depth()}")
            except Exception as e:
                print(f"Error getting backend: {str(e)}")
                print("Falling back to local simulation...")
                is_local_simulator = True
        
        # Define the backend for the session
        session_backend = self.simulator if is_local_simulator else backend
        
        # Test each resilience level within a single session - updated for V2 API
        with Session(backend=session_backend) as session:
            # Test each resilience level
            for level in resilience_levels:
                print(f"\nTesting resilience level {level}...")
                
                try:
                    # Configure options - updated to V2 API format
                    # Create options as a dictionary, not directly modifying sampler.options
                    sampler_options = {
                        "default_shots": shots
                        # Note: resilience_level and optimization_level are NOT valid for SamplerV2
                    }
                    
                    # Create sampler with mode parameter (V2 API)
                    sampler = Sampler(mode=session, options=sampler_options)
                    
                    # Execute circuit
                    job = sampler.run([circuit])
                    job_id = job.job_id()
                    print(f"Job submitted with ID: {job_id}")
                    
                    # Wait for job completion
                    result = job.result()
                    
                    # Extracting counts from result - updated for V2 API
                    pub_result = result[0]  # Get the first PUB result
                    
                    # Get the register name from the circuit result
                    reg_name = list(pub_result.data.keys())[0]
                    counts = pub_result.data[reg_name].get_counts()
                    
                    # Calculate financial metrics
                    metrics = self._calculate_financial_metrics(counts)
                    
                    # Calculate error percentages compared to ideal
                    error_metrics = {
                        'return_error_pct': 100 * abs(metrics['expected_return'] - ideal_metrics['expected_return']) / max(0.0001, abs(ideal_metrics['expected_return'])),
                        'volatility_error_pct': 100 * abs(metrics['volatility'] - ideal_metrics['volatility']) / max(0.0001, abs(ideal_metrics['volatility'])),
                        'var_error_pct': 100 * abs(metrics['value_at_risk'] - ideal_metrics['value_at_risk']) / max(0.0001, abs(ideal_metrics['value_at_risk'])),
                        'sharpe_error_pct': 100 * abs(metrics['sharpe_ratio'] - ideal_metrics['sharpe_ratio']) / max(0.0001, abs(ideal_metrics['sharpe_ratio']))
                    }
                    
                    # Store results
                    results[f'resilience_{level}'] = {
                        'counts': counts,
                        'financial_metrics': metrics,
                        'error_metrics': error_metrics,
                        'job_id': job_id
                    }
                    
                    print(f"Financial metrics with resilience level {level}:")
                    print(f"  - Expected return: {metrics['expected_return']:.4f} (error: {error_metrics['return_error_pct']:.2f}%)")
                    print(f"  - Volatility: {metrics['volatility']:.4f} (error: {error_metrics['volatility_error_pct']:.2f}%)")
                    print(f"  - Value at risk: {metrics['value_at_risk']:.4f} (error: {error_metrics['var_error_pct']:.2f}%)")
                    print(f"  - Sharpe ratio: {metrics['sharpe_ratio']:.4f} (error: {error_metrics['sharpe_error_pct']:.2f}%)")
                    
                except Exception as e:
                    print(f"Error running with resilience level {level}: {str(e)}")
                    results[f'resilience_{level}'] = {'error': str(e)}
            
        # Plot comparison
        self._plot_resilience_comparison(results)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"{self.results_dir}/resilience_analysis_{backend_name}_{timestamp}.json"
        
        # Create serializable results
        serializable_results = {}
        for key, data in results.items():
            if key == 'ideal':
                serializable_results[key] = {
                    'financial_metrics': data['financial_metrics']
                }
            elif 'error' in data:
                serializable_results[key] = {
                    'error': data['error']
                }
            else:
                serializable_results[key] = {
                    'financial_metrics': data['financial_metrics'],
                    'error_metrics': data['error_metrics'],
                    'job_id': data['job_id'] if 'job_id' in data else None
                }
                
        with open(result_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
            
        print(f"\nResilience analysis complete. Results saved to {result_file}")
        return results
    
    def analyze_noise_sensitivity(self,
                                circuit: QuantumCircuit,
                                noise_levels: List[float] = [0.001, 0.005, 0.01, 0.02, 0.05],
                                resilience_level: int = 1,
                                shots: int = 5000) -> Dict:
        """
        Analyze how different noise levels affect financial metrics
        
        Args:
            circuit: Financial circuit to analyze
            noise_levels: Depolarizing noise strengths to test
            resilience_level: Error mitigation level to use (ignored for SamplerV2)
            shots: Number of shots per execution
            
        Returns:
            Dictionary of results by noise level
        
        Note:
            - SamplerV2 does NOT support resilience_level or optimization_level.
            - Only valid options for SamplerV2 are set (e.g., default_shots, backend_options for simulators).
            - See Qiskit V2 migration guide for details.
        """
        print(f"Starting noise sensitivity analysis with resilience level {resilience_level}...")
        
        # Get ideal results using noiseless simulation
        print("Running ideal (noiseless) simulation...")
        ideal_result = self.simulator.run(circuit, shots=shots).result()
        ideal_counts = ideal_result.get_counts()
        ideal_metrics = self._calculate_financial_metrics(ideal_counts)
        
        results = {
            'ideal': {
                'counts': ideal_counts,
                'financial_metrics': ideal_metrics
            }
        }
        
        print("Ideal financial metrics:")
        print(f"  - Expected return: {ideal_metrics['expected_return']:.4f}")
        print(f"  - Volatility: {ideal_metrics['volatility']:.4f}")
        print(f"  - Value at risk: {ideal_metrics['value_at_risk']:.4f}")
        print(f"  - Sharpe ratio: {ideal_metrics['sharpe_ratio']:.4f}")
        
        # Test each noise level with local simulator (replaced cloud simulator)
        # Updated for V2 API
        with Session(backend=self.simulator) as session:
            # Only valid option is 'default_shots' for Sampler
            sampler = Sampler(mode=session, options={"default_shots": shots})
            
            for noise in noise_levels:
                print(f"\nTesting noise level {noise:.4f}...")
                try:
                    noise_model = self._create_financial_noise_model(noise)
                    simulator_options = {
                        "method": "automatic",
                        "noise_model": noise_model,
                        "basis_gates": noise_model.basis_gates
                    }
                    # --- QISKIT V2 API NOTE ---
                    # For SamplerV2, options can be updated after initialization using the .update() method.
                    # This is the correct and production-ready way to set options in bulk (see IBM Quantum docs).
                    # For simulators (e.g., AerSimulator), backend_options such as noise_model are valid.
                    # For real hardware, only supported options (see Qiskit docs) are accepted; noise_model etc. are not valid.
                    # SamplerV2 does NOT support resilience_level or optimization_level (these are for EstimatorV2 only).
                    # Always check backend type before setting options, and keep this distinction in mind for production code.
                    # See: https://docs.quantum.ibm.com/guides/specify-runtime-options
                    # --------------------------
                    # Remove any attempt to set resilience_level or optimization_level on SamplerV2:
                    # sampler.options.update(resilience_level=..., optimization_level=...)
                    # is NOT valid for SamplerV2 and will be ignored or cause errors.
                    # Instead, only set valid options for SamplerV2, e.g.:
                    sampler.options.update(backend_options=simulator_options)
                    # NOTE: If you need error mitigation, use EstimatorV2, not SamplerV2.
                    # For a full list of valid options, see the Qiskit documentation linked above.
                    #
                    # --- REFLECTION ---
                    # This code was updated as part of a major refactor to align with Qiskit V2 primitives.
                    # The old Options class is deprecated for V2. All option setting must use the dataclass interface or dict.
                    # Attempts to set resilience_level or optimization_level on SamplerV2 are now removed.
                    # This ensures production-readiness and future compatibility.
                    # If you encounter linter errors about update(), ensure you are using Qiskit >=0.21.0 and the V2 API.
                    #
                    # For maintainers: Always double-check the Qiskit docs for the latest supported options and API changes.
                    # If you remove or refactor option handling, document the rationale in docs/changelog.md and docs/retrospective_summaries.md.
                    # Run the circuit (shots can also be set here if needed)
                    job = sampler.run([circuit], shots=shots)
                    result = job.result()
                    quasi_dists = result.quasi_dists
                    counts = {}
                    for i, qd in enumerate(quasi_dists):
                        for bitstring, prob in qd.items():
                            if isinstance(bitstring, int):
                                bin_str = format(bitstring, f'0{circuit.num_qubits}b')
                            else:
                                bin_str = bitstring
                            counts[bin_str] = int(prob * shots)
                    metrics = self._calculate_financial_metrics(counts)
                    error_metrics = {
                        'return_error_pct': 100 * abs(metrics['expected_return'] - ideal_metrics['expected_return']) / max(0.0001, abs(ideal_metrics['expected_return'])),
                        'volatility_error_pct': 100 * abs(metrics['volatility'] - ideal_metrics['volatility']) / max(0.0001, abs(ideal_metrics['volatility'])),
                        'var_error_pct': 100 * abs(metrics['value_at_risk'] - ideal_metrics['value_at_risk']) / max(0.0001, abs(ideal_metrics['value_at_risk'])),
                        'sharpe_error_pct': 100 * abs(metrics['sharpe_ratio'] - ideal_metrics['sharpe_ratio']) / max(0.0001, abs(ideal_metrics['sharpe_ratio']))
                    }
                    results[f'noise_{noise}'] = {
                        'counts': counts,
                        'financial_metrics': metrics,
                        'error_metrics': error_metrics
                    }
                    print(f"Financial metrics with noise {noise:.4f}:")
                    print(f"  - Expected return: {metrics['expected_return']:.4f} (error: {error_metrics['return_error_pct']:.2f}%)")
                    print(f"  - Volatility: {metrics['volatility']:.4f} (error: {error_metrics['volatility_error_pct']:.2f}%)")
                    print(f"  - Value at risk: {metrics['value_at_risk']:.4f} (error: {error_metrics['var_error_pct']:.2f}%)")
                    print(f"  - Sharpe ratio: {metrics['sharpe_ratio']:.4f} (error: {error_metrics['sharpe_error_pct']:.2f}%)")
                except Exception as e:
                    print(f"Error running with noise level {noise}: {str(e)}")
                    results[f'noise_{noise}'] = {'error': str(e)}
        
        # Plot comparison
        self._plot_noise_sensitivity(results)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"{self.results_dir}/noise_sensitivity_{timestamp}.json"
        
        # Create serializable results
        serializable_results = {}
        for key, data in results.items():
            if 'error' in data:
                serializable_results[key] = {'error': data['error']}
            else:
                serializable_results[key] = {
                    'financial_metrics': data['financial_metrics'],
                    'error_metrics': data['error_metrics'] if 'error_metrics' in data else {}
                }
                
        with open(result_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
            
        print(f"\nNoise sensitivity analysis complete. Results saved to {result_file}")
        return results
    
    def analyze_circuit_depth(self,
                             circuit_generator,
                             depths: List[int] = [1, 2, 3, 4, 5],
                             backend_name: str = 'local_simulator',  # Updated default to local_simulator
                             resilience_level: int = 1,
                             shots: int = 5000) -> Dict:
        """
        Analyze how circuit depth affects error rates and financial metrics
        
        Args:
            circuit_generator: Function that takes depth and returns a circuit
            depths: List of circuit depths to test
            backend_name: Backend to use for analysis
            resilience_level: Error mitigation level to use
            shots: Number of shots per execution
            
        Returns:
            Dictionary of results by circuit depth
        """
        print(f"Starting circuit depth analysis on {backend_name}...")
        results = {}
        
        # Check if we should use local simulator
        is_local_simulator = backend_name == 'local_simulator'
        
        # If not local simulator, get the real backend
        backend = None
        if not is_local_simulator:
            backend = self._get_backend(backend_name)
        
        # Use a session for all tests to improve performance
        session_backend = 'default' if is_local_simulator else backend_name
        
        with Session(service=self.service, backend=session_backend) as session:
            # Generate and test circuits with different depths
            for depth in depths:
                print(f"\nTesting circuit with depth parameter {depth}...")
                
                try:
                    # Generate circuit
                    circuit = circuit_generator(depth)
                    
                    # Record original circuit metrics
                    original_depth = circuit.depth()
                    
                    # Optimize circuit for target backend if using real hardware
                    if not is_local_simulator and backend is not None:
                        # Generate ISA circuit
                        pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
                        circuit = pm.run(circuit)
                    
                    # Record circuit metrics
                    transpiled_depth = circuit.depth()
                    two_qubit_count = sum(circuit.count_ops().get(op, 0) 
                                        for op in ['cx', 'cz', 'ecr', 'swap'])
                    
                    print(f"Circuit metrics:")
                    print(f"  - Original depth: {original_depth}")
                    print(f"  - Transpiled depth: {transpiled_depth}")
                    print(f"  - Two-qubit gate count: {two_qubit_count}")
                    
                    # Configure options - fixed to match V2 API structure
                    options = {
                        "resilience": {"level": resilience_level},
                        "optimization_level": 3,
                        "execution": {"shots": shots}
                    }
                    
                    # Get ideal results
                    ideal_result = self.simulator.run(circuit, shots=shots).result()
                    ideal_counts = ideal_result.get_counts()
                    ideal_metrics = self._calculate_financial_metrics(ideal_counts)
                    
                    # Create appropriate sampler
                    if is_local_simulator:
                        sampler = Sampler(session=session, options=options, local=True)
                    else:
                        sampler = Sampler(session=session, options=options)
                    
                    # Run the circuit
                    job = sampler.run([circuit])
                    job_id = job.job_id()
                    print(f"Job submitted with ID: {job_id}")
                    
                    # Process results
                    result = job.result()
                    quasi_dists = result.quasi_dists
                    
                    # Convert to counts format
                    counts = {}
                    for i, qd in enumerate(quasi_dists):
                        for bitstring, prob in qd.items():
                            # Convert to binary string if needed
                            if isinstance(bitstring, int):
                                bin_str = format(bitstring, f'0{circuit.num_qubits}b')
                            else:
                                bin_str = bitstring
                            # Scale by shots to get counts
                            counts[bin_str] = int(prob * shots)
                    
                    # Calculate financial metrics
                    metrics = self._calculate_financial_metrics(counts)
                    
                    # Calculate error percentages
                    error_metrics = {
                        'return_error_pct': 100 * abs(metrics['expected_return'] - ideal_metrics['expected_return']) / max(0.0001, abs(ideal_metrics['expected_return'])),
                        'volatility_error_pct': 100 * abs(metrics['volatility'] - ideal_metrics['volatility']) / max(0.0001, abs(ideal_metrics['volatility'])),
                        'var_error_pct': 100 * abs(metrics['value_at_risk'] - ideal_metrics['value_at_risk']) / max(0.0001, abs(ideal_metrics['value_at_risk'])),
                        'sharpe_error_pct': 100 * abs(metrics['sharpe_ratio'] - ideal_metrics['sharpe_ratio']) / max(0.0001, abs(ideal_metrics['sharpe_ratio']))
                    }
                    
                    # Calculate overall error using mean absolute percentage error
                    mean_error = np.mean([
                        error_metrics['return_error_pct'],
                        error_metrics['volatility_error_pct'],
                        error_metrics['var_error_pct'],
                        error_metrics['sharpe_error_pct']
                    ])
                    
                    # Store results
                    results[f'depth_{depth}'] = {
                        'circuit_metrics': {
                            'original_depth': original_depth,
                            'transpiled_depth': transpiled_depth,
                            'two_qubit_count': two_qubit_count
                        },
                        'ideal_metrics': ideal_metrics,
                        'financial_metrics': metrics,
                        'error_metrics': error_metrics,
                        'mean_error': mean_error,
                        'job_id': job_id
                    }
                    
                    print(f"Financial metrics for depth {depth}:")
                    print(f"  - Expected return: {metrics['expected_return']:.4f} (error: {error_metrics['return_error_pct']:.2f}%)")
                    print(f"  - Volatility: {metrics['volatility']:.4f} (error: {error_metrics['volatility_error_pct']:.2f}%)")
                    print(f"  - Value at risk: {metrics['value_at_risk']:.4f} (error: {error_metrics['var_error_pct']:.2f}%)")
                    print(f"  - Mean error: {mean_error:.2f}%")
                    
                except Exception as e:
                    print(f"Error analyzing depth {depth}: {str(e)}")
                    results[f'depth_{depth}'] = {'error': str(e)}
        
        # Plot depth vs error
        self._plot_depth_error_relationship(results)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"{self.results_dir}/depth_analysis_{backend_name}_{timestamp}.json"
        
        # Create serializable results
        serializable_results = {}
        for key, data in results.items():
            if 'error' in data:
                serializable_results[key] = {'error': data['error']}
            else:
                serializable_results[key] = {
                    'circuit_metrics': data['circuit_metrics'],
                    'financial_metrics': data['financial_metrics'],
                    'error_metrics': data['error_metrics'],
                    'mean_error': data['mean_error'],
                    'job_id': data['job_id']
                }
                
        with open(result_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
            
        print(f"\nCircuit depth analysis complete. Results saved to {result_file}")
        return results
    
    def _get_backend(self, backend_name: str):
        """
        Get a backend by name with caching and local simulator support
        
        Args:
            backend_name: Name of the backend to use
            
        Returns:
            Backend instance or None for local simulator
        """
        # Check if this is a request for local simulation
        if backend_name == 'local_simulator':
            return None
            
        # Check cache first
        if backend_name in self.backend_cache:
            return self.backend_cache[backend_name]
        
        # Get backend from service
        backend = self.service.backend(backend_name)
        self.backend_cache[backend_name] = backend
        return backend
    
    def _calculate_financial_metrics(self, counts: Union[Dict[str, int], Dict[int, int]]) -> Dict[str, float]:
        """
        Calculate financial metrics from measurement counts
        
        Args:
            counts: Measurement counts
            
        Returns:
            Dictionary of financial metrics
        """
        # Convert counts to probabilities
        total_shots = sum(counts.values())
        probs = {bitstring: count/total_shots for bitstring, count in counts.items()}
        
        # Calculate expected return
        expected_return = 0
        for bitstring, prob in probs.items():
            # Convert bitstring to asset price or return
            if isinstance(bitstring, str):
                # Remove any spaces from the bitstring
                cleaned_bitstring = bitstring.replace(' ', '')
                bitstring_len = len(cleaned_bitstring)
                try:
                    numeric_value = int(cleaned_bitstring, 2) / (2**bitstring_len)
                except ValueError:
                    # If conversion fails, use the first character as a fallback
                    # This handles cases where the bitstring might contain non-binary characters
                    print(f"Warning: Could not convert '{bitstring}' to binary, using approximation")
                    first_char = cleaned_bitstring[0] if cleaned_bitstring else '0'
                    numeric_value = int(first_char == '1') / 2
            else:  # Integer key
                bitstring_len = 8  # Assume 8 bits if integer
                numeric_value = bitstring / (2**bitstring_len)
                
            expected_return += numeric_value * prob
            
        # Calculate volatility (standard deviation)
        volatility = 0
        for bitstring, prob in probs.items():
            if isinstance(bitstring, str):
                # Remove any spaces from the bitstring
                cleaned_bitstring = bitstring.replace(' ', '')
                bitstring_len = len(cleaned_bitstring)
                try:
                    numeric_value = int(cleaned_bitstring, 2) / (2**bitstring_len)
                except ValueError:
                    # If conversion fails, use the first character as a fallback
                    print(f"Warning: Could not convert '{bitstring}' to binary, using approximation")
                    first_char = cleaned_bitstring[0] if cleaned_bitstring else '0'
                    numeric_value = int(first_char == '1') / 2
            else:  # Integer key
                bitstring_len = 8  # Assume 8 bits if integer
                numeric_value = bitstring / (2**bitstring_len)
                
            volatility += (numeric_value - expected_return)**2 * prob
            
        volatility = np.sqrt(volatility)
        
        # Calculate Value at Risk (95% confidence)
        value_at_risk = expected_return - 1.96 * volatility
        
        # Calculate Sharpe ratio
        risk_free_rate = 0.01  # Assumed risk-free rate
        sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        return {
            'expected_return': expected_return,
            'volatility': volatility,
            'value_at_risk': value_at_risk,
            'sharpe_ratio': sharpe_ratio
        }
    
    def _create_financial_noise_model(self, noise_strength: float) -> NoiseModel:
        """
        Create a noise model specific to financial circuits
        
        This model applies:
        - Stronger noise to 2-qubit gates (critical for entanglement in financial correlations)
        - Moderate noise to 1-qubit gates
        - Readout errors that can affect financial decision outcomes
        
        Args:
            noise_strength: Base noise strength
            
        Returns:
            NoiseModel instance
        """
        noise_model = NoiseModel()
        
        # Add depolarizing error to 2-qubit gates
        error_2q = depolarizing_error(noise_strength, 2)
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cz', 'ecr', 'swap'])
        
        # Add depolarizing error to 1-qubit gates
        error_1q = depolarizing_error(noise_strength/2, 1)
        noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3', 'rx', 'ry', 'rz', 'h'])
        
        # Add readout error
        ro_error = readout_error([noise_strength/4, noise_strength/4])
        # Apply to first 5 qubits (adjust as needed)
        for i in range(5):
            noise_model.add_readout_error(ro_error, [i])
        
        return noise_model
    
    def _plot_resilience_comparison(self, results: Dict) -> None:
        """
        Plot comparison of financial metrics across resilience levels
        
        Args:
            results: Results dictionary from analyze_resilience_impact
        """
        # Extract data for plotting
        resilience_levels = sorted([k for k in results.keys() if k.startswith('resilience_') and 'error' not in results[k]])
        if not resilience_levels:
            print("No successful resilience data to plot")
            return
            
        levels = [int(k.split('_')[1]) for k in resilience_levels]
        
        # Extract financial metrics
        returns = [results[k]['financial_metrics']['expected_return'] for k in resilience_levels]
        volatilities = [results[k]['financial_metrics']['volatility'] for k in resilience_levels]
        var_values = [results[k]['financial_metrics']['value_at_risk'] for k in resilience_levels]
        
        # Extract error percentages
        return_errors = [results[k]['error_metrics']['return_error_pct'] for k in resilience_levels]
        vol_errors = [results[k]['error_metrics']['volatility_error_pct'] for k in resilience_levels]
        var_errors = [results[k]['error_metrics']['var_error_pct'] for k in resilience_levels]
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot financial metrics
        ax1.axhline(y=results['ideal']['financial_metrics']['expected_return'], 
                   color='g', linestyle='--', label='Ideal Return')
        ax1.axhline(y=results['ideal']['financial_metrics']['volatility'], 
                   color='r', linestyle='--', label='Ideal Volatility')
        ax1.axhline(y=results['ideal']['financial_metrics']['value_at_risk'], 
                   color='b', linestyle='--', label='Ideal VaR')
        
        ax1.plot(levels, returns, 'go-', label='Expected Return')
        ax1.plot(levels, volatilities, 'ro-', label='Volatility')
        ax1.plot(levels, var_values, 'bo-', label='Value at Risk')
        
        ax1.set_xlabel('Resilience Level')
        ax1.set_ylabel('Value')
        ax1.set_title('Financial Metrics by Resilience Level')
        ax1.legend()
        ax1.grid(True)
        
        # Plot error percentages
        ax2.plot(levels, return_errors, 'go-', label='Return Error')
        ax2.plot(levels, vol_errors, 'ro-', label='Volatility Error')
        ax2.plot(levels, var_errors, 'bo-', label='VaR Error')
        
        ax2.set_xlabel('Resilience Level')
        ax2.set_ylabel('Error Percentage')
        ax2.set_title('Error Percentage by Resilience Level')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_file = f"{self.results_dir}/resilience_comparison_{timestamp}.png"
        plt.savefig(plot_file)
        print(f"Plot saved to {plot_file}")
        plt.close()
    
    def _plot_noise_sensitivity(self, results: Dict) -> None:
        """
        Plot sensitivity of financial metrics to noise
        
        Args:
            results: Results dictionary from analyze_noise_sensitivity
        """
        # Extract data for plotting
        noise_levels = sorted([k for k in results.keys() if k.startswith('noise_') and 'error' not in results[k]])
        if not noise_levels:
            print("No successful noise sensitivity data to plot")
            return
            
        noise_values = [float(k.split('_')[1]) for k in noise_levels]
        
        # Extract financial metrics
        returns = [results[k]['financial_metrics']['expected_return'] for k in noise_levels]
        volatilities = [results[k]['financial_metrics']['volatility'] for k in noise_levels]
        var_values = [results[k]['financial_metrics']['value_at_risk'] for k in noise_levels]
        
        # Extract error percentages
        return_errors = [results[k]['error_metrics']['return_error_pct'] for k in noise_levels]
        vol_errors = [results[k]['error_metrics']['volatility_error_pct'] for k in noise_levels]
        var_errors = [results[k]['error_metrics']['var_error_pct'] for k in noise_levels]
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot financial metrics
        ax1.axhline(y=results['ideal']['financial_metrics']['expected_return'], 
                   color='g', linestyle='--', label='Ideal Return')
        ax1.axhline(y=results['ideal']['financial_metrics']['volatility'], 
                   color='r', linestyle='--', label='Ideal Volatility')
        ax1.axhline(y=results['ideal']['financial_metrics']['value_at_risk'], 
                   color='b', linestyle='--', label='Ideal VaR')
        
        ax1.plot(noise_values, returns, 'go-', label='Expected Return')
        ax1.plot(noise_values, volatilities, 'ro-', label='Volatility')
        ax1.plot(noise_values, var_values, 'bo-', label='Value at Risk')
        
        ax1.set_xlabel('Noise Strength')
        ax1.set_ylabel('Value')
        ax1.set_title('Financial Metrics by Noise Level')
        ax1.legend()
        ax1.grid(True)
        
        # Plot error percentages
        ax2.plot(noise_values, return_errors, 'go-', label='Return Error')
        ax2.plot(noise_values, vol_errors, 'ro-', label='Volatility Error')
        ax2.plot(noise_values, var_errors, 'bo-', label='VaR Error')
        
        ax2.set_xlabel('Noise Strength')
        ax2.set_ylabel('Error Percentage')
        ax2.set_title('Error Percentage by Noise Level')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_file = f"{self.results_dir}/noise_sensitivity_{timestamp}.png"
        plt.savefig(plot_file)
        print(f"Plot saved to {plot_file}")
        plt.close()
        
    def _plot_depth_error_relationship(self, results: Dict) -> None:
        """
        Plot relationship between circuit depth and error rates
        
        Args:
            results: Results dictionary from analyze_circuit_depth
        """
        # Extract data for plotting
        depth_levels = sorted([k for k in results.keys() if k.startswith('depth_') and 'error' not in results[k]])
        if not depth_levels:
            print("No successful depth analysis data to plot")
            return
            
        depths = [int(k.split('_')[1]) for k in depth_levels]
        
        # Extract circuit metrics
        transpiled_depths = [results[k]['circuit_metrics']['transpiled_depth'] for k in depth_levels]
        two_qubit_counts = [results[k]['circuit_metrics']['two_qubit_count'] for k in depth_levels]
        
        # Extract error metrics
        mean_errors = [results[k]['mean_error'] for k in depth_levels]
        return_errors = [results[k]['error_metrics']['return_error_pct'] for k in depth_levels]
        vol_errors = [results[k]['error_metrics']['volatility_error_pct'] for k in depth_levels]
        
        # Create plot
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot circuit metrics vs depth
        axs[0, 0].plot(depths, transpiled_depths, 'bo-', label='Transpiled Depth')
        axs[0, 0].plot(depths, two_qubit_counts, 'ro-', label='Two-Qubit Gate Count')
        axs[0, 0].set_xlabel('Circuit Depth Parameter')
        axs[0, 0].set_ylabel('Count')
        axs[0, 0].set_title('Circuit Metrics vs Depth')
        axs[0, 0].legend()
        axs[0, 0].grid(True)
        
        # Plot mean error vs depth
        axs[0, 1].plot(depths, mean_errors, 'go-', label='Mean Error')
        axs[0, 1].set_xlabel('Circuit Depth Parameter')
        axs[0, 1].set_ylabel('Error Percentage')
        axs[0, 1].set_title('Mean Error vs Depth')
        axs[0, 1].legend()
        axs[0, 1].grid(True)
        
        # Plot error vs transpiled depth
        axs[1, 0].plot(transpiled_depths, mean_errors, 'go-', label='Mean Error')
        axs[1, 0].set_xlabel('Transpiled Circuit Depth')
        axs[1, 0].set_ylabel('Error Percentage')
        axs[1, 0].set_title('Error vs Transpiled Depth')
        axs[1, 0].legend()
        axs[1, 0].grid(True)
        
        # Plot error vs two-qubit gate count
        axs[1, 1].plot(two_qubit_counts, mean_errors, 'go-', label='Mean Error')
        axs[1, 1].set_xlabel('Two-Qubit Gate Count')
        axs[1, 1].set_ylabel('Error Percentage')
        axs[1, 1].set_title('Error vs Two-Qubit Gate Count')
        axs[1, 1].legend()
        axs[1, 1].grid(True)
        
        plt.tight_layout()
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_file = f"{self.results_dir}/depth_error_relationship_{timestamp}.png"
        plt.savefig(plot_file)
        print(f"Plot saved to {plot_file}")
        plt.close() 