"""
Data sources module for the Quantum-AI Platform.
Provides various data source implementations for testing and production use.
"""

import random
import asyncio
from datetime import datetime
from typing import Dict, List, Any

class IoTSensor:
    """Simulated IoT sensor for testing."""
    
    def __init__(self, sensor_id: str = "test-sensor"):
        self.sensor_id = sensor_id
    
    async def get_data(self) -> Dict[str, Any]:
        """Generate simulated sensor data."""
        return {
            'source_id': self.sensor_id,
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'temperature': random.uniform(20, 30),
                'humidity': random.uniform(30, 70),
                'pressure': random.uniform(980, 1020)
            }
        }

class FinancialDataFeed:
    """Simulated financial data feed for testing."""
    
    def __init__(self, symbols: List[str] = None):
        self.symbols = symbols or ["BTC", "ETH"]
    
    async def get_data(self) -> Dict[str, Any]:
        """Generate simulated financial data."""
        market_data = {}
        for symbol in self.symbols:
            market_data[symbol] = {
                'price': random.uniform(100, 10000),
                'volume': random.randint(1000, 100000),
                'change': random.uniform(-5, 5)
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'market_data': market_data
        }

class WeatherStation:
    """Simulated weather station for testing."""
    
    def __init__(self, station_id: str = "test-station"):
        self.station_id = station_id
        self.conditions = ["Clear", "Cloudy", "Rain", "Snow"]
    
    async def get_data(self) -> Dict[str, Any]:
        """Generate simulated weather data."""
        return {
            'station_id': self.station_id,
            'timestamp': datetime.now().isoformat(),
            'weather_data': {
                'temperature': random.uniform(-10, 35),
                'wind_speed': random.uniform(0, 100),
                'humidity': random.uniform(0, 100),
                'condition': random.choice(self.conditions)
            }
        } 