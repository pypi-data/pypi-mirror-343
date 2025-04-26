#!/usr/bin/env python3

"""
Quantum Enhanced Cryptocurrency Risk Assessment (Compatibility Wrapper)

This script serves as a compatibility wrapper for the refactored quantum risk assessment package.
It provides the same interface as the original quantum_enhanced_crypto_risk.py script
but uses the refactored modular implementation.

Usage:
    python quantum_enhanced_crypto_risk_wrapper.py --symbol BTC --api_key YOUR_RAPIDAPI_KEY

Author: Quantum-AI Team
"""

import os
import argparse
import logging
from typing import Dict, List, Tuple, Optional, Any, Union

# Import the refactored components
from quantum_risk.analyzer import QuantumEnhancedCryptoRiskAnalyzer as _BaseAnalyzer
from quantum_risk.report_generator import ReportGenerator

# Provide the original class for backwards compatibility
class QuantumEnhancedCryptoRiskAnalyzer(_BaseAnalyzer):
    """
    Compatibility wrapper for the refactored QuantumEnhancedCryptoRiskAnalyzer class.
    This ensures existing code using the original implementation continues to work.
    """
    pass

def main():
    """Main function to run the quantum-enhanced risk analysis"""
    parser = argparse.ArgumentParser(description="Quantum-Enhanced Cryptocurrency Risk Assessment")
    parser.add_argument("--symbol", type=str, default="BTC", help="Cryptocurrency symbol (default: BTC)")
    parser.add_argument("--api_key", type=str, help="RapidAPI key for Binance API")
    parser.add_argument("--analog-backend", action="store_true",
                        help="Enable analog IMC backend using IBM's aihwkit for dense layers")
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = QuantumEnhancedCryptoRiskAnalyzer(api_key=args.api_key, analog_backend=args.analog_backend)
    
    # Run analysis
    print(f"Running quantum-enhanced risk analysis for {args.symbol}...")
    results = analyzer.analyze_with_quantum(args.symbol)
    
    # Generate report
    report_file = analyzer.generate_analysis_report(results)
    
    # Print summary
    print(f"\nAnalysis complete. Report saved to: {report_file}")
    print("\nSummary of results:")
    
    # Use report generator to get summary
    summary = ReportGenerator.generate_summary(results)
    for line in summary:
        print(line)

if __name__ == "__main__":
    main() 