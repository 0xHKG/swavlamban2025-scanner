"""
Entry schemas for API validation
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime


class EntryCreate(BaseModel):
    """Schema for creating a new attendee entry"""
    name: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    id_type: str = Field(...)
    id_number: str = Field(..., min_length=5, max_length=100)
    photo_url: Optional[str] = None
    
    # Pass selections (4 types)
    exhibition_day1: bool = False
    exhibition_day2: bool = False
    interactive_sessions: bool = False
    plenary: bool = False
    
    @field_validator('id_type')
    @classmethod
    def validate_id_type(cls, v):
        allowed_types = ['Aadhaar', 'PAN', 'Passport', 'Driving License', 'Voter ID']
        if v not in allowed_types:
            raise ValueError(f"ID type must be one of {allowed_types}")
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        # Remove spaces and dashes
        cleaned = v.replace(' ', '').replace('-', '').replace('+', '')
        if not cleaned.isdigit():
            raise ValueError("Phone must contain only digits, spaces, dashes, or + sign")
        if len(cleaned) < 10:
            raise ValueError("Phone must have at least 10 digits")
        return v


class EntryUpdate(BaseModel):
    """Schema for updating an existing entry"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None
    
    # Pass selections (4 types)
    exhibition_day1: Optional[bool] = None
    exhibition_day2: Optional[bool] = None
    interactive_sessions: Optional[bool] = None
    plenary: Optional[bool] = None


class EntryResponse(BaseModel):
    """Schema for entry response"""
    id: int
    username: str
    name: str
    phone: str
    email: str
    id_type: str
    id_number: str
    photo_url: Optional[str] = None
    
    # Pass allocations
    exhibition_day1: bool
    exhibition_day2: bool
    interactive_sessions: bool
    plenary: bool

    # Pass generation status
    pass_generated_exhibition_day1: bool
    pass_generated_exhibition_day2: bool
    pass_generated_interactive_sessions: bool
    pass_generated_plenary: bool
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EntryListResponse(BaseModel):
    """Schema for paginated entry list"""
    total: int
    entries: List[EntryResponse]
