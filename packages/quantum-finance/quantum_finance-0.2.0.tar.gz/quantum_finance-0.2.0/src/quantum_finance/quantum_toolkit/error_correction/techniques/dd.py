"""Functions for Dynamical Decoupling (DD)."""

# Note: The current implementation uses simplified gate insertion and 
# idle time identification. Accurate DD requires backend timing information.

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_aer import AerSimulator
from typing import List, Dict, Tuple, Any, Optional, Mapping, Union
import json
import os
from datetime import datetime

# Import necessary utilities
from ..utils import extract_v2_counts, calculate_distribution_fidelity
from .readout import _serialize_dict # Using serializer from readout for now


def apply_dynamical_decoupling(
    circuit: QuantumCircuit,
    backend_name: str,
    service: Optional[QiskitRuntimeService] = None,
    simulator: Optional[AerSimulator] = None,
    results_dir: str = './error_mitigation_results',
    sequence_type: str = 'XX',
    idle_time_threshold: Optional[float] = None,
    shots: int = 5000
) -> Dict:
    """
    Apply Dynamical Decoupling (DD) to mitigate decoherence.
    
    Args:
        circuit: Quantum circuit to apply DD to
        backend_name: Backend to run on  
        service: Optional QiskitRuntimeService instance.
        simulator: Optional AerSimulator instance for local simulation.
        results_dir: Directory to save results.
        sequence_type: Type of DD sequence ('X', 'XX', 'XY4', 'XY8', 'XY16')
        idle_time_threshold: Minimum idle time to insert DD (None for auto)
        shots: Number of shots per circuit execution
        
    Returns:
        Dictionary with DD results
    """
    print(f"\nApplying Dynamical Decoupling (DD) using {sequence_type} sequence...")
    
    if service is None:
        service = QiskitRuntimeService()
    if simulator is None:
        simulator = AerSimulator()

    results = {}
    original_counts = None
    dd_counts = None
    dd_circuit = None
    fidelity_improvement = None
    
    # Determine if running locally or on IBM backend
    is_local_simulator = backend_name == 'local_simulator'
    
    # Get backend instance or fallback to local simulator
    backend = None
    if not is_local_simulator:
        try:
            backend = service.backend(backend_name)
            # TODO: Fetch backend properties here for accurate timing
        except Exception as e:
            print(f"Error getting backend: {str(e)}")
            print("Falling back to local simulator...")
            is_local_simulator = True
            
    # Define backend for the session context
    session_backend = simulator if is_local_simulator else backend
    
    try:
        with Session(backend=session_backend) as session:
            # Use SamplerV2 for DD (comparing counts)
            primitive = Sampler(mode=session)
            runtime_params = {"shots": shots}
            
            # --- Run Original Circuit ---
            print("Running original circuit...")
            try:
                 job_orig = primitive.run([circuit], **runtime_params)
                 result_orig_list = job_orig.result()
                 if result_orig_list:
                     pub_result_orig = result_orig_list[0]
                     original_counts = extract_v2_counts(pub_result_orig, circuit.num_clbits)
                 else:
                     print("Warning: No result returned for original circuit.")
            except Exception as e:
                print(f"Error running original circuit: {str(e)}")
                # Don't necessarily stop if original fails, might still want DD run

            # --- Apply DD Sequences ---
            print(f"Applying {sequence_type} DD sequence...")
            try:
                dd_circuit = _apply_dd_sequences(circuit, sequence_type, idle_time_threshold)
                print("Dynamical decoupling sequence applied to circuit.")
            except Exception as e:
                print(f"Error applying DD sequences: {str(e)}")
                raise RuntimeError(f"DD sequence application failed: {str(e)}") from e

            # --- Run DD Circuit ---
            if dd_circuit:
                print("Running DD circuit...")
                try:
                    job_dd = primitive.run([dd_circuit], **runtime_params)
                    result_dd_list = job_dd.result()
                    if result_dd_list:
                        pub_result_dd = result_dd_list[0]
                        dd_counts = extract_v2_counts(pub_result_dd, dd_circuit.num_clbits)
                    else:
                        print("Warning: No result returned for DD circuit.")
                except Exception as e:
                    print(f"Error running DD circuit: {str(e)}")
                    dd_counts = None # Ensure dd_counts is None if run fails
            else:
                 print("Skipping DD circuit run because sequence application failed.")
                 dd_counts = None

            # --- Calculate fidelity improvement (optional) --- 
            if original_counts is not None and dd_counts is not None:
                 print("Calculating fidelity vs original...")
                 try:
                      mitigated_fidelity = calculate_distribution_fidelity(original_counts, dd_counts)
                      fidelity_improvement = mitigated_fidelity # Report fidelity directly against original
                      print(f"Fidelity vs Original: {fidelity_improvement:.4f}")
                 except Exception as e:
                      print(f"Could not calculate fidelity improvement: {str(e)}")
                      fidelity_improvement = None

    except Exception as main_error:
         print(f"DD execution failed: {main_error}")
         results['error'] = str(main_error)

    # --- Store results --- 
    results.update({
        'original_counts': original_counts,
        'dd_counts': dd_counts,
        'sequence_type': sequence_type,
        'fidelity_vs_original': fidelity_improvement,
        'original_circuit_depth': circuit.depth(),
        'dd_circuit_depth': dd_circuit.depth() if dd_circuit else None
    })
    
    # --- Create visualization --- 
    try:
        _plot_dd_comparison(original_counts, dd_counts, sequence_type, results_dir)
    except Exception as plot_err:
        print(f"Error generating DD plot: {plot_err}")

    # --- Save results --- 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"dd_results_{backend_name}_{timestamp}.json")
    
    serializable_results = _serialize_dict(results)
            
    try:
        os.makedirs(results_dir, exist_ok=True)
        with open(results_file, 'w') as f:
             json.dump(serializable_results, f, indent=2)
        print(f"Dynamical Decoupling complete. Results saved to {results_file}")
        if fidelity_improvement is not None:
            print(f"Final Fidelity vs Original: {fidelity_improvement:.4f}")
    except Exception as save_err:
        print(f"Error saving DD results: {save_err}")
            
    return results

def _apply_dd_sequences(
    circuit: QuantumCircuit, 
    sequence_type: str = 'XX',
    idle_time_threshold: Optional[float] = None
) -> QuantumCircuit:
    """
    Apply dynamical decoupling sequences to idle periods in the circuit.
    (Internal helper function for DD)

    Note: This implementation uses a simplified approach for identifying idle 
    time and inserting gates. It does not use precise backend timing.
    
    Args:
        circuit: Original quantum circuit
        sequence_type: Type of pulse sequence to use ('X', 'XX', 'XY4', 'XY8', 'XY16')
        idle_time_threshold: Minimum idle time (approximate duration units) to apply DD pulses.
                            If None, a default based on CX gate duration is used.
        
    Returns:
        Circuit with dynamical decoupling sequences inserted.
    """
    # Define approximate instruction durations (could be fetched from backend)
    instruction_durations = {
        'x': 1.0, 'y': 1.0, 'z': 1.0, 'h': 1.0,
        'rx': 1.0, 'ry': 1.0, 'rz': 1.0, 'id': 1.0,
        'cx': 5.0, 'cz': 5.0, 'swap': 6.0,
        'measure': 10.0, 'barrier': 0.1, 'reset': 1.0
    }
    default_duration = 1.0

    # Set threshold if not specified (heuristic based on CX duration)
    if idle_time_threshold is None:
        idle_time_threshold = instruction_durations.get('cx', 5.0) * 1.5

    # Build the new circuit instruction by instruction
    new_circuit = QuantumCircuit(circuit.num_qubits, circuit.num_clbits, name=f"{circuit.name}_dd_{sequence_type}")
    qubit_last_op_time = {q: 0.0 for q in range(circuit.num_qubits)}

    for inst, qargs, cargs in circuit.data:
        # Find the time this operation must start (max end time of previous ops on involved qubits)
        op_start_time = 0.0
        involved_qubits = [q.index for q in qargs]
        for q_idx in involved_qubits:
            op_start_time = max(op_start_time, qubit_last_op_time[q_idx])

        # Check for idle time on each involved qubit before this operation
        for q_idx in involved_qubits:
            idle_start = qubit_last_op_time[q_idx]
            idle_duration = op_start_time - idle_start
            
            # If idle duration exceeds threshold, insert DD sequence
            if idle_duration >= idle_time_threshold:
                print(f"  Inserting DD ({sequence_type}) on qubit {q_idx} during idle period [{idle_start:.1f}, {op_start_time:.1f}] duration {idle_duration:.1f}")
                _insert_dd_sequence(new_circuit, q_idx, sequence_type)
                # Update time marker after DD (simplified, assumes DD is fast)
                qubit_last_op_time[q_idx] = op_start_time 
        
        # Append the original instruction to the new circuit
        new_circuit.append(inst, qargs, cargs)
        
        # Update the last operation time for involved qubits
        gate_name = inst.name.lower()
        duration = instruction_durations.get(gate_name, default_duration)
        op_end_time = op_start_time + duration
        for q_idx in involved_qubits:
             qubit_last_op_time[q_idx] = op_end_time

    # Optional: Add final DD sequence if there's significant idle time at the end
    # circuit_duration = max(qubit_last_op_time.values())
    # for q_idx in range(circuit.num_qubits):
    #    # ... check idle time from last_op_time[q_idx] to circuit_duration ...

    return new_circuit
        
def _insert_dd_sequence(circuit: QuantumCircuit, qubit: int, sequence_type: str):
    """ Helper to insert a specific DD sequence on a qubit.
        (Internal helper function for DD)
        Appends gates without precise timing.
    """
    if sequence_type == 'X':
        circuit.x(qubit)
    elif sequence_type == 'XX':
        circuit.x(qubit)
        circuit.x(qubit)
    elif sequence_type == 'XY4':
        circuit.x(qubit)
        circuit.y(qubit)
        circuit.x(qubit)
        circuit.y(qubit)
    elif sequence_type == 'XY8':
        circuit.x(qubit); circuit.y(qubit); circuit.x(qubit); circuit.y(qubit)
        circuit.y(qubit); circuit.x(qubit); circuit.y(qubit); circuit.x(qubit)
    elif sequence_type == 'XY16':
        # XY4
        circuit.x(qubit); circuit.y(qubit); circuit.x(qubit); circuit.y(qubit)
        # inv(XY4) - YX YX
        circuit.y(qubit); circuit.x(qubit); circuit.y(qubit); circuit.x(qubit)
        # XY4
        circuit.x(qubit); circuit.y(qubit); circuit.x(qubit); circuit.y(qubit)
        # inv(XY4) - YX YX
        circuit.y(qubit); circuit.x(qubit); circuit.y(qubit); circuit.x(qubit)
    else:
        print(f"Warning: Unknown DD sequence type '{sequence_type}'. Defaulting to XX.")
        circuit.x(qubit)
        circuit.x(qubit)

def _identify_idle_periods( 
    circuit: QuantumCircuit, 
    instruction_durations: Dict[str, float]
) -> Dict[int, List[Tuple[float, float]]]:
    """
    Identify idle periods for each qubit based on approximate gate durations.
    (Internal helper function for DD)
    
    Args:
        circuit: Quantum circuit to analyze
        instruction_durations: Dictionary of approximate gate durations
            
    Returns:
        Dictionary mapping qubit index to list of (start_time, end_time) idle periods.
    """
    num_qubits = circuit.num_qubits
    idle_periods = {q: [] for q in range(num_qubits)}
    last_op_time = {q: 0.0 for q in range(num_qubits)}
    default_duration = 1.0

    for i, (inst, qargs, cargs) in enumerate(circuit.data):
        involved_qubits = [q.index for q in qargs]
        gate_name = inst.name.lower()
        duration = instruction_durations.get(gate_name, default_duration)

        op_start_time = 0.0
        for q_idx in involved_qubits:
            op_start_time = max(op_start_time, last_op_time[q_idx])
        
        for q_idx in involved_qubits:
            idle_start = last_op_time[q_idx]
            idle_duration = op_start_time - idle_start
            if idle_duration > 0.1: # Threshold to ignore tiny gaps
                idle_periods[q_idx].append((idle_start, op_start_time))
        
        op_end_time = op_start_time + duration
        for q_idx in involved_qubits:
            last_op_time[q_idx] = op_end_time
            
    # Add final idle periods from last op to overall circuit end time (approx)
    circuit_end_time = max(last_op_time.values()) if last_op_time else 0.0
    for q_idx in range(num_qubits):
        idle_start = last_op_time[q_idx]
        if circuit_end_time > idle_start:
             idle_periods[q_idx].append((idle_start, circuit_end_time))

    return idle_periods

def _plot_dd_comparison(
    original_counts: Optional[Dict[str, int]], 
    dd_counts: Optional[Dict[str, int]], 
    sequence_type: str,
    results_dir: str = '.'
):
    """
    Generate a plot comparing original counts with DD-mitigated counts.
    (Internal helper function for DD)
    
    Args:
        original_counts: Original circuit counts (Optional)
        dd_counts: Counts with dynamical decoupling (Optional)
        sequence_type: Type of DD sequence used
        results_dir: Directory to save the plot.
    """
    if original_counts is None or dd_counts is None:
        print("Skipping DD comparison plot because original or DD counts are missing.")
        return
            
    plt.figure(figsize=(12, 6))
    
    all_labels = sorted(list(set(original_counts.keys()) | set(dd_counts.keys())))
    
    orig_total = sum(original_counts.values())
    dd_total = sum(dd_counts.values())
    
    orig_freq = {label: original_counts.get(label, 0) / orig_total if orig_total > 0 else 0 for label in all_labels}
    dd_freq = {label: dd_counts.get(label, 0) / dd_total if dd_total > 0 else 0 for label in all_labels}

    orig_plot_values = [orig_freq[label] for label in all_labels]
    dd_plot_values = [dd_freq[label] for label in all_labels]
            
    x = np.arange(len(all_labels))
    width = 0.35
    
    plt.bar(x - width/2, orig_plot_values, width, label='Original', color='blue', alpha=0.6)
    plt.bar(x + width/2, dd_plot_values, width, label=f'With {sequence_type} DD', color='green', alpha=0.6)
    
    plt.xlabel('Bitstring')
    plt.ylabel('Frequency')
    plt.title(f'Dynamical Decoupling Results ({sequence_type} sequence)')
    plt.xticks(x, all_labels, rotation=70, fontsize=8)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Calculate fidelity vs original
    try:
        fidelity = calculate_distribution_fidelity(original_counts, dd_counts)
        plt.figtext(0.5, 0.01, f"Fidelity (vs Original): {fidelity:.4f}", ha="center", fontsize=12)
    except Exception as e:
         print(f"Could not calculate fidelity for DD plot: {e}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_path = os.path.join(results_dir, f"dd_comparison_{sequence_type}_{timestamp}.png")
    try:
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {fig_path}")
    except Exception as save_err:
        print(f"Error saving DD comparison plot: {save_err}")
    finally:
        plt.close()
