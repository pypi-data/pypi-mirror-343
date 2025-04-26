#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple Noise Test for Stochastic-Memsaur Error Analysis

This script demonstrates the impact of quantum noise on financial calculations
using a simplified model for educational and testing purposes.
"""

import os
import dotenv
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_aer.noise.errors import depolarizing_error
from qiskit_ibm_runtime import QiskitRuntimeService
from stochastic_memsaur_error_analysis import FinancialErrorAnalyzer

# Load environment variables (IBM Quantum API token)
dotenv.load_dotenv()

def create_financial_circuit(num_qubits, depth=1):
    """
    Create a simplified financial modeling circuit for testing
    """
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # Initialize with superposition (market uncertainty)
    qc.h(range(num_qubits))
    
    # Apply financial correlations
    for i in range(depth):
        # Create price correlations between adjacent assets
        for j in range(num_qubits-1):
            qc.crx(0.1 * (i+1), j, j+1)
        
        # Apply phase rotations to model market interactions
        for j in range(num_qubits):
            qc.rz(0.1 * j, j)
            
        # Add some entanglement
        for j in range(num_qubits-1):
            qc.cx(j, j+1)
        
        # Apply phase shifts representing different market trends
        for j in range(num_qubits):
            qc.rz(0.1 * j, j)
    
    # Measure all qubits
    qc.measure_all()
    
    return qc

def calculate_financial_metrics(counts):
    """
    Calculate financial metrics from measurement counts
    """
    # Convert counts to probabilities
    total_shots = sum(counts.values())
    probs = {bitstring: count/total_shots for bitstring, count in counts.items()}
    
    # Calculate expected return
    expected_return = 0
    for bitstring, prob in probs.items():
        # Remove any spaces from the bitstring
        cleaned_bitstring = bitstring.replace(' ', '')
        bitstring_len = len(cleaned_bitstring)
        try:
            numeric_value = int(cleaned_bitstring, 2) / (2**bitstring_len)
        except ValueError:
            # If conversion fails, use the first character as a fallback
            print(f"Warning: Could not convert '{bitstring}' to binary, using approximation")
            first_char = cleaned_bitstring[0] if cleaned_bitstring else '0'
            numeric_value = int(first_char == '1') / 2
                
        expected_return += numeric_value * prob
        
    # Calculate volatility (standard deviation)
    volatility = 0
    for bitstring, prob in probs.items():
        cleaned_bitstring = bitstring.replace(' ', '')
        bitstring_len = len(cleaned_bitstring)
        try:
            numeric_value = int(cleaned_bitstring, 2) / (2**bitstring_len)
        except ValueError:
            first_char = cleaned_bitstring[0] if cleaned_bitstring else '0'
            numeric_value = int(first_char == '1') / 2
                
        volatility += (numeric_value - expected_return)**2 * prob
        
    volatility = (volatility ** 0.5)  # Square root for standard deviation
    
    # Calculate Value at Risk (95% confidence)
    value_at_risk = expected_return - 1.96 * volatility
    
    # Calculate Sharpe ratio
    risk_free_rate = 0.01  # Assumed risk-free rate
    sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0
    
    return {
        'expected_return': expected_return,
        'volatility': volatility,
        'value_at_risk': value_at_risk,
        'sharpe_ratio': sharpe_ratio
    }

def create_test_circuit(num_qubits=3, depth=1):
    """
    Create a simple test circuit for financial modeling
    
    Args:
        num_qubits: Number of qubits (assets) in the model
        depth: Circuit depth parameter
        
    Returns:
        QuantumCircuit for financial modeling
    """
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # Initialize with superposition (market uncertainty)
    qc.h(range(num_qubits))
    
    for d in range(depth):
        # Create price correlations between assets
        for i in range(num_qubits-1):
            qc.rz(0.1 * (i+1), i)
            qc.rx(0.1 * (i+1), i+1)
    
    # Measure all qubits
    qc.measure_all()
    
    return qc

def main():
    # Initialize the error analyzer
    # Using local testing mode instead of cloud simulator
    service = QiskitRuntimeService()
    analyzer = FinancialErrorAnalyzer(service=service)
    
    # Create a test circuit
    test_circuit = create_test_circuit(num_qubits=3, depth=1)
    print("Created test circuit with 3 qubits and depth 1:")
    print(test_circuit.draw())
    
    # Run noise sensitivity analysis with local simulator
    results = analyzer.analyze_noise_sensitivity(
        circuit=test_circuit,
        noise_levels=[0.001, 0.01, 0.05],
        resilience_level=1,
        shots=1000
    )
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main() 