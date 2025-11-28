"""File SQLAlchemy models"""

from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PGUUID

from infrastructure.database.base import register_module_base
from config.settings import get_settings

# Register Base for file module
settings = get_settings()
# Import register_module_base - ADJUST PATH
# Register module and get Base + BaseModel
module_base = register_module_base("file", settings.MODULE_SCHEMAS["file"])

class FileModel(module_base.BaseModel):
    """File ORM model"""
    
    __tablename__ = "files"
    
    name = Column(String(255), nullable=False, unique=True, index=True, comment="Internal filename")
    original_name = Column(String(255), nullable=False, comment="Original filename")
    path = Column(String(500), nullable=False, comment="Storage path")
    size = Column(Integer, nullable=False, comment="File size in bytes")
    mime_type = Column(String(100), nullable=False, index=True, comment="MIME type")
    owner_id = Column(PGUUID(as_uuid=True), nullable=False, index=True, comment="Owner user ID")
    description = Column(Text, nullable=True, comment="File description")
    is_public = Column(Boolean, default=False, nullable=False, index=True, comment="Public access")
    download_count = Column(Integer, default=0, nullable=False, comment="Download count")
    shared_with = Column(ARRAY(PGUUID(as_uuid=True)), default=list, nullable=False, comment="Shared with user IDs")
    
    def __repr__(self) -> str:
        return f"<File(id={self.id}, name={self.original_name})>"