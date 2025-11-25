"""
Logging configuration for the application.
Provides structured logging with different formats.
"""

import logging
import sys
from typing import Any, Dict
from datetime import datetime
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        
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
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        # Add any extra attributes
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "message", "pathname", "process", "processName", "relativeCreated",
                "thread", "threadName", "exc_info", "exc_text", "stack_info"
            ]:
                log_data[key] = value
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            colored_levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
            record.levelname = colored_levelname
        
        # Format the message
        formatted = super().format(record)
        
        # Reset level name (in case logger is reused)
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
    
    # Set formatter
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
        file_handler.setFormatter(JSONFormatter())  # Always use JSON for files
        logger.addHandler(file_handler)
    
    # Suppress noisy loggers
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
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


# Context manager for request logging
class RequestLogger:
    """Context manager for logging request information"""
    
    def __init__(self, logger: logging.Logger, request_id: str):
        self.logger = logger
        self.request_id = request_id
        self.start_time = None
    
    def __enter__(self):
        """Enter context"""
        self.start_time = datetime.utcnow()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and log duration"""
        duration = (datetime.utcnow() - self.start_time).total_seconds()
        
        extra = {"request_id": self.request_id, "duration": duration}
        
        if exc_type:
            self.logger.error(
                f"Request failed: {exc_val}",
                extra=extra,
                exc_info=True
            )
        else:
            self.logger.info(f"Request completed", extra=extra)