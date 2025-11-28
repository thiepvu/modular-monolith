"""File API routes"""

from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

# Import module's DB dependency
from src.modules.file_management.infrastructure.database.connection import get_file_db_session

from src.shared.api.pagination import PaginationParams
from src.modules.file_management.application.dto.file_dto import FileUpdateDTO, FileShareDTO
from .controllers.file_controller import FileController

# Create router
router = APIRouter(prefix="/files", tags=["Files"])

# Create controller
controller = FileController()

from uuid import UUID
MOCK_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


@router.post(
    "/upload",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="Upload file",
    description="Upload a new file with metadata"
)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    description: Optional[str] = Query(None, description="File description"),
    is_public: bool = Query(False, description="Make file public"),
    session: AsyncSession = Depends(get_file_db_session)
):
    """Upload a new file"""
    return await controller.upload_file(
        file=file,
        description=description,
        is_public=is_public,
        user_id=MOCK_USER_ID,
        session=session
    )


@router.get(
    "/{file_id}",
    response_model=None,
    summary="Get file metadata",
    description="Retrieve file metadata by ID"
)
async def get_file(
    file_id: UUID,
    session: AsyncSession = Depends(get_file_db_session)
):
    """Get file metadata"""
    return await controller.get_file(file_id, MOCK_USER_ID, session)


@router.put(
    "/{file_id}",
    response_model=None,
    summary="Update file metadata",
    description="Update file description and visibility"
)
async def update_file(
    file_id: UUID,
    dto: FileUpdateDTO,
    session: AsyncSession = Depends(get_file_db_session)
):
    """Update file metadata"""
    return await controller.update_file(file_id, dto, MOCK_USER_ID, session)


@router.delete(
    "/{file_id}",
    response_model=None,
    summary="Delete file",
    description="Delete file (soft delete)"
)
async def delete_file(
    file_id: UUID,
    session: AsyncSession = Depends(get_file_db_session)
):
    """Delete file"""
    return await controller.delete_file(file_id, MOCK_USER_ID, session)


@router.get(
    "/",
    response_model=None,
    summary="List files",
    description="Get paginated list of files"
)
async def list_files(
    params: PaginationParams = Depends(),
    owner_only: bool = Query(False, description="Show only my files"),
    public_only: bool = Query(False, description="Show only public files"),
    session: AsyncSession = Depends(get_file_db_session)
):
    """List files with filters"""
    return await controller.list_files(
        params=params,
        owner_only=owner_only,
        public_only=public_only,
        user_id=MOCK_USER_ID,
        session=session
    )


@router.post(
    "/{file_id}/share",
    response_model=None,
    summary="Share file",
    description="Share file with another user"
)
async def share_file(
    file_id: UUID,
    dto: FileShareDTO,
    session: AsyncSession = Depends(get_file_db_session)
):
    """Share file with user"""
    return await controller.share_file(file_id, dto, MOCK_USER_ID, session)



@router.get(
    "/{file_id}/download",
    summary="Download file",
    description="Download file content",
    responses={
        200: {
            "description": "File content",
            "content": {"application/octet-stream": {}}
        }
    }
)
async def download_file(
    file_id: UUID,
    session: AsyncSession = Depends(get_file_db_session)
):
    """Download file"""
    return await controller.download_file(file_id, MOCK_USER_ID, session)