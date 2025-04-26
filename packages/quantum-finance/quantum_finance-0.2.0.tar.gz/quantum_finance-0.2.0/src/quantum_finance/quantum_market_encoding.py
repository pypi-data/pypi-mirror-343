#!/usr/bin/env python3

"""
Quantum Market Data Encoding

This module provides functions to encode cryptocurrency market microstructure data
into quantum states. It serves as the bridge between classical market data and 
quantum computation for risk assessment.

Key features:
- Amplitude encoding of order book imbalance
- Phase encoding of price volatility
- Basis encoding of liquidity metrics
- Combined encoding for multiple market factors

Author: Quantum-AI Team
"""

import numpy as np
from qiskit import QuantumCircuit
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def encode_order_book_imbalance(order_book_data: Dict[str, List], num_qubits: int = 4) -> QuantumCircuit:
    """
    Encode order book imbalance as a quantum state using amplitude encoding.
    
    Args:
        order_book_data: Dictionary containing 'bids' and 'asks' lists, where each 
                       item is a dictionary with 'price' and 'quantity' keys
        num_qubits: Number of qubits to use for encoding (default: 4)
        
    Returns:
        QuantumCircuit: Circuit encoding the order book imbalance
    """
    # Extract bid and ask data
    if 'bids' not in order_book_data or 'asks' not in order_book_data:
        raise ValueError("Order book data must contain 'bids' and 'asks' keys")
    
    # Calculate total volumes
    try:
        bid_volume = sum(float(level['quantity']) for level in order_book_data['bids'])
        ask_volume = sum(float(level['quantity']) for level in order_book_data['asks'])
    except (KeyError, TypeError) as e:
        logger.error(f"Error extracting volume data: {e}")
        logger.error(f"Order book structure: {order_book_data.keys()}")
        if 'bids' in order_book_data:
            logger.error(f"First bid item: {order_book_data['bids'][0] if order_book_data['bids'] else 'empty'}")
        raise ValueError(f"Invalid order book data structure: {e}")
    
    # Calculate imbalance ratio (-1 to 1 range)
    total_volume = bid_volume + ask_volume
    if total_volume == 0:
        imbalance = 0.0
    else:
        imbalance = (bid_volume - ask_volume) / total_volume
    
    logger.info(f"Order book imbalance: {imbalance:.4f} (Bid: {bid_volume:.2f}, Ask: {ask_volume:.2f})")
    
    # Create quantum circuit
    qc = QuantumCircuit(num_qubits)
    
    # Map imbalance to rotation angle (amplitude encoding)
    # Map [-1,1] to [0,π] 
    theta = (imbalance + 1) * np.pi / 2
    
    # Apply rotation to first qubit to encode imbalance
    qc.ry(theta, 0)
    
    # Create entanglement between qubits to distribute the information
    for i in range(num_qubits-1):
        qc.cx(i, i+1)
    
    # Add some depth to the circuit for more complex encoding
    for i in range(num_qubits):
        # Apply phase based on position in order book (simplified)
        if i < num_qubits - 1:
            # Calculate a phase angle based on the price levels
            if 'bids' in order_book_data and i < len(order_book_data['bids']):
                bid_price = float(order_book_data['bids'][i]['price'])
                phase = np.pi * (bid_price % 1)  # Use fractional part for phase
                qc.p(phase, i)
    
    logger.debug(f"Created order book imbalance circuit with {num_qubits} qubits")
    return qc

def encode_market_volatility(volatility: float, num_qubits: int = 3) -> QuantumCircuit:
    """
    Encode market volatility as a quantum state using phase encoding.
    
    Args:
        volatility: Volatility value (typically between 0 and 1)
        num_qubits: Number of qubits to use for encoding
        
    Returns:
        QuantumCircuit: Circuit encoding the volatility
    """
    # Ensure volatility is in valid range
    volatility = max(0.0, min(1.0, volatility))
    
    # Create quantum circuit
    qc = QuantumCircuit(num_qubits)
    
    # Put all qubits in superposition
    for i in range(num_qubits):
        qc.h(i)
    
    # Encode volatility in phase
    phase_angle = volatility * np.pi
    
    # Apply controlled phase rotations to create a pattern that represents volatility
    for i in range(num_qubits-1):
        qc.cp(phase_angle, i, i+1)
    
    # Add an extra layer of encoding with varying phases
    for i in range(num_qubits):
        qc.p(phase_angle * (i+1)/num_qubits, i)
    
    logger.debug(f"Created volatility encoding circuit with phase angle {phase_angle:.4f}")
    return qc

def encode_price_impact(order_book_data: Dict[str, List], trade_size: float, 
                        num_qubits: int = 4) -> Tuple[QuantumCircuit, float]:
    """
    Encode price impact of a trade as a quantum state.
    Also calculates the estimated price impact value.
    
    Args:
        order_book_data: Dictionary containing 'bids' and 'asks' lists
        trade_size: Size of the hypothetical trade
        num_qubits: Number of qubits to use for encoding
        
    Returns:
        Tuple of (QuantumCircuit, float): Circuit encoding the price impact and the impact value
    """
    # Calculate price impact (simplified model)
    impact = 0.0
    remaining_size = trade_size
    
    # For a sell order (going through the bids)
    if 'bids' in order_book_data and order_book_data['bids']:
        initial_price = float(order_book_data['bids'][0]['price'])
        current_price = initial_price
        
        for level in order_book_data['bids']:
            level_price = float(level['price'])
            level_quantity = float(level['quantity'])
            
            if remaining_size <= level_quantity:
                # Order can be fully executed at this level
                current_price = level_price
                remaining_size = 0
                break
            else:
                # Consume this level and continue
                remaining_size -= level_quantity
        
        # Calculate price impact as percentage
        if initial_price > 0:
            impact = (initial_price - current_price) / initial_price
    
    # Create quantum circuit
    qc = QuantumCircuit(num_qubits)
    
    # Map impact to rotation angle
    # Use sigmoid-like scaling to handle potentially large impacts
    scaled_impact = np.arctan(10 * impact) * 2 / np.pi  # Maps to [0,1] range
    theta = scaled_impact * np.pi
    
    # Apply rotation to first qubit
    qc.ry(theta, 0)
    
    # Use a different entanglement pattern for price impact
    for i in range(num_qubits-1):
        qc.cx(0, i+1)  # Star configuration with qubit 0 as center
    
    # Add some custom gates for more complex encoding
    for i in range(1, num_qubits):
        # Varying rotation angles
        qc.ry(theta / (i+1), i)
    
    logger.debug(f"Created price impact circuit with impact value {impact:.6f}")
    return qc, impact

def encode_liquidity_risk(
    bid_ask_spread: float, 
    order_book_depth: float,
    trade_volume: float,
    num_qubits: int = 4
) -> QuantumCircuit:
    """
    Encode liquidity risk combining multiple factors.
    
    Args:
        bid_ask_spread: Current bid-ask spread (percentage)
        order_book_depth: Depth of the order book (relative measure)
        trade_volume: Recent trading volume (normalized)
        num_qubits: Number of qubits to use
        
    Returns:
        QuantumCircuit: Circuit encoding liquidity risk
    """
    # Normalize inputs to [0,1] range if they aren't already
    bid_ask_spread = min(1.0, bid_ask_spread)  # Higher spread = higher risk
    order_book_depth = min(1.0, max(0.0, 1.0 - order_book_depth))  # Lower depth = higher risk
    trade_volume = min(1.0, max(0.0, 1.0 - trade_volume))  # Lower volume = higher risk
    
    # Create quantum circuit
    qc = QuantumCircuit(num_qubits)
    
    # Calculate an overall liquidity risk score (simplified model)
    # Using weighted average of factors
    liquidity_risk = 0.4 * bid_ask_spread + 0.4 * order_book_depth + 0.2 * trade_volume
    
    # Map to rotation angle
    theta = liquidity_risk * np.pi
    
    # Encode main liquidity risk in first qubit
    qc.ry(theta, 0)
    
    # Encode individual components in other qubits if we have enough
    if num_qubits >= 3:
        qc.ry(bid_ask_spread * np.pi, 1)
        qc.ry(order_book_depth * np.pi, 2)
        if num_qubits >= 4:
            qc.ry(trade_volume * np.pi, 3)
    
    # Create entanglement between main risk qubit and component qubits
    for i in range(1, num_qubits):
        qc.cx(0, i)
    
    # Add another layer of gates
    qc.h(0)
    for i in range(1, num_qubits):
        qc.cx(i, 0)
    
    logger.debug(f"Created liquidity risk circuit with risk value {liquidity_risk:.4f}")
    return qc

def combined_market_risk_encoding(
    order_book_data: Dict[str, List],
    volatility: float,
    trade_size: float,
    recent_volume: float,
    num_qubits: int = 8,
    fallback_on_error: bool = True
) -> QuantumCircuit:
    """
    Create a combined quantum circuit encoding multiple market risk factors.
    
    Args:
        order_book_data: Order book data with bids and asks
        volatility: Market volatility (0-1 scale)
        trade_size: Size of hypothetical trade to calculate price impact
        recent_volume: Recent trading volume (normalized)
        num_qubits: Total number of qubits to use
        fallback_on_error: Whether to use a fallback circuit on error
        
    Returns:
        QuantumCircuit: Combined circuit encoding all risk factors
    """
    if num_qubits < 8:
        logger.warning(f"Recommended minimum 8 qubits for combined encoding, got {num_qubits}")
    
    # Calculate how many qubits to allocate to each factor
    # For simplicity, we'll use a fixed allocation strategy
    imbalance_qubits = max(2, num_qubits // 4)
    volatility_qubits = max(2, num_qubits // 4)
    impact_qubits = max(2, num_qubits // 4)
    liquidity_qubits = num_qubits - imbalance_qubits - volatility_qubits - impact_qubits
    
    # Create the combined circuit
    qc = QuantumCircuit(num_qubits)
    
    # Helper function to safely get qubit indices
    def safe_get_qubit_indices(gate):
        """Safely extract qubit indices from gate.qubits, handling missing 'index' attribute."""
        try:
            # First try the standard approach
            return [q.index for q in gate.qubits]
        except AttributeError:
            # If 'index' attribute is missing, try alternative approaches
            if hasattr(gate, 'qubits') and all(isinstance(i, int) for i in gate.qubits):
                # If qubits are already integers, use them directly
                return gate.qubits
            elif hasattr(gate, '_qubits') and all(isinstance(i, int) for i in gate._qubits):
                # Try the _qubits attribute as a fallback
                return gate._qubits
            elif hasattr(gate, 'qargs') and all(isinstance(i, int) for i in gate.qargs):
                # Try the qargs attribute as a fallback
                return gate.qargs
            else:
                # If all else fails, try to use the positional index in the circuit
                logger.warning(f"Using qubit position as index for {gate.operation.name if hasattr(gate, 'operation') else 'unknown gate'}")
                return list(range(len(gate.qubits) if hasattr(gate, 'qubits') else 1))
    
    # Calculate individual encoding circuits
    try:
        # Extract bid-ask spread from order book
        best_bid = float(order_book_data['bids'][0]['price']) if order_book_data['bids'] else 0
        best_ask = float(order_book_data['asks'][0]['price']) if order_book_data['asks'] else 0
        
        if best_bid > 0 and best_ask > 0:
            bid_ask_spread = (best_ask - best_bid) / best_ask
        else:
            bid_ask_spread = 0.01  # Default value
            
        # Calculate order book depth (simplified)
        total_quantity = sum(float(level['quantity']) for level in order_book_data['bids'])
        total_quantity += sum(float(level['quantity']) for level in order_book_data['asks'])
        # Normalize to [0,1] with a reasonable scaling factor
        order_book_depth = min(1.0, total_quantity / 1000.0)  # Adjust scaling as needed
        
        # Encode each component using respective qubits
        # Order book imbalance
        imb_qc = encode_order_book_imbalance(order_book_data, num_qubits=imbalance_qubits)
        
        # Volatility
        vol_qc = encode_market_volatility(volatility, num_qubits=volatility_qubits)
        
        # Price impact
        imp_qc, impact_value = encode_price_impact(order_book_data, trade_size, num_qubits=impact_qubits)
        
        # Liquidity risk
        liq_qc = encode_liquidity_risk(bid_ask_spread, order_book_depth, recent_volume, num_qubits=liquidity_qubits)
        
        # Calculate qubit indices for each component
        vol_start = imbalance_qubits
        imp_start = vol_start + volatility_qubits
        liq_start = imp_start + impact_qubits
        
        # Compose the individual circuits into the combined circuit
        # Apply each subcircuit to its respective qubits
        for i, gate in enumerate(imb_qc.data):
            try:
                # Use the safe function to get qubit indices
                qargs = safe_get_qubit_indices(gate)
                qc.append(gate.operation, qargs)
            except Exception as e:
                logger.warning(f"Error adding imbalance gate {i}: {e}")
            
        for i, gate in enumerate(vol_qc.data):
            try:
                # Adjust qubit indices using the safe function
                qargs = [vol_start + idx for idx in safe_get_qubit_indices(gate)]
                qc.append(gate.operation, qargs)
            except Exception as e:
                logger.warning(f"Error adding volatility gate {i}: {e}")
            
        for i, gate in enumerate(imp_qc.data):
            try:
                # Adjust qubit indices using the safe function
                qargs = [imp_start + idx for idx in safe_get_qubit_indices(gate)]
                qc.append(gate.operation, qargs)
            except Exception as e:
                logger.warning(f"Error adding impact gate {i}: {e}")
            
        for i, gate in enumerate(liq_qc.data):
            try:
                # Adjust qubit indices using the safe function
                qargs = [liq_start + idx for idx in safe_get_qubit_indices(gate)]
                qc.append(gate.operation, qargs)
            except Exception as e:
                logger.warning(f"Error adding liquidity gate {i}: {e}")
        
        # Add entanglement between components
        # Connect representative qubits from each component
        qc.cx(0, vol_start)                # Connect imbalance to volatility
        qc.cx(vol_start, imp_start)        # Connect volatility to price impact
        qc.cx(imp_start, liq_start)        # Connect price impact to liquidity
        
        # Create a "summary" entanglement
        control_qubits = [0, vol_start, imp_start, liq_start]
        if len(control_qubits) > 1:
            # Add multi-controlled X gate if we have multiple controls
            # We'll decompose it into a series of CNOT gates for simplicity
            for i in range(len(control_qubits)-1):
                qc.cx(control_qubits[i], control_qubits[i+1])
        
        logger.info(f"Created combined market risk circuit with {num_qubits} qubits")
        
    except Exception as e:
        logger.error(f"Error creating combined market risk encoding: {e}")
        if not fallback_on_error:
            # If fallback is disabled, propagate the error
            raise
            
        # Create a simple default circuit in case of error
        for i in range(num_qubits):
            qc.h(i)
        
        logger.warning("Using fallback circuit due to encoding error")
    
    return qc

def visualize_quantum_market_encoding(circuit: QuantumCircuit, 
                                      title: str = "Quantum Market Encoding",
                                      output_file: Optional[str] = None) -> None:
    """
    Visualize the quantum circuit used for market data encoding.
    
    Args:
        circuit: The quantum circuit to visualize
        title: Title for the visualization
        output_file: Optional file path to save the visualization
    """
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Draw circuit directly to the matplotlib figure
    try:
        # Use text-based drawing as fallback
        circuit_diagram = circuit.draw(output='text')
        plt.text(0.1, 0.5, circuit_diagram, fontsize=9, family='monospace')
        plt.axis('off')
        plt.title(title)
    except Exception as e:
        logger.warning(f"Error drawing circuit with matplotlib: {e}")
        # Just show the circuit statistics instead
        stats = {
            'Num Qubits': circuit.num_qubits,
            'Depth': circuit.depth(),
            'Num Gates': sum(1 for _ in circuit.data)
        }
        # Count gate types
        gate_counts = {}
        for gate in circuit.data:
            gate_name = gate.operation.name
            gate_counts[gate_name] = gate_counts.get(gate_name, 0) + 1
        
        # Create a text representation
        text = f"Circuit: {title}\n\n"
        text += f"Qubits: {stats['Num Qubits']}\n"
        text += f"Depth: {stats['Depth']}\n"
        text += f"Gates: {stats['Num Gates']}\n\n"
        text += "Gate Counts:\n"
        for gate, count in gate_counts.items():
            text += f"  {gate}: {count}\n"
        
        plt.text(0.1, 0.5, text, fontsize=12)
        plt.axis('off')
        plt.title(title)
    
    # Save or show
    if output_file:
        plt.savefig(output_file, bbox_inches='tight')
        logger.info(f"Circuit visualization saved to {output_file}")
    else:
        plt.show()

# Example usage when run as script
if __name__ == "__main__":
    # Sample order book data
    sample_order_book = {
        'bids': [
            {'price': '40000.00', 'quantity': '2.5'},
            {'price': '39950.00', 'quantity': '3.8'},
            {'price': '39900.00', 'quantity': '5.2'},
            {'price': '39850.00', 'quantity': '7.1'},
            {'price': '39800.00', 'quantity': '8.5'}
        ],
        'asks': [
            {'price': '40050.00', 'quantity': '1.9'},
            {'price': '40100.00', 'quantity': '3.2'},
            {'price': '40150.00', 'quantity': '4.7'},
            {'price': '40200.00', 'quantity': '6.3'},
            {'price': '40250.00', 'quantity': '7.8'}
        ]
    }
    
    # Test individual encodings
    print("Testing quantum market encodings...")
    
    # Order book imbalance
    imb_circuit = encode_order_book_imbalance(sample_order_book)
    visualize_quantum_market_encoding(
        imb_circuit, 
        "Order Book Imbalance Encoding",
        "order_book_imbalance_circuit.png"
    )
    
    # Volatility
    vol_circuit = encode_market_volatility(0.35)
    visualize_quantum_market_encoding(
        vol_circuit, 
        "Market Volatility Encoding",
        "volatility_circuit.png"
    )
    
    # Price impact
    imp_circuit, impact = encode_price_impact(sample_order_book, 10.0)
    print(f"Calculated price impact: {impact:.6f}")
    visualize_quantum_market_encoding(
        imp_circuit, 
        f"Price Impact Encoding (Impact: {impact:.6f})",
        "price_impact_circuit.png"
    )
    
    # Combined encoding
    combined_circuit = combined_market_risk_encoding(
        sample_order_book,
        volatility=0.35,
        trade_size=10.0,
        recent_volume=0.7
    )
    visualize_quantum_market_encoding(
        combined_circuit, 
        "Combined Market Risk Encoding",
        "combined_market_risk_circuit.png"
    )
    
    print("Market encoding test complete. Visualizations saved as PNG files.") 