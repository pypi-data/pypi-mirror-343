"""
Stochastic Measurement Error Mitigation and Unified Reconstruction (MEMSAUR) Integration

This module provides integration between different error mitigation approaches and
circuit partitioning strategies for executing large quantum circuits on real hardware.

Key features:
- Unified interface for different error mitigation techniques
- Integration with circuit partitioning for systems beyond available hardware
- Stochastic sampling approaches for improved error estimation
- Hardware-aware optimization of mitigation strategies

Author: Quantum-AI Team
"""

import logging
import numpy as np
from typing import Dict, List, Tuple, Union, Optional, Callable, Any

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Measure
from qiskit.result import Result
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session, Options
from qiskit.primitives import SamplerResult
from qiskit.providers.basic_provider import BasicSimulator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("stochastic_memsaur")

class MEMSAURIntegrator:
    """
    Integration class for Measurement Error Mitigation and Unified Reconstruction (MEMSAUR).
    
    This class provides a framework to execute potentially large quantum circuits 
    on simulators or real quantum hardware by combining:
    1.  **Circuit Partitioning:** Breaking down circuits that exceed hardware qubit
        limits into smaller, executable partitions using various strategies.
    2.  **Measurement Error Mitigation (MEM):** Applying techniques to correct for 
        errors introduced during the measurement process.
    3.  **(Future/Intended):** Integration with quantum memory management (see 
        `quantum_toolkit.memory.memsaur`) for handling intermediate states, although 
        direct integration points are not explicitly implemented within this class currently.

    It supports both simulation (currently mocked) and execution via Qiskit Runtime.
    
    Attributes:
        service (Optional[QiskitRuntimeService]): Service object for IBM Quantum.
        simulator_mode (bool): Flag to run in simulation or hardware mode.
        mem_method (str): The chosen measurement error mitigation method.
        max_qubits_per_partition (int): Qubit limit for partitioning.
        region_size (int): Size parameter for regional MEM.
        stochastic_sampling (bool): Flag for using stochastic sampling (usage TBD).
        sampling_ratio (float): Ratio for stochastic sampling.
        random_seed (int): Seed for reproducibility.
        backend (Optional[BackendV1 | BackendV2]): Selected Qiskit backend object.
        backend_info (Dict): Information about the selected backend.
    """
    
    def __init__(
        self, 
        service: Optional[QiskitRuntimeService] = None,
        simulator_mode: bool = False,
        mem_method: str = "tensor_product", # Can be "tensor_product", "regional", "zero_noise", "auto"
        max_qubits_per_partition: int = 127,
        region_size: int = 25,
        stochastic_sampling: bool = True,
        sampling_ratio: float = 0.1,
        random_seed: int = 42
    ):
        """
        Initializes the MEMSAURIntegrator.
        
        Sets up configuration parameters for execution mode, partitioning, 
        error mitigation method, and backend connection.
        
        Args:
            service: QiskitRuntimeService instance for connecting to IBM Quantum. 
                     Required if `simulator_mode` is False.
            simulator_mode: If True, runs in simulation mode (currently mocked execution).
                            If False, attempts to connect to real hardware via `service`.
            mem_method: The measurement error mitigation method to use. 
                        Options: "tensor_product" (implemented), "regional" (placeholder), 
                        "zero_noise" (placeholder), "auto" (chooses based on size).
            max_qubits_per_partition: The maximum number of qubits allowed in a single 
                                      circuit partition. Also used as the limit in 
                                      simulator_mode if partitioning occurs.
            region_size: Parameter defining the size of qubit regions for the 
                         "regional" MEM method (currently placeholder).
            stochastic_sampling: If True, enables stochastic sampling (intended use 
                                 case within mitigation needs clarification).
            sampling_ratio: The ratio of shots to potentially use for stochastic 
                            sampling calibration.
            random_seed: Seed for numpy's random number generator for reproducibility.
        """
        # Validate mem_method
        valid_methods = ["tensor_product", "regional", "zero_noise", "auto"]
        if mem_method not in valid_methods:
            raise ValueError(f"Invalid mem_method '{mem_method}'. Valid options are: {valid_methods}")
        # Remove diagnostic logging
        # logger.warning(f"MEMSAURIntegrator __init__ called. Received simulator_mode={simulator_mode}, service={'provided' if service else 'None'}")
        self.service = service
        self.simulator_mode = simulator_mode
        self.mem_method = mem_method
        self.max_qubits_per_partition = max_qubits_per_partition
        self.region_size = region_size
        self.stochastic_sampling = stochastic_sampling
        self.sampling_ratio = sampling_ratio
        self.random_seed = random_seed
        
        # Set random seed
        np.random.seed(self.random_seed)
        
        # Initialize backend information
        self.backend = None
        self.backend_info = {}
        
        logger.info(f"Initialized MEMSAUR with {mem_method} mitigation method")
        if stochastic_sampling:
            logger.info(f"Using stochastic sampling with ratio {sampling_ratio}")
        # Remove diagnostic logging
        # logger.warning(f"MEMSAURIntegrator __init__ finished. Assigned self.simulator_mode={self.simulator_mode}")
    
    def select_backend(self, min_qubits: int = 5, custom_filters: Optional[Dict] = None) -> str:
        """
        Select the best backend based on requirements.
        
        Args:
            min_qubits: Minimum number of qubits required
            custom_filters: Additional filters for backend selection
        
        Returns:
            Name of the selected backend
        """
        if self.simulator_mode:
            logger.info("Running in simulator mode, no backend selection needed")
            return "simulator"
        
        if not self.service:
            raise ValueError("QiskitRuntimeService is required for backend selection")
        
        logger.info(f"Selecting backend with at least {min_qubits} qubits")
        
        # Get available backends
        backends = []
        for backend in self.service.backends():
            try:
                backend_qubits = backend.configuration().n_qubits
                if backend_qubits >= min_qubits:
                    # Calculate a simple score based on error rates (simplified)
                    score = 0.5 + 0.5 * np.random.random()  # Mock score for now
                    
                    backends.append({
                        'name': backend.name,
                        'qubits': backend_qubits,
                        'score': score,
                        'backend': backend
                    })
            except Exception as e:
                logger.warning(f"Error checking backend {backend.name}: {e}")
        
        if not backends:
            raise ValueError(f"No backends found with at least {min_qubits} qubits")
        
        # Sort by score (higher is better)
        backends.sort(key=lambda x: x['score'], reverse=True)
        
        # Select the best backend
        selected = backends[0]
        self.backend = selected['backend']
        
        logger.info(f"Selected backend: {selected['name']} with {selected['qubits']} qubits (score: {selected['score']:.4f})")
        
        return selected['name']
    
    def partition_circuit(self, circuit: QuantumCircuit, circuit_type: Optional[str] = None) -> List[Dict]:
        """
        Partition a quantum circuit if it's too large for the selected backend.
        
        Args:
            circuit: Circuit to partition
            circuit_type: Type of circuit for specialized partitioning
        
        Returns:
            List of partitioned circuits with mapping information
        """
        if not self.backend and not self.simulator_mode:
            raise ValueError("No backend selected. Call select_backend() first.")
        
        # Get maximum qubits available
        if self.simulator_mode:
            max_available_qubits = self.max_qubits_per_partition
        else:
            if not self.backend:
                raise ValueError("Backend object is None, cannot determine available qubits for partitioning.")
            max_available_qubits = self.backend.configuration().n_qubits
        
        # Check if partitioning is needed
        if circuit.num_qubits <= max_available_qubits:
            logger.info(f"No partitioning needed for {circuit.num_qubits}-qubit circuit")
            return [{
                "circuit": circuit,
                "qubit_mapping": {i: i for i in range(circuit.num_qubits)}
            }]
        
        logger.info(f"Partitioning {circuit.num_qubits}-qubit circuit for {max_available_qubits}-qubit backend")
        
        # Analyze circuit structure
        partitioning_strategy = self._analyze_circuit_for_partitioning(
            circuit, max_available_qubits, circuit_type
        )
        
        # Apply appropriate partitioning strategy
        if partitioning_strategy == "ghz":
            partitioned_circuits = self._partition_ghz_circuit(circuit, max_available_qubits)
        elif partitioning_strategy == "qft":
            partitioned_circuits = self._partition_qft_circuit(circuit, max_available_qubits)
        else:
            partitioned_circuits = self._partition_general_circuit(circuit, max_available_qubits)
        
        logger.info(f"Created {len(partitioned_circuits)} partitions")
        
        return partitioned_circuits
    
    def _analyze_circuit_for_partitioning(
        self, circuit: QuantumCircuit, max_qubits: int, circuit_type: Optional[str] = None
    ) -> str:
        """
        Analyzes a quantum circuit's structure to determine an optimal partitioning strategy.

        Uses heuristics based on circuit name hints or entanglement structure derived
        from two-qubit gates.

        Strategies:
        - Checks `circuit_type` hint first (e.g., "ghz", "qft").
        - Builds an entanglement graph from two-qubit gates.
        - Checks for GHZ-like structure (high connectivity to a central qubit).
        - Checks for QFT-like structure (sequential nearest-neighbor interactions).
        - Defaults to "general" if no specific structure is detected.

        Args:
            circuit: The qiskit.QuantumCircuit to analyze.
            max_qubits: The maximum number of qubits allowed per partition (used in heuristics).
            circuit_type: An optional string hint (case-insensitive) for the circuit type 
                          (e.g., "ghz", "bell", "qft", "fourier").
        
        Returns:
            A string representing the suggested partitioning strategy: "ghz", "qft", or "general".
        """
        # If circuit type is provided, use that
        if circuit_type:
            if circuit_type.lower() in ["ghz", "bell"]:
                return "ghz"
            elif circuit_type.lower() in ["qft", "fourier"]:
                return "qft"
        
        # Analyze circuit structure
        entanglement_graph = {}
        
        # Build entanglement graph from two-qubit gates
        for instruction in circuit.data:
            if len(instruction[1]) == 2:
                q1, q2 = instruction[1][0].index, instruction[1][1].index
                
                if q1 not in entanglement_graph:
                    entanglement_graph[q1] = set()
                if q2 not in entanglement_graph:
                    entanglement_graph[q2] = set()
                    
                entanglement_graph[q1].add(q2)
                entanglement_graph[q2].add(q1)
        
        # Check for GHZ-like structure (star topology with central qubit)
        if entanglement_graph:
            # Check if one qubit is connected to many others
            connections = [len(connections) for q, connections in entanglement_graph.items()]
            max_connections = max(connections) if connections else 0
            
            if max_connections > circuit.num_qubits * 0.4:
                return "ghz"
        
        # Check for QFT-like structure (sequential interactions)
        qft_pattern = True
        for i in range(circuit.num_qubits - 1):
            if i not in entanglement_graph or i+1 not in entanglement_graph:
                qft_pattern = False
                break
            if i+1 not in entanglement_graph[i]:
                qft_pattern = False
                break
        
        if qft_pattern:
            return "qft"
        
        # Default to general partitioning
        return "general"
    
    def _partition_ghz_circuit(self, circuit: QuantumCircuit, max_qubits: int) -> List[Dict]:
        """
        Partitions a circuit assumed to have a GHZ-like structure.

        Assumes qubit 0 is the central control qubit. Creates partitions where each 
        contains the control qubit and a subset of the target qubits, up to `max_qubits`.

        The generated partition circuits are simplified representations containing only 
        the H gate on the control and CNOTs to the targets within that partition, 
        followed by measurement. The original circuit's internal gates are **not** preserved
        in these simplified partition circuits.

        Args:
            circuit: The input QuantumCircuit (assumed GHZ-like).
            max_qubits: The maximum number of qubits allowed in each partition circuit.
        
        Returns:
            A list of dictionaries, each representing a partition:
            - "circuit": A simplified qiskit.QuantumCircuit for the partition (H + CNOTs + Measure).
            - "qubit_mapping": Dictionary mapping local partition indices to original indices.
        """
        total_qubits = circuit.num_qubits
        # Assume qubit 0 is the control in GHZ-like circuits
        control_qubit = 0
        
        # Calculate how many partitions we need
        # Each partition includes the control qubit plus some target qubits
        num_partitions = (total_qubits - 1 + max_qubits - 2) // (max_qubits - 1)
        
        partitioned_circuits = []
        
        for i in range(num_partitions):
            # Calculate which target qubits go in this partition
            start_idx = 1 + i * (max_qubits - 1)
            end_idx = min(start_idx + max_qubits - 1, total_qubits)
            partition_qubits = [control_qubit] + list(range(start_idx, end_idx))
            
            # Create new circuit for this partition
            num_qubits_in_partition = len(partition_qubits)
            partition_circuit = QuantumCircuit(num_qubits_in_partition, num_qubits_in_partition)
            
            # Add Hadamard to control qubit
            partition_circuit.h(0)
            
            # Add CNOT gates from control to each target in this partition
            for j in range(1, num_qubits_in_partition):
                partition_circuit.cx(0, j)
                
            # Add measurements
            partition_circuit.measure_all()
            
            # Store mapping information for recombining results
            qubit_mapping = {j: partition_qubits[j] for j in range(num_qubits_in_partition)}
            
            partitioned_circuits.append({
                "circuit": partition_circuit,
                "qubit_mapping": qubit_mapping
            })
        
        return partitioned_circuits
    
    def _partition_qft_circuit(self, circuit: QuantumCircuit, max_qubits: int) -> List[Dict]:
        """
        Partitions a circuit assumed to have a QFT-like structure.

        Uses a simple block-based partitioning approach, dividing the qubits sequentially 
        into blocks of size up to `max_qubits`.

        The generated partition circuits are simplified representations containing only 
        Hadamards and controlled-phase rotations *within* that partition block, 
        followed by measurement. Interactions between blocks from the original circuit 
        are **not** preserved in these simplified partition circuits.

        Args:
            circuit: The input QuantumCircuit (assumed QFT-like).
            max_qubits: The maximum number of qubits allowed in each partition block.
        
        Returns:
            A list of dictionaries, each representing a partition:
            - "circuit": A simplified qiskit.QuantumCircuit for the partition (H + local CPs + Measure).
            - "qubit_mapping": Dictionary mapping local partition indices to original indices.
        """
        total_qubits = circuit.num_qubits
        
        # For QFT, we use a block-based approach
        num_partitions = (total_qubits + max_qubits - 1) // max_qubits
        
        partitioned_circuits = []
        
        for i in range(num_partitions):
            # Calculate qubits for this partition
            start_idx = i * max_qubits
            end_idx = min(start_idx + max_qubits, total_qubits)
            partition_qubits = list(range(start_idx, end_idx))
            
            # Create circuit for this partition
            num_qubits_in_partition = len(partition_qubits)
            partition_circuit = QuantumCircuit(num_qubits_in_partition, num_qubits_in_partition)
            
            # Add Hadamard gates to all qubits
            for j in range(num_qubits_in_partition):
                partition_circuit.h(j)
            
            # Add controlled phase rotations within this partition
            for j in range(num_qubits_in_partition):
                for k in range(j+1, num_qubits_in_partition):
                    partition_circuit.cp(np.pi / (2 ** (k-j)), j, k)
            
            # Add measurements
            partition_circuit.measure_all()
            
            # Store mapping information
            qubit_mapping = {j: partition_qubits[j] for j in range(num_qubits_in_partition)}
            
            partitioned_circuits.append({
                "circuit": partition_circuit,
                "qubit_mapping": qubit_mapping
            })
        
        return partitioned_circuits
    
    def _partition_general_circuit(self, circuit: QuantumCircuit, max_qubits: int) -> List[Dict]:
        """
        Partitions a general circuit using a basic greedy graph partitioning approach.

        1. Builds an interaction graph based on multi-qubit gates in the `circuit`.
        2. Greedily assigns qubits to partitions, trying to keep connected qubits together,
           until `max_qubits` limit is reached or all qubits are assigned.

        NOTE: This implementation currently creates **empty** QuantumCircuits for each 
        partition. It only determines the qubit groupings (`qubit_mapping`). 
        The logic to map the original circuit's instructions onto these partitions 
        is missing and needs to be implemented for this method to be functional.

        Args:
            circuit: The input QuantumCircuit.
            max_qubits: The maximum number of qubits allowed per partition.
        
        Returns:
            A list of dictionaries, each representing a partition:
            - "circuit": An **empty** qiskit.QuantumCircuit for the partition.
            - "qubit_mapping": Dictionary mapping local partition indices to original indices.
        """
        total_qubits = circuit.num_qubits
        
        # Build interaction graph
        interaction_graph = {}
        for i in range(total_qubits):
            interaction_graph[i] = set()
            
        for instruction in circuit.data:
            # Look at multi-qubit gates to build the interaction graph
            if len(instruction[1]) > 1:
                qubits = [q.index for q in instruction[1]]
                for i in range(len(qubits)):
                    for j in range(i+1, len(qubits)):
                        interaction_graph[qubits[i]].add(qubits[j])
                        interaction_graph[qubits[j]].add(qubits[i])
        
        # Simple greedy partitioning
        partitions = []
        remaining_qubits = set(range(total_qubits))
        
        while remaining_qubits:
            # Start a new partition
            current_partition = []
            
            # Pick a seed qubit with minimal interactions
            if not current_partition:
                seed = min(remaining_qubits, 
                           key=lambda q: len(interaction_graph[q] & remaining_qubits))
                current_partition.append(seed)
                remaining_qubits.remove(seed)
            
            # Grow the partition
            while len(current_partition) < max_qubits and remaining_qubits:
                # Find qubit with most connections to current partition
                best_qubit = None
                best_connections = -1
                
                for qubit in remaining_qubits:
                    connections = sum(1 for q in current_partition if qubit in interaction_graph[q])
                    if connections > best_connections:
                        best_connections = connections
                        best_qubit = qubit
                
                if best_qubit is not None:
                    current_partition.append(best_qubit)
                    remaining_qubits.remove(best_qubit)
                else:
                    # If no connections, take any remaining qubit
                    next_qubit = next(iter(remaining_qubits))
                    current_partition.append(next_qubit)
                    remaining_qubits.remove(next_qubit)
            
            partitions.append(sorted(current_partition))
        
        # Create subcircuits for each partition
        partitioned_circuits = []
        
        for partition in partitions:
            num_qubits_in_partition = len(partition)
            partition_circuit = QuantumCircuit(num_qubits_in_partition, num_qubits_in_partition)
            
            # Map from original qubit index -> local qubit index within this partition
            local_qubit_map = {original: i for i, original in enumerate(partition)}
            
            # Iterate over the instructions of the original circuit and add
            # to this sub‑circuit any gate that is **fully contained** within the
            # current partition.
            # NOTE: Inter‑partition operations (i.e., multi‑qubit gates that span
            # more than one partition) are **ignored** by this basic splitter.
            for inst, qargs, cargs in circuit.data:
                q_indices = [q.index for q in qargs]
                # Skip instructions that touch qubits outside this partition
                if not set(q_indices).issubset(partition):
                    continue
                
                # Build local qubit list for the instruction
                local_qargs = [partition_circuit.qubits[local_qubit_map[q_idx]] for q_idx in q_indices]
                
                # Handle measurement separately so that we map classical bits
                if inst.name == "measure":
                    # We assume 1‑to‑1 qubit‑>clbit mapping for measurement
                    if len(q_indices) != 1 or len(cargs) != 1:
                        # Complex measurement patterns currently unsupported
                        continue
                    classical_idx = local_qubit_map[q_indices[0]]
                    partition_circuit.measure(local_qargs[0], classical_idx)
                else:
                    # For all other gates, simply append with copied params
                    partition_circuit.append(inst.copy(), local_qargs, [])
            
            # Ensure at least measurement exists so results can be read out
            if not any(instr.operation.name == "measure" for instr in partition_circuit.data):
                partition_circuit.measure_all()
            
            # Store mapping information
            qubit_mapping = {i: partition[i] for i in range(num_qubits_in_partition)}
            
            partitioned_circuits.append({
                "circuit": partition_circuit,
                "qubit_mapping": qubit_mapping
            })
        
        return partitioned_circuits
    
    def generate_mem_circuits(self, circuit: QuantumCircuit) -> Tuple[List[QuantumCircuit], str]:
        """
        Generates calibration circuits required for the chosen measurement error mitigation method.

        Selects the MEM method based on `self.mem_method` (or uses "auto" logic based 
        on `num_qubits`) and calls the corresponding private generation method.

        Args:
            circuit: The target QuantumCircuit for which mitigation is needed. 
                     Its size influences the "auto" method selection and is used by 
                     some generation methods (e.g., the placeholder zero_noise).
        
        Returns:
            A tuple containing:
            - List[QuantumCircuit]: The list of generated calibration circuits.
            - str: The name of the mitigation method that was actually used 
              (e.g., "tensor_product", "regional", "zero_noise").

        Raises:
            ValueError: If `self.mem_method` is set to an unknown value.
        """
        num_qubits = circuit.num_qubits
        
        # Choose mitigation method based on circuit size
        method_used = self.mem_method
        if method_used == "auto":
            if num_qubits <= 50:
                method_used = "tensor_product"
            else:
                method_used = "regional"
        
        logger.info(f"Generating calibration circuits using {method_used} method")
        
        if method_used == "tensor_product":
            # Simple tensor product approach
            cal_circuits = self._generate_tensor_product_circuits(num_qubits)
        elif method_used == "regional":
            # Regional approach for larger systems
            cal_circuits = self._generate_regional_circuits(num_qubits)
        elif method_used == "zero_noise":
            # Zero-noise extrapolation approach
            cal_circuits = self._generate_zero_noise_circuits(circuit)
        else:
            raise ValueError(f"Unknown mitigation method: {method_used}")
        
        logger.info(f"Generated {len(cal_circuits)} calibration circuits")
        
        return cal_circuits, method_used
    
    def _generate_tensor_product_circuits(self, num_qubits: int) -> List[QuantumCircuit]:
        """
        Generates calibration circuits for the tensor product measurement error mitigation method.

        Creates circuits to prepare and measure each qubit individually in the |0> and |1> 
        states. For circuits larger than 5 qubits, it also adds circuits preparing 
        nearest-neighbor pairs in the |11> state to capture some correlation information 
        (limited to the first 5 pairs for efficiency).

        Args:
            num_qubits: The number of qubits in the target circuit.
        
        Returns:
            A list of qiskit.QuantumCircuit objects for calibration.
        """
        cal_circuits = []
        
        # Generate |0⟩ and |1⟩ state preparation for each qubit
        for q_idx in range(num_qubits):
            # |0⟩ state circuit
            q0_circuit = QuantumCircuit(num_qubits, num_qubits)
            q0_circuit.measure_all()
            cal_circuits.append(q0_circuit)
            
            # |1⟩ state circuit
            q1_circuit = QuantumCircuit(num_qubits, num_qubits)
            q1_circuit.x(q_idx)
            q1_circuit.measure_all()
            cal_circuits.append(q1_circuit)
        
        # Add overlap circuits for capturing correlations
        if num_qubits > 5:
            # Limit to 5 neighbor pairs for efficiency
            for i in range(min(num_qubits-1, 5)):
                # Adjacent qubits in |11⟩ state
                nn_circuit = QuantumCircuit(num_qubits, num_qubits)
                nn_circuit.x(i)
                nn_circuit.x(i+1)
                nn_circuit.measure_all()
                cal_circuits.append(nn_circuit)
        
        return cal_circuits
    
    def _generate_regional_circuits(self, num_qubits: int) -> List[QuantumCircuit]:
        """
        Generates calibration circuits for the regional measurement error mitigation method.

        NOTE: The mitigation logic (`_apply_regional_mitigation`) currently falls back 
        to the tensor product method. This generation function reflects a potential 
        regional approach but may not be optimally used by the current mitigation logic.

        1. Divides qubits into regions using `_create_qubit_regions`.
        2. For each region, generates |0> and |1> preparation circuits for qubits 
           within that region.
        3. Adds nearest-neighbor |11> state preparations within each region (limited pairs).

        Args:
            num_qubits: The number of qubits in the target circuit.
        
        Returns:
            A list of qiskit.QuantumCircuit objects for regional calibration.
        """
        # Create regions
        regions = self._create_qubit_regions(num_qubits)
        
        # Generate calibration circuits for each region
        all_circuits = []
        
        for region in regions:
            region_qubits = region["qubits"]
            
            # Generate |0⟩ and |1⟩ state preparation for each qubit in this region
            for q_idx in region_qubits:
                # |0⟩ state circuit
                q0_circuit = QuantumCircuit(num_qubits, num_qubits)
                q0_circuit.measure_all()
                all_circuits.append(q0_circuit)
                
                # |1⟩ state circuit
                q1_circuit = QuantumCircuit(num_qubits, num_qubits)
                q1_circuit.x(q_idx)
                q1_circuit.measure_all()
                all_circuits.append(q1_circuit)
            
            # Add some nearest-neighbor calibration circuits
            region_size = len(region_qubits)
            if region_size > 5:
                for i in range(min(region_size-1, 5)):
                    if i+1 < region_size:
                        nn_circuit = QuantumCircuit(num_qubits, num_qubits)
                        nn_circuit.x(region_qubits[i])
                        nn_circuit.x(region_qubits[i+1])
                        nn_circuit.measure_all()
                        all_circuits.append(nn_circuit)
        
        return all_circuits
    
    def _generate_zero_noise_circuits(self, circuit: QuantumCircuit) -> List[QuantumCircuit]:
        """
        Generates circuits for Zero-Noise Extrapolation (ZNE) measurement error mitigation.

        NOTE: This is currently a **placeholder** implementation. It returns copies
        of the original circuit but does **not** implement noise amplification 
        (e.g., by gate folding/insertion) required for actual ZNE.
        The corresponding mitigation logic (`_apply_zero_noise_mitigation`) is also
        a placeholder.

        Args:
            circuit: The base QuantumCircuit.
        
        Returns:
            A list containing copies of the input circuit. This needs to be replaced
            with circuits implementing varying levels of noise amplification.
        """
        # Simplified implementation of zero-noise extrapolation
        # We create copies of the circuit with noise "amplification"
        
        cal_circuits = []
        
        # Add the original circuit
        cal_circuits.append(circuit.copy())
        
        # Create a 2x noise circuit (insert identity pairs to double gate count)
        noise_2x = circuit.copy()
        
        # Create a 3x noise circuit
        noise_3x = circuit.copy()
        
        return cal_circuits
    
    def _create_qubit_regions(self, num_qubits: int) -> List[Dict]:
        """
        Divides the total number of qubits into roughly equal-sized regions.

        Used by the `_generate_regional_circuits` method.
        
        Args:
            num_qubits: The total number of qubits.
        
        Returns:
            A list of dictionaries, where each dictionary represents a region and contains:
            - "name": A string identifier for the region (e.g., "region_0").
            - "qubits": A list of integer qubit indices belonging to that region.
        """
        # Simple implementation: divide qubits into regions of roughly equal size
        region_size = self.region_size
        num_regions = (num_qubits + region_size - 1) // region_size
        
        regions = []
        for i in range(num_regions):
            start_idx = i * region_size
            end_idx = min(start_idx + region_size, num_qubits)
            
            regions.append({
                "name": f"region_{i}",
                "qubits": list(range(start_idx, end_idx))
            })
        
        return regions
    
    def execute_circuits(
        self, 
        circuits: List[Union[QuantumCircuit, Dict]],
        shots: int = 4096,
        optimize_level: int = 1
    ) -> Dict:
        """
        Executes a list of quantum circuits, handling partitioning and measurement error mitigation.

        This is the main entry point for running computations with MEMSAUR.

        Workflow:
        1. Processes the input `circuits` list, which can contain QuantumCircuit objects
           or partition dictionaries (from `partition_circuit`).
        2. Iterates through each circuit (or partition):
           a. Generates necessary calibration circuits (`generate_mem_circuits`).
           b. Executes the main circuit and calibration circuits using either the
              mock simulator (`_simulate_circuit`) or real hardware (`_execute_on_hardware`).
           c. Applies the chosen error mitigation method (`_apply_error_mitigation`).
        3. If the execution involved partitions, combines the mitigated results from 
           each partition (`_combine_partitioned_results`).
        
        Args:
            circuits: A list where each element is either a qiskit.QuantumCircuit or a 
                      dictionary representing a partition (containing "circuit" and 
                      "qubit_mapping" keys).
            shots: The number of measurement shots to execute for each circuit 
                   (main and calibration).
            optimize_level: The Qiskit transpiler optimization level to use when 
                            executing on hardware.
        
        Returns:
            A dictionary containing the results. 
            - If partitions were used: {"combined": combined_counts_dict, "partitions": [list_of_partition_results]}
            - If no partitioning: {"results": [list_of_individual_circuit_results]}
            Each result dictionary typically includes mitigated "counts", "raw_counts", 
            and the "method" used.

        Raises:
            ValueError: If the input `circuits` list is empty or contains invalid formats.
            ValueError: If hardware execution is attempted without providing `service`
                        or selecting a `backend`.
        """
        # Handle cases where circuits are provided directly or as partition dictionaries
        circuit_list = []
        partition_info = []
        
        for item in circuits:
            if isinstance(item, QuantumCircuit):
                circuit_list.append(item)
                partition_info.append(None)
            elif isinstance(item, dict) and "circuit" in item:
                circuit_list.append(item["circuit"])
                partition_info.append(item.get("qubit_mapping", None))
            else:
                raise ValueError("Invalid circuit format provided")
        
        # Check if we have circuits to execute
        if not circuit_list:
            raise ValueError("No circuits provided for execution")
        
        results = []
        
        # Execute each circuit separately with error mitigation
        for i, (circuit, partition) in enumerate(zip(circuit_list, partition_info)):
            # Remove diagnostic logging
            # logger.warning(f"Executing circuit {i+1}/{len(circuit_list)}. Simulator mode check: {self.simulator_mode}")
            
            logger.info(f"Executing circuit {i+1}/{len(circuit_list)}")
            
            # Generate calibration circuits
            cal_circuits, method = self.generate_mem_circuits(circuit)
            
            # Execute circuit with calibration
            # Remove diagnostic logging
            # logger.info(f"Inside execute_circuits: self.simulator_mode = {self.simulator_mode}") 
            if self.simulator_mode:
                # Simplified simulation
                circuit_result = self._simulate_circuit(circuit, shots)
                cal_results = [self._simulate_circuit(c, shots) for c in cal_circuits]
            else:
                # Execute on real hardware
                # Add safeguard: Ensure service and backend exist before calling hardware execution
                if not self.service or not self.backend:
                     logger.error("Hardware execution path entered incorrectly (simulator_mode might be unexpectedly False or service/backend missing).")
                     # Raise error to highlight the logic issue
                     raise ValueError("Hardware execution requires service and backend, but they are missing. Check simulator_mode flag.")
                
                circuit_result, cal_results = self._execute_on_hardware(
                    circuit, cal_circuits, shots, optimize_level
                )
            
            # Apply error mitigation
            mitigated_result = self._apply_error_mitigation(
                circuit_result, cal_results, method, circuit.num_qubits, shots
            )
            
            # Add partition information if available
            if partition:
                mitigated_result["partition_map"] = partition
            
            results.append(mitigated_result)
        
        # If these were partitioned circuits, combine the results
        if all(p is not None for p in partition_info) and len(circuit_list) > 1:
            logger.info("Combining results from partitioned circuits")
            total_qubits = sum(len(p) for p in partition_info if p)
            combined_result = self._combine_partitioned_results(results, total_qubits)
            return {"combined": combined_result, "partitions": results}
        
        return {"results": results}
    
    def _simulate_circuit(self, circuit: QuantumCircuit, shots: int) -> Dict:
        """
        Simplified stub simulation: returns a dummy count for the zero bitstring of the circuit.
        """
        logger.debug(f"Stub simulating circuit with {circuit.num_qubits} qubits for {shots} shots.")
        bitstring = '0' * circuit.num_qubits
        counts = {bitstring: shots}
        return {"counts": counts}
    
    def _execute_on_hardware(
        self, 
        circuit: QuantumCircuit, 
        cal_circuits: List[QuantumCircuit],
        shots: int,
        optimize_level: int
    ) -> Tuple[Dict, List[Dict]]:
        """
        Executes a main circuit and its calibration circuits on IBM Quantum hardware.

        Uses the QiskitRuntimeService and the selected backend (`self.backend`) to 
        submit the circuits as a single job using the Sampler primitive within a Session.

        Args:
            circuit: The main qiskit.QuantumCircuit to execute.
            cal_circuits: A list of calibration circuits for error mitigation.
            shots: The number of measurement shots.
            optimize_level: The Qiskit transpiler optimization level.
        
        Returns:
            A tuple containing:
            - Dict: Result dictionary for the main circuit, e.g., {"counts": {...}}.
            - List[Dict]: A list of result dictionaries for the calibration circuits.
            Returns ({}, []) if an error occurs during execution.

        Raises:
            ValueError: If `self.service` or `self.backend` is not set.
        """
        if not self.service or not self.backend:
            raise ValueError("QiskitRuntimeService and backend required for hardware execution")
        
        # Ensure backend name is accessible
        backend_name = self.backend.name

        try:
            # Transpile all circuits
            transpiled_circuit = transpile(
                circuit, backend=self.backend, optimization_level=optimize_level
            )
            transpiled_cal_circuits = [
                transpile(c, backend=self.backend, optimization_level=optimize_level)
                for c in cal_circuits
            ]
            
            all_circuits = [transpiled_circuit] + transpiled_cal_circuits
            
            # Create a runtime Session using the selected backend.
            # Passing only the backend avoids stub mismatches on parameter order.
            # `type: ignore` added to suppress static type checker complaints stemming
            # from incomplete third‑party stubs.
            with Session(self.backend) as session:  # type: ignore[arg-type]
                # Instantiate a Sampler bound to this session
                sampler = Sampler(session)  # type: ignore[arg-type]
                
                # Run with specified shots
                logger.info(f"Running circuit {getattr(transpiled_circuit, 'name', 'Unnamed')} on AerSimulator with {shots} shots")
                # Pass the single circuit as a list to the run method
                # This might address issues where Aer processes single circuits differently
                job = sampler.run([transpiled_circuit], shots=shots)
                result = job.result()
                # Get counts for the first (and only) circuit in the list result
                counts = result.get_counts(0)
            
            # Process results
            quasi_dists = result.quasi_dists
            
            # Convert to counts format
            main_counts = {
                format(k, f"0{circuit.num_qubits}b"): int(v * shots) 
                for k, v in quasi_dists[0].items()
            }
            
            cal_counts = []
            for i, dist in enumerate(quasi_dists[1:]):
                cal_count = {
                    format(k, f"0{cal_circuits[i].num_qubits}b"): int(v * shots) 
                    for k, v in dist.items()
                }
                cal_counts.append({"counts": cal_count})
            
            return {"counts": main_counts}, cal_counts
            
        except Exception as e:
            logger.error(f"Error executing on hardware: {e}")
            # Return empty results in case of error
            return {"counts": {}}, []
    
    def _apply_error_mitigation(
        self,
        result: Dict,
        cal_results: List[Dict],
        method: str,
        num_qubits: int,
        shots: int
    ) -> Dict:
        """
        Applies the specified measurement error mitigation method to the results.

        Takes the raw execution result (counts) and the results from calibration
        circuits, then calls the appropriate private mitigation function based on
        the `method` string.

        Args:
            result: The result dictionary from circuit execution (must contain "counts").
            cal_results: A list of result dictionaries from the calibration circuit executions.
            method: The name of the mitigation method used ("tensor_product", "regional", "zero_noise").
            num_qubits: The number of qubits in the circuit.
            shots: The number of shots used in the execution.
        
        Returns:
            A dictionary containing the mitigated results, typically including:
            - "counts": The mitigated counts dictionary.
            - "raw_counts": The original counts dictionary before mitigation.
            - "method": The name of the mitigation method applied.
            Returns the original `result` dictionary if an error occurs or counts are missing.
        """
        try:
            # Extract counts
            if "counts" not in result:
                logger.warning("No counts found in result")
                return result
            
            raw_counts = result["counts"]
            
            # Apply mitigation based on the method
            if method == "tensor_product":
                mitigated_counts = self._apply_tensor_product_mitigation(
                    raw_counts, cal_results, num_qubits, shots
                )
            elif method == "regional":
                mitigated_counts = self._apply_regional_mitigation(
                    raw_counts, cal_results, num_qubits, shots
                )
            elif method == "zero_noise":
                mitigated_counts = self._apply_zero_noise_mitigation(
                    raw_counts, cal_results, num_qubits, shots
                )
            else:
                logger.warning(f"Unknown mitigation method: {method}")
                mitigated_counts = raw_counts
            
            # Combine results
            return {
                "counts": mitigated_counts,
                "raw_counts": raw_counts,
                "method": method
            }
            
        except Exception as e:
            logger.error(f"Error in error mitigation: {e}")
            return result
    
    def _apply_tensor_product_mitigation(
        self,
        counts: Dict[str, int],
        cal_results: List[Dict],
        num_qubits: int,
        shots: int
    ) -> Dict[str, int]:
        """
        Applies tensor product measurement error mitigation.

        1. Constructs a 2x2 calibration matrix for each qubit based on the results
           of running |0> and |1> state preparation circuits (`cal_results`).
        2. Calculates the inverse of each per-qubit calibration matrix.
        3. Iterates through the raw `counts` and applies the inverse tensor product
           of the calibration matrices to estimate the "true" counts before measurement
           noise.
        4. Cleans the resulting distribution (removes small/negative probabilities) and
           normalizes back to the original number of shots.

        Args:
            counts: The raw measurement counts dictionary.
            cal_results: List of calibration results (expects 2*num_qubits results for 
                         |0>, |1> preps at the beginning).
            num_qubits: The number of qubits.
            shots: The total number of shots.
        
        Returns:
            The mitigated counts dictionary.
            Returns original `counts` if calibration results are insufficient or an error occurs.
        """
        # Extract per-qubit mitigation matrices from calibration results
        qubit_matrices = []
        
        # Number of cal circuits should be 2*num_qubits plus some overlap circuits
        if len(cal_results) < 2 * num_qubits:
            logger.warning("Insufficient calibration results for tensor product MEM")
            return counts
        
        try:
            # Process calibration circuits for individual qubits
            for q_idx in range(num_qubits):
                # Get calibration results for this qubit
                q0_result = cal_results[2*q_idx]
                q1_result = cal_results[2*q_idx + 1]
                
                # Extract counts
                if "counts" not in q0_result or "counts" not in q1_result:
                    logger.warning(f"Missing counts in calibration result for qubit {q_idx}")
                    continue
                
                q0_counts = q0_result["counts"]
                q1_counts = q1_result["counts"]
                
                # Build 2x2 mitigation matrix for this qubit
                matrix = np.zeros((2, 2))
                
                # Calculate probabilities for measuring 0 or 1 when preparing |0⟩
                p_meas_0_given_0 = sum(count for bitstring, count in q0_counts.items() 
                                    if bitstring[q_idx] == '0') / shots
                p_meas_1_given_0 = sum(count for bitstring, count in q0_counts.items() 
                                    if bitstring[q_idx] == '1') / shots
                
                # Calculate probabilities for measuring 0 or 1 when preparing |1⟩
                p_meas_0_given_1 = sum(count for bitstring, count in q1_counts.items() 
                                    if bitstring[q_idx] == '0') / shots
                p_meas_1_given_1 = sum(count for bitstring, count in q1_counts.items() 
                                    if bitstring[q_idx] == '1') / shots
                
                # Fill the matrix
                matrix[0, 0] = p_meas_0_given_0
                matrix[0, 1] = p_meas_1_given_0
                matrix[1, 0] = p_meas_0_given_1
                matrix[1, 1] = p_meas_1_given_1
                
                # Handle potential singularity or numerical issues
                if np.linalg.det(matrix) < 1e-10:
                    matrix += np.identity(2) * 1e-10
                
                # Calculate inverse for mitigation
                inv_matrix = np.linalg.inv(matrix)
                qubit_matrices.append(inv_matrix)
            
            # Apply tensor product mitigation
            mitigated_counts = {}
            
            # For each observed bitstring
            for bitstring, count in counts.items():
                # Convert to list of 0s and 1s
                bit_list = [int(b) for b in bitstring.zfill(num_qubits)]
                
                # For each possible "true" bitstring
                for true_bits in range(2**num_qubits):
                    true_bitstring = format(true_bits, f'0{num_qubits}b')
                    true_bit_list = [int(b) for b in true_bitstring]
                    
                    # Calculate product of transition probabilities
                    prob = 1.0
                    for q_idx in range(num_qubits):
                        # Skip if we don't have a matrix for this qubit
                        if q_idx >= len(qubit_matrices):
                            continue
                        # Mitigation matrix: inv_matrix[true_bit][measured_bit]
                        prob *= qubit_matrices[q_idx][true_bit_list[q_idx], bit_list[q_idx]]
                    
                    # Accumulate mitigated counts
                    if true_bitstring in mitigated_counts:
                        mitigated_counts[true_bitstring] += count * prob
                    else:
                        mitigated_counts[true_bitstring] = count * prob
            
            # Clean up mitigated counts - remove negative and tiny values
            cleaned_counts = {}
            for bitstring, count in mitigated_counts.items():
                if count > 0.5:  # Only keep substantial counts
                    cleaned_counts[bitstring] = count
            
            # Normalize to maintain total shots
            total_mitigated = sum(cleaned_counts.values())
            if total_mitigated > 0:
                normalization_factor = shots / total_mitigated
                normalized_counts = {b: int(count * normalization_factor) for b, count in cleaned_counts.items()}
                return normalized_counts
            else:
                return counts  # Fallback if mitigation fails
                
        except Exception as e:
            logger.error(f"Error in tensor product MEM: {e}")
            return counts  # Return original counts on error
    
    def _apply_regional_mitigation(
        self,
        counts: Dict[str, int],
        cal_results: List[Dict],
        num_qubits: int,
        shots: int
    ) -> Dict[str, int]:
        """
        Applies regional measurement error mitigation.

        NOTE: This is currently a **placeholder**. It simply calls the 
        `_apply_tensor_product_mitigation` method. A proper implementation would 
        use the regional calibration data (`_generate_regional_circuits`) to 
        potentially build denser calibration matrices for each region or use other
        regional mitigation techniques.

        Args:
            counts: Raw measurement counts.
            cal_results: Calibration circuit results (intended for regional analysis).
            num_qubits: Number of qubits.
            shots: Total shots.
        
        Returns:
            Mitigated counts (currently using tensor product method).
        """
        # Simple implementation that falls back to tensor product MEM
        return self._apply_tensor_product_mitigation(counts, cal_results, num_qubits, shots)
    
    def _apply_zero_noise_mitigation(
        self,
        counts: Dict[str, int],
        cal_results: List[Dict],
        num_qubits: int,
        shots: int
    ) -> Dict[str, int]:
        """
        Applies zero-noise extrapolation (ZNE) mitigation to counts.

        NOTE: This is currently a **placeholder** implementation. It applies a 
        heuristic (boosting the highest probability outcome, reducing others) and 
        does **not** perform proper ZNE based on results from circuits with 
        amplified noise levels (as generated by the placeholder 
        `_generate_zero_noise_circuits`). This requires a complete rewrite to 
        implement actual ZNE fitting and extrapolation.

        Args:
            counts: Raw measurement counts from the base circuit.
            cal_results: Calibration circuit results (intended to be results from 
                         circuits with different noise levels for ZNE).
            num_qubits: Number of qubits.
            shots: Total shots.
        
        Returns:
            Mitigated counts dictionary (currently using mock logic).
            Returns original `counts` if calibration results are missing or an error occurs.
        """
        # Simple implementation that adds some noise reduction
        # For a real implementation, this would use zero-noise extrapolation techniques
        
        if not cal_results or len(cal_results) < 2:
            return counts
        
        try:
            # For demonstration purposes, we'll just boost the highest count
            # and reduce the others to simulate error mitigation
            
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            highest_bitstring = sorted_counts[0][0] if sorted_counts else None
            
            if not highest_bitstring:
                return counts
            
            mitigated_counts = {}
            
            for bitstring, count in counts.items():
                if bitstring == highest_bitstring:
                    # Boost the highest count
                    mitigated_counts[bitstring] = int(count * 1.2)
                else:
                    # Reduce other counts
                    reduced_count = int(count * 0.8)
                    if reduced_count > 0:
                        mitigated_counts[bitstring] = reduced_count
            
            # Normalize to maintain total shots
            total_mitigated = sum(mitigated_counts.values())
            normalization_factor = shots / total_mitigated if total_mitigated > 0 else 1
            
            normalized_counts = {b: int(count * normalization_factor) for b, count in mitigated_counts.items()}
            
            return normalized_counts
            
        except Exception as e:
            logger.error(f"Error in zero-noise MEM: {e}")
            return counts
    
    def _combine_partitioned_results(self, results: List[Dict], total_qubits: int) -> Dict:
        """
        Combines mitigated results from multiple circuit partitions into a single result dictionary.

        Iterates through the results list, where each item corresponds to a partition 
        and contains mitigated counts and a qubit mapping.
        It reconstructs the full bitstring for each outcome in each partition using the
        mapping and aggregates the counts for identical full bitstrings.
        Finally, it normalizes the combined counts to match the original total shots.

        Args:
            results: A list of result dictionaries, one for each partition. Each dictionary
                     must contain "counts" and a "partition_map" (the qubit mapping).
            total_qubits: The total number of qubits in the original, unpartitioned circuit.
        
        Returns:
            A dictionary containing the combined counts for the full system.
        """
        # Initialize combined counts
        combined_counts = {}
        
        # Get total shots from first result
        total_shots = sum(results[0].get("counts", {}).values()) if results else 0
        
        # Process each partition's results
        for result in results:
            counts = result.get("counts", {})
            partition_map = result.get("partition_map", {})
            
            if not partition_map:
                logger.warning("Missing partition mapping information")
                continue
            
            # For each outcome in this partition
            for bitstring, count in counts.items():
                # Create a full-sized bitstring initialized to '0's
                full_bitstring = ['0'] * total_qubits
                
                # Map each bit from the partition result to its place in the full bitstring
                for local_idx, bit in enumerate(bitstring.zfill(len(partition_map))):
                    if local_idx in partition_map:
                        original_idx = partition_map[local_idx]
                        if original_idx < total_qubits:
                            full_bitstring[original_idx] = bit
                
                # Convert list to string
                full_bitstring = ''.join(full_bitstring)
                
                # Add to combined counts
                if full_bitstring in combined_counts:
                    combined_counts[full_bitstring] += count
                else:
                    combined_counts[full_bitstring] = count
        
        # Normalize the combined counts to match expected total shots
        if total_shots > 0:
            current_total = sum(combined_counts.values())
            if current_total > 0:
                scale = total_shots / current_total
                normalized_counts = {k: int(v * scale) for k, v in combined_counts.items()}
                return normalized_counts
        
        return combined_counts 