"""
Main application entry point for the Quantum-AI Platform.

This module initializes the Flask application with the correct configuration
and sets up all necessary extensions and blueprints.
"""

import os
import socket
import logging.config
import yaml

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .unified_data_pipeline import UnifiedDataPipeline
from .data_sources import FinancialDataFeed, IoTSensor, WeatherStation
from .config import config
from .config.logging_config import setup_logging
from .backend.api import api as api_blueprint


def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port"""
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    # Set up logging first
    setup_logging()
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app) if hasattr(config[config_name], 'init_app') else None
    
    # Initialize extensions
    CORS(app)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    
    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    # Initialize data pipeline
    app.data_pipeline = UnifiedDataPipeline() # type: ignore
    app.data_sources = [ # type: ignore
        IoTSensor(),
        FinancialDataFeed(),
        WeatherStation()
    ]
    
    return app

app = create_app()

if __name__ == '__main__':
    # Check for port in environment variable
    env_port = os.environ.get('SERVER_PORT')
    
    try:
        if env_port:
            # If env_port is '0', find an available port, otherwise use the specified port
            if env_port == '0':
                port = find_available_port(5002)
            else:
                port = int(env_port)
        else:
            # Default behavior: find an available port starting from 5002
            port = find_available_port(5002)
            
        print(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        exit(1)