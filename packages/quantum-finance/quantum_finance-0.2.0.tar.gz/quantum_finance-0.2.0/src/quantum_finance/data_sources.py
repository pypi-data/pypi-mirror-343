"""
Data source implementations for the Quantum-AI Platform.

This module provides various data source implementations that can be used
with the real-time data pipeline for quantum-enhanced data processing.
"""

from abc import ABC, abstractmethod
import asyncio
import random
from datetime import datetime
from typing import Dict, Any

class DataSource(ABC):
    """Abstract base class for all data sources."""
    
    @abstractmethod
    async def get_data(self) -> Dict[str, Any]:
        """Retrieve data from the source."""
        pass

class IoTSensor(DataSource):
    """Simulated IoT sensor data source."""
    
    def __init__(self, sensor_id: str = "iot-001"):
        self.sensor_id = sensor_id
        self.metrics = ["temperature", "humidity", "pressure"]
    
    async def get_data(self) -> Dict[str, Any]:
        """Generate simulated IoT sensor data."""
        await asyncio.sleep(0.1)  # Simulate network delay
        return {
            "source_id": self.sensor_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "temperature": round(random.uniform(20, 30), 2),
                "humidity": round(random.uniform(30, 70), 2),
                "pressure": round(random.uniform(980, 1020), 2)
            }
        }

class FinancialDataFeed(DataSource):
    """Simulated financial market data feed."""
    
    def __init__(self, symbols: list = None):
        self.symbols = symbols or ["BTC", "ETH", "QAI"]
    
    async def get_data(self) -> Dict[str, Any]:
        """Generate simulated financial market data."""
        await asyncio.sleep(0.1)  # Simulate network delay
        return {
            "timestamp": datetime.now().isoformat(),
            "market_data": {
                symbol: {
                    "price": round(random.uniform(100, 10000), 2),
                    "volume": round(random.uniform(1000, 100000), 2),
                    "change": round(random.uniform(-5, 5), 2)
                }
                for symbol in self.symbols
            }
        }

class WeatherStation(DataSource):
    """Simulated weather station data source."""
    
    def __init__(self, station_id: str = "ws-001"):
        self.station_id = station_id
        self.conditions = ["Clear", "Cloudy", "Rain", "Snow"]
    
    async def get_data(self) -> Dict[str, Any]:
        """Generate simulated weather station data."""
        await asyncio.sleep(0.1)  # Simulate network delay
        return {
            "station_id": self.station_id,
            "timestamp": datetime.now().isoformat(),
            "weather_data": {
                "temperature": round(random.uniform(-10, 35), 2),
                "wind_speed": round(random.uniform(0, 100), 2),
                "humidity": round(random.uniform(0, 100), 2),
                "condition": random.choice(self.conditions)
            }
        } 