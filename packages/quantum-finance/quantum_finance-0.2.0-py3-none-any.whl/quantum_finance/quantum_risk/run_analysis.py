#!/usr/bin/env python3

"""
Command-line interface for quantum-enhanced cryptocurrency risk assessment.

This script provides a command-line interface for running the quantum-enhanced
cryptocurrency risk assessment.

Usage:
    python -m quantum_risk.run_analysis --symbol BTC

Author: Quantum-AI Team
"""

import argparse
# Use relative imports for internal modules to maintain package consistency
from .analyzer import QuantumEnhancedCryptoRiskAnalyzer  # Updated to relative import
from .report_generator import ReportGenerator             # Updated to relative import
from .utils.logging_util import setup_logger               # Updated to relative import

logger = setup_logger(__name__)


def main():
    """Main function to run the quantum-enhanced risk analysis"""

    parser = argparse.ArgumentParser(
        description=("Quantum-Enhanced Cryptocurrency Risk Assessment"),
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTC",
        help="Cryptocurrency symbol (default: BTC)",
    )
    parser.add_argument(
        "--api_key",
        type=str,
        help="RapidAPI key for Binance API",
    )
    parser.add_argument(
        "--analog-backend",
        action="store_true",
        help="Enable analog IMC backend for neuromorphic integration",
    )
    args = parser.parse_args()

    # Initialize analyzer
    analyzer = QuantumEnhancedCryptoRiskAnalyzer(
        api_key=args.api_key,
        analog_backend=args.analog_backend
    )

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

"""
End of file with newline preserved for lint compliance
"""
