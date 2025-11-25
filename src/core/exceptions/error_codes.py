"""Error code enumeration"""

from enum import Enum


class ErrorCode(str, Enum):
    """
    Standard error codes used throughout the application.
    Provides consistent error identification.
    """
    
    # Client errors (4xx)
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    UNPROCESSABLE_ENTITY = "UNPROCESSABLE_ENTITY"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    
    # Server errors (5xx)
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    
    # Domain errors
    DOMAIN_VALIDATION_ERROR = "DOMAIN_VALIDATION_ERROR"
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    
    # Infrastructure errors
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    CACHE_ERROR = "CACHE_ERROR"
    
    def __str__(self) -> str:
        """String representation"""
        return self.value