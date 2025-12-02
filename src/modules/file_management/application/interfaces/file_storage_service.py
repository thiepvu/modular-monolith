"""
File Storage Service Interface

Defines the contract for physical file storage operations.
"""

from abc import ABC, abstractmethod
from typing import BinaryIO

from core.interfaces.services import IService

class IFileStorageService(IService):
    """
    Interface for file storage service.
    
    Handles physical file operations such as saving, reading,
    and deleting files from the storage system.
    """
    
    @abstractmethod
    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Generate unique filename while preserving extension.
        
        Args:
            original_filename: Original filename
            
        Returns:
            Unique filename with UUID
            
        Example:
            "document.pdf" -> "550e8400-e29b-41d4-a716-446655440000.pdf"
        """
        pass
    
    @abstractmethod
    async def save_file(
        self,
        file_content: BinaryIO,
        filename: str,
        owner_id: str
    ) -> str:
        """
        Save file to storage.
        
        Args:
            file_content: File binary content
            filename: Filename (should be unique)
            owner_id: Owner user ID (used for directory structure)
            
        Returns:
            Relative path to saved file
            
        Example:
            Returns: "user-123/550e8400-e29b-41d4-a716-446655440000.pdf"
        """
        pass
    
    @abstractmethod
    async def read_file(self, file_path: str) -> bytes:
        """
        Read file from storage.
        
        Args:
            file_path: Relative file path
            
        Returns:
            File content as bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        pass
    
    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from storage.
        
        Args:
            file_path: Relative file path
            
        Returns:
            True if file was deleted, False if file didn't exist
        """
        pass
    
    @abstractmethod
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Relative file path
            
        Returns:
            File size in bytes, or 0 if file doesn't exist
        """
        pass