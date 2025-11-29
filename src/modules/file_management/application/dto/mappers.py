"""File entity to DTO mappers"""

from typing import List
from .file_dto import FileResponseDTO, FileListResponseDTO, FileDownloadResponseDTO
from modules.file_management.domain.entities.file import File
class FileMapper:
    """File domain entity to DTO mapper"""
    
    @staticmethod
    def to_response_dto(file: File) -> FileResponseDTO:
        """Convert file entity to response DTO"""
        return FileResponseDTO(
            id=file.id,
            name=file.name,
            original_name=file.original_name,
            path=file.path.value,
            size=file.size.bytes,
            size_human=file.size.human_readable(),
            mime_type=file.mime_type.value,
            owner_id=file.owner_id,
            description=file.description,
            is_public=file.is_public,
            download_count=file.download_count,
            shared_with=file.shared_with,
            file_extension=file.file_extension,
            is_image=file.is_image,
            is_document=file.is_document,
            created_at=file.created_at,
            updated_at=file.updated_at
        )
    
    @staticmethod
    def to_list_dto(file: File) -> FileListResponseDTO:
        """Convert file entity to list DTO"""
        return FileListResponseDTO(
            id=file.id,
            original_name=file.original_name,
            size_human=file.size.human_readable(),
            mime_type=file.mime_type.value,
            is_public=file.is_public,
            download_count=file.download_count,
            created_at=file.created_at
        )
    
    @staticmethod
    def to_list_dtos(files: List[File]) -> List[FileListResponseDTO]:
        """Convert list of file entities to list DTOs"""
        return [FileMapper.to_list_dto(file) for file in files]
    
    @staticmethod
    def to_download_dto(file: File) -> FileDownloadResponseDTO:
        """Convert file entity to download DTO"""
        return FileDownloadResponseDTO(
            id=file.id,
            name=file.name,
            original_name=file.original_name,
            path=file.path.value,
            mime_type=file.mime_type.value,
            size=file.size.bytes
        )