"""
File Service Interface

Defines the contract for file application service operations.
"""

from abc import ABC, abstractmethod
from typing import List, BinaryIO, Tuple
from uuid import UUID

from core.interfaces.services import IService
from modules.file_management.application.dto.file_dto import (
    FileUploadDTO,
    FileUpdateDTO,
    FileResponseDTO,
    FileListResponseDTO,
    FileShareDTO,
    FileDownloadResponseDTO
)


class IFileService(IService):
    """
    Interface for file application service.
    
    Orchestrates file-related use cases including upload, download,
    sharing, and metadata management.
    """
    
    @abstractmethod
    async def upload_file(
        self,
        dto: FileUploadDTO,
        file_content: BinaryIO,
        owner_id: UUID
    ) -> FileResponseDTO:
        """
        Upload a new file.
        
        Args:
            dto: File upload data
            file_content: File binary content
            owner_id: Owner user ID
            
        Returns:
            Uploaded file DTO
        """
        pass
    
    @abstractmethod
    async def get_file(self, file_id: UUID, user_id: UUID) -> FileResponseDTO:
        """
        Get file by ID with access check.
        
        Args:
            file_id: File UUID
            user_id: Requesting user ID
            
        Returns:
            File DTO
            
        Raises:
            NotFoundException: If file not found
            ForbiddenException: If user doesn't have access
        """
        pass
    
    @abstractmethod
    async def update_file(
        self,
        file_id: UUID,
        dto: FileUpdateDTO,
        user_id: UUID
    ) -> FileResponseDTO:
        """
        Update file metadata.
        
        Args:
            file_id: File UUID
            dto: Update data
            user_id: Requesting user ID
            
        Returns:
            Updated file DTO
            
        Raises:
            NotFoundException: If file not found
            ForbiddenException: If user is not the owner
        """
        pass
    
    @abstractmethod
    async def delete_file(self, file_id: UUID, user_id: UUID) -> None:
        """
        Delete file.
        
        Args:
            file_id: File UUID
            user_id: Requesting user ID
            
        Raises:
            NotFoundException: If file not found
            ForbiddenException: If user is not the owner
        """
        pass
    
    @abstractmethod
    async def list_files(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        owner_only: bool = False,
        public_only: bool = False
    ) -> List[FileListResponseDTO]:
        """
        List files accessible by user.
        
        Args:
            user_id: Requesting user ID
            skip: Number of records to skip
            limit: Maximum number of records
            owner_only: Only files owned by user
            public_only: Only public files
            
        Returns:
            List of file DTOs
        """
        pass
    
    @abstractmethod
    async def share_file(
        self,
        file_id: UUID,
        dto: FileShareDTO,
        owner_id: UUID
    ) -> FileResponseDTO:
        """
        Share file with another user.
        
        Args:
            file_id: File UUID
            dto: Share data containing target user_id
            owner_id: File owner ID
            
        Returns:
            Updated file DTO
            
        Raises:
            NotFoundException: If file not found
            ForbiddenException: If user is not the owner
        """
        pass
    
    @abstractmethod
    async def download_file(
        self,
        file_id: UUID,
        user_id: UUID
    ) -> Tuple[FileDownloadResponseDTO, bytes]:
        """
        Download file content.
        
        Records download count and performs access check.
        
        Args:
            file_id: File UUID
            user_id: Requesting user ID
            
        Returns:
            Tuple of (file download DTO, file content bytes)
            
        Raises:
            NotFoundException: If file not found
            ForbiddenException: If user doesn't have access
        """
        pass
    
    @abstractmethod
    async def count_files(self, user_id: UUID, owner_only: bool = False) -> int:
        """
        Count files.
        
        Args:
            user_id: User ID
            owner_only: Count only files owned by user
            
        Returns:
            File count
        """
        pass