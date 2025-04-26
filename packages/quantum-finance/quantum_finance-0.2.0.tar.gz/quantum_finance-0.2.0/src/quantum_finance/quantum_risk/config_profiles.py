#!/usr/bin/env python3

"""
Configuration Profiles for Quantum Risk Package

This module defines different configuration profiles for the quantum risk assessment
package, tailored for various use cases and risk assessment scenarios.

Each profile contains settings for:
- Exchange selection
- Data retrieval parameters
- Quantum algorithm configuration
- Risk assessment thresholds
- Reporting preferences

Author: Quantum-AI Team
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path

from quantum_finance.quantum_risk.utils.logging_util import setup_logger

logger = setup_logger(__name__)

# Default configuration path
DEFAULT_CONFIG_PATH = Path(os.path.dirname(os.path.abspath(__file__))) / "configs"


class ConfigurationProfiles:
    """
    Manages configuration profiles for the quantum risk assessment package.

    This class provides methods to:
    - Load predefined profiles
    - Create custom profiles
    - Save profiles to disk
    - Validate profile configurations
    """

    # Predefined configuration profiles
    PREDEFINED_PROFILES = {
        "default": {
            "description": "Balanced configuration for general risk assessment",
            "exchanges": ["binance_futures", "kucoin"],
            "symbols": ["BTC", "ETH"],
            "risk_parameters": {
                "quantum_circuit_depth": 3,
                "shots": 1024,
                "optimization_level": 1,
                "bayesian_priors": "auto",
                "risk_threshold": 0.7,
            },
            "data_parameters": {
                "historical_days": 30,
                "order_book_depth": 20,
                "trade_limit": 100,
            },
            "report_parameters": {
                "generate_charts": True,
                "include_raw_data": False,
                "output_format": "json",
            },
        },
        "high_frequency": {
            "description": "Configuration optimized for high-frequency trading risk assessment",
            "exchanges": ["binance_futures", "kucoin"],
            "symbols": ["BTC", "ETH"],
            "risk_parameters": {
                "quantum_circuit_depth": 4,
                "shots": 2048,
                "optimization_level": 2,
                "bayesian_priors": "adaptive",
                "risk_threshold": 0.6,
                "volatility_weight": 1.5,
                "liquidity_weight": 1.2,
                "correlation_weight": 1.3,
            },
            "data_parameters": {
                "historical_days": 7,
                "order_book_depth": 50,
                "trade_limit": 500,
                "time_interval": "5min",
            },
            "report_parameters": {
                "generate_charts": True,
                "include_raw_data": True,
                "output_format": "json",
                "real_time_alerts": True,
            },
        },
        "conservative": {
            "description": "Conservative configuration with stricter risk thresholds",
            "exchanges": ["binance_futures", "kucoin"],
            "symbols": ["BTC", "ETH", "USDT", "USDC"],
            "risk_parameters": {
                "quantum_circuit_depth": 3,
                "shots": 1024,
                "optimization_level": 1,
                "bayesian_priors": "conservative",
                "risk_threshold": 0.5,
                "volatility_weight": 2.0,
                "liquidity_weight": 1.5,
                "correlation_weight": 1.0,
            },
            "data_parameters": {
                "historical_days": 90,
                "order_book_depth": 20,
                "trade_limit": 100,
                "time_interval": "1day",
            },
            "report_parameters": {
                "generate_charts": True,
                "include_raw_data": False,
                "output_format": "json",
                "include_correlation_matrix": True,
                "include_stress_tests": True,
            },
        },
        "aggressive": {
            "description": "Aggressive configuration for opportunity detection",
            "exchanges": ["binance_futures", "kucoin"],
            "symbols": ["BTC", "ETH", "SOL", "ADA", "XRP"],
            "risk_parameters": {
                "quantum_circuit_depth": 2,
                "shots": 512,
                "optimization_level": 0,
                "bayesian_priors": "optimistic",
                "risk_threshold": 0.8,
                "volatility_weight": 0.7,
                "liquidity_weight": 0.5,
                "correlation_weight": 0.8,
            },
            "data_parameters": {
                "historical_days": 14,
                "order_book_depth": 10,
                "trade_limit": 50,
                "time_interval": "15min",
            },
            "report_parameters": {
                "generate_charts": True,
                "include_raw_data": False,
                "output_format": "json",
                "focus_on_opportunities": True,
            },
        },
    }

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the configuration profiles manager.

        Args:
            config_dir: Optional directory path where configuration files are stored
        """
        self.config_dir = (
            config_dir
            or os.environ.get("QUANTUM_RISK_CONFIG_DIR")
            or DEFAULT_CONFIG_PATH
        )

        # Ensure the config directory exists
        os.makedirs(self.config_dir, exist_ok=True)

        # Load and merge custom profiles with predefined ones
        self.profiles = self.PREDEFINED_PROFILES.copy()
        self._load_custom_profiles()

        logger.info(
            f"Initialized ConfigurationProfiles with {len(self.profiles)} profiles"
        )

    def _load_custom_profiles(self):
        """Load custom profiles from the configuration directory"""
        config_path = Path(self.config_dir)

        if not config_path.exists() or not config_path.is_dir():
            logger.warning(
                f"Configuration directory {self.config_dir} not found or not a directory"
            )
            return

        # Look for JSON and YAML configuration files
        config_files = (
            list(config_path.glob("*.json"))
            + list(config_path.glob("*.yaml"))
            + list(config_path.glob("*.yml"))
        )

        for config_file in config_files:
            try:
                profile_name = config_file.stem

                # Skip if a predefined profile with the same name exists
                if profile_name in self.PREDEFINED_PROFILES:
                    logger.warning(
                        f"Custom profile '{profile_name}' conflicts with a predefined profile, skipping"
                    )
                    continue

                # Load the profile based on the file extension
                if config_file.suffix == ".json":
                    with open(config_file, "r") as f:
                        profile = json.load(f)
                else:  # YAML file
                    with open(config_file, "r") as f:
                        profile = yaml.safe_load(f)

                # Validate the profile
                if self._validate_profile(profile):
                    self.profiles[profile_name] = profile
                    logger.info(f"Loaded custom profile: {profile_name}")
                else:
                    logger.warning(f"Invalid profile format in {config_file}, skipping")

            except Exception as e:
                logger.error(f"Error loading profile from {config_file}: {e}")

    def _validate_profile(self, profile: Dict[str, Any]) -> bool:
        """
        Validate a configuration profile.

        Args:
            profile: Configuration profile dictionary

        Returns:
            True if the profile is valid, False otherwise
        """
        # Basic validation - check for required sections
        required_sections = ["risk_parameters", "data_parameters", "report_parameters"]

        for section in required_sections:
            if section not in profile:
                logger.warning(f"Profile missing required section: {section}")
                return False

        # TODO: Add more detailed validation of each section's parameters

        return True

    def get_profile(self, profile_name: str) -> Dict[str, Any]:
        """
        Get a configuration profile by name.

        Args:
            profile_name: Name of the profile to retrieve

        Returns:
            Configuration profile dictionary

        Raises:
            ValueError: If the profile does not exist
        """
        if profile_name not in self.profiles:
            raise ValueError(f"Profile '{profile_name}' not found")

        return self.profiles[profile_name]

    def create_profile(
        self, profile_name: str, profile_data: Dict[str, Any], save: bool = True
    ) -> None:
        """
        Create a new configuration profile.

        Args:
            profile_name: Name of the new profile
            profile_data: Configuration profile dictionary
            save: Whether to save the profile to disk

        Raises:
            ValueError: If the profile name already exists or the profile data is invalid
        """
        # Check if the profile already exists
        if profile_name in self.PREDEFINED_PROFILES:
            raise ValueError(f"Cannot override predefined profile '{profile_name}'")

        if profile_name in self.profiles:
            raise ValueError(f"Profile '{profile_name}' already exists")

        # Validate the profile
        if not self._validate_profile(profile_data):
            raise ValueError("Invalid profile format")

        # Add the profile
        self.profiles[profile_name] = profile_data
        logger.info(f"Created new profile: {profile_name}")

        # Save to disk if requested
        if save:
            self.save_profile(profile_name)

    def save_profile(self, profile_name: str, format: str = "json") -> None:
        """
        Save a configuration profile to disk.

        Args:
            profile_name: Name of the profile to save
            format: File format (json or yaml)

        Raises:
            ValueError: If the profile does not exist or the format is invalid
        """
        if profile_name not in self.profiles:
            raise ValueError(f"Profile '{profile_name}' not found")

        if profile_name in self.PREDEFINED_PROFILES:
            logger.warning(f"Saving a copy of predefined profile '{profile_name}'")

        # Get the profile
        profile = self.profiles[profile_name]

        # Determine the file path
        if format.lower() == "json":
            file_path = Path(self.config_dir) / f"{profile_name}.json"
            # Save as JSON
            with open(file_path, "w") as f:
                json.dump(profile, f, indent=2)
        elif format.lower() in ["yaml", "yml"]:
            file_path = Path(self.config_dir) / f"{profile_name}.yaml"
            # Save as YAML
            with open(file_path, "w") as f:
                yaml.dump(profile, f, default_flow_style=False)
        else:
            raise ValueError(f"Invalid format: {format}")

        logger.info(f"Saved profile '{profile_name}' to {file_path}")

    def list_profiles(self) -> List[Dict[str, Any]]:
        """
        Get a list of available profiles with their descriptions.

        Returns:
            List of dictionaries containing profile names and descriptions
        """
        return [
            {
                "name": name,
                "description": profile.get("description", "No description"),
                "predefined": name in self.PREDEFINED_PROFILES,
            }
            for name, profile in self.profiles.items()
        ]

    def delete_profile(self, profile_name: str) -> None:
        """
        Delete a custom configuration profile.

        Args:
            profile_name: Name of the profile to delete

        Raises:
            ValueError: If the profile does not exist or is predefined
        """
        if profile_name not in self.profiles:
            raise ValueError(f"Profile '{profile_name}' not found")

        if profile_name in self.PREDEFINED_PROFILES:
            raise ValueError(f"Cannot delete predefined profile '{profile_name}'")

        # Remove from memory
        del self.profiles[profile_name]

        # Remove from disk
        for ext in [".json", ".yaml", ".yml"]:
            file_path = Path(self.config_dir) / f"{profile_name}{ext}"
            if file_path.exists():
                file_path.unlink()
                break

        logger.info(f"Deleted profile: {profile_name}")


# Create a singleton instance for easy access
config_profiles = ConfigurationProfiles()


if __name__ == "__main__":
    # Simple test code
    profiles = ConfigurationProfiles()

    print("Available profiles:")
    for profile_info in profiles.list_profiles():
        predefined = "predefined" if profile_info["predefined"] else "custom"
        print(f"- {profile_info['name']} ({predefined}): {profile_info['description']}")

    # Get the high frequency profile and print its risk parameters
    try:
        high_freq = profiles.get_profile("high_frequency")
        print("\nHigh Frequency Profile Risk Parameters:")
        for key, value in high_freq["risk_parameters"].items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")
