from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, Query, status

from shared.api.pagination import PaginationParams
from shared.decorators.session_decorator import with_session  # ✅ Decorator

from modules.file_management.presentation.dependencies import FileServiceDep
from modules.file_management.application.dto.file_dto import FileUpdateDTO, FileShareDTO

from .controllers.file_controller import FileController

# Create router
router = APIRouter(prefix="/files", tags=["Files"])

# Create controller
controller = FileController()

# Mock user ID (TODO: Replace with auth)
MOCK_USER_ID = UUID("9acbe950-6c96-42df-9314-829e74cc64ef")


# ============================================================================
# UPLOAD FILE
# ============================================================================

@router.post(
    "/upload",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="Upload file",
    description="Upload a new file with metadata"
)
@with_session  # ✅ Auto inject session to ContextVar!
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    description: Optional[str] = Query(None, description="File description"),
    is_public: bool = Query(False, description="Make file public"),
    file_service: FileServiceDep = None
):
    """
    Upload a new file.
    
    """
    return await controller.upload_file(
        file=file,
        description=description,
        is_public=is_public,
        user_id=MOCK_USER_ID,
        file_service=file_service
    )


# ============================================================================
# GET FILE BY ID
# ============================================================================

@router.get(
    "/{file_id}",
    response_model=None,
    summary="Get file metadata",
    description="Retrieve file metadata by ID"
)
@with_session
async def get_file(
    file_id: UUID,
    file_service: FileServiceDep = None 
):
    """Get file metadata"""
    return await controller.get_file(file_id, MOCK_USER_ID, file_service)


# ============================================================================
# UPDATE FILE
# ============================================================================

@router.put(
    "/{file_id}",
    response_model=None,
    summary="Update file metadata",
    description="Update file description and visibility"
)
@with_session
async def update_file(
    file_id: UUID,
    dto: FileUpdateDTO,
    file_service: FileServiceDep = None
):
    """Update file metadata"""
    return await controller.update_file(file_id, dto, MOCK_USER_ID, file_service)


# ============================================================================
# DELETE FILE
# ============================================================================

@router.delete(
    "/{file_id}",
    response_model=None,
    summary="Delete file",
    description="Delete file (soft delete)"
)
@with_session
async def delete_file(
    file_id: UUID,
    file_service: FileServiceDep = None
):
    """Delete file"""
    return await controller.delete_file(file_id, MOCK_USER_ID, file_service)


# ============================================================================
# LIST FILES
# ============================================================================

@router.get(
    "/",
    response_model=None,
    summary="List files",
    description="Get paginated list of files"
)
@with_session
async def list_files(
    params: PaginationParams = Depends(),
    owner_only: bool = Query(False, description="Show only my files"),
    public_only: bool = Query(False, description="Show only public files"),
    file_service: FileServiceDep = None
):
    """List files with filters"""
    return await controller.list_files(
        params=params,
        owner_only=owner_only,
        public_only=public_only,
        user_id=MOCK_USER_ID,
        file_service=file_service
    )


# ============================================================================
# SHARE FILE
# ============================================================================

@router.post(
    "/{file_id}/share",
    response_model=None,
    summary="Share file",
    description="Share file with another user"
)
@with_session
async def share_file(
    file_id: UUID,
    dto: FileShareDTO,
    file_service: FileServiceDep = None
):
    """Share file with user"""
    return await controller.share_file(file_id, dto, MOCK_USER_ID, file_service)


# ============================================================================
# DOWNLOAD FILE
# ============================================================================

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
@with_session
async def download_file(
    file_id: UUID,
    file_service: FileServiceDep = None
):
    """Download file"""
    return await controller.download_file(file_id, MOCK_USER_ID, file_service)
