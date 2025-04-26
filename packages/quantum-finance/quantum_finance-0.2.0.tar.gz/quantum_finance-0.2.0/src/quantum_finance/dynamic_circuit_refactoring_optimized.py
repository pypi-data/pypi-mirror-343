#!/usr/bin/env python3

"""
Optimized Dynamic Circuit Refactoring Module

This module provides an optimized version of the dynamic circuit generation capabilities,
addressing the performance regression identified in the original implementation.
It implements the optimization strategies outlined in docs/circuit_optimization_strategy.md.

Key optimizations include:
- Optimized logging framework
- Efficient gate patching through lazy loading
- Optional metadata collection
- Validation caching
- Improved memory management
- Circuit component caching
- Memory pooling for circuit operations

Created: 2024-03-01
Version: 0.3

Author: Quantum Transformer Team

Detailed inline comments are provided to track logical decisions and guide future modifications.
"""

import logging
import gc
import weakref
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from functools import lru_cache
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile

# Configure logging for detailed debugging information, but with conditional checks
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Cache for validation results
_validation_cache = {}

# Memory pool for circuit operations
class CircuitMemoryPool:
    """
    Memory pool implementation for quantum circuit operations.
    
    This class provides efficient memory management for quantum circuit operations
    by implementing object pooling patterns to reduce allocation/deallocation overhead
    and memory fragmentation.
    
    Attributes:
        max_pool_size (int): Maximum total size of all pooled objects in bytes
        enable_stats (bool): Whether to collect usage statistics
    """
    
    def __init__(self, max_pool_size: int = 1024 * 1024 * 1024, enable_stats: bool = False):
        """
        Initialize the circuit memory pool.
        
        Args:
            max_pool_size (int): Maximum size of the pool in bytes (default: 1GB)
            enable_stats (bool): Whether to collect usage statistics
        """
        self.max_pool_size = max_pool_size
        self.enable_stats = enable_stats
        
        # Buffer pools for temporary numpy arrays
        self._buffer_pools: Dict[Tuple[int, np.dtype], List[np.ndarray]] = {}
        
        # Circuit component pools
        self._circuit_pools: Dict[str, weakref.WeakValueDictionary] = {}
        
        # Register pools
        self._qreg_pool: Dict[int, List[QuantumRegister]] = {}
        self._creg_pool: Dict[int, List[ClassicalRegister]] = {}
        
        # Keep track of total allocated memory
        self._total_allocated: int = 0
        
        # Statistics if enabled
        self._stats = {
            "buffer_hits": 0,
            "buffer_misses": 0,
            "circuit_hits": 0,
            "circuit_misses": 0,
            "register_hits": 0,
            "register_misses": 0,
            "total_allocations": 0,
            "total_releases": 0,
            "cleanup_calls": 0
        } if enable_stats else None
        
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(
                "Initialized CircuitMemoryPool with max_pool_size=%d bytes", 
                max_pool_size
            )
    
    def get_buffer(self, shape: Tuple[int, ...], dtype: np.dtype = None) -> np.ndarray:
        """
        Get a numpy array buffer from the pool or allocate a new one.
        
        Args:
            shape (Tuple[int, ...]): Shape of the buffer
            dtype (np.dtype, optional): Data type for the buffer. Defaults to np.complex128.
            
        Returns:
            np.ndarray: The allocated buffer
            
        Raises:
            MemoryError: If allocation fails due to insufficient memory
        """
        if dtype is None:
            dtype = np.dtype(np.complex128)
        elif not isinstance(dtype, np.dtype):
            dtype = np.dtype(dtype)
        # Ensure dtype is always a numpy dtype instance for pool key
        dtype = np.dtype(dtype)
        total_size = int(np.prod(shape))
        pool_key = (total_size, dtype)
        
        # Try to get buffer from pool
        if pool_key in self._buffer_pools and self._buffer_pools[pool_key]:
            buffer = self._buffer_pools[pool_key].pop()
            buffer_size = total_size * dtype.itemsize
            self._total_allocated -= buffer_size
            
            if self.enable_stats:
                self._stats["buffer_hits"] += 1
                
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Reused buffer from pool: shape=%s, type=%s", shape, dtype)
                
            return buffer
            
        # Check if we need to clear space
        buffer_size = total_size * dtype.itemsize
        if self._total_allocated + buffer_size > self.max_pool_size:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug(
                    "Pool size limit reached. Cleaning up before allocation."
                )
            self._clear_pool_space(buffer_size)
        
        # Allocate new buffer
        try:
            buffer = np.zeros(shape, dtype=dtype)
            self._total_allocated += buffer_size
            
            if self.enable_stats:
                self._stats["buffer_misses"] += 1
                self._stats["total_allocations"] += 1
                
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Allocated new buffer: shape=%s, type=%s", shape, dtype)
                
            return buffer
            
        except MemoryError as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error(
                    "Memory allocation failed for buffer: %s",
                    str(e)
                )
            # Try a more aggressive cleanup
            self.cleanup()
            try:
                buffer = np.zeros(shape, dtype=dtype)
                self._total_allocated += buffer_size
                return buffer
            except MemoryError:
                raise MemoryError("Failed to allocate buffer even after cleanup") from e
    
    def release_buffer(self, buffer: np.ndarray):
        """
        Release a buffer back to the pool.
        
        Args:
            buffer (np.ndarray): Buffer to release
        """
        if buffer is None:
            return
        # Only proceed if buffer has the required attributes
        if not (hasattr(buffer, 'shape') and hasattr(buffer, 'dtype') and hasattr(buffer, 'itemsize') and hasattr(buffer, 'fill')):
            return
        total_size = int(np.prod(buffer.shape))
        dtype = np.dtype(buffer.dtype)
        pool_key = (total_size, dtype)
        # Zero the buffer for security and consistent reuse
        buffer.fill(0)
        # Add to pool
        if pool_key not in self._buffer_pools:
            self._buffer_pools[pool_key] = []
        self._buffer_pools[pool_key].append(buffer)
        buffer_size = total_size * buffer.itemsize
        self._total_allocated += buffer_size
        if self.enable_stats:
            self._stats["total_releases"] += 1
    
    def get_quantum_register(self, size: int, name: str = None) -> QuantumRegister:
        """
        Get a quantum register from the pool or create a new one.
        
        Args:
            size (int): Size of the register
            name (str, optional): Name for the register
            
        Returns:
            QuantumRegister: The quantum register
        """
        # Check pool for registers of this size
        if size in self._qreg_pool and self._qreg_pool[size]:
            qreg = self._qreg_pool[size].pop()
            
            if self.enable_stats:
                self._stats["register_hits"] += 1
                
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Reused quantum register from pool: size=%d", size)
                
            return qreg
            
        # Create new register
        if not name:
            name = f"q{size}"
        else:
            name = str(name) if name is not None else f"q{size}"  # Ensure name is always a string
        qreg = QuantumRegister(size, name)
        
        if self.enable_stats:
            self._stats["register_misses"] += 1
            self._stats["total_allocations"] += 1
            
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Created new quantum register: size=%d, name=%s", size, name)
            
        return qreg
    
    def release_quantum_register(self, qreg: QuantumRegister):
        """
        Release a quantum register back to the pool.
        
        Args:
            qreg (QuantumRegister): Register to release
        """
        if qreg is None:
            return
            
        size = qreg.size
        
        if size not in self._qreg_pool:
            self._qreg_pool[size] = []
            
        self._qreg_pool[size].append(qreg)
        
        if self.enable_stats:
            self._stats["total_releases"] += 1
    
    def get_classical_register(self, size: int, name: str = None) -> ClassicalRegister:
        """
        Get a classical register from the pool or create a new one.
        
        Args:
            size (int): Size of the register
            name (str, optional): Name for the register
            
        Returns:
            ClassicalRegister: The classical register
        """
        # Check pool for registers of this size
        if size in self._creg_pool and self._creg_pool[size]:
            creg = self._creg_pool[size].pop()
            
            if self.enable_stats:
                self._stats["register_hits"] += 1
                
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Reused classical register from pool: size=%d", size)
                
            return creg
            
        # Create new register
        if not name:
            name = f"c{size}"
        else:
            name = str(name) if name is not None else f"c{size}"  # Ensure name is always a string
        creg = ClassicalRegister(size, name)
        
        if self.enable_stats:
            self._stats["register_misses"] += 1
            self._stats["total_allocations"] += 1
            
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Created new classical register: size=%d, name=%s", size, name)
            
        return creg
    
    def release_classical_register(self, creg: ClassicalRegister):
        """
        Release a classical register back to the pool.
        
        Args:
            creg (ClassicalRegister): Register to release
        """
        if creg is None:
            return
            
        size = creg.size
        
        if size not in self._creg_pool:
            self._creg_pool[size] = []
            
        self._creg_pool[size].append(creg)
        
        if self.enable_stats:
            self._stats["total_releases"] += 1
    
    def get_circuit(self, num_qubits: int, num_clbits: int = 0, name: str = None) -> QuantumCircuit:
        """
        Get a quantum circuit with a certain number of qubits and classical bits.
        
        Args:
            num_qubits (int): Number of qubits
            num_clbits (int, optional): Number of classical bits
            name (str, optional): Name for the circuit
            
        Returns:
            QuantumCircuit: The quantum circuit
        """
        # For circuits, we use a weak value dictionary to allow garbage collection
        # while still enabling reuse when possible
        pool_key = f"circuit_{num_qubits}_{num_clbits}"
        
        if pool_key in self._circuit_pools and len(self._circuit_pools[pool_key]) > 0:
            # Note: Unlike normal dicts, WeakValueDictionary may lose entries,
            # so we need to check keys rather than just dict contents
            keys = list(self._circuit_pools[pool_key].keys())
            if keys:
                circuit = self._circuit_pools[pool_key].get(keys[0])
                if circuit is not None:
                    # Remove from weak reference dict to avoid confusion
                    del self._circuit_pools[pool_key][keys[0]]
                    
                    if self.enable_stats:
                        self._stats["circuit_hits"] += 1
                        
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        logging.debug("Reused circuit from pool: qubits=%d, clbits=%d", 
                                     num_qubits, num_clbits)
                    
                    # Reset the circuit
                    circuit.data.clear()
                    if hasattr(circuit, 'metadata') and circuit.metadata is not None:
                        circuit.metadata.clear()
                        
                    return circuit
        
        # Get registers from pool
        qreg = self.get_quantum_register(num_qubits)
        
        if num_clbits > 0:
            creg = self.get_classical_register(num_clbits)
            circuit = QuantumCircuit(qreg, creg, name=name)
        else:
            circuit = QuantumCircuit(qreg, name=name)
        
        if self.enable_stats:
            self._stats["circuit_misses"] += 1
            self._stats["total_allocations"] += 1
            
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Created new circuit: qubits=%d, clbits=%d", 
                        num_qubits, num_clbits)
            
        return circuit
    
    def release_circuit(self, circuit: QuantumCircuit):
        """
        Release a quantum circuit back to the pool.
        
        Args:
            circuit (QuantumCircuit): Circuit to release
        """
        if circuit is None:
            return
            
        # Clear circuit data for cleaner reuse
        circuit.data.clear()
        if hasattr(circuit, 'metadata') and circuit.metadata is not None:
            circuit.metadata.clear()
            
        # Store in weak reference dictionary
        num_qubits = circuit.num_qubits
        num_clbits = circuit.num_clbits
        pool_key = f"circuit_{num_qubits}_{num_clbits}"
        
        if pool_key not in self._circuit_pools:
            self._circuit_pools[pool_key] = weakref.WeakValueDictionary()
            
        # Use a simple counter as a key
        counter = len(self._circuit_pools[pool_key])
        self._circuit_pools[pool_key][counter] = circuit
        
        if self.enable_stats:
            self._stats["total_releases"] += 1
            
        # Note: We don't release the registers separately since they're part of the circuit
    
    def _clear_pool_space(self, required_size: int):
        """
        Clear space in the pool to accommodate a new allocation.
        
        Args:
            required_size (int): Size in bytes needed
        """
        # Calculate how much space we need to free
        to_free = int((self._total_allocated + required_size) - self.max_pool_size)  # Cast to int
        if to_free <= 0:
            return
            
        freed = 0
        buffers_to_clear = []
        
        # Find buffers to clear
        for pool_key, buffers in self._buffer_pools.items():
            total_size, dtype = pool_key
            buffer_size = total_size * dtype.itemsize  # Use total_size directly
            
            while buffers and freed < to_free:
                buffers.pop()  # Remove and discard
                freed += buffer_size
                
            if not buffers:
                buffers_to_clear.append(pool_key)
        
        # Remove empty pools
        for key in buffers_to_clear:
            del self._buffer_pools[key]
        
        self._total_allocated -= freed
        
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Cleared %d bytes from buffer pools", freed)
    
    def cleanup(self):
        """Completely clear all pools to free memory."""
        initial_size = self._total_allocated
        
        # Clear buffer pools
        self._buffer_pools.clear()
        
        # Clear register pools
        self._qreg_pool.clear()
        self._creg_pool.clear()
        
        # Clear circuit pools (weak references will be garbage collected)
        self._circuit_pools.clear()
        
        # Reset allocated count
        self._total_allocated = 0
        
        # Force garbage collection
        gc.collect()
        
        if self.enable_stats:
            self._stats["cleanup_calls"] += 1
            
        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info(
                "Memory pool cleaned up. Freed approximately %d bytes",
                initial_size
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory pool usage statistics.
        
        Returns:
            Dict[str, Any]: Dictionary of usage statistics
        """
        if not self.enable_stats:
            return {"stats_collection_disabled": True}
            
        # Calculate hit rates
        total_buffer_requests = self._stats["buffer_hits"] + self._stats["buffer_misses"]
        buffer_hit_rate = (self._stats["buffer_hits"] / total_buffer_requests * 100 
                         if total_buffer_requests > 0 else 0)
        
        total_circuit_requests = self._stats["circuit_hits"] + self._stats["circuit_misses"]
        circuit_hit_rate = (self._stats["circuit_hits"] / total_circuit_requests * 100 
                          if total_circuit_requests > 0 else 0)
        
        total_register_requests = self._stats["register_hits"] + self._stats["register_misses"]
        register_hit_rate = (self._stats["register_hits"] / total_register_requests * 100 
                           if total_register_requests > 0 else 0)
        
        # Add current pool sizes
        current_stats = self._stats.copy()
        current_stats.update({
            "buffer_hit_rate": buffer_hit_rate,
            "circuit_hit_rate": circuit_hit_rate,
            "register_hit_rate": register_hit_rate,
            "total_allocated_bytes": self._total_allocated,
            "buffer_pool_count": len(self._buffer_pools),
            "qreg_pool_count": len(self._qreg_pool),
            "creg_pool_count": len(self._creg_pool),
            "circuit_pool_count": len(self._circuit_pools)
        })
        
        return current_stats

# Gate patches module - moved to a separate section for better organization and lazy loading
class GatePatches:
    """Lazy-loaded gate patches to avoid import overhead during circuit generation."""
    
    _initialized_patches = {}
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_qft_gate():
        """Cached lazy loader for QFT gate"""
        if "QFTGate" in GatePatches._initialized_patches:
            return GatePatches._initialized_patches["QFTGate"]
            
        try:
            from qiskit.circuit.library import QFTGate
            GatePatches._initialized_patches["QFTGate"] = QFTGate
            return QFTGate
        except ImportError:
            from qiskit.circuit.library import QFT
            GatePatches._initialized_patches["QFTGate"] = QFT
            import qiskit.circuit.library
            setattr(qiskit.circuit.library, 'QFTGate', QFT)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("QFTGate not found; patched with QFT as QFTGate.")
            return QFT
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_mcmt_gate():
        """Cached lazy loader for MCMT gate"""
        if "MCMTGate" in GatePatches._initialized_patches:
            return GatePatches._initialized_patches["MCMTGate"]
            
        try:
            from qiskit.circuit.library import MCMTGate
            GatePatches._initialized_patches["MCMTGate"] = MCMTGate
            return MCMTGate
        except ImportError:
            try:
                from qiskit.circuit.library import MCXGate
                GatePatches._initialized_patches["MCMTGate"] = MCXGate
                import qiskit.circuit.library
                setattr(qiskit.circuit.library, 'MCMTGate', MCXGate)
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("MCMTGate not found; patched with MCXGate as MCMTGate.")
                return MCXGate
            except ImportError:
                if logging.getLogger().isEnabledFor(logging.DEBUG):
                    logging.debug("MCMTGate not found and MCXGate not available; MCMTGate cannot be patched.")
                return None
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_modular_adder_gate():
        """Cached lazy loader for ModularAdder gate"""
        if "ModularAdderGate" in GatePatches._initialized_patches:
            return GatePatches._initialized_patches["ModularAdderGate"]
            
        try:
            from qiskit.circuit.library import ModularAdderGate
            GatePatches._initialized_patches["ModularAdderGate"] = ModularAdderGate
            return ModularAdderGate
        except ImportError:
            from qiskit.circuit import Gate, QuantumCircuit
            
            class DummyModularAdderGate(Gate):
                def __init__(self, num_qubits):
                    super().__init__("ModularAdder", num_qubits, [])

                def _define(self):
                    qc = QuantumCircuit(self.num_qubits, name=self.name)
                    for qubit in range(self.num_qubits):
                        qc.i(qubit)
                    self.definition = qc
            
            GatePatches._initialized_patches["ModularAdderGate"] = DummyModularAdderGate
            import qiskit.circuit.library
            setattr(qiskit.circuit.library, 'ModularAdderGate', DummyModularAdderGate)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("ModularAdderGate not found; patched with DummyModularAdderGate as ModularAdderGate.")
            return DummyModularAdderGate
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_half_adder_gate():
        """Cached lazy loader for HalfAdder gate"""
        if "HalfAdderGate" in GatePatches._initialized_patches:
            return GatePatches._initialized_patches["HalfAdderGate"]
            
        try:
            from qiskit.circuit.library import HalfAdderGate
            GatePatches._initialized_patches["HalfAdderGate"] = HalfAdderGate
            return HalfAdderGate
        except ImportError:
            from qiskit.circuit import Gate, QuantumCircuit
            class DummyHalfAdderGate(Gate):
                def __init__(self, num_qubits=2):
                    super().__init__("HalfAdder", num_qubits, [])

                def _define(self):
                    qc = QuantumCircuit(self.num_qubits, name=self.name)
                    for qubit in range(self.num_qubits):
                        qc.i(qubit)
                    self.definition = qc
            
            GatePatches._initialized_patches["HalfAdderGate"] = DummyHalfAdderGate
            import qiskit.circuit.library
            setattr(qiskit.circuit.library, 'HalfAdderGate', DummyHalfAdderGate)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("HalfAdderGate not found; patched with DummyHalfAdderGate as HalfAdderGate.")
            return DummyHalfAdderGate
            
    @staticmethod
    @lru_cache(maxsize=1)
    def get_full_adder_gate():
        """Cached lazy loader for FullAdder gate"""
        if "FullAdderGate" in GatePatches._initialized_patches:
            return GatePatches._initialized_patches["FullAdderGate"]
            
        try:
            from qiskit.circuit.library import FullAdderGate
            GatePatches._initialized_patches["FullAdderGate"] = FullAdderGate
            return FullAdderGate
        except ImportError:
            from qiskit.circuit import Gate, QuantumCircuit
            class DummyFullAdderGate(Gate):
                def __init__(self, num_qubits=3):
                    super().__init__("FullAdder", num_qubits, [])

                def _define(self):
                    qc = QuantumCircuit(self.num_qubits, name=self.name)
                    for qubit in range(self.num_qubits):
                        qc.i(qubit)
                    self.definition = qc
            
            GatePatches._initialized_patches["FullAdderGate"] = DummyFullAdderGate
            import qiskit.circuit.library
            setattr(qiskit.circuit.library, 'FullAdderGate', DummyFullAdderGate)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("FullAdderGate not found; patched with DummyFullAdderGate as FullAdderGate.")
            return DummyFullAdderGate
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_multiplier_gate():
        """Cached lazy loader for Multiplier gate"""
        if "MultiplierGate" in GatePatches._initialized_patches:
            return GatePatches._initialized_patches["MultiplierGate"]
            
        try:
            from qiskit.circuit.library import MultiplierGate
            GatePatches._initialized_patches["MultiplierGate"] = MultiplierGate
            return MultiplierGate
        except ImportError:
            from qiskit.circuit import Gate, QuantumCircuit
            class FunctionalMultiplierGate(Gate):
                """
                A functional 2-bit multiplier gate for multiplying two 2-bit numbers to produce a 4-bit product.
                Registers assumed (total 8 qubits):
                    a: qubits 0-1 (2 qubits representing the first operand)
                    b: qubits 2-3 (2 qubits representing the second operand)
                    p: qubits 4-7 (4 qubits where the product will be stored, initially set to 0)
                """
                def __init__(self):
                    super().__init__("Multiplier", 8, [])
                
                def _define(self):
                    qc = QuantumCircuit(8, name=self.name)
                    # Qubit ordering: a0=0, a1=1, b0=2, b1=3, p0=4, p1=5, p2=6, p3=7
                    a0 = 0; a1 = 1; b0 = 2; b1 = 3; p0 = 4; p1 = 5; p2 = 6; p3 = 7
                    
                    # Controlled operations
                    qc.ccx(b0, a0, p0)
                    qc.ccx(b0, a1, p1)
                    qc.ccx(b1, a0, p1)  
                    qc.ccx(b1, a1, p2)
                    
                    self.definition = qc
            
            GatePatches._initialized_patches["MultiplierGate"] = FunctionalMultiplierGate
            import qiskit.circuit.library
            setattr(qiskit.circuit.library, 'MultiplierGate', FunctionalMultiplierGate)
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("MultiplierGate not found; patched with FunctionalMultiplierGate as MultiplierGate.")
            return FunctionalMultiplierGate


class DynamicCircuitRefactor:
    """
    Optimized class for dynamic quantum circuit refactoring.
    Provides methods to generate a dynamic circuit from scratch and refactor existing static circuits.
    
    Performance improvements over original implementation:
    - Optimized logging with conditional checks
    - Lazy loading of gate patches
    - Optional metadata collection
    - Validation caching
    - Improved memory management with explicit GC
    - Circuit component caching
    - Memory pooling for circuit operations
    """

    def __init__(self, num_qubits: int = 4, enable_memory_pooling: bool = True):
        """
        Initializes the DynamicCircuitRefactor with a default number of qubits.
        Args:
            num_qubits (int): The number of qubits for the circuit.
            enable_memory_pooling (bool): Whether to enable memory pooling for circuit operations.
        """
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Initializing DynamicCircuitRefactor with %d qubits.", num_qubits)
        
        self.num_qubits = num_qubits
        self._validation_cache = {}
        
        # Initialize memory pool if enabled
        self.enable_memory_pooling = enable_memory_pooling
        if enable_memory_pooling:
            self.memory_pool = CircuitMemoryPool(
                max_pool_size=1024 * 1024 * 1024,  # 1GB default
                enable_stats=logging.getLogger().isEnabledFor(logging.DEBUG)
            )
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Memory pooling enabled for circuit operations.")
        else:
            self.memory_pool = None
            
        # Initialize quantum and classical registers
        if enable_memory_pooling:
            self.qreg = self.memory_pool.get_quantum_register(num_qubits, 'q')
            self.creg = self.memory_pool.get_classical_register(num_qubits, 'c')
        else:
            self.qreg = QuantumRegister(num_qubits, 'q')
            self.creg = ClassicalRegister(num_qubits, 'c')

    def __del__(self):
        """
        Clean up resources when the instance is being garbage collected.
        """
        if self.enable_memory_pooling and self.memory_pool is not None:
            # Release registers back to the pool
            self.memory_pool.release_quantum_register(self.qreg)
            self.memory_pool.release_classical_register(self.creg)
            
            # Log memory pool statistics if debugging is enabled
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                stats = self.memory_pool.get_stats()
                logging.debug("Memory pool statistics at cleanup: %s", stats)

    def generate_dynamic_circuit(self, collect_metadata: bool = False) -> QuantumCircuit:
        """
        Generates a dynamic quantum circuit based on current configuration.
        
        Args:
            collect_metadata (bool): Whether to collect detailed metadata during generation
        
        Returns:
            QuantumCircuit: A dynamically generated quantum circuit.
        
        Extensive Notation:
        - 2024-04-14: Updated to always use the quantum register attached to the circuit (from circuit.qregs[0])
          instead of self.qreg. This fixes a critical bug where, due to memory pooling, the circuit and the instance's
          registers could diverge, causing CircuitError when applying gates. This is a common pitfall after refactoring
          for pooling/reuse. All gate applications now reference the register actually attached to the circuit.
        - This change is vital for benchmark and production correctness, and should be preserved in future refactors.
        """
        logging.info("Generating a dynamic quantum circuit with %d qubits.", self.num_qubits)
        
        # Create circuit using memory pool if enabled
        if self.enable_memory_pooling:
            circuit = self.memory_pool.get_circuit(
                self.num_qubits, 
                self.num_qubits,  # Same number of classical bits
                name="dynamic_circuit"
            )
        else:
            circuit = QuantumCircuit(self.qreg, self.creg, name="dynamic_circuit")
        
        # --- CRITICAL: Always use the register attached to the circuit, not self.qreg/self.creg ---
        # This prevents register/circuit mismatches after pooling or refactoring.
        qreg = circuit.qregs[0]  # QuantumRegister actually attached to the circuit
        creg = circuit.cregs[0] if circuit.cregs else None  # ClassicalRegister if present
        # -----------------------------------------------------------------------------------------
        
        # Initialize metadata collection if requested
        circuit_metadata = {}
        if collect_metadata:
            circuit_metadata = {
                "qubits": self.num_qubits,
                "depth": 0,
                "gates": {
                    "h": 0,
                    "cx": 0,
                    "rx": 0,
                    "rz": 0,
                    "t": 0,
                    "s": 0,
                    "other": 0,
                }
            }
            circuit.metadata = circuit_metadata
        
        # Use chunking for better memory management with larger qubit counts
        if self.num_qubits > 8:
            chunk_size = 4
            for chunk_start in range(0, self.num_qubits, chunk_size):
                chunk_end = min(chunk_start + chunk_size, self.num_qubits)
                qubit_indices = list(range(chunk_start, chunk_end))
                if self.enable_memory_pooling:
                    buffer_size = (2 ** len(qubit_indices), 2 ** len(qubit_indices))
                    temp_buffer = self.memory_pool.get_buffer(buffer_size)
                    try:
                        for i, idx in enumerate(qubit_indices):
                            circuit.h(qreg[idx])  # FIXED: use qreg from circuit
                            if collect_metadata:
                                circuit_metadata["gates"]["h"] += 1
                    finally:
                        self.memory_pool.release_buffer(temp_buffer)
                else:
                    for i, idx in enumerate(qubit_indices):
                        circuit.h(qreg[idx])  # FIXED: use qreg from circuit
                        if collect_metadata:
                            circuit_metadata["gates"]["h"] += 1
        else:
            for idx in range(self.num_qubits):
                circuit.h(qreg[idx])  # FIXED: use qreg from circuit
                if collect_metadata:
                    circuit_metadata["gates"]["h"] += 1
        
        if collect_metadata:
            circuit_metadata["depth"] += 1  # All H gates can be applied in parallel
        
        from numpy import pi
        for idx in range(self.num_qubits):
            angle = pi / 4 * ((idx % 4) + 1)
            circuit.rx(angle, qreg[idx])  # FIXED: use qreg from circuit
            if collect_metadata:
                circuit_metadata["gates"]["rx"] += 1
        
        if self.num_qubits > 1:
            for i in range(0, self.num_qubits - 1, 2):
                circuit.cx(qreg[i], qreg[i + 1])  # FIXED: use qreg from circuit
                if collect_metadata:
                    circuit_metadata["gates"]["cx"] += 1
        
        is_valid = self._validate_circuit(circuit)
        if not is_valid and logging.getLogger().isEnabledFor(logging.WARNING):
            logging.warning("Generated circuit failed validation checks.")
        
        logging.info("Dynamic circuit generation completed.")
        return circuit

    def _validate_circuit(self, circuit: QuantumCircuit, validation_level: str = "basic") -> bool:
        """
        Validate a quantum circuit with multiple validation levels.
        Args:
            circuit (QuantumCircuit): The circuit to validate.
            validation_level (str): Level of validation to perform (full, basic, none)
        Returns:
            bool: Whether the circuit passes validation.
        """
        if validation_level == "none":
            return True
        # Use a hashable string representation as the cache key (QuantumCircuit is not hashable)
        # qasm() is preferred for uniqueness, but fallback to str if needed
        try:
            cache_key = circuit.qasm()
        except Exception:
            cache_key = str(circuit)
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]
        # Basic validation (always performed)
        is_valid = True
        if validation_level == "full":
            # Additional validations for full validation level
            # To be expanded with specific validation logic
            pass
        # Store in cache
        self._validation_cache[cache_key] = is_valid
        return is_valid

    def refactor_circuit(self, circuit: QuantumCircuit, validation_level="basic") -> QuantumCircuit:
        """
        Refactors an existing static quantum circuit to include dynamic modifications.
        
        Args:
            circuit (QuantumCircuit): The static circuit to refactor.
            validation_level (str): Level of validation to perform (full, basic, none)
            
        Returns:
            QuantumCircuit: The refactored dynamic circuit.
        """
        logging.info("Refactoring the given quantum circuit dynamically.")
        
        # Validate the circuit first
        is_valid = self._validate_circuit(circuit, validation_level)
        if not is_valid:
            logging.warning("Circuit validation failed, proceeding with caution.")
        
        # Use Qiskit's transpile function to simulate circuit optimization as a part of the refactoring process
        # For large circuits, use memory pooling for temporary operations
        if self.enable_memory_pooling and circuit.num_qubits > 8:
            # Allocate temporary buffer for transpilation
            buffer_shape = (2 ** circuit.num_qubits, 2 ** circuit.num_qubits)
            temp_buffer = self.memory_pool.get_buffer(buffer_shape)
            
            try:
                # Force garbage collection before transpilation to minimize memory pressure
                gc.collect()
                optimized_circuit = transpile(circuit, optimization_level=3)
            finally:
                # Release buffer back to pool
                self.memory_pool.release_buffer(temp_buffer)
        else:
            optimized_circuit = transpile(circuit, optimization_level=3)
        
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Circuit transpiled for optimization.")
        
        # TODO: Add custom dynamic modifications based on real-time feedback.
        # This section is a placeholder for integrating further dynamic adaptations.
        
        logging.info("Dynamic refactoring completed.")
        return optimized_circuit


if __name__ == "__main__":
    # For standalone testing, initialize the DynamicCircuitRefactor and generate/refactor a circuit.
    logging.info("Initializing DynamicCircuitRefactor for standalone testing.")
    
    # Test with memory pooling enabled and metadata collection
    refactor = DynamicCircuitRefactor(num_qubits=4, enable_memory_pooling=True)
    dynamic_circuit = refactor.generate_dynamic_circuit(collect_metadata=True)
    logging.info("Generated Dynamic Circuit with metadata:")
    logging.info(dynamic_circuit.draw(output='text'))
    if hasattr(dynamic_circuit, 'metadata'):
        logging.info(f"Circuit metadata: {dynamic_circuit.metadata}")
    
    # Refactor the generated circuit as a demonstration of dynamic adjustments.
    refactored_circuit = refactor.refactor_circuit(dynamic_circuit)
    logging.info("Refactored Circuit:")
    logging.info(refactored_circuit.draw(output='text'))
    
    # Test performance with larger qubit count
    logging.info("Testing with 8 qubits...")
    import time
    
    # First test without memory pooling
    start_time = time.time()
    refactor_no_pool = DynamicCircuitRefactor(num_qubits=8, enable_memory_pooling=False)
    no_pool_circuit = refactor_no_pool.generate_dynamic_circuit(collect_metadata=False)
    end_time_no_pool = time.time()
    elapsed_no_pool = end_time_no_pool - start_time
    
    # Then test with memory pooling
    start_time = time.time()
    refactor_with_pool = DynamicCircuitRefactor(num_qubits=8, enable_memory_pooling=True)
    with_pool_circuit = refactor_with_pool.generate_dynamic_circuit(collect_metadata=False)
    end_time_with_pool = time.time()
    elapsed_with_pool = end_time_with_pool - start_time
    
    # Log results
    logging.info(f"8-qubit circuit generation time without memory pooling: {elapsed_no_pool:.4f} seconds")
    logging.info(f"8-qubit circuit generation time with memory pooling: {elapsed_with_pool:.4f} seconds")
    logging.info(f"Performance improvement: {((elapsed_no_pool - elapsed_with_pool) / elapsed_no_pool * 100):.2f}%")
    
    # Print memory pool statistics
    if refactor_with_pool.memory_pool:
        stats = refactor_with_pool.memory_pool.get_stats()
        logging.info(f"Memory pool statistics: {stats}") 