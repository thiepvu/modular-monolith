"""Standard API response models"""

from datetime import datetime
from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    
    success: bool = Field(default=True, description="Request success status")
    data: Optional[T] = Field(default=None, description="Response data")
    message: Optional[str] = Field(default=None, description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorDetail(BaseModel):
    """Error detail model"""
    
    field: Optional[str] = Field(None, description="Field that caused the error")
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class ErrorResponse(BaseModel):
    """Standard error response"""
    
    success: bool = Field(default=False, description="Always false for errors")
    error: Dict[str, Any] = Field(..., description="Error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }