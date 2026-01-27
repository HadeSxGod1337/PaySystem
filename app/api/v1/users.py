from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.account import AccountResponse
from app.schemas.payment import PaymentResponse
from app.schemas.user import UserResponse
from app.services.payment_service import PaymentService
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(user: Annotated[User, Depends(get_current_user)]):
    """Get current user information"""
    return user


@router.get("/accounts", response_model=list[AccountResponse])
async def get_my_accounts(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get user accounts list with balances"""
    service = UserService(db)
    user_id: int = int(user.id)
    accounts = await service.get_user_accounts(user_id)
    return accounts


@router.get("/payments", response_model=list[PaymentResponse])
async def get_my_payments(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """Get user payments list"""
    service = PaymentService(db)
    user_id: int = int(user.id)
    payments = await service.get_user_payments(user_id, skip, limit)
    return payments
