"""
Quantum Circuit Implementations for Portfolio Optimization

This module provides quantum circuit implementations for portfolio optimization
using QAOA (Quantum Approximate Optimization Algorithm) and VQE (Variational 
Quantum Eigensolver) approaches.
"""

from typing import List, Dict, Tuple, Optional, Any
import numpy as np
import logging

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter

# Attempt to import from various possible locations based on Qiskit version
try:
    # New structure (Qiskit 1.0+)
    from qiskit.algorithms.minimum_eigensolvers import QAOA, VQE
    from qiskit.algorithms.optimizers import COBYLA, SPSA
except ImportError:
    try:
        # Direct imports (might work across multiple versions)
        from qiskit.algorithms import QAOA, VQE
        from qiskit.algorithms.optimizers import COBYLA, SPSA
    except ImportError:
        try:
            # Old structure (pre-1.0)
            from qiskit.algorithms.minimum_eigen import QAOA, VQE
            from qiskit.algorithms.optimizers import COBYLA, SPSA
        except ImportError:
            # Very old structure with underscores
            try:
                from qiskit_algorithms.minimum_eigen import QAOA, VQE
                from qiskit_algorithms.optimizers import COBYLA, SPSA
            except ImportError:
                # If all imports fail, use stubs for compatibility
                # This allows the module to load but functions will raise NotImplementedError
                class DummyClass:
                    def __init__(self, *args, **kwargs):
                        raise NotImplementedError("Required Qiskit components not available")
                
                QAOA = VQE = COBYLA = SPSA = DummyClass

from qiskit.quantum_info import Pauli, SparsePauliOp

logger = logging.getLogger(__name__)

class PortfolioOptimizationCircuits:
    """Quantum circuit implementations for portfolio optimization."""
    
    def __init__(self,
                 num_assets: int,
                 returns: np.ndarray,
                 risk_aversion: float = 1.0,
                 quantum_instance: Optional[Any] = None):
        """
        Initialize portfolio optimization circuits.
        
        Args:
            num_assets: Number of assets in portfolio
            returns: Historical returns matrix
            risk_aversion: Risk aversion parameter
            quantum_instance: Optional Qiskit quantum instance
        """
        self.num_assets = num_assets
        self.returns = returns
        self.risk_aversion = risk_aversion
        self.quantum_instance = quantum_instance
        
        # Calculate covariance matrix
        self.cov_matrix = np.cov(returns.T)
        self.expected_returns = np.mean(returns, axis=0)
        
        # Initialize circuit parameters
        self.num_qubits = self._calculate_required_qubits()
        self.qaoa_depth = 3  # Start with 3 layers
        
        logger.info(f"Initialized PortfolioOptimizationCircuits with {num_assets} assets")
        
    def _calculate_required_qubits(self) -> int:
        """Calculate number of qubits needed for encoding the problem."""
        # We need at least num_assets qubits to encode portfolio weights
        # Plus some ancilla qubits for intermediate calculations
        return self.num_assets + 2
        
    def create_qaoa_circuit(self) -> Tuple[QuantumCircuit, List[Parameter]]:
        """
        Create QAOA circuit for portfolio optimization.
        
        Returns:
            Tuple of (quantum circuit, list of parameters)
        """
        # Create quantum registers
        qr = QuantumRegister(self.num_qubits, 'q')
        cr = ClassicalRegister(self.num_assets, 'c')
        circuit = QuantumCircuit(qr, cr)
        
        # Parameters for QAOA
        gammas = [Parameter(f'γ_{i}') for i in range(self.qaoa_depth)]
        betas = [Parameter(f'β_{i}') for i in range(self.qaoa_depth)]
        
        # Initial state preparation - equal superposition
        circuit.h(qr[:self.num_assets])
        
        # QAOA layers
        for layer in range(self.qaoa_depth):
            # Problem unitary (phase separation)
            self._add_cost_operator(circuit, qr, gammas[layer])
            
            # Mixing unitary
            self._add_mixing_operator(circuit, qr, betas[layer])
        
        # Measurement
        circuit.measure(qr[:self.num_assets], cr)
        
        return circuit, gammas + betas
        
    def _add_cost_operator(self, 
                          circuit: QuantumCircuit,
                          qr: QuantumRegister,
                          gamma: Parameter) -> None:
        """Add cost operator to circuit."""
        # Encode expected returns
        for i in range(self.num_assets):
            angle = gamma * self.expected_returns[i]
            circuit.rz(angle, qr[i])
        
        # Encode risk (covariance matrix)
        for i in range(self.num_assets):
            for j in range(i+1, self.num_assets):
                angle = gamma * self.risk_aversion * self.cov_matrix[i,j]
                circuit.rzz(angle, qr[i], qr[j])
                
    def _add_mixing_operator(self,
                           circuit: QuantumCircuit,
                           qr: QuantumRegister,
                           beta: Parameter) -> None:
        """Add mixing operator to circuit."""
        for i in range(self.num_assets):
            circuit.rx(2 * beta, qr[i])
            
    def create_vqe_circuit(self) -> Tuple[QuantumCircuit, List[Parameter]]:
        """
        Create VQE circuit for portfolio optimization.
        
        Returns:
            Tuple of (quantum circuit, list of parameters)
        """
        # Create quantum registers
        qr = QuantumRegister(self.num_qubits, 'q')
        cr = ClassicalRegister(self.num_assets, 'c')
        circuit = QuantumCircuit(qr, cr)
        
        # Parameters for variational form
        theta = [Parameter(f'θ_{i}') for i in range(self.num_assets * 2)]
        
        # Initial state preparation
        for i in range(self.num_assets):
            circuit.ry(theta[i], qr[i])
            circuit.rz(theta[i + self.num_assets], qr[i])
            
        # Add entangling layers
        for i in range(self.num_assets - 1):
            circuit.cx(qr[i], qr[i+1])
            
        # Add final rotation layer
        for i in range(self.num_assets):
            circuit.ry(theta[i], qr[i])
            
        # Measurement
        circuit.measure(qr[:self.num_assets], cr)
        
        return circuit, theta
        
    def optimize_portfolio(self, method: str = 'qaoa') -> Dict[str, Any]:
        """
        Optimize portfolio using specified quantum method.
        
        Args:
            method: Either 'qaoa' or 'vqe'
            
        Returns:
            Dictionary with optimization results
        """
        if method.lower() == 'qaoa':
            circuit, parameters = self.create_qaoa_circuit()
            optimizer = SPSA(maxiter=100)
        else:
            circuit, parameters = self.create_vqe_circuit()
            optimizer = COBYLA(maxiter=100)
            
        # Create cost Hamiltonian
        cost_hamiltonian = self._create_cost_hamiltonian()
        
        # Run quantum optimization
        if method.lower() == 'qaoa':
            qaoa = QAOA(optimizer=optimizer,
                       quantum_instance=self.quantum_instance,
                       initial_point=[0.1] * len(parameters))
            result = qaoa.compute_minimum_eigenvalue(cost_hamiltonian)
        else:
            vqe = VQE(ansatz=circuit,
                      optimizer=optimizer,
                      quantum_instance=self.quantum_instance,
                      initial_point=[0.1] * len(parameters))
            result = vqe.compute_minimum_eigenvalue(cost_hamiltonian)
            
        # Extract optimal portfolio weights
        optimal_bitstring = max(result.eigenstate, key=result.eigenstate.get)
        weights = self._bitstring_to_weights(optimal_bitstring)
        
        return {
            'weights': weights,
            'optimal_value': result.optimal_value,
            'optimal_parameters': result.optimal_point,
            'cost_function_evals': result.cost_function_evals
        }
        
    def _create_cost_hamiltonian(self) -> SparsePauliOp:
        """Create cost Hamiltonian for the optimization problem."""
        # Initialize empty Hamiltonian
        hamiltonian = SparsePauliOp.from_list([("I" * self.num_qubits, 0.0)])
        
        # Add expected returns terms
        for i in range(self.num_assets):
            pauli_str = ["I"] * self.num_qubits
            pauli_str[i] = "Z"
            hamiltonian += SparsePauliOp.from_list(
                [(("".join(pauli_str)), -self.expected_returns[i])]
            )
            
        # Add risk terms
        for i in range(self.num_assets):
            for j in range(i+1, self.num_assets):
                pauli_str = ["I"] * self.num_qubits
                pauli_str[i] = "Z"
                pauli_str[j] = "Z"
                hamiltonian += SparsePauliOp.from_list(
                    [(("".join(pauli_str)), 
                      self.risk_aversion * self.cov_matrix[i,j])]
                )
                
        return hamiltonian
        
    def _bitstring_to_weights(self, bitstring: str) -> List[float]:
        """Convert measurement bitstring to portfolio weights."""
        # Convert binary string to weights between 0 and 1
        weights = [int(bit) for bit in bitstring[:self.num_assets]]
        total = sum(weights)
        if total == 0:
            return [1.0 / self.num_assets] * self.num_assets
        return [w / total for w in weights] 