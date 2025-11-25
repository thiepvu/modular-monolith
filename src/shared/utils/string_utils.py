"""String utility functions"""

import re
import secrets
import string
from typing import Optional


class StringUtils:
    """String utility functions"""
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        Convert string to snake_case.
        
        Args:
            text: String to convert
            
        Returns:
            snake_case string
        """
        # Insert underscore before capital letters
        text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        # Insert underscore before capital letters that follow lowercase
        text = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
        return text.lower()
    
    @staticmethod
    def to_camel_case(text: str) -> str:
        """
        Convert string to camelCase.
        
        Args:
            text: String to convert
            
        Returns:
            camelCase string
        """
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def to_pascal_case(text: str) -> str:
        """
        Convert string to PascalCase.
        
        Args:
            text: String to convert
            
        Returns:
            PascalCase string
        """
        components = text.split('_')
        return ''.join(x.title() for x in components)
    
    @staticmethod
    def slugify(text: str) -> str:
        """
        Convert string to URL-friendly slug.
        
        Args:
            text: String to slugify
            
        Returns:
            Slugified string
        """
        # Convert to lowercase
        text = text.lower()
        # Replace spaces and special chars with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        # Remove leading/trailing hyphens
        return text.strip('-')
    
    @staticmethod
    def truncate(
        text: str,
        length: int,
        suffix: str = "..."
    ) -> str:
        """
        Truncate string to specified length.
        
        Args:
            text: String to truncate
            length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated string
        """
        if len(text) <= length:
            return text
        
        return text[:length - len(suffix)] + suffix
    
    @staticmethod
    def generate_random_string(
        length: int = 32,
        include_digits: bool = True,
        include_special: bool = False
    ) -> str:
        """
        Generate random string.
        
        Args:
            length: Length of string
            include_digits: Include digits
            include_special: Include special characters
            
        Returns:
            Random string
        """
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        if include_special:
            chars += string.punctuation
        
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @staticmethod
    def mask_sensitive(
        text: str,
        visible_start: int = 4,
        visible_end: int = 4,
        mask_char: str = "*"
    ) -> str:
        """
        Mask sensitive information in string.
        
        Args:
            text: String to mask
            visible_start: Number of visible characters at start
            visible_end: Number of visible characters at end
            mask_char: Character to use for masking
            
        Returns:
            Masked string
        """
        if len(text) <= visible_start + visible_end:
            return text
        
        masked_length = len(text) - visible_start - visible_end
        return (
            text[:visible_start] +
            mask_char * masked_length +
            text[-visible_end:] if visible_end > 0 else ""
        )