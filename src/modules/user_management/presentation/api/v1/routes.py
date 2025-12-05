from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, status

from shared.api.response import ApiResponse
from shared.api.pagination import PaginationParams, PaginatedResponse
from shared.decorators.session_decorator import with_session  # ✅ Decorator

from modules.user_management.presentation.dependencies import UserServiceDep
from modules.user_management.application.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserEmailUpdateDTO,
    UserListResponseDTO,
)

from .controllers.user_controller import UserController

# Create router
router = APIRouter(prefix="/users", tags=["Users"])

# Create controller instance
controller = UserController()


# ============================================================================
# CREATE USER
# ============================================================================

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
@with_session  # ✅ Auto inject session!
async def create_user(
    dto: UserCreateDTO,
    user_service: UserServiceDep  # ✅ Clean! Auto-injected
):
    """Create a new user"""
    return await controller.create_user(dto, user_service)


# ============================================================================
# GET USER BY ID
# ============================================================================

@router.get(
    "/{user_id}",
    response_model=None,
    summary="Get user by ID",
    description="Retrieve a specific user by their unique identifier",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    },
)
@with_session
async def get_user(
    user_id: UUID,
    user_service: UserServiceDep
):
    """Get user by ID"""
    return await controller.get_user(user_id, user_service)


# ============================================================================
# GET USER BY EMAIL
# ============================================================================

@router.get(
    "/email/{email}",
    response_model=None,
    summary="Get user by email",
    description="Retrieve a user by their email address",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    },
)
@with_session
async def get_user_by_email(
    email: str,
    user_service: UserServiceDep
):
    """Get user by email"""
    return await controller.get_user_by_email(email, user_service)


# ============================================================================
# GET USER BY USERNAME
# ============================================================================

@router.get(
    "/username/{username}",
    response_model=None,
    summary="Get user by username",
    description="Retrieve a user by their username",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    },
)
@with_session
async def get_user_by_username(
    username: str,
    user_service: UserServiceDep
):
    """Get user by username"""
    return await controller.get_user_by_username(username, user_service)


# ============================================================================
# UPDATE USER
# ============================================================================

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
@with_session
async def update_user(
    user_id: UUID,
    dto: UserUpdateDTO,
    user_service: UserServiceDep
):
    """Update user profile"""
    return await controller.update_user(user_id, dto, user_service)


# ============================================================================
# UPDATE USER EMAIL
# ============================================================================

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
@with_session
async def update_user_email(
    user_id: UUID,
    dto: UserEmailUpdateDTO,
    user_service: UserServiceDep
):
    """Update user email"""
    return await controller.update_user_email(user_id, dto, user_service)


# ============================================================================
# ACTIVATE USER
# ============================================================================

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
@with_session
async def activate_user(
    user_id: UUID,
    user_service: UserServiceDep
):
    """Activate user account"""
    return await controller.activate_user(user_id, user_service)


# ============================================================================
# DEACTIVATE USER
# ============================================================================

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
@with_session
async def deactivate_user(
    user_id: UUID,
    user_service: UserServiceDep
):
    """Deactivate user account"""
    return await controller.deactivate_user(user_id, user_service)


# ============================================================================
# DELETE USER
# ============================================================================

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
@with_session
async def delete_user(
    user_id: UUID,
    user_service: UserServiceDep
):
    """Delete user (soft delete)"""
    return await controller.delete_user(user_id, user_service)


# ============================================================================
# LIST USERS
# ============================================================================

@router.get(
    "/",
    response_model=ApiResponse[PaginatedResponse[UserListResponseDTO]],
    summary="List users",
    description="Get a paginated list of all users with optional filtering and search",
    responses={200: {"description": "Users retrieved successfully"}},
)
@with_session
async def list_users(
    request: Request,
    params: PaginationParams = Depends(),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in username, name, or email"),
    user_service: UserServiceDep = None  # ✅ Auto-injected
):
    """List all users with pagination, filtering, and search"""
    return await controller.list_users(params, is_active, search, user_service)
