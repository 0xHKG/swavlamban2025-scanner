"""
User schemas for API validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user/organization"""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6)
    organization: str = Field(..., min_length=2, max_length=255)
    max_entries: int = Field(default=0, ge=0)
    role: str = Field(default="user")
    allowed_passes: Dict[str, bool] = Field(default_factory=dict)
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['user', 'admin', 'scanner']
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """Schema for user response (excluding password)"""
    username: str
    organization: str
    max_entries: int
    role: str
    allowed_passes: Dict[str, bool]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
