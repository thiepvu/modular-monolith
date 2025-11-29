"""File application service"""

from typing import List, Optional, BinaryIO
from uuid import UUID

from core.interfaces.services import IService
from core.exceptions.base_exceptions import NotFoundException, ForbiddenException
from src.modules.file_management.domain.entities.file import File
from src.modules.file_management.domain.exceptions.file_exceptions import FileAccessDeniedException
from src.modules.file_management.infrastructure.persistence.repositories.file_repository import FileRepository
from ..dto.file_dto import (
    FileUploadDTO,
    FileUpdateDTO,
    FileResponseDTO,
    FileListResponseDTO,
    FileShareDTO,
    FileDownloadResponseDTO
)
from ..dto.mappers import FileMapper
from .file_storage_service import FileStorageService


class FileService(IService):
    """
    File application service.
    Orchestrates file-related use cases.
    """
    
    def __init__(
        self,
        file_repository: FileRepository,
        storage_service: FileStorageService
    ):
        """
        Initialize file service.
        
        Args:
            file_repository: File repository
            storage_service: File storage service
        """
        self._repository = file_repository
        self._storage = storage_service
        self._mapper = FileMapper()
    
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
        # Generate unique filename
        unique_name = self._storage.generate_unique_filename(dto.original_name)
        
        # Save file to storage
        path = await self._storage.save_file(file_content, unique_name, str(owner_id))
        
        # Create file entity
        file = File.create(
            name=unique_name,
            original_name=dto.original_name,
            path=path,
            size=dto.size,
            mime_type=dto.mime_type,
            owner_id=owner_id,
            description=dto.description,
            is_public=dto.is_public
        )
        
        # Save to repository
        saved = await self._repository.add(file)
        
        return self._mapper.to_response_dto(saved)
    
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
        file = await self._repository.get_by_id(file_id)
        if not file:
            raise NotFoundException("File", file_id)
        
        if not file.can_be_accessed_by(user_id):
            raise ForbiddenException(f"Access denied to file {file_id}")
        
        return self._mapper.to_response_dto(file)
    
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
        """
        file = await self._repository.get_by_id(file_id)
        if not file:
            raise NotFoundException("File", file_id)
        
        # Only owner can update
        if file.owner_id != user_id:
            raise ForbiddenException("Only file owner can update metadata")
        
        # Update metadata
        file.update_metadata(dto.original_name, dto.description)
        
        # Update visibility
        if dto.is_public is not None:
            if dto.is_public:
                file.make_public()
            else:
                file.make_private()
        
        updated = await self._repository.update(file)
        
        return self._mapper.to_response_dto(updated)
    
    async def delete_file(self, file_id: UUID, user_id: UUID) -> None:
        """
        Delete file.
        
        Args:
            file_id: File UUID
            user_id: Requesting user ID
        """
        file = await self._repository.get_by_id(file_id)
        if not file:
            raise NotFoundException("File", file_id)
        
        # Only owner can delete
        if file.owner_id != user_id:
            raise ForbiddenException("Only file owner can delete")
        
        # Soft delete in database
        file.soft_delete()
        await self._repository.update(file)
        
        # Optionally delete physical file
        # await self._storage.delete_file(file.path.value)
    
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
            skip: Number to skip
            limit: Maximum number
            owner_only: Only files owned by user
            public_only: Only public files
            
        Returns:
            List of file DTOs
        """
        if owner_only:
            files = await self._repository.get_by_owner(user_id, skip, limit)
        elif public_only:
            files = await self._repository.get_public_files(skip, limit)
        else:
            files = await self._repository.get_accessible_by_user(user_id, skip, limit)
        
        return self._mapper.to_list_dtos(files)
    
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
            dto: Share data
            owner_id: File owner ID
            
        Returns:
            Updated file DTO
        """
        file = await self._repository.get_by_id(file_id)
        if not file:
            raise NotFoundException("File", file_id)
        
        # Only owner can share
        if file.owner_id != owner_id:
            raise ForbiddenException("Only file owner can share")
        
        file.share_with(dto.user_id)
        updated = await self._repository.update(file)
        
        return self._mapper.to_response_dto(updated)
    
    async def download_file(
        self,
        file_id: UUID,
        user_id: UUID
    ) -> tuple[FileDownloadResponseDTO, bytes]:
        """
        Download file content.
        
        Args:
            file_id: File UUID
            user_id: Requesting user ID
            
        Returns:
            Tuple of (file DTO, file content)
        """
        file = await self._repository.get_by_id(file_id)
        if not file:
            raise NotFoundException("File", file_id)
        
        # Record download (includes access check)
        file.record_download(user_id)
        await self._repository.update(file)
        
        # Read file content
        content = await self._storage.read_file(file.path.value)
        
        return self._mapper.to_download_dto(file), content
    
    async def count_files(self, user_id: UUID, owner_only: bool = False) -> int:
        """
        Count files.
        
        Args:
            user_id: User ID
            owner_only: Count only owned files
            
        Returns:
            File count
        """
        if owner_only:
            return await self._repository.count_by_owner(user_id)
        return await self._repository.count()