"""
Advanced Error Mitigation Techniques Module (Refactored)

This module now primarily acts as an interface, importing and 
re-exporting functionalities from the `techniques` and `utils` submodules.
The main class `AdvancedErrorMitigation` has been decomposed.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Union, Callable, Tuple, Any, Mapping
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Instruction, Gate
from qiskit.circuit.library import CXGate, XGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import Options
import json
import os
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor

# Import the refactored utility functions
from .utils import (
    calculate_distribution_fidelity,
    get_ideal_counts,
    get_ideal_expectation
)

# Import technique-specific functionalities (will be done as they are refactored)
from .techniques.zne import apply_zne
from .techniques.readout import apply_readout_mitigation
from .techniques.pec import apply_pec
from .techniques.dd import apply_dynamical_decoupling


class AdvancedErrorMitigation:
    """Implements advanced error mitigation techniques for quantum circuits."""
    
    def __init__(self, 
                 service: Optional[QiskitRuntimeService] = None,
                 results_dir: str = './error_mitigation_results',
                 max_session_time: int = 1800):
        """
        Initialize the advanced error mitigation module.
        
        Args:
            service: QiskitRuntimeService instance (created if None)
            results_dir: Directory to store mitigation results
            max_session_time: Maximum session time in seconds (default: 30 minutes)
        """
        self.service = service if service else QiskitRuntimeService()
        self.results_dir = results_dir
        self.max_session_time = max_session_time
        
        # Create results directory if it doesn't exist
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        # Initialize simulator
        self.simulator = AerSimulator()

    def benchmark_error_mitigation_techniques(self,
                                             circuit: QuantumCircuit,
                                             backend_name: str,
                                             observable: Optional[Any] = None,
                                             shots: int = 5000,
                                             use_threading: bool = True) -> Dict:
        """
        Benchmark and compare different error mitigation techniques.
        
        Args:
            circuit: Quantum circuit to evaluate
            backend_name: Backend to run on
            observable: Observable to measure (required for expectation values)
            shots: Number of shots per circuit execution
            use_threading: Whether to run techniques in parallel using threads
            
        Returns:
            Dictionary with combined benchmark results
        """
        print(f"\nBenchmarking error mitigation techniques on {backend_name}...")
        
        benchmark_results = {}
        
        # Check if we should use local simulator
        is_local_simulator = backend_name == 'local_simulator'
        
        # Get the backend
        backend = None
        if not is_local_simulator:
            try:
                backend = self.service.backend(backend_name)
                print(f"Using backend: {backend.name}")
            except Exception as e:
                print(f"Error getting backend: {str(e)}")
                print("Falling back to local simulator...")
                is_local_simulator = True
                
        # Define the backend for the session
        session_backend = self.simulator if is_local_simulator else backend
        
        # Define worker functions for each mitigation technique
        def run_zne(estimator, circuit, observable, tag):
            print(f"Starting ZNE with tag: {tag}")
            try:
                # Call the imported apply_zne function with correct arguments
                # Note: apply_zne handles primitive creation internally, so we don't pass the estimator.
                # We need service, simulator, backend_name, results_dir from the class/method scope.
                # Using self.service, self.simulator, self.results_dir and method's backend_name
                # estimator.options.environment.job_tags = [tag, "zne"] # Tagging should be handled inside apply_zne if needed
                zne_results = apply_zne(
                    # estimator=estimator, # Removed: apply_zne creates its own primitive
                    circuit=circuit,
                    observable=observable,
                    shots=shots,
                    backend_name=backend_name, # Pass backend_name
                    service=self.service,      # Pass service instance from class
                    simulator=self.simulator,  # Pass simulator instance from class
                    results_dir=self.results_dir # Pass results_dir from class
                    # noise_scaling_factors and extrapolation_method use defaults in apply_zne
                )
                print(f"Finished ZNE with tag: {tag}")
                # Ensure the returned dict has a 'method' key for consistency if possible
                if isinstance(zne_results, dict) and 'method' not in zne_results:
                    zne_results['method'] = 'zne'
                return zne_results
            except Exception as e:
                print(f"Error in ZNE ({tag}): {e}")
                return {"method": "zne", "error": str(e)}
        
        def run_readout(sampler, circuit, tag):
            print(f"Starting readout mitigation with tag: {tag}")
            try:
                # Call the imported apply_readout_mitigation function with correct arguments
                # Note: apply_readout_mitigation handles primitive creation internally.
                # We need backend_name, service, simulator, results_dir.
                # sampler.options.environment.job_tags = [tag, "readout"] # Tagging should be handled inside apply_readout_mitigation
                readout_results = apply_readout_mitigation(
                    # sampler=sampler, # Removed
                    circuit=circuit,
                    # num_qubits=circuit.num_qubits, # Removed: function can get this from circuit
                    shots=shots,
                    backend_name=backend_name,    # Pass backend_name
                    service=self.service,         # Pass service instance
                    simulator=self.simulator,     # Pass simulator instance
                    results_dir=self.results_dir  # Pass results_dir
                    # method uses default in apply_readout_mitigation
                )
                print(f"Finished readout mitigation with tag: {tag}")
                 # Ensure the returned dict has a 'method' key for consistency if possible
                if isinstance(readout_results, dict) and 'method' not in readout_results:
                    readout_results['method'] = 'readout'
                return readout_results
            except Exception as e:
                print(f"Error in Readout Mitigation ({tag}): {e}")
                return {"method": "readout", "error": str(e)}
        
        def run_pec(estimator, circuit, observable, tag):
            print(f"Starting PEC with tag: {tag}")
            try:
                # Call the imported apply_pec function with correct arguments
                # Note: apply_pec handles primitive creation internally.
                # We need backend_name, service, simulator, results_dir.
                # estimator.options.environment.job_tags = [tag, "pec"] # Tagging should be handled inside apply_pec
                pec_results = apply_pec(
                    # estimator=estimator, # Removed
                    circuit=circuit,
                    observable=observable,
                    shots=shots,
                    backend_name=backend_name,    # Pass backend_name
                    service=self.service,         # Pass service instance
                    simulator=self.simulator,     # Pass simulator instance
                    results_dir=self.results_dir  # Pass results_dir
                    # noise_amplification_factor uses default in apply_pec
                )
                print(f"Finished PEC with tag: {tag}")
                 # Ensure the returned dict has a 'method' key for consistency if possible
                if isinstance(pec_results, dict) and 'method' not in pec_results:
                    pec_results['method'] = 'pec'
                return pec_results
            except Exception as e:
                print(f"Error in PEC ({tag}): {e}")
                return {"method": "pec", "error": str(e)}
        
        def run_dd(primitive, circuit, tag):
            print(f"Starting DD benchmark ({tag})...")
            try:
                # Call the imported function directly
                dd_result = apply_dynamical_decoupling(
                    circuit=circuit,
                    backend_name=backend_name, # Pass backend name
                    shots=shots,
                    sequence_type='XX' # Example sequence
                )
                print(f"Finished DD benchmark ({tag}).")
                return tag, dd_result
            except Exception as e:
                print(f"Error in DD benchmark ({tag}): {e}")
                return tag, {"error": str(e)}

        # Execute all mitigation techniques in a single session
        with Session(backend=session_backend, max_time=self.max_session_time) as session:
            # Define options as a dictionary
            options_dict = {
                "resilience_level": 0,  # Use the key directly for resilience
                "execution": {"shots": shots} # Nest shots under execution
            }
            
            # Create primitives with proper session mode, passing the dictionary
            estimator = Estimator(mode=session, options=options_dict)
            sampler = Sampler(mode=session, options=options_dict)
            
            # Generate unique timestamp for this benchmark
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if observable is None and not is_local_simulator:
                print("Warning: Observable is required for expectation-based techniques. " +
                      "Only readout mitigation will be performed.")
            
            if use_threading and observable is not None:
                # Use threading to run all techniques concurrently
                with ThreadPoolExecutor(max_workers=3) as executor:
                    futures = {}
                    
                    # Submit ZNE task
                    zne_future = executor.submit(
                        run_zne, None, circuit, observable, f"zne_{timestamp}" # Pass None for estimator arg
                    )
                    futures['zne'] = zne_future
                    
                    # Submit readout task
                    readout_future = executor.submit(
                        run_readout, None, circuit, f"readout_{timestamp}" # Pass None for sampler arg
                    )
                    futures['readout'] = readout_future
                    
                    # Submit PEC task
                    pec_future = executor.submit(
                        run_pec, None, circuit, observable, f"pec_{timestamp}" # Pass None for estimator arg
                    )
                    futures['pec'] = pec_future
                    
                    # Submit DD task
                    dd_future = executor.submit(run_dd, sampler, circuit, f"dd_{timestamp}")
                    futures['dd'] = dd_future
                    
                    # Collect results
                    for name, future in futures.items():
                        try:
                            benchmark_results[name] = future.result()
                        except Exception as e:
                            print(f"Error in {name}: {str(e)}")
                            benchmark_results[name] = {'error': str(e)}
            else:
                # Run sequentially
                try:
                    if observable is not None:
                        benchmark_results['zne'] = run_zne(
                            None, circuit, observable, f"zne_{timestamp}" # Pass None for estimator arg
                        )
                        benchmark_results['pec'] = run_pec(
                            None, circuit, observable, f"pec_{timestamp}" # Pass None for estimator arg
                        )
                    
                    benchmark_results['readout'] = run_readout(
                        None, circuit, f"readout_{timestamp}" # Pass None for sampler arg
                    )
                    
                    benchmark_results['dd'] = run_dd(sampler, circuit, f"dd_{timestamp}") # Keep sampler for DD call for now
                except Exception as e:
                    print(f"Error during sequential execution: {str(e)}")
                    benchmark_results['error'] = str(e)
            
            # Combine and save results
            result_file = f"{self.results_dir}/benchmark_{backend_name}_{timestamp}.json"
            
            # Make results JSON serializable
            serializable_results = {}
            for technique, result in benchmark_results.items():
                serializable_results[technique] = {}
                for k, v in result.items():
                    if isinstance(v, np.ndarray):
                        serializable_results[technique][k] = v.tolist()
                    elif isinstance(v, dict):
                        serializable_results[technique][k] = {str(sk): sv for sk, sv in v.items()}
                    else:
                        serializable_results[technique][k] = v
                        
            with open(result_file, 'w') as f:
                json.dump(serializable_results, f, indent=2)
                
            print(f"\nBenchmark complete. Results saved to {result_file}")
            
            # Compare techniques when possible
            if observable is not None and 'zne' in benchmark_results and 'pec' in benchmark_results:
                self._plot_mitigation_comparison(benchmark_results, observable)
                
        return benchmark_results
    
    def _plot_mitigation_comparison(self, benchmark_results: Dict, observable: Any):
        """
        Create a comparison plot of different error mitigation techniques.
        
        Args:
            benchmark_results: Dictionary with benchmark results
            observable: Observable that was measured
        """
        plt.figure(figsize=(10, 6))
        
        # Extract values
        techniques = []
        values = []
        errors = []
        
        if 'zne' in benchmark_results and 'extrapolated_value' in benchmark_results['zne']:
            techniques.append('ZNE')
            values.append(benchmark_results['zne']['extrapolated_value'])
            errors.append(benchmark_results['zne']['extrapolation_error'])
            
            # Also show unmitigated value
            if 'measured_values' in benchmark_results['zne']:
                techniques.append('Unmitigated')
                # Convert to regular float to avoid type issues
                measured_value = float(benchmark_results['zne']['measured_values'][1.0])
                variance_value = float(benchmark_results['zne']['measured_variances'][1.0])
                values.append(measured_value)
                errors.append(np.sqrt(variance_value))
        
        if 'pec' in benchmark_results and 'mitigated_expectation' in benchmark_results['pec']:
            techniques.append('PEC')
            values.append(benchmark_results['pec']['mitigated_expectation'])
            # Use estimated error (would be more complex in real implementation)
            errors.append(abs(benchmark_results['pec']['mitigated_expectation'] * 0.1))
        
        # Plot results
        if techniques:
            x_pos = np.arange(len(techniques))
            
            plt.bar(x_pos, values, yerr=errors, align='center', alpha=0.7, capsize=10)
            plt.xticks(x_pos, techniques)
            plt.ylabel('Expectation Value')
            plt.title('Comparison of Error Mitigation Techniques')
            plt.grid(alpha=0.3)
            
            # Save the figure
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            fig_path = f"{self.results_dir}/comparison_{timestamp}.png"
            plt.savefig(fig_path, dpi=300, bbox_inches='tight')
            print(f"Comparison plot saved to {fig_path}")
            
            plt.close()