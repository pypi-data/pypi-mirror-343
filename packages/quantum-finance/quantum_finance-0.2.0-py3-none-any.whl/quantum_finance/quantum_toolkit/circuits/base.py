"""
Quantum Circuits Module

This module provides a unified interface for creating and manipulating quantum circuits.
It combines functionality from multiple implementations while maintaining backward compatibility.
"""

import numpy as np
import random
from typing import Optional, List, Tuple, Dict
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
import logging

# Configure logging
logger = logging.getLogger(__name__)

def create_bell_state(add_measurement: bool = True) -> QuantumCircuit:
    """
    Creates a Bell state quantum circuit.
    
    Args:
        add_measurement (bool): Whether to add measurement operations
    
    Returns:
        QuantumCircuit: Quantum circuit representing the Bell state
    """
    # Create quantum registers
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c') if add_measurement else None
    qc = QuantumCircuit(qr, cr) if cr else QuantumCircuit(qr)
    
    # Apply Hadamard gate to the first qubit to create superposition
    qc.h(0)
    
    # Apply CNOT gate with control qubit 0 and target qubit 1 to entangle qubits
    qc.cx(0, 1)
    
    # Add measurements if requested
    if add_measurement:
        qc.measure(qr, cr)
    
    logger.debug("Created Bell state circuit")
    return qc

def create_ghz_state(num_qubits: int, add_measurement: bool = True) -> QuantumCircuit:
    """
    Creates a GHZ state circuit (generalized Bell state for multiple qubits).
    
    Args:
        num_qubits (int): Number of qubits in the GHZ state
        add_measurement (bool): Whether to add measurement operations
    
    Returns:
        QuantumCircuit: Quantum circuit implementing the GHZ state
    
    Raises:
        ValueError: If num_qubits < 2
    """
    if num_qubits < 2:
        raise ValueError("GHZ state requires at least 2 qubits")
    
    # Create quantum registers
    qr = QuantumRegister(num_qubits, 'q')
    cr = ClassicalRegister(num_qubits, 'c') if add_measurement else None
    qc = QuantumCircuit(qr, cr) if cr else QuantumCircuit(qr)
    
    # Apply Hadamard to the first qubit
    qc.h(0)
    
    # Apply CNOT gates to create the GHZ state
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    
    # Add measurements if requested
    if add_measurement:
        qc.measure(qr, cr)
    
    logger.debug(f"Created GHZ state circuit with {num_qubits} qubits")
    return qc

def create_w_state(num_qubits: int, add_measurement: bool = True) -> QuantumCircuit:
    """
    Creates a W state circuit.
    
    The W state is a quantum state of n qubits where exactly one qubit is in state |1⟩
    and all others are in state |0⟩, in an equal superposition. For example, for 3 qubits:
    |W⟩ = (|100⟩ + |010⟩ + |001⟩)/√3
    
    This implementation uses a recursive approach with explicit rotations and controlled operations
    to create a W state that works reliably across different Qiskit versions.
    
    Args:
        num_qubits (int): Number of qubits in the W state
        add_measurement (bool): Whether to add measurement operations
    
    Returns:
        QuantumCircuit: Quantum circuit implementing the W state
    
    Raises:
        ValueError: If num_qubits < 2
    """
    if num_qubits < 2:
        raise ValueError("W state requires at least 2 qubits")
    
    # Import necessary Qiskit components
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    import numpy as np
    
    # Create quantum registers
    qr = QuantumRegister(num_qubits, 'q')
    if add_measurement:
        cr = ClassicalRegister(num_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
    else:
        qc = QuantumCircuit(qr)
    
    # Use a named circuit to help with debugging
    qc.name = f"w_state_{num_qubits}"
    
    # Base cases
    if num_qubits == 2:
        # This is the most reliable way to create a 2-qubit W state
        # First set qubit 0 to |1⟩
        qc.x(0)
        # Apply Hadamard to create superposition
        qc.h(0)
        # Apply CNOT to entangle the qubits
        qc.cx(0, 1)
        # Apply X to the first qubit to get the W state
        qc.x(0)
        # The resulting state is (|01⟩ + |10⟩)/√2
    else:
        # For 3+ qubits, use a recursive approach
        
        # First set qubit 0 to |1⟩
        qc.x(0)
        
        # Calculate and apply rotation to distribute amplitude correctly
        theta = 2 * np.arccos(np.sqrt(1 / num_qubits))
        qc.ry(theta, 0)
        
        # Flip first qubit for controlled operation
        qc.x(0)
        
        # Recursively build W-state for remaining qubits
        sub_circuit = create_w_state(num_qubits - 1, False)
        sub_gate = sub_circuit.to_gate(label=f"W_{num_qubits-1}")
        controlled_gate = sub_gate.control(1)
        
        # Apply controlled W-state operation on remaining qubits
        qc.append(controlled_gate, [0] + list(range(1, num_qubits)))
        
        # Restore first qubit
        qc.x(0)
    
    # Add measurement operations if requested
    if add_measurement:
        qc.measure(qr, cr)
    
    return qc

def create_quantum_fourier_transform(num_qubits: int, add_measurement: bool = True) -> QuantumCircuit:
    """
    Creates a Quantum Fourier Transform (QFT) circuit.
    
    This implementation uses Qiskit's built-in QFT implementation
    to avoid deprecation warnings and ensure optimal implementation.
    
    Args:
        num_qubits (int): Number of qubits in the QFT
        add_measurement (bool): Whether to add measurement operations
    
    Returns:
        QuantumCircuit: Quantum circuit implementing the QFT
        
    Raises:
        ValueError: If num_qubits < 1
    """
    if num_qubits < 1:
        raise ValueError("QFT requires at least 1 qubit")
    
    # Create quantum registers
    qr = QuantumRegister(num_qubits, 'q')
    cr = ClassicalRegister(num_qubits, 'c') if add_measurement else None
    
    # Create circuit using Qiskit's QFT implementation with decomposition to basic gates
    # This ensures compatibility with the simulator
    qft = QFT(num_qubits, do_swaps=True, inverse=False, insert_barriers=True).decompose()
    
    # Create the full circuit with registers
    qc = QuantumCircuit(qr, cr) if cr else QuantumCircuit(qr)
    
    # Append the decomposed QFT circuit to our circuit
    qc.compose(qft, inplace=True)
    
    # Add measurements if requested
    if add_measurement:
        qc.measure(qr, cr)
    
    logger.debug(f"Created QFT circuit with {num_qubits} qubits")
    return qc

def create_inverse_quantum_fourier_transform(num_qubits: int, add_measurement: bool = True) -> QuantumCircuit:
    """
    Creates an Inverse Quantum Fourier Transform (IQFT) circuit.
    
    This implementation uses Qiskit's built-in QFT implementation with inverse=True
    to avoid deprecation warnings and ensure optimal implementation.
    
    Args:
        num_qubits (int): Number of qubits in the IQFT
        add_measurement (bool): Whether to add measurement operations
    
    Returns:
        QuantumCircuit: Quantum circuit implementing the IQFT
        
    Raises:
        ValueError: If num_qubits < 1
    """
    if num_qubits < 1:
        raise ValueError("IQFT requires at least 1 qubit")
    
    # Create quantum registers
    qr = QuantumRegister(num_qubits, 'q')
    cr = ClassicalRegister(num_qubits, 'c') if add_measurement else None
    
    # Create circuit using Qiskit's QFT implementation with inverse=True and decomposition
    iqft = QFT(num_qubits, do_swaps=True, inverse=True, insert_barriers=True).decompose()
    
    # Create the full circuit with registers
    qc = QuantumCircuit(qr, cr) if cr else QuantumCircuit(qr)
    
    # Append the decomposed IQFT circuit to our circuit
    qc.compose(iqft, inplace=True)
    
    # Add measurements if requested
    if add_measurement:
        qc.measure(qr, cr)
    
    logger.debug(f"Created IQFT circuit with {num_qubits} qubits")
    return qc

def create_random_circuit(
    num_qubits: int,
    depth: int = 3,
    seed: Optional[int] = None,
    add_measurement: bool = True
) -> QuantumCircuit:
    """
    Creates a random quantum circuit.
    
    Args:
        num_qubits (int): Number of qubits
        depth (int): Circuit depth parameter
        seed (Optional[int]): Random seed for reproducibility
        add_measurement (bool): Whether to add measurement operations
    
    Returns:
        QuantumCircuit: A random quantum circuit
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Create quantum registers
    qr = QuantumRegister(num_qubits, 'q')
    cr = ClassicalRegister(num_qubits, 'c') if add_measurement else None
    qc = QuantumCircuit(qr, cr) if cr else QuantumCircuit(qr)
    
    # Available gates
    single_qubit_gates = [
        lambda circ, q: circ.h(q),
        lambda circ, q: circ.x(q),
        lambda circ, q: circ.y(q),
        lambda circ, q: circ.z(q),
        lambda circ, q: circ.s(q),
        lambda circ, q: circ.t(q),
        lambda circ, q: circ.rx(np.random.uniform(0, 2*np.pi), q),
        lambda circ, q: circ.ry(np.random.uniform(0, 2*np.pi), q),
        lambda circ, q: circ.rz(np.random.uniform(0, 2*np.pi), q),
    ]
    
    two_qubit_gates = [
        lambda circ, q1, q2: circ.cx(q1, q2),
        lambda circ, q1, q2: circ.cz(q1, q2),
        lambda circ, q1, q2: circ.swap(q1, q2),
    ]
    
    # Apply random gates for the specified depth
    for _ in range(depth):
        # Apply single-qubit gates
        for i in range(num_qubits):
            gate = random.choice(single_qubit_gates)
            gate(qc, qr[i])
        
        # Apply two-qubit gates to random pairs
        for _ in range(num_qubits // 2):
            i, j = random.sample(range(num_qubits), 2)
            gate = random.choice(two_qubit_gates)
            gate(qc, qr[i], qr[j])
    
    # Add measurements if requested
    if add_measurement:
        qc.measure(qr, cr)
    
    logger.debug(f"Created random circuit with {num_qubits} qubits and depth {depth}")
    return qc

def run_circuit_simulation(
    circuit: QuantumCircuit,
    shots: int = 1000,
    optimization_level: int = 1
) -> Dict[str, int]:
    """
    Executes a quantum circuit simulation with enhanced error handling.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit to simulate
        shots (int): Number of shots for the simulation
        optimization_level (int): Circuit optimization level (0-3)
    
    Returns:
        Dict[str, int]: Measurement counts from the simulation
    """
    # Import necessary Qiskit components
    import importlib
    import numpy as np
    
    # Ensure the circuit has measurements
    if not hasattr(circuit, 'num_clbits') or not circuit.num_clbits:
        print("Adding measurements to circuit")
        circuit.measure_all()
    
    # Print the circuit for debugging
    print(f"Circuit to simulate:\n{circuit}")
    
    # Initialize variables
    simulator = None
    transpile_func = None
    
    # Try to import transpile function
    try:
        from qiskit import transpile
        transpile_func = transpile
    except ImportError as e:
        print(f"Could not import transpile from qiskit: {str(e)}")
        # Try alternative import if available
        try:
            from qiskit.compiler import transpile
            transpile_func = transpile
        except ImportError:
            print("Could not import transpile from qiskit.compiler")
    
    # Find available simulator backend
    # Try multiple options in order of preference
    simulation_approaches = [
        # Approach 1: qiskit_aer.AerSimulator (newer versions)
        {
            'module': 'qiskit_aer',
            'class': 'AerSimulator',
            'args': [],
            'kwargs': {}
        },
        # Approach 2: qiskit.Aer.get_backend('qasm_simulator') (older versions)
        {
            'module': 'qiskit',
            'class': 'Aer',
            'method': 'get_backend',
            'args': ['qasm_simulator']
        },
        # Approach 3: qiskit.providers.aer.QasmSimulator (alternative)
        {
            'module': 'qiskit.providers.aer',
            'class': 'QasmSimulator',
            'args': [],
            'kwargs': {}
        },
        # Approach 4: qiskit.BasicAer.get_backend('qasm_simulator') (basic)
        {
            'module': 'qiskit',
            'class': 'BasicAer',
            'method': 'get_backend',
            'args': ['qasm_simulator']
        },
        # Approach 5: qiskit.providers.BasicAer.get_backend('qasm_simulator') (alternative path)
        {
            'module': 'qiskit.providers.basic_provider',
            'class': 'BasicProvider',
            'instantiate': True,
            'method': 'get_backend',
            'args': ['basic_simulator']
        }
    ]
    
    # Try each simulation approach until one works
    for approach in simulation_approaches:
        try:
            module = importlib.import_module(approach['module'])
            if 'class' in approach:
                sim_class = getattr(module, approach['class'])
                
                if approach.get('instantiate', False):
                    # Instantiate the class first
                    sim_instance = sim_class()
                    if 'method' in approach:
                        # Call method on instance
                        simulator = getattr(sim_instance, approach['method'])(*approach.get('args', []))
                    else:
                        simulator = sim_instance
                else:
                    if 'method' in approach:
                        # Call static method on class
                        simulator = getattr(sim_class, approach['method'])(*approach.get('args', []))
                    else:
                        # Instantiate the class directly
                        simulator = sim_class(*approach.get('args', []), **approach.get('kwargs', {}))
            
            if simulator:
                print(f"Successfully created simulator using {approach['module']}.{approach['class']}")
                break
                
        except (ImportError, AttributeError) as e:
            print(f"Could not use simulation approach {approach['module']}: {str(e)}")
    
    # If we still don't have a simulator, raise an error
    if simulator is None:
        raise RuntimeError("No suitable quantum simulator found. Please check your Qiskit installation.")
    
    # If we don't have a transpile function, we can't proceed
    if transpile_func is None:
        raise RuntimeError("Transpile function not found. Please check your Qiskit installation.")
    
    # Transpile the circuit for the simulator
    print("Transpiling circuit...")
    try:
        transpiled_circuit = transpile_func(circuit, simulator, optimization_level=optimization_level)
        print(f"Transpiled circuit:\n{transpiled_circuit}")
    except Exception as e:
        print(f"Error during transpilation: {str(e)}. Using original circuit.")
        transpiled_circuit = circuit
    
    # Execute the circuit
    print(f"Running simulation with {shots} shots...")
    try:
        job = simulator.run(transpiled_circuit, shots=shots)
        result = job.result()
        
        # Get the counts
        try:
            counts = result.get_counts(transpiled_circuit)
        except Exception as e1:
            print(f"Error getting counts with transpiled circuit: {str(e1)}")
            try:
                # Try without specifying the circuit
                counts = result.get_counts()
            except Exception as e2:
                print(f"Error getting counts without specifying circuit: {str(e2)}")
                # Last resort: try to extract counts from raw data if available
                try:
                    raw_data = result.data()
                    if hasattr(raw_data, 'counts'):
                        counts = raw_data.counts
                    else:
                        raise ValueError("No counts found in result data")
                except Exception as e3:
                    print(f"Error extracting counts from result data: {str(e3)}")
                    raise RuntimeError("Could not obtain measurement counts from simulation result")
        
    except Exception as sim_error:
        print(f"Error during simulation: {str(sim_error)}")
        
        # Try statevector simulation as an alternative approach
        print("Attempting statevector simulation as alternative...")
        try:
            # Find a statevector simulator
            sv_simulator = None
            sv_approaches = [
                # Try qiskit_aer
                {'module': 'qiskit_aer', 'class': 'Aer', 'method': 'get_backend', 'args': ['statevector_simulator']},
                # Try qiskit Aer
                {'module': 'qiskit', 'class': 'Aer', 'method': 'get_backend', 'args': ['statevector_simulator']},
                # Try BasicAer
                {'module': 'qiskit', 'class': 'BasicAer', 'method': 'get_backend', 'args': ['statevector_simulator']}
            ]
            
            for approach in sv_approaches:
                try:
                    module = importlib.import_module(approach['module'])
                    sim_class = getattr(module, approach['class'])
                    if 'method' in approach:
                        sv_simulator = getattr(sim_class, approach['method'])(*approach.get('args', []))
                    else:
                        sv_simulator = sim_class(*approach.get('args', []), **approach.get('kwargs', {}))
                    
                    if sv_simulator is None:
                        raise RuntimeError("No statevector simulator found")
                    
                    # Create a copy of circuit without measurements for statevector sim
                    from qiskit import QuantumCircuit
                    sv_circuit = QuantumCircuit(circuit.num_qubits)
                    
                    # Copy all gates except measurements
                    for instruction, qargs, cargs in circuit.data:
                        if instruction.name != 'measure':
                            sv_circuit.append(instruction, qargs)
                    
                    # Run statevector simulation
                    sv_job = sv_simulator.run(transpile_func(sv_circuit, sv_simulator))
                    sv_result = sv_job.result()
                    
                    # Get the statevector
                    try:
                        statevector = sv_result.get_statevector(sv_circuit)
                    except:
                        try:
                            statevector = sv_result.get_statevector()
                        except:
                            # Try to extract from Qiskit 1.0 result object format
                            statevector = sv_result.data()['statevector']
                    
                    # Calculate probabilities from statevector
                    probs = np.abs(statevector) ** 2
                    
                    # Generate sampling from probabilities to simulate shots
                    import random
                    random.seed()  # Use system time as seed
                    
                    # Create list of states
                    states = [format(i, f'0{circuit.num_qubits}b') for i in range(2**circuit.num_qubits)]
                    
                    # Get cumulative probabilities for efficient sampling
                    cum_probs = np.cumsum(probs)
                    
                    # Sample according to probabilities
                    samples = []
                    for _ in range(shots):
                        r = random.random()  # Random number between 0 and 1
                        # Find the index where r fits in the cumulative distribution
                        for i, cp in enumerate(cum_probs):
                            if r < cp:
                                samples.append(states[i])
                                break
                    
                    # Count occurrences
                    counts = {}
                    for sample in samples:
                        if sample in counts:
                            counts[sample] += 1
                        else:
                            counts[sample] = 1
                    
                    print(f"Generated counts from statevector sampling: {counts}")
                    
                    return counts
                except Exception as sv_error:
                    print(f"Statevector approach also failed: {str(sv_error)}")
                    # No dummy fallback - raise the original error since we couldn't get valid results
                    raise RuntimeError(f"Failed to simulate circuit: {str(sim_error)}") from sim_error
        except Exception as sv_error:
            print(f"Statevector approach also failed: {str(sv_error)}")
            # No dummy fallback - raise the original error since we couldn't get valid results
            raise RuntimeError(f"Failed to simulate circuit: {str(sim_error)}") from sim_error
    
    # Print the counts for debugging
    print(f"Simulation counts: {counts}")
    
    # Ensure the counts are valid (not empty)
    if not counts:
        raise ValueError("Simulation produced empty counts")
    
    return counts

# Backward compatibility aliases
create_basic_circuit = create_bell_state
quantum_fourier_transform = create_quantum_fourier_transform
create_ghz_circuit = create_ghz_state
create_w_state_circuit = create_w_state

if __name__ == "__main__":
    # Example usage
    bell_circuit = create_bell_state()
    result = run_circuit_simulation(bell_circuit, shots=1000)
    print(f"Bell state measurement counts: {result}")
    
    # Test QFT
    qft_circuit = create_quantum_fourier_transform(3)
    qft_result = run_circuit_simulation(qft_circuit, shots=1000)
    print(f"QFT measurement counts: {qft_result}") 