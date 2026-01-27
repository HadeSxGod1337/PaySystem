from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin
from app.database import get_db
from app.models.user import Admin
from app.schemas.account import AccountResponse
from app.schemas.user import AdminResponse, UserCreate, UserResponse, UserUpdate
from app.services.admin_service import AdminService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=AdminResponse)
async def get_current_admin_info(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    """Get current admin information"""
    return current_admin


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    _current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create user"""
    service = UserService(db)
    user = await service.create_user(user_data)
    return user


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    _current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """Get all users list"""
    service = UserService(db)
    users = await service.get_all_users(skip, limit)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    _current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get user by ID"""
    service = UserService(db)
    user = await service.get_user(user_id)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    _current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update user"""
    service = UserService(db)
    user = await service.update_user(user_id, user_data)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    _current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete user"""
    service = UserService(db)
    await service.delete_user(user_id)


@router.get("/users/{user_id}/accounts", response_model=list[AccountResponse])
async def get_user_accounts(
    user_id: int,
    _current_admin: Annotated[Admin, Depends(get_current_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get user accounts list with balances"""
    service = AdminService(db)
    accounts = await service.get_user_accounts(user_id)
    return accounts
