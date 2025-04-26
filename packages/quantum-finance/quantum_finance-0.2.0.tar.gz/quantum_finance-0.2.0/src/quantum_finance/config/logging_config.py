"""
Logging configuration for the quantum-AI platform.
Implements structured logging with proper handlers and formatters.
"""

import os
import logging.config
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Logging configuration dictionary
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filename": LOGS_DIR / "quantum_ai.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filename": LOGS_DIR / "error.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "backend": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False
        },
        "backend.api": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False
        },
        "backend.nlp_processor": {
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

def setup_logging():
    """Initialize logging configuration"""
    try:
        logging.config.dictConfig(LOGGING_CONFIG)
        logging.info("Logging configuration initialized successfully")
    except Exception as e:
        print(f"Error setting up logging configuration: {str(e)}")
        # Fallback to basic configuration
        logging.basicConfig(level=logging.INFO) 