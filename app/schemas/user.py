from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""

    password: str


class UserUpdate(BaseModel):
    """User update schema"""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """User data response schema"""

    id: int

    class Config:
        from_attributes = True


class AdminBase(BaseModel):
    """Base admin schema"""

    email: EmailStr
    full_name: Optional[str] = None


class AdminCreate(AdminBase):
    """Admin creation schema"""

    password: str


class AdminResponse(AdminBase):
    """Admin data response schema"""

    id: int

    class Config:
        from_attributes = True
