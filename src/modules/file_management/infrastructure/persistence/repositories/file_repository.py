"""File repository implementation"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ......shared.repositories.base_repository import BaseRepository
from ....domain.entities.file import File
from ....domain.value_objects.file_path import FilePath
from ....domain.value_objects.file_size import FileSize
from ....domain.value_objects.mime_type import MimeType
from ..models import FileModel


class FileRepository(BaseRepository[File, FileModel]):
    """File repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, File, FileModel)
    
    async def get_by_name(self, name: str) -> Optional[File]:
        """Get file by internal name"""
        stmt = select(FileModel).where(
            FileModel.name == name,
            FileModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        
        return self._to_entity(model) if model else None
    
    async def get_by_owner(
        self,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[File]:
        """Get files by owner"""
        stmt = select(FileModel).where(
            FileModel.owner_id == owner_id,
            FileModel.is_deleted == False
        ).offset(skip).limit(limit).order_by(FileModel.created_at.desc())
        
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def get_public_files(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[File]:
        """Get public files"""
        stmt = select(FileModel).where(
            FileModel.is_public == True,
            FileModel.is_deleted == False
        ).offset(skip).limit(limit).order_by(FileModel.created_at.desc())
        
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def get_accessible_by_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[File]:
        """Get files accessible by user"""
        stmt = select(FileModel).where(
            or_(
                FileModel.owner_id == user_id,
                FileModel.is_public == True,
                FileModel.shared_with.contains([user_id])
            ),
            FileModel.is_deleted == False
        ).offset(skip).limit(limit).order_by(FileModel.created_at.desc())
        
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    async def count_by_owner(self, owner_id: UUID) -> int:
        """Count files by owner"""
        from sqlalchemy import func
        
        stmt = select(func.count()).select_from(FileModel).where(
            FileModel.owner_id == owner_id,
            FileModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()
    
    def _to_entity(self, model: FileModel) -> File:
        """Convert ORM model to domain entity"""
        entity = File(
            name=model.name,
            original_name=model.original_name,
            path=FilePath(model.path),
            size=FileSize(model.size),
            mime_type=MimeType(model.mime_type),
            owner_id=model.owner_id,
            description=model.description,
            is_public=model.is_public,
            download_count=model.download_count,
            id=model.id
        )
        
        # Set internal state
        entity._created_at = model.created_at
        entity._updated_at = model.updated_at
        entity._is_deleted = model.is_deleted
        entity._shared_with = model.shared_with or []
        
        return entity
    
    def _to_model(self, entity: File) -> FileModel:
        """Convert domain entity to ORM model"""
        return FileModel(
            id=entity.id,
            name=entity.name,
            original_name=entity.original_name,
            path=entity.path.value,
            size=entity.size.bytes,
            mime_type=entity.mime_type.value,
            owner_id=entity.owner_id,
            description=entity.description,
            is_public=entity.is_public,
            download_count=entity.download_count,
            shared_with=entity.shared_with,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_deleted=entity.is_deleted
        )