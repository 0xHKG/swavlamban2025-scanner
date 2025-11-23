"""
CheckIn schemas for API validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class CheckInCreate(BaseModel):
    """Schema for creating a check-in record"""
    entry_id: int = Field(..., gt=0)
    session_type: str = Field(...)
    session_name: Optional[str] = None
    gate_number: Optional[str] = None
    gate_location: Optional[str] = None
    scanner_device_id: Optional[str] = None
    scanner_operator: Optional[str] = None
    verification_status: str = Field(default="verified")
    notes: Optional[str] = None
    
    @field_validator('session_type')
    @classmethod
    def validate_session_type(cls, v):
        allowed_sessions = [
            'exhibition_day1', 
            'exhibition_day2',
            'interactive_sessions', 
            'interactive_sessions', 
            'plenary'
        ]
        if v not in allowed_sessions:
            raise ValueError(f"Session type must be one of {allowed_sessions}")
        return v


class CheckInResponse(BaseModel):
    """Schema for check-in response"""
    id: int
    entry_id: int
    session_type: str
    session_name: Optional[str] = None
    check_in_time: datetime
    gate_number: Optional[str] = None
    gate_location: Optional[str] = None
    scanner_device_id: Optional[str] = None
    scanner_operator: Optional[str] = None
    verification_status: str
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True
