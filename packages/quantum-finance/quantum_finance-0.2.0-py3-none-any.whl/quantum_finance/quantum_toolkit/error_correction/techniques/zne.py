"""Functions for Zero Noise Extrapolation (ZNE)."""

# Imports will be added here as functions are moved
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_aer import AerSimulator
from typing import List, Dict, Tuple, Any, Optional
import json
import os
from datetime import datetime

# Import necessary utilities
# Try relative import for module structure
from ..utils import extract_v2_counts


def apply_zne( 
    circuit: QuantumCircuit,
    backend_name: str,
    service: Optional[QiskitRuntimeService] = None, # Added service
    simulator: Optional[AerSimulator] = None, # Added simulator
    results_dir: str = './error_mitigation_results', # Added results_dir
    noise_scaling_factors: List[float] = [1.0, 2.0, 3.0],
    extrapolation_method: str = 'linear',
    shots: int = 5000,
    observable: Optional[Any] = None
) -> Dict:
    """
    Apply Zero Noise Extrapolation (ZNE) to mitigate errors.
    
    ZNE works by deliberately introducing additional noise through circuit 
    folding, then extrapolating back to the zero-noise limit.
    
    Args:
        circuit: Quantum circuit to apply ZNE to
        backend_name: Backend to run on
        service: Optional QiskitRuntimeService instance.
        simulator: Optional AerSimulator instance for local simulation.
        results_dir: Directory to save results.
        noise_scaling_factors: List of noise scaling factors
        extrapolation_method: Method to use for extrapolation ('linear', 'polynomial', 'exponential')
        shots: Number of shots per circuit execution
        observable: Observable to measure (for Estimator) or None for Sampler
        
    Returns:
        Dictionary with ZNE results
    """
    print(f"Applying Zero Noise Extrapolation (ZNE) with {extrapolation_method} extrapolation...")
    
    if service is None:
        service = QiskitRuntimeService()
    if simulator is None:
        simulator = AerSimulator()

    results = {}
    
    # Sort scaling factors for predictable processing
    noise_scaling_factors = sorted(noise_scaling_factors)
    
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
    
    with Session(backend=session_backend) as session:
        # Define runtime parameters compatible with V2 primitives
        runtime_params = {"shots": shots}
        
        # Instantiate the appropriate V2 primitive based on observable presence
        if observable is None:
            primitive = Sampler(mode=session)
        else:
            primitive = Estimator(mode=session)
        
        # Dictionaries to store results per noise scale
        folded_circuits = {}
        values = {}
        variances = {}
        
        # Iterate through noise scaling factors
        for scale in noise_scaling_factors:
            print(f"Running with noise scaling factor {scale}...")
            
            # Create or retrieve the circuit for this noise level
            if scale == 1.0:
                folded_circuits[scale] = circuit
            else:
                # Apply circuit folding for noise amplification
                folded_circuits[scale] = _fold_circuit_gates(circuit, scale)
                
            # --- Start of Try block for this scale --- 
            try:
                # Run the job using the selected primitive
                if observable is None:
                    job = primitive.run([folded_circuits[scale]], **runtime_params)
                    result = job.result()
                    
                    # Extract and process results from V2 Sampler format
                    pub_result = result[0]  # Get the first Primitive Unified Bloc (PUB) result
                    
                    # Use the UTILITY function to get counts robustly
                    counts = extract_v2_counts(pub_result, folded_circuits[scale].num_clbits)
                        
                    if counts: # Check if counts were successfully extracted
                        # Calculate expectation value from counts assuming Z-basis measurement
                        # (Even parity = +1, Odd parity = -1)
                        expectation = 0
                        total_shots = sum(counts.values())
                        
                        for bitstring, count in counts.items():
                            num_ones = bitstring.count('1')
                            if num_ones % 2 == 0:
                                expectation += count
                            else:
                                expectation -= count
                                
                        expectation /= total_shots
                        
                        # Estimate variance (simple binomial variance approximation)
                        variance = (1 - expectation**2) / total_shots
                        
                        values[scale] = expectation
                        variances[scale] = variance
                    else:
                        print(f"Warning: No counts extracted for scale {scale}. Setting results to None.")
                        values[scale] = None
                        variances[scale] = None
                else:
                    # Prepare PUBs (Primitive Unified Blocs) for EstimatorV2 run
                    pubs = [(folded_circuits[scale], observable)] 
                    job = primitive.run(pubs, **runtime_params) 
                    result = job.result()
                    
                    # Extract expectation value and variance from V2 Estimator result
                    if result and len(result) > 0:
                        pub_result = result[0] # Get the first PUB result
                        values[scale] = pub_result.data.values[0] # Get the actual value
                        variances[scale] = pub_result.metadata.get('variance', 0.0) 
                    else:
                        print(f"Warning: No results returned from Estimator for scale {scale}.")
                        values[scale] = None
                        variances[scale] = None

                # Print results for the current scale if available
                if values.get(scale) is not None:
                     print(f"Noise scaling {scale}: expectation = {values[scale]:.6f}, variance = {variances[scale]:.6f}")
                    
            # --- End of Try block, start Except --- 
            except Exception as e:
                print(f"Error running ZNE job with noise scale {scale}: {str(e)}")
                values[scale] = None
                variances[scale] = None
        # --- End of loop --- 
        
        # Perform extrapolation using the collected data
        valid_scales = [s for s in noise_scaling_factors if values.get(s) is not None]
        valid_values = [values[s] for s in valid_scales]
        valid_variances = [variances[s] for s in valid_scales]

        extrapolated_value = None
        extrapolation_error = None
        if len(valid_scales) >= 2: # Need at least two points to extrapolate
            try:
                extrapolated_value, extrapolation_error = _extrapolate_to_zero(
                    valid_scales, 
                    valid_values,
                    valid_variances,
                    method=extrapolation_method
                )
            except ValueError as e:
                 print(f"Extrapolation failed: {e}")
            except Exception as e:
                 print(f"Unexpected error during extrapolation: {e}")
        else:
            print("Warning: Not enough valid data points for extrapolation.")
            
        # Store results in a dictionary
        results = {
            'noise_scaling_factors': noise_scaling_factors,
            'measured_values': values,
            'measured_variances': variances,
            'extrapolated_value': extrapolated_value,
            'extrapolation_error': extrapolation_error,
            'extrapolation_method': extrapolation_method
        }
        
        # Create visualization
        try:
            _plot_zne_extrapolation(
                noise_scaling_factors,
                [values[s] for s in noise_scaling_factors if values[s] is not None],
                [variances[s] for s in noise_scaling_factors if values[s] is not None],
                extrapolated_value,
                extrapolation_error,
                method=extrapolation_method,
                results_dir=results_dir # Pass results_dir to plotting func
            )
        except Exception as e:
            print(f"Error generating ZNE plot: {e}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(results_dir, f"zne_results_{backend_name}_{timestamp}.json")
        
        # Ensure all results are serializable
        serializable_results = {k: v for k, v in results.items() if k != 'circuits'}
        for k, v in serializable_results.items():
            if isinstance(v, np.ndarray):
                serializable_results[k] = v.tolist()
            elif isinstance(v, dict):
                # Convert numeric keys in inner dicts if necessary
                serializable_results[k] = {str(sk): sv for sk, sv in v.items()}
            elif isinstance(v, (np.integer, np.floating)):
                 serializable_results[k] = float(v) if not np.isnan(v) else None
            elif isinstance(v, float) and np.isnan(v):
                serializable_results[k] = None
                
        try:
            with open(results_file, 'w') as f:
                json.dump(serializable_results, f, indent=2)
            print(f"ZNE analysis complete. Results saved to {results_file}")
            if extrapolated_value is not None and extrapolation_error is not None:
                print(f"Extrapolated value at zero noise: {extrapolated_value:.6f} ± {extrapolation_error:.6f}")
        except Exception as e:
             print(f"Error saving ZNE results to JSON: {e}")
            
    return results


def _fold_circuit_gates(circuit: QuantumCircuit, scaling_factor: float) -> QuantumCircuit:
    """
    Apply circuit folding to increase the effective noise.
    (Internal helper function for ZNE)
    
    Args:
        circuit: Original quantum circuit
        scaling_factor: Noise scaling factor
        
    Returns:
        Folded quantum circuit
    """
    # Create a new circuit with the same structure (including classical registers)
    folded = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    folded.name = f"{circuit.name}_folded_{scaling_factor}"
    
    # Need to keep track of gate count for partial folding
    target_gate_count = int(circuit.size() * scaling_factor)
    current_gate_count = 0
    fold_remainder = scaling_factor - int(scaling_factor)
    
    # Process each instruction in the original circuit
    for inst, qargs, cargs in circuit.data:
        # Skip over any barrier, measure, or reset operations when counting gates
        is_foldable = not (inst.name in ['measure', 'barrier', 'reset'])
        
        if is_foldable:
            # For integer part of scaling factor, apply folding
            whole_factor = int(scaling_factor)
            
            # Apply the original gate
            folded.append(inst, qargs, cargs)
            current_gate_count += 1
            
            # Apply additional folding pairs (gate + inverse + gate + inverse...)
            # Each pair cancels out, leaving only the original gate's effect
            for _ in range(whole_factor - 1):
                # Add inverse gate then original gate again for each folding
                if hasattr(inst, 'inverse') and callable(inst.inverse):
                    folded.append(inst.inverse(), qargs, cargs)
                    folded.append(inst, qargs, cargs)
                    current_gate_count += 2
                else:
                    # For gates without defined inverse, just duplicate them an odd number of times
                    # This isn't ideal but maintains the circuit's mathematical operation while
                    # still increasing noise exposure
                    folded.append(inst, qargs, cargs)
                    current_gate_count += 1
            
            # Handle fractional part with probability
            if fold_remainder > 0 and np.random.random() < fold_remainder:
                if hasattr(inst, 'inverse') and callable(inst.inverse):
                    folded.append(inst.inverse(), qargs, cargs)
                    folded.append(inst, qargs, cargs)
                    current_gate_count += 2
        else:
            # For non-foldable gates (measure, reset, barrier), just copy them
            folded.append(inst, qargs, cargs)
    
    return folded


def _extrapolate_to_zero( 
    scales: List[float], 
    values: List[float], 
    variances: List[float],
    method: str = 'linear'
) -> Tuple[float, float]:
    """
    Extrapolate measured values to the zero-noise limit.
    (Internal helper function for ZNE)
    
    Args:
        scales: List of noise scaling factors
        values: List of measured expectation values
        variances: List of measurement variances
        method: Method to use for extrapolation ('linear', 'polynomial', 'exponential')
        
    Returns:
        (extrapolated_value, extrapolation_error)
    """
    # Filter out None values (already done before calling, but good practice)
    valid_points = [(s, v, var) for s, v, var in zip(scales, values, variances) if v is not None]
    
    if len(valid_points) < 2:
        raise ValueError("Need at least 2 valid data points for extrapolation")
        
    # Convert lists to numpy arrays
    scales_arr = np.array([s for s, _, _ in valid_points])
    values_arr = np.array([v for _, v, _ in valid_points])
    variances_arr = np.array([var for _, _, var in valid_points])
    weights = 1.0 / np.maximum(variances_arr, 1e-10)  # Avoid division by zero
    
    if method == 'linear':
        # Linear extrapolation
        coeffs, cov = np.polyfit(scales_arr, values_arr, 1, w=weights, cov=True)
        extrapolated_value = coeffs[1]  # y-intercept is the zero-noise value
        extrapolation_error = np.sqrt(cov[1, 1])  # Error in y-intercept
        
    elif method == 'polynomial':
        # Polynomial extrapolation
        order = min(len(scales_arr) - 1, 3)  # Avoid overfitting
        coeffs, cov = np.polyfit(scales_arr, values_arr, order, w=weights, cov=True)
        extrapolated_value = coeffs[-1]  # Constant term is the zero-noise value
        extrapolation_error = np.sqrt(cov[-1, -1])  # Error in constant term
        
    elif method == 'exponential':
        # Exponential extrapolation (fit to exp decay)
        # For exponential fit, convert to log space for linear fit
        # Use only positive values for logarithmic transform
        pos_indices = np.where(values_arr > 0)[0]
        if len(pos_indices) >= 2:
            log_values = np.log(values_arr[pos_indices])
            log_scales = scales_arr[pos_indices]
            log_weights = weights[pos_indices] * values_arr[pos_indices]**2  # Error propagation
            
            coeffs, cov = np.polyfit(log_scales, log_values, 1, w=log_weights, cov=True)
            extrapolated_value = np.exp(coeffs[1])  # y-intercept in log space
            extrapolation_error = extrapolated_value * np.sqrt(cov[1, 1])  # Error propagation
        else:
            # Fall back to linear if not enough positive values
            print("Warning: Not enough positive values for exponential extrapolation, falling back to linear")
            coeffs, cov = np.polyfit(scales_arr, values_arr, 1, w=weights, cov=True)
            extrapolated_value = coeffs[1]
            extrapolation_error = np.sqrt(cov[1, 1])
    else:
        raise ValueError(f"Unknown extrapolation method: {method}")
        
    return extrapolated_value, extrapolation_error


def _plot_zne_extrapolation(
    scales: List[float], 
    values: List[float], 
    variances: List[float],
    extrapolated_value: Optional[float], 
    extrapolation_error: Optional[float],
    method: str = 'linear',
    results_dir: str = '.' # Add results_dir parameter
):
    """
    Generate a plot of the ZNE extrapolation.
    (Internal helper function for ZNE)
    
    Args:
        scales: List of noise scaling factors
        values: List of measured expectation values
        variances: List of measurement variances
        extrapolated_value: Extrapolated zero-noise value (Optional)
        extrapolation_error: Error in the extrapolated value (Optional)
        method: Method used for extrapolation
        results_dir: Directory to save the plot.
    """
    plt.figure(figsize=(10, 6))
    
    # Convert inputs to numpy arrays
    scales_arr = np.array(scales)
    values_arr = np.array(values)
    variances_arr = np.array(variances)
    
    # Plot measured points with error bars
    plt.errorbar(scales_arr, values_arr, yerr=np.sqrt(variances_arr), 
               fmt='o', label='Measured values', color='blue', capsize=4)
    
    # Generate extrapolation curve only if extrapolation succeeded and values are valid
    if extrapolated_value is not None and len(scales_arr) > 0:
        x_extrap = np.linspace(0, max(scales_arr), 100)
        valid_points_exist = len(scales_arr) >= 2 # Need at least 2 points to fit

        try: # Add try-except for fitting robustness
            if method == 'linear' and valid_points_exist:
                coeffs, cov = np.polyfit(scales_arr, values_arr, 1, w=1.0/variances_arr, cov=True)
                y_fit = np.polyval(coeffs, x_extrap)
                plt.plot(x_extrap, y_fit, '--', label=f'Linear fit: y = {coeffs[0]:.4f}x + {coeffs[1]:.4f}', color='red')
                
            elif method == 'polynomial' and valid_points_exist:
                order = min(len(scales_arr) - 1, 3)
                coeffs, cov = np.polyfit(scales_arr, values_arr, order, w=1.0/variances_arr, cov=True)
                y_fit = np.polyval(coeffs, x_extrap)
                plt.plot(x_extrap, y_fit, '--', label=f'Poly fit (order {order})', color='red')
                
            elif method == 'exponential':
                pos_indices = np.where(values_arr > 0)[0]
                if len(pos_indices) >= 2:
                    log_values = np.log(values_arr[pos_indices])
                    log_scales = scales_arr[pos_indices]
                    log_weights = (1.0 / variances_arr[pos_indices]) * values_arr[pos_indices]**2
                    coeffs, cov = np.polyfit(log_scales, log_values, 1, w=log_weights, cov=True)
                    y_fit = np.exp(np.polyval(coeffs, x_extrap))
                    plt.plot(x_extrap, y_fit, '--', label='Exponential fit', color='red')
                elif valid_points_exist:
                     print("Could not perform exponential fit due to insufficient positive data. Falling back to linear.")
                     # Fallback to linear if exponential fit fails
                     coeffs, cov = np.polyfit(scales_arr, values_arr, 1, w=1.0/variances_arr, cov=True)
                     y_fit = np.polyval(coeffs, x_extrap)
                     plt.plot(x_extrap, y_fit, '--', label='Linear fit (fallback)', color='orange')
            
            # Plot the extrapolated zero-noise point
            if extrapolation_error is not None:
                 plt.errorbar(0, extrapolated_value, yerr=extrapolation_error,
                           fmt='o', label='Extrapolated zero noise', color='green', markersize=8, capsize=5)
            else:
                 plt.plot(0, extrapolated_value, 'o', label='Extrapolated zero noise (no error)', color='green', markersize=8)
        
        except np.linalg.LinAlgError:
             print(f"Warning: Fitting failed for {method} extrapolation plot due to singular matrix.")
        except Exception as plot_err:
             print(f"Warning: Error during plot generation for {method} extrapolation: {plot_err}")

    plt.xlabel('Noise Scaling Factor')
    plt.ylabel('Expectation Value')
    plt.title(f'Zero Noise Extrapolation ({method.capitalize()} Method)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_path = os.path.join(results_dir, f"zne_extrapolation_{method}_{timestamp}.png")
    try:
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {fig_path}")
    except Exception as save_err:
         print(f"Error saving ZNE plot: {save_err}")
    finally:
        plt.close()
