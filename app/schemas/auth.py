from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Authorization request schema"""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response schema"""

    access_token: str
    token_type: str = "bearer"
