"""
Logging Configuration
Configures application-wide logging with structured output
"""

import logging
import sys
from app.config import settings


def setup_logging():
    """
    Configure logging for the application
    - Development: Human-readable format
    - Production: JSON format for log aggregation
    """
    
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Format based on environment
    if settings.is_development:
        # Human-readable format for development
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        # Structured format for production
        formatter = logging.Formatter(
            fmt='{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.INFO)
    
    logger.info(f"Logging configured - Level: {settings.LOG_LEVEL}")
