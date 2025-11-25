"""DateTime utility functions"""

from datetime import datetime, timezone, timedelta
from typing import Optional


class DateTimeUtils:
    """DateTime utility functions"""
    
    @staticmethod
    def utc_now() -> datetime:
        """
        Get current UTC datetime.
        
        Returns:
            Current UTC datetime
        """
        return datetime.now(timezone.utc)
    
    @staticmethod
    def to_utc(dt: datetime) -> datetime:
        """
        Convert datetime to UTC.
        
        Args:
            dt: Datetime to convert
            
        Returns:
            UTC datetime
        """
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    
    @staticmethod
    def format_iso(dt: datetime) -> str:
        """
        Format datetime as ISO 8601 string.
        
        Args:
            dt: Datetime to format
            
        Returns:
            ISO 8601 formatted string
        """
        return dt.isoformat()
    
    @staticmethod
    def parse_iso(iso_string: str) -> datetime:
        """
        Parse ISO 8601 datetime string.
        
        Args:
            iso_string: ISO 8601 string to parse
            
        Returns:
            Parsed datetime
        """
        return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """
        Add days to datetime.
        
        Args:
            dt: Base datetime
            days: Number of days to add
            
        Returns:
            New datetime
        """
        return dt + timedelta(days=days)
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """
        Add hours to datetime.
        
        Args:
            dt: Base datetime
            hours: Number of hours to add
            
        Returns:
            New datetime
        """
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def is_expired(dt: datetime, now: Optional[datetime] = None) -> bool:
        """
        Check if datetime is expired.
        
        Args:
            dt: Datetime to check
            now: Current datetime (defaults to UTC now)
            
        Returns:
            True if expired, False otherwise
        """
        if now is None:
            now = DateTimeUtils.utc_now()
        return dt < now