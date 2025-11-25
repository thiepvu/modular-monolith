"""
File storage service - handles physical file operations
"""

import os
import uuid
from pathlib import Path
from typing import BinaryIO, Optional
import aiofiles
import logging

logger = logging.getLogger(__name__)


class FileStorageService:
    """
    File storage service for handling physical file operations.
    This is an application service that manages file system operations.
    """
    
    def __init__(self, storage_path: str = "uploads"):
        """
        Initialize file storage service.
        
        Args:
            storage_path: Base path for file storage
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Generate unique filename while preserving extension.
        
        Args:
            original_filename: Original filename
            
        Returns:
            Unique filename
        """
        extension = Path(original_filename).suffix
        unique_name = f"{uuid.uuid4()}{extension}"
        return unique_name
    
    def get_storage_path(self, owner_id: str) -> Path:
        """
        Get storage path for a user.
        Creates directory if it doesn't exist.
        
        Args:
            owner_id: Owner user ID
            
        Returns:
            Storage path
        """
        user_path = self.storage_path / str(owner_id)
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path
    
    async def save_file(
        self,
        file_content: BinaryIO,
        filename: str,
        owner_id: str
    ) -> str:
        """
        Save file to storage.
        
        Args:
            file_content: File content
            filename: Filename
            owner_id: Owner user ID
            
        Returns:
            Relative path to saved file
        """
        storage_path = self.get_storage_path(owner_id)
        file_path = storage_path / filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = file_content.read()
            await f.write(content)
        
        # Return relative path
        relative_path = f"{owner_id}/{filename}"
        logger.info(f"File saved: {relative_path}")
        
        return relative_path
    
    async def read_file(self, file_path: str) -> bytes:
        """
        Read file from storage.
        
        Args:
            file_path: Relative file path
            
        Returns:
            File content
        """
        full_path = self.storage_path / file_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        async with aiofiles.open(full_path, 'rb') as f:
            content = await f.read()
        
        return content
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from storage.
        
        Args:
            file_path: Relative file path
            
        Returns:
            True if deleted, False otherwise
        """
        full_path = self.storage_path / file_path
        
        if full_path.exists():
            full_path.unlink()
            logger.info(f"File deleted: {file_path}")
            return True
        
        return False
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size.
        
        Args:
            file_path: Relative file path
            
        Returns:
            File size in bytes
        """
        full_path = self.storage_path / file_path
        return full_path.stat().st_size if full_path.exists() else 0