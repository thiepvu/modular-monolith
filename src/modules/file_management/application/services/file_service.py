"""
File Application Service - WITH CORRECT FACADE

FileService sử dụng Facade để isolate cross-module dependencies.
"""

from typing import List, BinaryIO, Tuple
from uuid import UUID
import logging

from core.exceptions.base_exceptions import (
    NotFoundException,
    ForbiddenException,
    ValidationException
)
from modules.file_management.domain.entities.file import File
from modules.file_management.domain.repositories.file_repository import IFileRepository
from modules.file_management.application.interfaces.file_service import IFileService
from modules.file_management.application.interfaces.file_storage_service import IFileStorageService

# ✅ ONLY import facade - NOT UserService!
from modules.file_management.application.facades.file_facades_service import FileServiceFacade

from modules.file_management.application.dto.file_dto import (
    FileUploadDTO,
    FileUpdateDTO,
    FileResponseDTO,
    FileListResponseDTO,
    FileShareDTO,
    FileDownloadResponseDTO
)
from modules.file_management.application.dto.mappers import FileMapper

logger = logging.getLogger(__name__)


class FileService(IFileService):
    """
    File application service.
    
    Uses Facade pattern to isolate cross-module dependencies.
    FileService KHÔNG biết về User module!
    """
    
    def __init__(
        self,
        file_repository: IFileRepository,
        storage_service: IFileStorageService,
        facade: FileServiceFacade  # ✅ Facade instance!
    ):
        """
        Initialize file service.
        
        Args:
            file_repository: File repository
            storage_service: File storage service
            facade: Cross-module facade (handles user operations)
        """
        self._repository = file_repository
        self._storage = storage_service
        self._facade = facade  # ✅ Store facade instance
        self._mapper = FileMapper()
        
        logger.info("FileService initialized with facade")
    
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
            
        Raises:
            ValidationException: If owner doesn't exist
        """
        logger.info(f"Uploading file: {dto.original_name} for owner: {owner_id}")
        
        # ✅ Use facade - FileService doesn't know about UserService!
        owner_exists = await self._facade.check_owner_exists(owner_id)
        if not owner_exists:
            logger.warning(f"Upload failed: Owner {owner_id} does not exist")
            raise ValidationException(
                f"Owner user {owner_id} does not exist or is inactive. "
                "Please ensure the user account is valid."
            )
        
        logger.debug(f"Owner validated via facade: {owner_id}")
        
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
        
        logger.info(f"File uploaded successfully: {saved.id}")
        
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
        if dto.original_name or dto.description:
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
        
        # ✅ Validate target user via facade
        target_exists = await self._facade.check_user_exists(dto.user_id)
        if not target_exists:
            logger.warning(f"Share failed: Target user {dto.user_id} does not exist")
            raise ValidationException(
                f"Target user {dto.user_id} does not exist or is inactive"
            )
        
        file.share_with(dto.user_id)
        updated = await self._repository.update(file)
        
        logger.info(f"File {file_id} shared with user {dto.user_id}")
        
        return self._mapper.to_response_dto(updated)
    
    async def download_file(
        self,
        file_id: UUID,
        user_id: UUID
    ) -> Tuple[FileDownloadResponseDTO, bytes]:
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
