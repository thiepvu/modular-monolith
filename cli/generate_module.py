#!/usr/bin/env python3
"""
Module Generator CLI
Generates new bounded context modules with complete Clean Architecture structure
"""

import os
import sys
from pathlib import Path
from typing import Dict
import re

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}   Module Generator - Clean Architecture{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")

def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def to_snake_case(text: str) -> str:
    """Convert text to snake_case"""
    text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    text = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
    return text.lower().replace(' ', '_').replace('-', '_')

def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase"""
    return ''.join(word.capitalize() for word in text.replace('_', ' ').replace('-', ' ').split())

def to_title_case(text: str) -> str:
    """Convert text to Title Case"""
    return ' '.join(word.capitalize() for word in text.replace('_', ' ').replace('-', ' ').split())

class ModuleGenerator:
    """Generate a new module with Clean Architecture structure"""
    
    def __init__(self, module_name: str, entity_name: str = None):
        self.module_name_snake = to_snake_case(module_name)
        self.module_name_pascal = to_pascal_case(module_name)
        self.module_name_title = to_title_case(module_name)
        
        # Entity name defaults to singular of module name
        if entity_name:
            self.entity_name_snake = to_snake_case(entity_name)
            self.entity_name_pascal = to_pascal_case(entity_name)
        else:
            # Remove trailing 's' for entity name
            singular = module_name.rstrip('s')
            self.entity_name_snake = to_snake_case(singular)
            self.entity_name_pascal = to_pascal_case(singular)
        
        self.base_path = Path(f"src/modules/{self.module_name_snake}")
    
    def generate(self):
        """Generate complete module structure"""
        print_info(f"Generating module: {self.module_name_title}")
        print_info(f"Entity: {self.entity_name_pascal}")
        print()
        
        # Create directory structure
        self._create_directories()
        
        # Generate domain layer
        self._generate_domain_layer()
        
        # Generate application layer
        self._generate_application_layer()
        
        # Generate infrastructure layer
        self._generate_infrastructure_layer()
        
        # Generate presentation layer
        self._generate_presentation_layer()
        
        print()
        print_success(f"Module '{self.module_name_snake}' generated successfully!")
        print()
        print_info("Next steps:")
        print(f"  1. Review generated files in: {self.base_path}")
        print(f"  2. Customize domain logic in: domain/entities/{self.entity_name_snake}.py")
        print(f"  3. Add business rules and validations")
        print(f"  4. Create migration: python scripts/migrate.py --create 'Add {self.module_name_snake} tables'")
        print(f"  5. Run migration: python scripts/migrate.py --upgrade")
        print(f"  6. Test endpoints: http://localhost:8000/api/docs")
        print()
    
    def _create_directories(self):
        """Create module directory structure"""
        dirs = [
            "domain/entities",
            "domain/value_objects",
            "domain/events",
            "domain/exceptions",
            "application/dto",
            "application/services",
            "infrastructure/persistence/repositories",
            "presentation/api/v1/controllers",
        ]
        
        for d in dirs:
            path = self.base_path / d
            path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py
            init_file = path / "__init__.py"
            if not init_file.exists():
                init_file.write_text(f'"""{d.split("/")[-1].capitalize()} for {self.module_name_title}"""\n')
        
        print_success("Created directory structure")
    
    def _generate_domain_layer(self):
        """Generate domain layer files"""
        
        # Entity
        entity_content = f'''"""
{self.entity_name_pascal} domain entity
"""

from typing import Optional
from uuid import UUID

from .....core.domain.base_aggregate import AggregateRoot
from ..events.{self.entity_name_snake}_events import {self.entity_name_pascal}CreatedEvent, {self.entity_name_pascal}UpdatedEvent


class {self.entity_name_pascal}(AggregateRoot):
    """
    {self.entity_name_pascal} domain entity (Aggregate Root).
    
    TODO: Add your business logic here
    """
    
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        is_active: bool = True,
        id: Optional[UUID] = None
    ):
        """
        Initialize {self.entity_name_snake} entity.
        
        Args:
            name: {self.entity_name_pascal} name
            description: Optional description
            is_active: Whether {self.entity_name_snake} is active
            id: Entity UUID (generated if not provided)
        """
        super().__init__(id)
        self._name = name
        self._description = description
        self._is_active = is_active
    
    # Properties (read-only access)
    
    @property
    def name(self) -> str:
        """Get {self.entity_name_snake} name"""
        return self._name
    
    @property
    def description(self) -> Optional[str]:
        """Get description"""
        return self._description
    
    @property
    def is_active(self) -> bool:
        """Check if {self.entity_name_snake} is active"""
        return self._is_active
    
    # Factory method
    
    @staticmethod
    def create(
        name: str,
        description: Optional[str] = None
    ) -> "{self.entity_name_pascal}":
        """
        Factory method to create a new {self.entity_name_snake}.
        
        Args:
            name: {self.entity_name_pascal} name
            description: Optional description
            
        Returns:
            New {self.entity_name_pascal} instance
        """
        {self.entity_name_snake} = {self.entity_name_pascal}(
            name=name,
            description=description,
            is_active=True
        )
        
        # Emit domain event
        {self.entity_name_snake}.add_domain_event({self.entity_name_pascal}CreatedEvent({self.entity_name_snake}.id, name))
        
        return {self.entity_name_snake}
    
    # Business logic methods
    
    def update_info(self, name: str, description: Optional[str] = None) -> None:
        """
        Update {self.entity_name_snake} information.
        
        Args:
            name: New name
            description: New description
        """
        self._name = name
        if description is not None:
            self._description = description
        self.update_timestamp()
        
        # Emit domain event
        self.add_domain_event({self.entity_name_pascal}UpdatedEvent(self.id))
    
    def activate(self) -> None:
        """Activate {self.entity_name_snake}"""
        if self._is_active:
            from ..exceptions.{self.entity_name_snake}_exceptions import Invalid{self.entity_name_pascal}StateException
            raise Invalid{self.entity_name_pascal}StateException("{self.entity_name_pascal} is already active")
        
        self._is_active = True
        self.update_timestamp()
    
    def deactivate(self) -> None:
        """Deactivate {self.entity_name_snake}"""
        if not self._is_active:
            from ..exceptions.{self.entity_name_snake}_exceptions import Invalid{self.entity_name_pascal}StateException
            raise Invalid{self.entity_name_pascal}StateException("{self.entity_name_pascal} is already inactive")
        
        self._is_active = False
        self.update_timestamp()
'''
        
        # Events
        events_content = f'''"""
{self.entity_name_pascal} domain events
"""

from typing import Dict, Any
from uuid import UUID

from .....core.domain.events import DomainEvent


class {self.entity_name_pascal}CreatedEvent(DomainEvent):
    """{self.entity_name_pascal} created domain event"""
    
    def __init__(self, {self.entity_name_snake}_id: UUID, name: str):
        super().__init__()
        self.{self.entity_name_snake}_id = {self.entity_name_snake}_id
        self.name = name
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({{
            "{self.entity_name_snake}_id": str(self.{self.entity_name_snake}_id),
            "name": self.name
        }})
        return data


class {self.entity_name_pascal}UpdatedEvent(DomainEvent):
    """{self.entity_name_pascal} updated domain event"""
    
    def __init__(self, {self.entity_name_snake}_id: UUID):
        super().__init__()
        self.{self.entity_name_snake}_id = {self.entity_name_snake}_id
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({{"entity_name_snake}_id": str(self.{self.entity_name_snake}_id)}})
        return data
'''
        
        # Exceptions
        exceptions_content = f'''"""
{self.entity_name_pascal}-specific domain exceptions
"""

from .....core.exceptions.base_exceptions import DomainException


class Invalid{self.entity_name_pascal}StateException(DomainException):
    """Invalid {self.entity_name_snake} state exception"""
    
    def __init__(self, message: str):
        super().__init__(message=message, details={{}})


class {self.entity_name_pascal}AlreadyExistsException(DomainException):
    """{self.entity_name_pascal} already exists exception"""
    
    def __init__(self, identifier: str):
        super().__init__(
            message=f"{self.entity_name_pascal} with identifier '{{identifier}}' already exists",
            details={{"identifier": identifier}}
        )
'''
        
        # Write files
        self._write_file(f"domain/entities/{self.entity_name_snake}.py", entity_content)
        self._write_file(f"domain/events/{self.entity_name_snake}_events.py", events_content)
        self._write_file(f"domain/exceptions/{self.entity_name_snake}_exceptions.py", exceptions_content)
        
        print_success("Generated domain layer")
    
    def _generate_application_layer(self):
        """Generate application layer files"""
        
        # DTOs
        dto_content = f'''"""
{self.entity_name_pascal} Data Transfer Objects
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import Field

from .....core.application.dto import DTO


class {self.entity_name_pascal}CreateDTO(DTO):
    """{self.entity_name_pascal} creation DTO"""
    
    name: str = Field(..., min_length=1, max_length=255, description="{self.entity_name_pascal} name")
    description: Optional[str] = Field(None, max_length=1000, description="Description")


class {self.entity_name_pascal}UpdateDTO(DTO):
    """{self.entity_name_pascal} update DTO"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class {self.entity_name_pascal}ResponseDTO(DTO):
    """{self.entity_name_pascal} response DTO"""
    
    id: UUID
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class {self.entity_name_pascal}ListResponseDTO(DTO):
    """{self.entity_name_pascal} list item DTO"""
    
    id: UUID
    name: str
    is_active: bool
'''
        
        # Mappers
        mapper_content = f'''"""
{self.entity_name_pascal} entity to DTO mappers
"""

from typing import List
from .{self.entity_name_snake}_dto import {self.entity_name_pascal}ResponseDTO, {self.entity_name_pascal}ListResponseDTO
from ...domain.entities.{self.entity_name_snake} import {self.entity_name_pascal}


class {self.entity_name_pascal}Mapper:
    """{self.entity_name_pascal} domain entity to DTO mapper"""
    
    @staticmethod
    def to_response_dto({self.entity_name_snake}: {self.entity_name_pascal}) -> {self.entity_name_pascal}ResponseDTO:
        """Convert {self.entity_name_snake} entity to response DTO"""
        return {self.entity_name_pascal}ResponseDTO(
            id={self.entity_name_snake}.id,
            name={self.entity_name_snake}.name,
            description={self.entity_name_snake}.description,
            is_active={self.entity_name_snake}.is_active,
            created_at={self.entity_name_snake}.created_at,
            updated_at={self.entity_name_snake}.updated_at
        )
    
    @staticmethod
    def to_list_dto({self.entity_name_snake}: {self.entity_name_pascal}) -> {self.entity_name_pascal}ListResponseDTO:
        """Convert {self.entity_name_snake} entity to list DTO"""
        return {self.entity_name_pascal}ListResponseDTO(
            id={self.entity_name_snake}.id,
            name={self.entity_name_snake}.name,
            is_active={self.entity_name_snake}.is_active
        )
    
    @staticmethod
    def to_list_dtos({self.entity_name_snake}s: List[{self.entity_name_pascal}]) -> List[{self.entity_name_pascal}ListResponseDTO]:
        """Convert list of entities to list DTOs"""
        return [{self.entity_name_pascal}Mapper.to_list_dto({self.entity_name_snake}) for {self.entity_name_snake} in {self.entity_name_snake}s]
'''
        
        # Service
        service_content = f'''"""
{self.entity_name_pascal} application service
"""

from typing import List, Optional
from uuid import UUID

from .....core.interfaces.services import IService
from .....core.exceptions.base_exceptions import NotFoundException, ConflictException
from ...domain.entities.{self.entity_name_snake} import {self.entity_name_pascal}
from ...infrastructure.persistence.repositories.{self.entity_name_snake}_repository import {self.entity_name_pascal}Repository
from ..dto.{self.entity_name_snake}_dto import (
    {self.entity_name_pascal}CreateDTO,
    {self.entity_name_pascal}UpdateDTO,
    {self.entity_name_pascal}ResponseDTO,
    {self.entity_name_pascal}ListResponseDTO
)
from ..dto.mappers import {self.entity_name_pascal}Mapper


class {self.entity_name_pascal}Service(IService):
    """
    {self.entity_name_pascal} application service.
    Orchestrates {self.entity_name_snake}-related use cases.
    """
    
    def __init__(self, {self.entity_name_snake}_repository: {self.entity_name_pascal}Repository):
        self._repository = {self.entity_name_snake}_repository
        self._mapper = {self.entity_name_pascal}Mapper()
    
    async def create_{self.entity_name_snake}(self, dto: {self.entity_name_pascal}CreateDTO) -> {self.entity_name_pascal}ResponseDTO:
        """Create a new {self.entity_name_snake}"""
        # Create entity
        {self.entity_name_snake} = {self.entity_name_pascal}.create(
            name=dto.name,
            description=dto.description
        )
        
        # Save
        saved = await self._repository.add({self.entity_name_snake})
        
        return self._mapper.to_response_dto(saved)
    
    async def get_{self.entity_name_snake}(self, {self.entity_name_snake}_id: UUID) -> {self.entity_name_pascal}ResponseDTO:
        """Get {self.entity_name_snake} by ID"""
        {self.entity_name_snake} = await self._repository.get_by_id({self.entity_name_snake}_id)
        if not {self.entity_name_snake}:
            raise NotFoundException("{self.entity_name_pascal}", {self.entity_name_snake}_id)
        
        return self._mapper.to_response_dto({self.entity_name_snake})
    
    async def update_{self.entity_name_snake}(
        self,
        {self.entity_name_snake}_id: UUID,
        dto: {self.entity_name_pascal}UpdateDTO
    ) -> {self.entity_name_pascal}ResponseDTO:
        """Update {self.entity_name_snake}"""
        {self.entity_name_snake} = await self._repository.get_by_id({self.entity_name_snake}_id)
        if not {self.entity_name_snake}:
            raise NotFoundException("{self.entity_name_pascal}", {self.entity_name_snake}_id)
        
        if dto.name:
            {self.entity_name_snake}.update_info(dto.name, dto.description)
        
        updated = await self._repository.update({self.entity_name_snake})
        
        return self._mapper.to_response_dto(updated)
    
    async def delete_{self.entity_name_snake}(self, {self.entity_name_snake}_id: UUID) -> None:
        """Delete {self.entity_name_snake}"""
        exists = await self._repository.exists({self.entity_name_snake}_id)
        if not exists:
            raise NotFoundException("{self.entity_name_pascal}", {self.entity_name_snake}_id)
        
        await self._repository.delete({self.entity_name_snake}_id, soft=True)
    
    async def list_{self.entity_name_snake}s(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[{self.entity_name_pascal}ListResponseDTO]:
        """List all {self.entity_name_snake}s"""
        {self.entity_name_snake}s = await self._repository.get_all(skip, limit)
        return self._mapper.to_list_dtos({self.entity_name_snake}s)
    
    async def count_{self.entity_name_snake}s(self) -> int:
        """Count total {self.entity_name_snake}s"""
        return await self._repository.count()
'''
        
        # Write files
        self._write_file(f"application/dto/{self.entity_name_snake}_dto.py", dto_content)
        self._write_file(f"application/dto/mappers.py", mapper_content)
        self._write_file(f"application/services/{self.entity_name_snake}_service.py", service_content)
        
        print_success("Generated application layer")
    
    def _generate_infrastructure_layer(self):
        """Generate infrastructure layer files"""
        
        # Model
        model_content = f'''"""
{self.entity_name_pascal} SQLAlchemy models
"""

from sqlalchemy import Column, String, Boolean, Text

from .....infrastructure.database.base import BaseModel


class {self.entity_name_pascal}Model(BaseModel):
    """{self.entity_name_pascal} ORM model"""
    
    __tablename__ = "{self.module_name_snake}"
    
    name = Column(String(255), nullable=False, index=True, comment="{self.entity_name_pascal} name")
    description = Column(Text, nullable=True, comment="Description")
    is_active = Column(Boolean, default=True, nullable=False, index=True, comment="Active status")
    
    def __repr__(self) -> str:
        return f"<{self.entity_name_pascal}Model(id={{self.id}}, name={{self.name}})>"
'''
        
        # Repository
        repository_content = f'''"""
{self.entity_name_pascal} repository implementation
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ......shared.repositories.base_repository import BaseRepository
from ....domain.entities.{self.entity_name_snake} import {self.entity_name_pascal}
from ..models import {self.entity_name_pascal}Model


class {self.entity_name_pascal}Repository(BaseRepository[{self.entity_name_pascal}, {self.entity_name_pascal}Model]):
    """{self.entity_name_pascal} repository implementation"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, {self.entity_name_pascal}, {self.entity_name_pascal}Model)
    
    async def get_by_name(self, name: str) -> Optional[{self.entity_name_pascal}]:
        """Get {self.entity_name_snake} by name"""
        stmt = select({self.entity_name_pascal}Model).where(
            {self.entity_name_pascal}Model.name == name,
            {self.entity_name_pascal}Model.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return self._to_entity(model)
    
    def _to_entity(self, model: {self.entity_name_pascal}Model) -> {self.entity_name_pascal}:
        """Convert ORM model to domain entity"""
        entity = {self.entity_name_pascal}(
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            id=model.id
        )
        
        # Set internal timestamps
        entity._created_at = model.created_at
        entity._updated_at = model.updated_at
        entity._is_deleted = model.is_deleted
        
        return entity
    
    def _to_model(self, entity: {self.entity_name_pascal}) -> {self.entity_name_pascal}Model:
        """Convert domain entity to ORM model"""
        return {self.entity_name_pascal}Model(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_deleted=entity.is_deleted
        )
'''
        
        # Write files
        self._write_file("infrastructure/persistence/models.py", model_content)
        self._write_file(f"infrastructure/persistence/repositories/{self.entity_name_snake}_repository.py", repository_content)
        
        print_success("Generated infrastructure layer")
    
    def _generate_presentation_layer(self):
        """Generate presentation layer files"""
        
        # Controller
        controller_content = f'''"""
{self.entity_name_pascal} API controller
"""

from uuid import UUID
from typing import Optional
from fastapi import Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ......infrastructure.database.connection import get_db_session
from ......shared.api.base_controller import BaseController
from ......shared.api.response import ApiResponse
from ......shared.api.pagination import PaginationParams, PaginatedResponse
from ......shared.repositories.unit_of_work import UnitOfWork
from ....infrastructure.persistence.repositories.{self.entity_name_snake}_repository import {self.entity_name_pascal}Repository
from ....application.services.{self.entity_name_snake}_service import {self.entity_name_pascal}Service
from ....application.dto.{self.entity_name_snake}_dto import (
    {self.entity_name_pascal}CreateDTO,
    {self.entity_name_pascal}UpdateDTO,
    {self.entity_name_pascal}ResponseDTO,
    {self.entity_name_pascal}ListResponseDTO
)


class {self.entity_name_pascal}Controller(BaseController):
    """{self.entity_name_pascal} API controller"""
    
    def __init__(self):
        super().__init__()
    
    def _get_service(self, session: AsyncSession) -> {self.entity_name_pascal}Service:
        """Get service instance"""
        repository = {self.entity_name_pascal}Repository(session)
        return {self.entity_name_pascal}Service(repository)
    
    async def create_{self.entity_name_snake}(
        self,
        dto: {self.entity_name_pascal}CreateDTO,
        session: AsyncSession = Depends(get_db_session)
    ) -> ApiResponse[{self.entity_name_pascal}ResponseDTO]:
        """Create a new {self.entity_name_snake}"""
        async with UnitOfWork(session):
            service = self._get_service(session)
            {self.entity_name_snake} = await service.create_{self.entity_name_snake}(dto)
            return self.created({self.entity_name_snake}, "{self.entity_name_pascal} created successfully")
    
    async def get_{self.entity_name_snake}(
        self,
        {self.entity_name_snake}_id: UUID,
        session: AsyncSession = Depends(get_db_session)
    ) -> ApiResponse[{self.entity_name_pascal}ResponseDTO]:
        """Get {self.entity_name_snake} by ID"""
        service = self._get_service(session)
        {self.entity_name_snake} = await service.get_{self.entity_name_snake}({self.entity_name_snake}_id)
        return self.success({self.entity_name_snake})
    
    async def update_{self.entity_name_snake}(
        self,
        {self.entity_name_snake}_id: UUID,
        dto: {self.entity_name_pascal}UpdateDTO,
        session: AsyncSession = Depends(get_db_session)
    ) -> ApiResponse[{self.entity_name_pascal}ResponseDTO]:
        """Update {self.entity_name_snake}"""
        async with UnitOfWork(session):
            service = self._get_service(session)
            {self.entity_name_snake} = await service.update_{self.entity_name_snake}({self.entity_name_snake}_id, dto)
            return self.success({self.entity_name_snake}, "{self.entity_name_pascal} updated successfully")
    
    async def delete_{self.entity_name_snake}(
        self,
        {self.entity_name_snake}_id: UUID,
        session: AsyncSession = Depends(get_db_session)
    ) -> ApiResponse:
        """Delete {self.entity_name_snake}"""
        async with UnitOfWork(session):
            service = self._get_service(session)
            await service.delete_{self.entity_name_snake}({self.entity_name_snake}_id)
            return self.no_content("{self.entity_name_pascal} deleted successfully")
    
    async def list_{self.entity_name_snake}s(
        self,
        params: PaginationParams = Depends(),
        session: AsyncSession = Depends(get_db_session)
    ) -> ApiResponse[PaginatedResponse[{self.entity_name_pascal}ListResponseDTO]]:
        """List all {self.entity_name_snake}s"""
        service = self._get_service(session)
        {self.entity_name_snake}s = await service.list_{self.entity_name_snake}s(params.skip, params.limit)
        total = await service.count_{self.entity_name_snake}s()
        
        return self.paginated({self.entity_name_snake}s, total, params)
'''
        
        # Routes
        routes_content = f'''"""
{self.entity_name_pascal} API routes
"""

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .....infrastructure.database.connection import get_db_session
from .....shared.api.pagination import PaginationParams
from ...application.dto.{self.entity_name_snake}_dto import {self.entity_name_pascal}CreateDTO, {self.entity_name_pascal}UpdateDTO
from .controllers.{self.entity_name_snake}_controller import {self.entity_name_pascal}Controller

# Create router
router = APIRouter(prefix="/{self.module_name_snake}", tags=["{self.module_name_title}"])

# Create controller
controller = {self.entity_name_pascal}Controller()


@router.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="Create {self.entity_name_snake}",
    description="Create a new {self.entity_name_snake}"
)
async def create_{self.entity_name_snake}(
    dto: {self.entity_name_pascal}CreateDTO,
    session: AsyncSession = Depends(get_db_session)
):
    return await controller.create_{self.entity_name_snake}(dto, session)


@router.get(
    "/{{id}}",
    response_model=None,
    summary="Get {self.entity_name_snake}",
    description="Get {self.entity_name_snake} by ID"
)
async def get_{self.entity_name_snake}(
    id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    return await controller.get_{self.entity_name_snake}(id, session)


@router.put(
    "/{{id}}",
    response_model=None,
    summary="Update {self.entity_name_snake}",
    description="Update {self.entity_name_snake}"
)
async def update_{self.entity_name_snake}(
    id: UUID,
    dto: {self.entity_name_pascal}UpdateDTO,
    session: AsyncSession = Depends(get_db_session)
):
    return await controller.update_{self.entity_name_snake}(id, dto, session)


@router.delete(
    "/{{id}}",
    response_model=None,
    summary="Delete {self.entity_name_snake}",
    description="Delete {self.entity_name_snake}"
)
async def delete_{self.entity_name_snake}(
    id: UUID,
    session: AsyncSession = Depends(get_db_session)
):
    return await controller.delete_{self.entity_name_snake}(id, session)


@router.get(
    "/",
    response_model=None,
    summary="List {self.entity_name_snake}s",
    description="Get paginated list of {self.entity_name_snake}s"
)
async def list_{self.entity_name_snake}s(
    params: PaginationParams = Depends(),
    session: AsyncSession = Depends(get_db_session)
):
    return await controller.list_{self.entity_name_snake}s(params, session)
'''
        
        # Write files
        self._write_file(f"presentation/api/v1/controllers/{self.entity_name_snake}_controller.py", controller_content)
        self._write_file("presentation/api/v1/routes.py", routes_content)
        
        print_success("Generated presentation layer")
    
    def _write_file(self, path: str, content: str):
        """Write content to file"""
        file_path = self.base_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

def main():
    print_header()
    
    # Get module name
    module_name = input(f"{Colors.BLUE}Module name (e.g., file_management, projects): {Colors.RESET}").strip()
    if not module_name:
        print_error("Module name is required")
        sys.exit(1)
    
    # Get entity name (optional)
    entity_name = input(f"{Colors.BLUE}Entity name (leave empty for auto-detection): {Colors.RESET}").strip()
    
    # Confirm
    print()
    print_info(f"Module: {to_title_case(module_name)}")
    print_info(f"Entity: {to_pascal_case(entity_name or module_name.rstrip('s'))}")
    print()
    
    confirm = input(f"{Colors.YELLOW}Generate module? (y/N): {Colors.RESET}").strip().lower()
    if confirm != 'y':
        print_error("Cancelled")
        return
    
    # Generate
    print()
    generator = ModuleGenerator(module_name, entity_name)
    generator.generate()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Cancelled{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()