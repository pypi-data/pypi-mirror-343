"""Functions for Probabilistic Error Cancellation (PEC)."""

# Note: The current implementation is highly simplified and placeholder.
# Real PEC requires learning noise models and quasi-probability sampling.

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel # Needed for _create_depolarizing_noise_model
from typing import List, Dict, Tuple, Any, Optional, Union
import json
import os
from datetime import datetime

# Import necessary utilities
# NOTE: Changed from absolute 'quantum.error_correction.utils' to relative
from ..utils import (\
    extract_v2_counts,\
    calculate_distribution_fidelity,\
    get_ideal_counts,\
    get_ideal_expectation\
)
# Import the general serializer from readout (could be moved to utils)
from .readout import _serialize_dict 


def apply_pec(
    circuit: QuantumCircuit,
    backend_name: str,
    service: Optional[QiskitRuntimeService] = None,
    simulator: Optional[AerSimulator] = None,
    results_dir: str = './error_mitigation_results',
    shots: int = 5000,
    noise_amplification_factor: float = 1.0, # Currently unused placeholder
    observable: Optional[Any] = None
) -> Dict:
    """
    Apply Probabilistic Error Cancellation (PEC) to mitigate errors.
    (Currently a simplified placeholder implementation)
    
    Args:
        circuit: Quantum circuit to apply PEC to
        backend_name: Backend name (used to potentially fetch noise model)
        service: Optional QiskitRuntimeService instance.
        simulator: Optional AerSimulator instance for local simulation.
        results_dir: Directory to save results.
        shots: Number of shots per circuit execution
        noise_amplification_factor: Factor for noise inversion (placeholder)
        observable: Observable to measure (for Estimator) or None for Sampler
        
    Returns:
        Dictionary with PEC results (comparison of raw vs. basic mitigated vs. ideal)
    """
    print("\nApplying Probabilistic Error Cancellation (PEC)... [Simplified Version]")
    
    if service is None:
        service = QiskitRuntimeService()
    if simulator is None:
        simulator = AerSimulator()

    results = {}
    original_counts = None
    original_expectation = None
    mitigated_counts = None
    mitigated_expectation = None
    ideal_counts = None
    ideal_expectation = None
    
    # Determine if running locally or on IBM backend
    is_local_simulator = backend_name == 'local_simulator'
    
    # Get backend instance or fallback to local simulator
    backend = None
    if not is_local_simulator:
        try:
            backend = service.backend(backend_name)
        except Exception as e:
            print(f"Error getting backend: {str(e)}")
            print("Falling back to local simulator...")
            is_local_simulator = True
            
    # Define backend for the session context
    session_backend = simulator if is_local_simulator else backend
    
    try:
        with Session(backend=session_backend) as session:
            # Instantiate the appropriate V2 primitive
            runtime_params = {"shots": shots}
            if observable is None:
                primitive = Sampler(mode=session)
            else:
                primitive = Estimator(mode=session)
                
            # --- Run Original Circuit (Noisy) ---
            print("Running original circuit (noisy)...")
            try:
                if observable is None:
                    job = primitive.run([circuit], **runtime_params)
                    result = job.result()
                    if result:
                        pub_result = result[0]
                        original_counts = extract_v2_counts(pub_result, circuit.num_clbits)
                    else:
                        print("Warning: No result returned for original circuit (Sampler).")
                else:
                    pubs = [(circuit, observable)]
                    job = primitive.run(pubs, **runtime_params)
                    result = job.result()
                    if result and len(result) > 0:
                         pub_result = result[0]
                         original_expectation = pub_result.data.values[0]
                    else:
                        print("Warning: No result returned for original circuit (Estimator).")
            except Exception as e:
                print(f"Error running original circuit: {str(e)}")
                # Continue if possible, results dict will reflect missing data

            # --- Apply Basic PEC Mitigation ---
            # This is a placeholder/simplified version.
            print("Applying simplified PEC correction...")
            if original_counts is not None:
                try:
                    mitigated_counts = _apply_basic_pec_to_counts(original_counts)
                except Exception as e:
                    print(f"Error applying basic PEC correction to counts: {str(e)}")
                    mitigated_counts = None
            elif original_expectation is not None:
                 # Placeholder adjustment for expectation values
                 mitigated_expectation = original_expectation * 1.1 # Example adjustment
                 print("Note: Applied placeholder adjustment for PEC on expectation value.")

            # --- Get Ideal Results (Simulation) ---
            print("Running ideal simulation...")
            try:
                 if observable is None:
                      ideal_counts = get_ideal_counts(circuit, shots)
                 else:
                      ideal_expectation = get_ideal_expectation(circuit, observable)
            except Exception as e:
                 print(f"Error running ideal simulation: {str(e)}")
                 ideal_counts = None
                 ideal_expectation = None

    except Exception as main_error:
        print(f"PEC execution failed: {main_error}")
        results['error'] = str(main_error)

    # --- Store results --- 
    results.update({
        'original_counts': original_counts,
        'mitigated_counts': mitigated_counts,
        'ideal_counts': ideal_counts,
        'original_expectation': original_expectation,
        'mitigated_expectation': mitigated_expectation,
        'ideal_expectation': ideal_expectation,
        'noise_amplification_factor': noise_amplification_factor 
    })
    
    # --- Calculate Metrics --- 
    if original_counts and ideal_counts and mitigated_counts:
        try:
            results['original_fidelity'] = calculate_distribution_fidelity(original_counts, ideal_counts)
            results['mitigated_fidelity'] = calculate_distribution_fidelity(mitigated_counts, ideal_counts)
            results['fidelity_improvement'] = results['mitigated_fidelity'] - results['original_fidelity']
        except Exception as e:
            print(f"Error calculating PEC fidelity: {e}")
    
    if original_expectation is not None and ideal_expectation is not None and mitigated_expectation is not None and not np.isnan(ideal_expectation):
        try:
            results['original_error_magnitude'] = abs(original_expectation - ideal_expectation)
            results['mitigated_error_magnitude'] = abs(mitigated_expectation - ideal_expectation)
            results['error_reduction'] = results['original_error_magnitude'] - results['mitigated_error_magnitude']
        except Exception as e:
             print(f"Error calculating PEC error reduction: {e}")

    # --- Create visualization --- 
    try:
        if observable is None:
            _plot_pec_comparison(original_counts, mitigated_counts, ideal_counts, results_dir)
        else:
             _plot_pec_expectation_comparison(original_expectation, mitigated_expectation, ideal_expectation, results_dir)
    except Exception as plot_err:
         print(f"Error generating PEC plot: {plot_err}")
    
    # --- Save results --- 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"pec_results_{backend_name}_{timestamp}.json")
    
    serializable_results = _serialize_dict(results)
    
    try:
        os.makedirs(results_dir, exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        print(f"Probabilistic Error Cancellation complete. Results saved to {results_file}")
        if results.get('fidelity_improvement') is not None:
            print(f"Fidelity improvement: {results['fidelity_improvement']:.4f}")
        if results.get('error_reduction') is not None:
            print(f"Error reduction: {results['error_reduction']:.6f}")
    except Exception as save_err:
        print(f"Error saving PEC results: {save_err}")
            
    return results

def _create_depolarizing_noise_model(
    num_qubits: int, 
    depolarizing_error: float = 0.01,
    readout_error: float = 0.02
) -> NoiseModel:
    """
    Create a simple depolarizing noise model for simulation.
    (Internal helper function for PEC demonstration/testing)
    
    Args:
        num_qubits: Number of qubits
        depolarizing_error: Depolarizing error rate for gates
        readout_error: Readout error rate
        
    Returns:
        NoiseModel object
    """
    # Corrected import for Qiskit Aer noise functions
    from qiskit_aer.noise import depolarizing_error as create_depolarizing_error
    from qiskit_aer.noise import ReadoutError # Use class name
    
    noise_model = NoiseModel()
    
    # Add depolarizing error to all single-qubit gates
    error_1q = create_depolarizing_error(depolarizing_error, 1)
    noise_model.add_all_qubit_quantum_error(error_1q, ['x', 'y', 'z', 'h', 'rx', 'ry', 'rz'])
    
    # Add depolarizing error to all two-qubit gates
    error_2q = create_depolarizing_error(depolarizing_error * 2, 2)
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cz', 'swap'])
    
    # Add readout error
    for qubit in range(num_qubits):
        p_error = readout_error
        # Use the ReadoutError class directly
        error = ReadoutError([[1-p_error, p_error], [p_error, 1-p_error]])
        noise_model.add_readout_error(error, [qubit])
    
    return noise_model

def _apply_basic_pec_to_counts(counts: Dict[str, int]) -> Dict[str, float]:
    """
    Apply a simplified PEC algorithm to measurement counts.
    (Internal helper function for PEC)
    
    Args:
        counts: Raw measurement counts
        
    Returns:
        Mitigated counts (float values)
    """
    total_shots = sum(counts.values())
    if total_shots == 0: return {}

    mitigated_counts = {}
    
    # Apply a simple bias correction (heuristic)
    for bitstring, count in counts.items():
        prob = count / total_shots
        num_ones = bitstring.count('1')
        num_zeros = len(bitstring) - num_ones
        
        p_0_to_1 = 0.05  # Heuristic
        p_1_to_0 = 0.07  # Heuristic
        
        # Basic correction logic (placeholder)
        corrected_prob = prob
        corrected_prob += num_zeros * p_0_to_1 * (1 - prob)
        corrected_prob += num_ones * p_1_to_0 * (1 - prob)  
        
        mitigated_counts[bitstring] = corrected_prob * total_shots
    
    # Normalize results (optional but often desired)
    corrected_total = sum(mitigated_counts.values())
    if corrected_total > 0:
         for bs in mitigated_counts:
             mitigated_counts[bs] *= (total_shots / corrected_total)
             
    return mitigated_counts

def _plot_pec_comparison(
    original_counts: Optional[Dict[str, int]], 
    mitigated_counts: Optional[Dict[str, float]], 
    ideal_counts: Optional[Dict[str, int]],
    results_dir: str = '.'
):
    """
    Create a bar chart comparing original, mitigated, and ideal counts for PEC.
    (Internal helper function for PEC)
    
    Args:
        original_counts: Original circuit counts (Optional)
        mitigated_counts: Counts after PEC mitigation (Optional)
        ideal_counts: Ideal (noiseless) counts (Optional)
        results_dir: Directory to save the plot.
    """
    if original_counts is None or mitigated_counts is None or ideal_counts is None:
        print("Skipping PEC comparison plot due to missing counts data.")
        return

    # Corrected set union using set.union()
    all_bitstrings = sorted(list(set(original_counts.keys()).union(set(mitigated_counts.keys())).union(set(ideal_counts.keys()))))
    
    orig_total = sum(original_counts.values())
    mitigated_total = sum(mitigated_counts.values())
    ideal_total = sum(ideal_counts.values())
    
    orig_probs = [original_counts.get(bs, 0) / orig_total if orig_total > 0 else 0 for bs in all_bitstrings]
    mitigated_probs = [mitigated_counts.get(bs, 0) / mitigated_total if mitigated_total > 0 else 0 for bs in all_bitstrings]
    ideal_probs = [ideal_counts.get(bs, 0) / ideal_total if ideal_total > 0 else 0 for bs in all_bitstrings]
    
    plt.figure(figsize=(12, 6))
    x = np.arange(len(all_bitstrings))
    width = 0.25
    
    plt.bar(x - width, orig_probs, width, label='Original', color='blue', alpha=0.6)
    plt.bar(x, mitigated_probs, width, label='PEC Mitigated', color='green', alpha=0.6)
    plt.bar(x + width, ideal_probs, width, label='Ideal', color='red', alpha=0.6)
    
    plt.xlabel('Bitstring')
    plt.ylabel('Probability')
    plt.title('Probabilistic Error Cancellation Results')
    plt.xticks(x, all_bitstrings, rotation=70, fontsize=8)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Calculate fidelities
    try:
        orig_fidelity = calculate_distribution_fidelity(original_counts, ideal_counts)
        mitigated_fidelity = calculate_distribution_fidelity(mitigated_counts, ideal_counts)
        improvement = mitigated_fidelity - orig_fidelity
        
        plt.figtext(0.5, 0.01, 
                  f"Original Fidelity: {orig_fidelity:.4f}, Mitigated Fidelity: {mitigated_fidelity:.4f}, Improvement: {improvement:.4f}", 
                  ha="center", fontsize=10)
    except Exception as e:
        print(f"Could not calculate fidelity for PEC plot: {e}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_path = os.path.join(results_dir, f"pec_comparison_{timestamp}.png")
    try:
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {fig_path}")
    except Exception as save_err:
        print(f"Error saving PEC comparison plot: {save_err}")
    finally:
        plt.close()

def _plot_pec_expectation_comparison(
    original_expectation: Optional[float], 
    mitigated_expectation: Optional[float], 
    ideal_expectation: Optional[float],
    results_dir: str = '.'
):
    """
    Create a bar chart comparing original, mitigated, and ideal expectation values for PEC.
    (Internal helper function for PEC)
    
    Args:
        original_expectation: Original expectation value (Optional)
        mitigated_expectation: Expectation after PEC mitigation (Optional)
        ideal_expectation: Ideal (noiseless) expectation (Optional)
        results_dir: Directory to save the plot.
    """
    if original_expectation is None or mitigated_expectation is None or ideal_expectation is None or np.isnan(ideal_expectation):
        print("Skipping PEC expectation comparison plot due to missing or invalid values.")
        return
            
    plt.figure(figsize=(8, 6))
    x = np.arange(3)
    labels = ['Original', 'PEC Mitigated', 'Ideal']
    values = [original_expectation, mitigated_expectation, ideal_expectation]
    colors = ['blue', 'green', 'red']
    
    plt.bar(x, values, color=colors, alpha=0.7)
    # Ensure ideal_expectation is float before passing to axhline
    plt.axhline(y=float(ideal_expectation), color='r', linestyle='--', alpha=0.5)
    
    try:
        orig_error = abs(original_expectation - ideal_expectation)
        mitigated_error = abs(mitigated_expectation - ideal_expectation)
        improvement = orig_error - mitigated_error
        
        plt.figtext(0.5, 0.01, 
                  f"Original Error: {orig_error:.4f}, Mitigated Error: {mitigated_error:.4f}, Improvement: {improvement:.4f}", 
                  ha="center", fontsize=10)
    except Exception as e:
        print(f"Could not calculate error metrics for PEC plot: {e}")
    
    plt.xlabel('Method')
    plt.ylabel('Expectation Value')
    plt.title('Probabilistic Error Cancellation - Expectation Values')
    plt.xticks(x, labels)
    plt.grid(True, alpha=0.3)
    
    for i, v in enumerate(values):
        plt.text(i, v + 0.01, f"{v:.4f}", ha='center')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_path = os.path.join(results_dir, f"pec_expectation_{timestamp}.png")
    try:
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {fig_path}")
    except Exception as save_err:
        print(f"Error saving PEC expectation plot: {save_err}")
    finally:
        plt.close()
