"""
Logger utility for LifeUnity AI Cognitive Twin System.
Provides centralized logging functionality with different log levels.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class CognitiveTwinLogger:
    """Custom logger for the Cognitive Twin system."""
    
    def __init__(self, name: str = "CognitiveTwin", log_dir: str = "logs"):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            log_dir: Directory to store log files
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # File handler
        log_file = log_path / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """Log error message."""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        """Log critical message."""
        self.logger.critical(message, exc_info=exc_info)


# Global logger instance
logger = CognitiveTwinLogger()


def get_logger(name: str = "CognitiveTwin") -> CognitiveTwinLogger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        CognitiveTwinLogger instance
    """
    return CognitiveTwinLogger(name)
