"""File API controller"""

from uuid import UUID
from typing import Optional
from fastapi import Depends, UploadFile, File as FastAPIFile, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import io

from shared.api.base_controller import BaseController
from shared.api.response import ApiResponse
from shared.api.pagination import PaginationParams, PaginatedResponse
from shared.repositories.unit_of_work import UnitOfWork

# Import module's DB dependency
from modules.file_management.presentation.dependencies import get_file_db_session, get_file_service
from modules.file_management.application.dto.file_dto import (
    FileUploadDTO,
    FileUpdateDTO,
    FileResponseDTO,
    FileListResponseDTO,
    FileShareDTO
)


class FileController(BaseController):
    """File API controller"""
    
    def __init__(self):
        super().__init__()
        self._file_service = get_file_service  # Initialized per request
    
    async def upload_file(
        self,
        file: UploadFile,
        description: Optional[str] = None,
        is_public: bool = False,
        user_id: UUID = None,  # TODO: Get from auth
        session: AsyncSession = Depends(get_file_db_session)
    ) -> ApiResponse[FileResponseDTO]:
        """
        Upload a new file.
        
        Args:
            file: Uploaded file
            description: File description
            is_public: Public access flag
            user_id: Current user ID
            session: Database session
            
        Returns:
            Uploaded file response
        """
        # Create DTO
        dto = FileUploadDTO(
            name=file.filename,
            path="",
            original_name=file.filename or "unnamed",
            size=file.size or 0,
            mime_type=file.content_type or "application/octet-stream",
            description=description,
            is_public=is_public
        )
        
        async with UnitOfWork(session):
            service = self._file_service(session)
            
            # Upload file
            uploaded = await service.upload_file(
                dto=dto,
                file_content=file.file,
                owner_id=user_id
            )
            
            return self.created(uploaded, "File uploaded successfully")
    
    async def get_file(
        self,
        file_id: UUID,
        user_id: UUID = None,  # TODO: Get from auth
        session: AsyncSession = Depends(get_file_db_session)
    ) -> ApiResponse[FileResponseDTO]:
        """Get file metadata"""
        service = self._file_service(session)
        file = await service.get_file(file_id, user_id)
        return self.success(file)
    
    async def update_file(
        self,
        file_id: UUID,
        dto: FileUpdateDTO,
        user_id: UUID = None,  # TODO: Get from auth
        session: AsyncSession = Depends(get_file_db_session)
    ) -> ApiResponse[FileResponseDTO]:
        """Update file metadata"""
        async with UnitOfWork(session):
            service = self._file_service(session)
            updated = await service.update_file(file_id, dto, user_id)
            return self.success(updated, "File updated successfully")
    
    async def delete_file(
        self,
        file_id: UUID,
        user_id: UUID = None,  # TODO: Get from auth
        session: AsyncSession = Depends(get_file_db_session)
    ) -> ApiResponse:
        """Delete file"""
        async with UnitOfWork(session):
            service = self._file_service(session)
            await service.delete_file(file_id, user_id)
            return self.no_content("File deleted successfully")
    
    async def list_files(
        self,
        params: PaginationParams = Depends(),
        owner_only: bool = Query(False, description="Only my files"),
        public_only: bool = Query(False, description="Only public files"),
        user_id: UUID = None,  # TODO: Get from auth
        session: AsyncSession = Depends(get_file_db_session)
    ) -> ApiResponse[PaginatedResponse[FileListResponseDTO]]:
        """List files"""
        service = self._file_service(session)
        
        files = await service.list_files(
            user_id=user_id,
            skip=params.skip,
            limit=params.limit,
            owner_only=owner_only,
            public_only=public_only
        )
        
        total = await service.count_files(user_id, owner_only)
        
        return self.paginated(files, total, params)
    
    async def share_file(
        self,
        file_id: UUID,
        dto: FileShareDTO,
        user_id: UUID = None,  # TODO: Get from auth
        session: AsyncSession = Depends(get_file_db_session)
    ) -> ApiResponse[FileResponseDTO]:
        """Share file with another user"""
        async with UnitOfWork(session):
            service = self._file_service(session)
            shared = await service.share_file(file_id, dto, user_id)
            return self.success(shared, "File shared successfully")
    
    async def download_file(
        self,
        file_id: UUID,
        user_id: UUID = None,  # TODO: Get from auth
        session: AsyncSession = Depends(get_file_db_session)
    ) -> StreamingResponse:
        """Download file content"""
        async with UnitOfWork(session):
            service = self._file_service(session)
            file_dto, content = await service.download_file(file_id, user_id)
            
            # Return file as streaming response
            return StreamingResponse(
                io.BytesIO(content),
                media_type=file_dto.mime_type,
                headers={
                    "Content-Disposition": f'attachment; filename="{file_dto.original_name}"'
                }
            )