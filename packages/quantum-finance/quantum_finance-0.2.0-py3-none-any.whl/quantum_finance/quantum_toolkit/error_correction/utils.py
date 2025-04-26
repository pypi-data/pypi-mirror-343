"""Utility functions for quantum error correction techniques."""

# Imports will be added here as functions are moved
import numpy as np
from typing import Dict, Mapping, Union, Any, Optional
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
# Need to import this for type hint, though it's used in get_ideal_expectation
from qiskit.primitives import Estimator as LocalEstimator 


def extract_v2_counts(pub_result, num_clbits: int) -> Dict[str, int]:
    """
    Extracts counts from a Qiskit Runtime V2 Sampler PUB result.
    Handles potential hexadecimal keys and dynamically finds the classical register data.

    Args:
        pub_result: A single PUB result object from a SamplerV2 job.result().
        num_clbits: The number of classical bits in the circuit, used for padding binary strings.

    Returns:
        A dictionary mapping binary measurement outcomes (str) to counts (int).
        Returns an empty dictionary if extraction fails.
    """
    counts = {}
    try:
        # Check if the PUB result has data
        if not hasattr(pub_result, 'data') or not pub_result.data:
            print("Warning (extract_v2_counts): PUB result has no 'data' attribute.")
            return {}
            
        # Find the first attribute within 'data' that looks like a DataBin object
        # (i.e., has a get_counts() method)
        data_bin = None
        for attr_name in dir(pub_result.data):
             if not attr_name.startswith('_'): # Skip private/protected attrs
                 attr = getattr(pub_result.data, attr_name, None)
                 if attr and callable(getattr(attr, 'get_counts', None)):
                      data_bin = attr
                      break # Use the first one found
                      
        if data_bin is None:
            print("Warning (extract_v2_counts): Could not find classical register data with get_counts() method.")
            return {}
            
        # Call get_counts() on the found DataBin object
        raw_counts = data_bin.get_counts()
        
        if not raw_counts:
            return {}

        # Check if keys are hexadecimal (start with '0x')
        first_key = next(iter(raw_counts.keys()))
        is_hex = first_key.startswith('0x')
        
        # Process counts: Convert hex to binary if needed, ensure consistent format
        processed_counts = {}
        for key, count in raw_counts.items():
            if is_hex:
                try:
                    # Convert hex string to integer
                    val = int(key, 16)
                    # Format integer as binary string, padding with zeros to num_clbits
                    bin_key = format(val, f'0{num_clbits}b')
                    processed_counts[bin_key] = count
                except ValueError:
                    print(f"Warning (extract_v2_counts): Could not convert supposed hex key '{key}' to int. Skipping.")
                    continue # Skip this key if conversion fails
            else:
                # Assume key is already binary or another format we accept directly
                # Optional: Add validation here to ensure key format is as expected (e.g., correct length binary)
                processed_counts[key] = count
        
        return processed_counts

    except Exception as e:
        print(f"Error during V2 counts extraction: {str(e)}")
        return {} # Return empty dict on error


def calculate_distribution_fidelity(
    counts1: Mapping[str, Union[int, float]], 
    counts2: Mapping[str, Union[int, float]]
) -> float:
    """
    Calculate the fidelity between two probability distributions represented by counts.
    Uses the Hellinger fidelity formula: F(P, Q) = (sum(sqrt(p_i * q_i)))^2
    
    Args:
        counts1: First measurement counts dictionary
        counts2: Second measurement counts dictionary
        
    Returns:
        Fidelity between the distributions (0 to 1)
    """
    # Convert to probability distributions
    total1 = sum(counts1.values())
    total2 = sum(counts2.values())
    
    # Handle cases where one or both counts dicts might be empty
    if total1 == 0 and total2 == 0:
        return 1.0 # Fidelity of empty distributions is 1
    if total1 == 0 or total2 == 0:
        return 0.0 # Fidelity with an empty distribution is 0
        
    # Get all possible bit strings
    all_bitstrings = set(list(counts1.keys()) + list(counts2.keys()))
    
    # Calculate the classical fidelity
    fidelity_term = 0.0
    for bs in all_bitstrings:
        p1 = counts1.get(bs, 0) / total1
        p2 = counts2.get(bs, 0) / total2
        fidelity_term += np.sqrt(p1 * p2)
    
    # Fidelity is the square of the sum of square roots of probabilities
    return fidelity_term ** 2


def get_ideal_counts(circuit: QuantumCircuit, shots: int) -> Dict[str, int]:
    """
    Get the ideal measurement counts for a circuit using a noiseless simulator.
    
    Args:
        circuit: Quantum circuit
        shots: Number of shots
        
    Returns:
        Ideal measurement counts
    """
    # Create a noiseless simulation
    simulator = AerSimulator()
    
    # Run the circuit
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts()
    
    return counts


def get_ideal_expectation(circuit: QuantumCircuit, observable: Any) -> float:
    """
    Get the ideal expectation value for a circuit and observable using a noiseless simulator.
    
    Args:
        circuit: Quantum circuit
        observable: Observable to measure
        
    Returns:
        Ideal expectation value
    """
    # Create a noiseless estimator for local simulation
    local_estimator = LocalEstimator() # Use the imported name
    # Correctly pass circuits and observables to Qiskit Estimator V1
    job = local_estimator.run(circuits=[circuit], observables=[observable])
    result = job.result()
    
    # Handle potential case where no value is returned
    if result.values is None or len(result.values) == 0:
        print("Warning: Ideal expectation estimation returned no values.")
        return np.nan # Return Not a Number if estimation failed
        
    return result.values[0]

# Placeholder for other potential utilities (e.g., plotting helpers) if needed
