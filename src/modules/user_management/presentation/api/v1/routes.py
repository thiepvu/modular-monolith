"""User API routes"""

from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from modules.user_management.presentation.dependencies import get_user_db_session
from shared.api.response import ApiResponse
from shared.api.pagination import PaginationParams, PaginatedResponse
from core.domain.enums import UserRoleEnum
from modules.user_management.application.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserEmailUpdateDTO,
    UserResponseDTO,
    UserListResponseDTO,
)
from .controllers.user_controller import UserController

# Create router
router = APIRouter(prefix="/users", tags=["Users"])

# Create controller instance
controller = UserController()


@router.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with email, username, and profile information",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User with email or username already exists"},
        422: {"description": "Validation error"},
    },
)
async def create_user(dto: UserCreateDTO, session: AsyncSession = Depends(get_user_db_session)):
    """Create a new user"""
    return await controller.create_user(dto, session)


@router.get(
    "/{user_id}",
    response_model=None,
    summary="Get user by ID",
    description="Retrieve a specific user by their unique identifier",
    responses={200: {"description": "User found"}, 404: {"description": "User not found"}},
)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_user_db_session)):
    """Get user by ID"""
    return await controller.get_user(user_id, session)


@router.get(
    "/email/{email}",
    response_model=None,
    summary="Get user by email",
    description="Retrieve a user by their email address",
    responses={200: {"description": "User found"}, 404: {"description": "User not found"}},
)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_user_db_session)):
    """Get user by email"""
    return await controller.get_user_by_email(email, session)


@router.get(
    "/username/{username}",
    response_model=None,
    summary="Get user by username",
    description="Retrieve a user by their username",
    responses={200: {"description": "User found"}, 404: {"description": "User not found"}},
)
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_user_db_session)):
    """Get user by username"""
    return await controller.get_user_by_username(username, session)


@router.put(
    "/{user_id}",
    response_model=None,
    summary="Update user profile",
    description="Update user's first name and last name",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        422: {"description": "Validation error"},
    },
)
async def update_user(
    user_id: UUID, dto: UserUpdateDTO, session: AsyncSession = Depends(get_user_db_session)
):
    """Update user profile"""
    return await controller.update_user(user_id, dto, session)


@router.patch(
    "/{user_id}/email",
    response_model=None,
    summary="Update user email",
    description="Update user's email address",
    responses={
        200: {"description": "Email updated successfully"},
        404: {"description": "User not found"},
        409: {"description": "Email already in use"},
        422: {"description": "Validation error"},
    },
)
async def update_user_email(
    user_id: UUID, dto: UserEmailUpdateDTO, session: AsyncSession = Depends(get_user_db_session)
):
    """Update user email"""
    return await controller.update_user_email(user_id, dto, session)


@router.post(
    "/{user_id}/activate",
    response_model=None,
    summary="Activate user",
    description="Activate a user account",
    responses={
        200: {"description": "User activated successfully"},
        404: {"description": "User not found"},
    },
)
async def activate_user(user_id: UUID, session: AsyncSession = Depends(get_user_db_session)):
    """Activate user account"""
    return await controller.activate_user(user_id, session)


@router.post(
    "/{user_id}/deactivate",
    response_model=None,
    summary="Deactivate user",
    description="Deactivate a user account",
    responses={
        200: {"description": "User deactivated successfully"},
        404: {"description": "User not found"},
    },
)
async def deactivate_user(user_id: UUID, session: AsyncSession = Depends(get_user_db_session)):
    """Deactivate user account"""
    return await controller.deactivate_user(user_id, session)


@router.delete(
    "/{user_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    description="Soft delete a user from the system",
    responses={
        200: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
    },
)
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_user_db_session)):
    """Delete user (soft delete)"""
    return await controller.delete_user(user_id, session)


@router.get(
    "/",
    response_model=ApiResponse[PaginatedResponse[UserListResponseDTO]],
    summary="List users",
    description="Get a paginated list of all users with optional filtering and search",
    responses={200: {"description": "Users retrieved successfully"}},
)

async def list_users(
    request: Request,
    params: PaginationParams = Depends(),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in username, name, or email"),
    session: AsyncSession = Depends(get_user_db_session),
):
    """List all users with pagination, filtering, and search"""
    return await controller.list_users(params, is_active, search, session)