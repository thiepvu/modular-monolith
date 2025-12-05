from uuid import UUID
from typing import Optional
from fastapi import  UploadFile
from fastapi.responses import StreamingResponse
import io

from shared.api.base_controller import BaseController
from shared.api.response import ApiResponse
from shared.api.pagination import PaginationParams, PaginatedResponse
from shared.repositories.unit_of_work import UnitOfWork

from modules.file_management.presentation.dependencies import FileServiceDep
from modules.file_management.application.dto.file_dto import (
    FileUploadDTO,
    FileUpdateDTO,
    FileResponseDTO,
    FileListResponseDTO,
    FileShareDTO
)


class FileController(BaseController):
    """
    File API controller.
    """
    
    def __init__(self):
        super().__init__()
    
    # ========================================================================
    # WRITE OPERATIONS - with UnitOfWork
    # ========================================================================
    
    async def upload_file(
        self,
        file: UploadFile,
        description: Optional[str],
        is_public: bool,
        user_id: UUID,
        file_service: FileServiceDep  # ✅ NO session parameter!
    ) -> ApiResponse[FileResponseDTO]:
        """
        Upload a new file.
        
        Args:
            file: Uploaded file
            description: File description
            is_public: Public access flag
            user_id: Current user ID (TODO: from auth)
            file_service: File service (auto-injected)
            
        Returns:
            Uploaded file response
            
        Note:
            Session has set ContextVar (set by @with_session decorator).
            UnitOfWork auto get session từ ContextVar.
        """
        # Create DTO
        dto = FileUploadDTO(
            name=file.filename,
            path="",  # Will be set by storage service
            original_name=file.filename or "unnamed",
            size=file.size or 0,
            mime_type=file.content_type or "application/octet-stream",
            description=description,
            is_public=is_public
        )
        
        # UnitOfWork tự lấy session từ ContextVar
        async with UnitOfWork():
            # Upload file
            uploaded = await file_service.upload_file(
                dto=dto,
                file_content=file.file,
                owner_id=user_id
            )
            # UnitOfWork tự commit khi exit context
            return self.created(uploaded, "File uploaded successfully")
    
    async def update_file(
        self,
        file_id: UUID,
        dto: FileUpdateDTO,
        user_id: UUID,
        file_service: FileServiceDep  # ✅ NO session!
    ) -> ApiResponse[FileResponseDTO]:
        """
        Update file metadata.
        
        Args:
            file_id: File UUID
            dto: Update data
            user_id: Current user ID
            file_service: File service
            
        Returns:
            Updated file response
        """
        async with UnitOfWork():
            updated = await file_service.update_file(file_id, dto, user_id)
            return self.success(updated, "File updated successfully")
    
    async def delete_file(
        self,
        file_id: UUID,
        user_id: UUID,
        file_service: FileServiceDep
    ) -> ApiResponse:
        """
        Delete file.
        
        Args:
            file_id: File UUID
            user_id: Current user ID
            file_service: File service
            
        Returns:
            Success response
        """
        async with UnitOfWork():
            await file_service.delete_file(file_id, user_id)
            return self.no_content("File deleted successfully")
    
    async def share_file(
        self,
        file_id: UUID,
        dto: FileShareDTO,
        user_id: UUID,
        file_service: FileServiceDep
    ) -> ApiResponse[FileResponseDTO]:
        """
        Share file with another user.
        
        Args:
            file_id: File UUID
            dto: Share data
            user_id: Current user ID (file owner)
            file_service: File service
            
        Returns:
            Updated file response
        """
        async with UnitOfWork():
            shared = await file_service.share_file(file_id, dto, user_id)
            return self.success(shared, "File shared successfully")
    
    async def download_file(
        self,
        file_id: UUID,
        user_id: UUID,
        file_service: FileServiceDep
    ) -> StreamingResponse:
        """
        Download file content.
        
        Args:
            file_id: File UUID
            user_id: Current user ID
            file_service: File service
            
        Returns:
            Streaming response with file content
        """
        async with UnitOfWork():
            file_dto, content = await file_service.download_file(file_id, user_id)
            
            # Return file as streaming response
            return StreamingResponse(
                io.BytesIO(content),
                media_type=file_dto.mime_type,
                headers={
                    "Content-Disposition": f'attachment; filename="{file_dto.original_name}"'
                }
            )
    
    # ========================================================================
    # READ OPERATIONS - No need UnitOfWork
    # ========================================================================
    
    async def get_file(
        self,
        file_id: UUID,
        user_id: UUID,
        file_service: FileServiceDep  # ✅ NO session!
    ) -> ApiResponse[FileResponseDTO]:
        """
        Get file metadata.
        
        Args:
            file_id: File UUID
            user_id: Current user ID
            file_service: File service
            
        Returns:
            File response
            
        Note:
            Read-only operation, No need UnitOfWork.
            Repository auto get session from ContextVar.
        """
        file = await file_service.get_file(file_id, user_id)
        return self.success(file)
    
    async def list_files(
        self,
        params: PaginationParams,
        owner_only: bool,
        public_only: bool,
        user_id: UUID,
        file_service: FileServiceDep
    ) -> ApiResponse[PaginatedResponse[FileListResponseDTO]]:
        """
        List files with pagination.
        
        Args:
            params: Pagination parameters
            owner_only: Show only user's files
            public_only: Show only public files
            user_id: Current user ID
            file_service: File service
            
        Returns:
            Paginated file list response
        """
        files = await file_service.list_files(
            user_id=user_id,
            skip=params.skip,
            limit=params.limit,
            owner_only=owner_only,
            public_only=public_only
        )
        
        total = await file_service.count_files(user_id, owner_only)
        
        return self.paginated(files, total, params)
