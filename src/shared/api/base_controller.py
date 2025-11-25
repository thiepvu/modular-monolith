"""Base controller with common response methods"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from fastapi import HTTPException, status
from pydantic import BaseModel

from .response import ApiResponse
from .pagination import PaginatedResponse, PaginationParams

T = TypeVar("T")


class BaseController:
    """Base controller with common response methods"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: Optional[str] = None,
        status_code: int = status.HTTP_200_OK
    ) -> ApiResponse:
        """
        Return success response.
        
        Args:
            data: Response data
            message: Optional success message
            status_code: HTTP status code
            
        Returns:
            ApiResponse with success=True
        """
        return ApiResponse(
            success=True,
            data=data,
            message=message
        )
    
    @staticmethod
    def created(
        data: Any,
        message: str = "Resource created successfully"
    ) -> ApiResponse:
        """
        Return created response (201).
        
        Args:
            data: Created resource data
            message: Success message
            
        Returns:
            ApiResponse with created data
        """
        return ApiResponse(
            success=True,
            data=data,
            message=message
        )
    
    @staticmethod
    def no_content(message: str = "Operation completed successfully") -> ApiResponse:
        """
        Return no content response.
        
        Args:
            message: Success message
            
        Returns:
            ApiResponse with no data
        """
        return ApiResponse(
            success=True,
            data=None,
            message=message
        )
    
    @staticmethod
    def paginated(
        items: List[T],
        total: int,
        params: PaginationParams
    ) -> ApiResponse[PaginatedResponse[T]]:
        """
        Return paginated response.
        
        Args:
            items: List of items for current page
            total: Total number of items
            params: Pagination parameters
            
        Returns:
            ApiResponse with paginated data
        """
        paginated_data = PaginatedResponse.create(items, total, params)
        return ApiResponse(
            success=True,
            data=paginated_data
        )
    
    @staticmethod
    def error(
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None
    ) -> HTTPException:
        """
        Raise HTTP exception with error response.
        
        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
            
        Raises:
            HTTPException with formatted error
        """
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "error": {
                    "message": message,
                    "details": details or {}
                }
            }
        )