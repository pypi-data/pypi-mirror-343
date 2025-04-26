"""
Configuration module for the Quantum-AI Platform.

This module provides configuration management for different environments
(development, testing, production) and handles loading of environment variables.
"""

import os
from pathlib import Path

class Config:
    """Base configuration class."""
    # Basic Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Application root directory
    BASE_DIR = Path(__file__).parent.parent.absolute()
    
    # API configuration
    API_PREFIX = '/api/v1'
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Quantum simulation settings
    MAX_QUBITS = int(os.getenv('MAX_QUBITS', '10'))
    SIMULATION_BACKEND = os.getenv('SIMULATION_BACKEND', 'aer_simulator')
    
    # AI Model settings
    MODEL_PATH = os.path.join(BASE_DIR, 'models')
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '32'))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'quantum_ai.log')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    FLASK_ENV = 'development'
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    
    # Testing-specific settings
    FLASK_ENV = 'testing'
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    FLASK_ENV = 'production'
    RATELIMIT_DEFAULT = "100 per day"  # More restrictive in production
    
    @classmethod
    def init_app(cls, app):
        """Production-specific initialization."""
        # Set up production-specific logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        file_handler = RotatingFileHandler(
            'logs/quantum_ai.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 