from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from app.models.user import UserType


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)
    user_type: UserType


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=6)