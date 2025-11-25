"""Custom validators for common use cases"""

import re
from typing import Any, Optional
from pydantic import field_validator


class CommonValidators:
    """Common validation methods"""
    
    @staticmethod
    def validate_username(value: str) -> str:
        """
        Validate username format.
        
        Args:
            value: Username to validate
            
        Returns:
            Validated username
            
        Raises:
            ValueError: If username is invalid
        """
        if not value:
            raise ValueError("Username cannot be empty")
        
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if len(value) > 50:
            raise ValueError("Username must be at most 50 characters")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise ValueError(
                "Username can only contain letters, numbers, underscores, and hyphens"
            )
        
        return value.lower()
    
    @staticmethod
    def validate_phone_number(value: Optional[str]) -> Optional[str]:
        """
        Validate phone number format.
        
        Args:
            value: Phone number to validate
            
        Returns:
            Validated phone number
            
        Raises:
            ValueError: If phone number is invalid
        """
        if not value:
            return value
        
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)]+', '', value)
        
        # Check if it's a valid phone number (simple validation)
        if not re.match(r'^\+?[1-9]\d{1,14}$', cleaned):
            raise ValueError("Invalid phone number format")
        
        return cleaned
    
    @staticmethod
    def validate_url(value: Optional[str]) -> Optional[str]:
        """
        Validate URL format.
        
        Args:
            value: URL to validate
            
        Returns:
            Validated URL
            
        Raises:
            ValueError: If URL is invalid
        """
        if not value:
            return value
        
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        
        if not url_pattern.match(value):
            raise ValueError("Invalid URL format")
        
        return value