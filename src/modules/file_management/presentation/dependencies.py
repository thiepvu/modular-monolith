from typing import Annotated
from fastapi import Depends

from modules.file_management.application.services.file_service import FileService
from modules.file_management.application.interfaces.file_service import IFileService
from modules.file_management.application.services.file_storage_service import FileStorageService
from modules.file_management.application.interfaces.file_storage_service import IFileStorageService
from modules.file_management.infrastructure.persistence.repositories.file_repository import FileRepository
from modules.file_management.domain.repositories.file_repository import IFileRepository

# ✅ Facade
from modules.file_management.application.facades.file_facades_service import FileServiceFacade

# ✅ CROSS-MODULE DEPENDENCY (only for facade creation)
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
    Get user service instance (for facade).
    
    Returns:
        IUserService instance
    """
    return UserService(UserRepository())


def get_file_facade() -> FileServiceFacade:
    """
    Get file service facade instance.
    
    Facade isolates cross-module dependencies.
    
    Returns:
        FileServiceFacade instance
    """
    user_service = get_user_service()
    return FileServiceFacade(user_service)  # ✅ Pass instance to facade!


def get_file_service() -> IFileService:
    """
    Get file service instance with dependencies.
    
    FileService depends on:
    - IFileRepository (same module)
    - IFileStorageService (same module)
    - FileServiceFacade (isolates cross-module deps) ✅
    
    Returns:
        IFileService instance
    """
    return FileService(
        file_repository=get_file_repository(),
        storage_service=get_file_storage_service(),
        facade=get_file_facade()  # ✅ Pass facade instance!
    )


# ============================================================================
# TYPE ANNOTATIONS FOR CLEAN DEPENDENCY INJECTION
# ============================================================================

# ✅ Clean type annotation for file service
FileServiceDep = Annotated[IFileService, Depends(get_file_service)]
