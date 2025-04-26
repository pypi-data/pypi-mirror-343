from qiskit.circuit import QuantumCircuit  # Core circuit class
from qiskit import transpile  # Qiskit transpiler for circuit optimization
from qiskit.circuit.library import QFT  # Quantum Fourier Transform library circuit
from qiskit_aer import AerSimulator  # Aer simulator backend
from qiskit_aer.primitives import Sampler as LocalSampler  # Local sampler primitive (Qiskit 2.x)
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Sampler  # IBM Quantum runtime primitives

def create_bell_state():
    """
    Creates a Bell state quantum circuit.
    
    Returns:
        QuantumCircuit: Quantum circuit representing the Bell state.
    """
    # Create a quantum circuit with 2 qubits and 2 classical bits for measurement
    qc = QuantumCircuit(2, 2)
    
    # Apply Hadamard gate to the first qubit to create superposition
    qc.h(0)
    
    # Apply CNOT gate with control qubit 0 and target qubit 1 to entangle qubits
    qc.cx(0, 1)
    
    # Measure both qubits to collapse the state
    qc.measure([0, 1], [0, 1])
    
    return qc

def quantum_fourier_transform(n_qubits):
    """
    Creates a Quantum Fourier Transform circuit.
    
    Args:
        n_qubits (int): Number of qubits for the QFT
        
    Returns:
        QuantumCircuit: QFT circuit
    """
    qc = QFT(n_qubits)
    # Add measurement to all qubits
    cr = QuantumCircuit(n_qubits, n_qubits)
    cr.measure_all()
    return qc.compose(cr)

def run_qft_simulation(n_qubits, shots=1000):
    """
    Executes a Quantum Fourier Transform (QFT) simulation.
    
    Args:
        n_qubits (int): Number of qubits in the QFT circuit.
        shots (int): Number of simulation runs.
    
    Returns:
        dict: Measurement counts from the QFT simulation.
    """
    qft_circuit = quantum_fourier_transform(n_qubits)
    
    # Use Aer's qasm_simulator backend
    simulator = AerSimulator()
    
    # Execute the QFT circuit
    job = simulator.run(qft_circuit, shots=shots)
    result = job.result()
    
    # Return the measurement counts
    return result.get_counts(qft_circuit)

if __name__ == "__main__":
    # Create and run a Bell state circuit
    bell_state_circuit = create_bell_state()
    
    # Use Aer's qasm_simulator backend for simulation
    simulator = AerSimulator()
    
    # Execute the circuit on the simulator
    job = simulator.run(bell_state_circuit, shots=1000)
    
    # Retrieve the results of the simulation
    result = job.result()
    
    # Get the counts of measurement outcomes
    counts = result.get_counts(bell_state_circuit)
    print("Measurement counts:", counts)