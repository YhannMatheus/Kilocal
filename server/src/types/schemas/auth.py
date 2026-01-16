from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import date
from src.types.enums.user import RoleEnum, GenderEnum, ActivityLevelEnum

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    role: RoleEnum = RoleEnum.USER


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember: bool = Field(default=False)


class RegisterRequest(BaseModel):
    email: EmailStr
    name : str
    password: str
    birth_date: date
    height_cm: float
    gender: GenderEnum