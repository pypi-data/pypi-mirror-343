"""Functions for Readout Error Mitigation."""

# Imports will be added here as functions are moved
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_aer import AerSimulator
from typing import List, Dict, Tuple, Any, Optional, Mapping, Union
import json
import os
from datetime import datetime

# Import necessary utilities
# NOTE: Changed from absolute 'quantum.error_correction.utils' to relative
from ..utils import extract_v2_counts, calculate_distribution_fidelity, get_ideal_counts

def apply_readout_mitigation(
    circuit: QuantumCircuit,
    backend_name: str,
    service: Optional[QiskitRuntimeService] = None,
    simulator: Optional[AerSimulator] = None,
    results_dir: str = './error_mitigation_results',
    shots: int = 5000,
    method: str = 'matrix_inversion'
) -> Dict:
    """
    Apply readout error mitigation to correct measurement errors.
    
    Readout error mitigation works by characterizing the measurement errors
    for each qubit and then using the error pattern to correct subsequent 
    measurements.
    
    Args:
        circuit: Quantum circuit to apply readout mitigation to
        backend_name: Backend to run on
        service: Optional QiskitRuntimeService instance.
        simulator: Optional AerSimulator instance for local simulation.
        results_dir: Directory to save results.
        shots: Number of shots per circuit execution
        method: Method to use ('matrix_inversion' or 'least_squares')
        
    Returns:
        Dictionary with readout mitigation results
    """
    print(f"\nApplying Readout Error Mitigation using {method} method...")
    
    if service is None:
        service = QiskitRuntimeService()
    if simulator is None:
        simulator = AerSimulator()

    results = {}
    raw_counts = None
    mitigated_counts = None
    correction_matrix = None
    ideal_counts_binary = None
    raw_fidelity = None
    mitigated_fidelity = None
    fidelity_improvement = None
    
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
            # Use SamplerV2 for readout mitigation (needs counts)
            primitive = Sampler(mode=session)
            
            # Step 1: Create calibration circuits
            num_qubits = circuit.num_qubits
            cal_circuits = _create_readout_calibration_circuits(num_qubits)
            print(f"Generated {len(cal_circuits)} calibration circuits for {num_qubits} qubits.")
            
            # Step 2: Run calibration circuits
            print("Running calibration circuits...")
            try:
                job_cal = primitive.run(cal_circuits, shots=shots)
                cal_results = job_cal.result()
                print("Calibration circuits run complete.")
                
                cal_counts_list = []
                if cal_results:
                    for i in range(len(cal_circuits)):
                        if i < len(cal_results):
                            pub_result = cal_results[i]
                            counts = extract_v2_counts(pub_result, cal_circuits[i].num_clbits)
                            cal_counts_list.append(counts)
                        else:
                            print(f"Warning: Missing result for calibration circuit {i}")
                            cal_counts_list.append({})
                else:
                    raise RuntimeError("No results returned for calibration circuits.")
                        
            except Exception as e:
                 print(f"Error running calibration circuits: {str(e)}")
                 raise RuntimeError(f"Calibration failed: {str(e)}") from e

            # Step 3: Construct the correction matrix
            print(f"Constructing correction matrix using {method}...")
            try:
                if method == 'matrix_inversion':
                    correction_matrix = _construct_correction_matrix(cal_counts_list, num_qubits)
                elif method == 'least_squares':
                    correction_matrix = _construct_correction_matrix_ls(cal_counts_list, num_qubits)
                else:
                    raise ValueError(f"Unknown readout mitigation method: {method}")
            except Exception as e:
                print(f"Error constructing correction matrix: {str(e)}")
                raise RuntimeError(f"Matrix construction failed: {str(e)}") from e

            # Step 4: Run the main circuit
            print("Running the main circuit...")
            try:
                job_main = primitive.run([circuit], shots=shots)
                main_result_list = job_main.result()
                print("Main circuit run complete.")
                
                if not main_result_list:
                     raise RuntimeError("No results returned for the main circuit.")
                     
                main_result = main_result_list[0]
                raw_counts = extract_v2_counts(main_result, circuit.num_clbits)
                if not raw_counts:
                    print("Warning: Main circuit run produced no counts.")
                
            except Exception as e:
                 print(f"Error running main circuit: {str(e)}")
                 raise RuntimeError(f"Main circuit run failed: {str(e)}") from e

            # Step 5: Apply the correction matrix
            if raw_counts and correction_matrix is not None:
                print("Applying readout correction...")
                try:
                    mitigated_counts = _apply_correction(raw_counts, correction_matrix, num_qubits)
                except Exception as e:
                    print(f"Error applying correction: {str(e)}")
                    mitigated_counts = None 
            else:
                print("Skipping correction application due to missing raw counts or matrix.")
                mitigated_counts = None
                
            # Step 6: Calculate fidelity improvement (optional)
            if raw_counts and mitigated_counts:
                print("Calculating fidelity improvement...")
                try:
                    ideal_counts_raw = get_ideal_counts(circuit, shots)
                    ideal_counts_binary = {_format_bitstring(k, num_qubits): v for k, v in ideal_counts_raw.items()}
                                            
                    raw_fidelity = calculate_distribution_fidelity(raw_counts, ideal_counts_binary)
                    mitigated_fidelity = calculate_distribution_fidelity(mitigated_counts, ideal_counts_binary)
                    fidelity_improvement = mitigated_fidelity - raw_fidelity
                    print(f"Fidelity: Raw={raw_fidelity:.4f}, Mitigated={mitigated_fidelity:.4f}")
                except Exception as e:
                    print(f"Could not calculate fidelity improvement: {str(e)}")
                    raw_fidelity, mitigated_fidelity, fidelity_improvement = None, None, None
            
    except Exception as main_error:
        print(f"Readout mitigation failed: {main_error}")
        results['error'] = str(main_error)
        # Ensure partially computed results are still returned
        results.update({
            'raw_counts': raw_counts,
            'mitigated_counts': mitigated_counts,
            'correction_matrix': correction_matrix.tolist() if correction_matrix is not None else None,
            'method': method,
            'ideal_counts': ideal_counts_binary,
            'raw_fidelity': raw_fidelity,
            'mitigated_fidelity': mitigated_fidelity,
            'fidelity_improvement': fidelity_improvement
        })
        return results # Exit early on major failure

    # Store results if successful execution
    results = {
        'raw_counts': raw_counts,
        'mitigated_counts': mitigated_counts,
        'correction_matrix': correction_matrix.tolist() if correction_matrix is not None else None,
        'method': method,
        'ideal_counts': ideal_counts_binary,
        'raw_fidelity': raw_fidelity,
        'mitigated_fidelity': mitigated_fidelity,
        'fidelity_improvement': fidelity_improvement
    }
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"readout_mitigation_{backend_name}_{timestamp}.json")
    
    # Ensure results are serializable
    serializable_results = _serialize_dict(results)
        
    try:
        os.makedirs(results_dir, exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        print(f"\nReadout error mitigation complete. Results saved to {results_file}")
        if raw_fidelity is not None and mitigated_fidelity is not None:
             print(f"Final Fidelity: Raw={raw_fidelity:.4f}, Mitigated={mitigated_fidelity:.4f}, Improvement={fidelity_improvement:.4f}")
    except Exception as save_err:
        print(f"Error saving readout mitigation results: {save_err}")
    
    # Create visualization of raw vs. mitigated counts
    try:
        _plot_readout_correction(raw_counts, mitigated_counts, results_dir)
    except Exception as plot_err:
        print(f"Error generating readout plot: {plot_err}")
        
    return results

def _create_readout_calibration_circuits(num_qubits: int) -> List[QuantumCircuit]:
    """
    Create calibration circuits for readout error characterization.
    Generates circuits that prepare each computational basis state.
    (Internal helper function for Readout Mitigation)
    
    Args:
        num_qubits: Number of qubits
        
    Returns:
        List of calibration circuits
    """
    cal_circuits = []
    # Generate circuits for all 2**num_qubits basis states
    # This becomes inefficient for large num_qubits, but is standard.
    for i in range(2**num_qubits):
        # Get the binary representation of the state index
        bitstring = format(i, f'0{num_qubits}b')
        
        # Create a circuit for this basis state
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.name = f"cal_{bitstring}"
        
        # Apply X gates to qubits that should be |1>
        for qubit, bit in enumerate(reversed(bitstring)):
            if bit == '1':
                qc.x(qubit)
        
        # Add measurements
        qc.measure_all()
        
        cal_circuits.append(qc)
        
    return cal_circuits

def _construct_correction_matrix(
    cal_counts_list: List[Dict[str, int]], 
    num_qubits: int
) -> np.ndarray:
    """
    Construct the readout correction matrix using matrix inversion.
    Requires calibration circuits for all 2^n basis states.
    (Internal helper function for Readout Mitigation)
    
    Args:
        cal_counts_list: List of counts from calibration circuits (ordered 0 to 2^n - 1)
        num_qubits: Number of qubits
        
    Returns:
        Correction matrix (inverse of the measurement matrix)
    """
    dim = 2**num_qubits
    if len(cal_counts_list) != dim:
        raise ValueError(f"Expected {dim} calibration circuits, but got {len(cal_counts_list)}.")

    measurement_matrix = np.zeros((dim, dim))
    
    # cal_counts_list[i] corresponds to preparing state |i>
    for i, counts in enumerate(cal_counts_list):
        total_shots = sum(counts.values())
        if total_shots == 0: continue # Skip if no shots for this cal circuit
        
        # Fill the i-th column of the measurement matrix
        for bitstring, count in counts.items():
            try:
                j = _bitstring_to_int(bitstring, num_qubits) # Measured state is |j>
                if 0 <= j < dim:
                    measurement_matrix[j, i] = count / total_shots # M[measured, prepared]
                else:
                     print(f"Warning: Invalid measured bitstring index {j} from '{bitstring}' for {num_qubits} qubits.")
            except ValueError as e:
                 print(f"Warning: Could not convert measured bitstring '{bitstring}' to int: {e}")
    
    # Invert the measurement matrix to get the correction matrix
    try:
        # Use pseudo-inverse for numerical stability
        correction_matrix = np.linalg.pinv(measurement_matrix)
    except np.linalg.LinAlgError as e:
        print(f"Fatal Error: Measurement matrix inversion failed: {e}")
        raise 
        
    return correction_matrix
    
def _construct_correction_matrix_ls(
    cal_counts_list: List[Dict[str, int]], 
    num_qubits: int
) -> np.ndarray:
    """
    Construct the readout correction matrix using least-squares fitting.
    This is essentially equivalent to pseudo-inverse for this problem setup.
    (Internal helper function for Readout Mitigation)
    
    Args:
        cal_counts_list: List of counts from calibration circuits
        num_qubits: Number of qubits
        
    Returns:
        Correction matrix (least-squares solution)
    """
    # This method is generally equivalent to pseudo-inverse here.
    # We call the standard pseudo-inverse method for consistency.
    return _construct_correction_matrix(cal_counts_list, num_qubits)

def _apply_correction(
    raw_counts: Dict[str, int], 
    correction_matrix: np.ndarray, 
    num_qubits: int
) -> Dict[str, float]:
    """
    Apply the correction matrix to raw measurement counts.
    (Internal helper function for Readout Mitigation)
    
    Args:
        raw_counts: Raw measurement counts dictionary
        correction_matrix: Readout correction matrix
        num_qubits: Number of qubits
        
    Returns:
        Mitigated counts dictionary (values are floats)
    """
    dim = 2**num_qubits
    raw_vector = np.zeros(dim)
    total_shots = sum(raw_counts.values())
    
    if total_shots == 0: return {}
    
    # Convert raw counts to a probability vector
    for bitstring, count in raw_counts.items():
        try:
            idx = _bitstring_to_int(bitstring, num_qubits)
            if 0 <= idx < dim:
                raw_vector[idx] = count / total_shots
            else:
                print(f"Warning: Invalid raw bitstring index {idx} from '{bitstring}' for {num_qubits} qubits.")
        except ValueError as e:
             print(f"Warning: Could not convert raw bitstring '{bitstring}' to int: {e}")
            
    # Apply the correction matrix
    corrected_vector = correction_matrix @ raw_vector
    
    # Apply constraints (non-negativity, sum to 1)
    corrected_vector = np.maximum(corrected_vector, 0)
    vec_sum = np.sum(corrected_vector)
    if vec_sum > 0:
        corrected_vector /= vec_sum
    
    # Convert corrected vector back to counts dictionary
    mitigated_counts = {}
    for i in range(dim):
        if corrected_vector[i] > 1e-10: # Threshold small values
            bitstring = format(i, f'0{num_qubits}b')
            mitigated_counts[bitstring] = corrected_vector[i] * total_shots
    
    return mitigated_counts
    
def _bitstring_to_int(bitstring: str, num_qubits: int) -> int:
    """
    Convert a bitstring to integer, handling qiskit's different formats.
    (Internal helper function)
    
    Args:
        bitstring: Bitstring in format like '01', '0 1', or '0x1'
        num_qubits: Expected number of qubits (for validation)
        
    Returns:
        Integer representation
        
    Raises:
         ValueError if conversion fails or length mismatch.
    """
    # Remove any spaces
    clean_str = bitstring.replace(' ', '')
    val = -1

    # Try interpreting as binary
    if all(c in '01' for c in clean_str):
        if len(clean_str) != num_qubits:
            raise ValueError(f"Bitstring '{clean_str}' length {len(clean_str)} != num_qubits {num_qubits}")
        val = int(clean_str, 2)
    # Try interpreting as hex (common from SamplerV2)
    elif clean_str.startswith('0x'):
        val = int(clean_str, 16)
        # Check if hex value fits within num_qubits
        if val >= (1 << num_qubits):
             raise ValueError(f"Hex bitstring '{clean_str}' value {val} too large for {num_qubits} qubits.")
    else:
         raise ValueError(f"Cannot interpret bitstring: '{bitstring}'")

    return val

def _format_bitstring(key: str, num_qubits: int) -> str:
     """ Formats a key from counts (potentially hex) into a binary string. """
     if key.startswith('0x'):
         val = int(key, 16)
         return format(val, f'0{num_qubits}b')
     # Assume already binary or handle other formats if needed
     return key

def _plot_readout_correction(
    raw_counts: Optional[Dict[str, int]], 
    mitigated_counts: Optional[Dict[str, float]],
    results_dir: str = '.' # Add results_dir parameter
):
    """
    Create a bar chart comparing raw and mitigated counts.
    (Internal helper function for Readout Mitigation)
    
    Args:
        raw_counts: Dictionary of raw counts (Optional)
        mitigated_counts: Dictionary of mitigated counts (Optional)
        results_dir: Directory to save the plot.
    """
    if raw_counts is None or mitigated_counts is None:
        print("Skipping readout correction plot due to missing counts data.")
        return

    # Get all unique bitstrings
    all_bitstrings = sorted(set(list(raw_counts.keys()) + list(mitigated_counts.keys())))
    num_qubits = len(all_bitstrings[0]) if all_bitstrings else 0
    
    # Convert to probabilities
    raw_total = sum(raw_counts.values())
    mitigated_total = sum(mitigated_counts.values())
    
    raw_probs = [raw_counts.get(bs, 0) / raw_total if raw_total > 0 else 0 for bs in all_bitstrings]
    mitigated_probs = [mitigated_counts.get(bs, 0) / mitigated_total if mitigated_total > 0 else 0 for bs in all_bitstrings]
    
    # Create plot
    plt.figure(figsize=(12, 6))
    x = np.arange(len(all_bitstrings))
    width = 0.35
    
    plt.bar(x - width/2, raw_probs, width, label='Raw', color='blue', alpha=0.6)
    plt.bar(x + width/2, mitigated_probs, width, label='Mitigated', color='green', alpha=0.6)
    
    plt.xlabel('Bitstring')
    plt.ylabel('Probability')
    plt.title('Readout Error Mitigation Results')
    plt.xticks(x, all_bitstrings, rotation=70, fontsize=8)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the figure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_path = os.path.join(results_dir, f"readout_correction_{timestamp}.png")
    try:
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {fig_path}")
    except Exception as save_err:
        print(f"Error saving readout plot: {save_err}")
    finally:
        plt.close()

# Helper for serializing results dictionary
def _serialize_dict(data: Dict) -> Dict:
    """ Recursively makes dictionary contents JSON serializable. """
    serializable = {}
    if not isinstance(data, dict):
        return data # Return non-dict items as is

    for k, v in data.items():
        key_str = str(k)
        if isinstance(v, np.ndarray):
            serializable[key_str] = v.tolist()
        elif isinstance(v, dict):
            serializable[key_str] = _serialize_dict(v)
        elif isinstance(v, (np.integer, np.floating)):
             serializable[key_str] = float(v) if not np.isnan(v) else None
        elif isinstance(v, float) and np.isnan(v):
            serializable[key_str] = None
        elif isinstance(v, (int, float, bool, str)) or v is None:
             serializable[key_str] = v
        else:
            try:
                 json.dumps(v)
                 serializable[key_str] = v
            except TypeError:
                 serializable[key_str] = str(v)
    return serializable
