import hashlib
from datetime import datetime, timedelta
from typing import Optional, Union, cast

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import Admin, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    result: bool = pwd_context.verify(plain_password, hashed_password)
    return result


def get_password_hash(password: str) -> str:
    """Hash password"""
    result: str = pwd_context.hash(password)
    return result


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    # Convert datetime to timestamp (seconds since epoch)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_signature(data: dict, signature: str, secret_key: str) -> bool:
    """Verify webhook signature"""
    # Sort keys in alphabetical order
    sorted_keys = sorted(data.keys())
    # Form string for hashing
    message = "".join(str(data[key]) for key in sorted_keys) + secret_key
    # Calculate SHA256 hash
    expected_signature = hashlib.sha256(message.encode()).hexdigest()
    return expected_signature == signature


async def authenticate_user(
    db: AsyncSession, email: str, password: str, is_admin: bool = False
) -> Optional[Union[User, Admin]]:
    """Authenticate user or admin"""
    if is_admin:
        result = await db.execute(select(Admin).where(Admin.email == email))
        user = result.scalar_one_or_none()
    else:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    # Type narrowing: at this point user is definitely User or Admin
    return cast(Union[User, Admin], user)
