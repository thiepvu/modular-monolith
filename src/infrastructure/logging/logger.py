"""
Logging configuration and utilities.
Provides structured logging with JSON format support.
"""

import logging
import sys
from typing import Any, Dict
from datetime import datetime
import json


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Outputs log records as JSON objects.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON formatted log string
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        extra_fields = [
            "request_id", "user_id", "correlation_id",
            "duration", "status_code", "method", "path"
        ]
        
        for field in extra_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """
    Colored formatter for console output.
    Makes logs easier to read in development.
    """
    
    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        
        # Save original levelname
        levelname = record.levelname
        
        # Add color to level name
        if levelname in self.COLORS:
            colored_levelname = (
                f"{self.BOLD}{self.COLORS[levelname]}"
                f"{levelname}{self.RESET}"
            )
            record.levelname = colored_levelname
        
        # Format the message
        formatted = super().format(record)
        
        # Reset level name
        record.levelname = levelname
        
        return formatted


def setup_logging(
    level: str = "INFO",
    format_type: str = "json",
    log_file: str = None
) -> None:
    """
    Setup application logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Format type ('json' or 'text')
        log_file: Optional log file path
    """
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Set formatter based on format type
    if format_type == "json":
        formatter = JSONFormatter()
    else:
        formatter = ColoredFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(JSONFormatter())  # Always JSON for files
        logger.addHandler(file_handler)
    
    # Suppress noisy loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)