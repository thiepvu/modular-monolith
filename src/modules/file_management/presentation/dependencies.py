
from typing import Annotated
from fastapi import Depends

from modules.file_management.application.services.file_service import FileService
from modules.file_management.application.interfaces.file_service import IFileService
from modules.file_management.application.services.file_storage_service import FileStorageService
from modules.file_management.application.interfaces.file_storage_service import IFileStorageService
from modules.file_management.infrastructure.persistence.repositories.file_repository import FileRepository
from modules.file_management.domain.repositories.file_repository import IFileRepository

# ✅ CROSS-MODULE DEPENDENCY
from modules.user_management.application.services.user_service import UserService
from modules.user_management.application.interfaces.user_service import IUserService
from modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository


# ============================================================================
# SERVICE DEPENDENCIES
# ============================================================================

def get_file_storage_service() -> IFileStorageService:
    """
    Get file storage service instance.
    
    Returns:
        IFileStorageService instance
    """
    return FileStorageService(storage_path="uploads")


def get_file_repository() -> IFileRepository:
    """
    Get file repository instance.
    
    Repository tự lấy session từ ContextVar (đã set bởi @with_session decorator).
    
    Returns:
        IFileRepository instance
    """
    return FileRepository()


def get_user_service() -> IUserService:
    """
    Get user service instance (cross-module dependency).
    
    Returns:
        IUserService instance
    """
    return UserService(UserRepository())


def get_file_service() -> IFileService:
    """
    Get file service instance with dependencies.
    
    FileService depends on:
    - IFileRepository (same module)
    - IFileStorageService (same module)
    - IUserService (cross-module) ✅
    
    Returns:
        IFileService instance
    """
    return FileService(
        file_repository=get_file_repository(),
        storage_service=get_file_storage_service(),
    )

# ============================================================================
# TYPE ANNOTATIONS FOR CLEAN DEPENDENCY INJECTION
# ============================================================================

# ✅ Clean type annotation for service
FileServiceDep = Annotated[IFileService, Depends(get_file_service)]
