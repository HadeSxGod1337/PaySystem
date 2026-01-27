from typing import Any, Annotated, Dict, Optional, TypeVar

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.error_messages import ErrorMessages
from app.database import get_db
from app.exceptions import AdminInactiveError, InvalidCredentialsError, UserInactiveError
from app.models.user import Admin, User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token")

T = TypeVar("T", User, Admin)


async def _decode_jwt_token(token: str, expected_type: str) -> Dict[str, Any]:
    """Decode and validate JWT token"""
    try:
        payload: Dict[str, Any] = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"verify_exp": True},
        )
        sub = payload.get("sub")
        user_type_raw = payload.get("type")
        if not isinstance(user_type_raw, str):
            raise InvalidCredentialsError(
                message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
            ) from None
        user_type: str = user_type_raw

        if sub is None or user_type != expected_type:
            raise InvalidCredentialsError(
                message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
            ) from None

        # Convert sub (string) back to int for user_id
        try:
            user_id: int = int(sub)
        except (ValueError, TypeError) as err:
            raise InvalidCredentialsError(
                message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
            ) from err
        else:
            payload["sub"] = user_id  # Save as int for further use
            return payload
    except JWTError as err:
        raise InvalidCredentialsError(
            message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
        ) from err


async def _get_user_from_db(db: AsyncSession, model_class: type[T], user_id: int) -> Optional[T]:
    """Get user or admin from database"""
    result = await db.execute(select(model_class).where(model_class.id == user_id))
    return result.scalar_one_or_none()


async def get_current_user(
    token: Annotated[str, Depends(reusable_oauth2)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get current user from JWT token"""
    payload = await _decode_jwt_token(token, "user")
    user_id_raw = payload.get("sub")
    if not isinstance(user_id_raw, int):
        raise InvalidCredentialsError(
            message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
        )
    user_id: int = user_id_raw

    user = await _get_user_from_db(db, User, user_id)
    if user is None:
        raise InvalidCredentialsError(
            message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
        )

    if not user.is_active:
        raise UserInactiveError(
            message=ErrorMessages.USER_INACTIVE, detail=ErrorMessages.USER_INACTIVE
        )

    return user


async def get_current_admin(
    token: Annotated[str, Depends(reusable_oauth2)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Admin:
    """Get current admin from JWT token"""
    payload = await _decode_jwt_token(token, "admin")
    admin_id_raw = payload.get("sub")
    if not isinstance(admin_id_raw, int):
        raise InvalidCredentialsError(
            message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
        )
    admin_id: int = admin_id_raw

    admin = await _get_user_from_db(db, Admin, admin_id)
    if admin is None:
        raise InvalidCredentialsError(
            message=ErrorMessages.INVALID_CREDENTIALS, detail=ErrorMessages.INVALID_CREDENTIALS
        )

    if not admin.is_active:
        raise AdminInactiveError(
            message=ErrorMessages.ADMIN_INACTIVE, detail=ErrorMessages.ADMIN_INACTIVE
        )

    return admin
