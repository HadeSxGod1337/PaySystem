from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.error_messages import ErrorMessages
from app.core.security import authenticate_user, create_access_token
from app.database import get_db
from app.exceptions import IncorrectEmailOrPasswordError
from app.schemas.auth import Token

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Universal authorization: works for users and admins.
    First tries to find a user, then an admin.
    """
    # In OAuth2PasswordRequestForm username is email
    # First try to find as regular user
    user = await authenticate_user(db, form_data.username, form_data.password, is_admin=False)

    if user:
        # Found regular user
        access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "type": "user"}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    # If user not found, try to find admin
    admin = await authenticate_user(db, form_data.username, form_data.password, is_admin=True)

    if admin:
        # Found admin
        access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(admin.id), "type": "admin"}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    # If neither user nor admin found
    raise IncorrectEmailOrPasswordError(
        message=ErrorMessages.INCORRECT_EMAIL_OR_PASSWORD,
        detail=ErrorMessages.INCORRECT_EMAIL_OR_PASSWORD,
    )
