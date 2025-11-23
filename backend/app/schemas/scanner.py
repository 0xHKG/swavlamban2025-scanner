"""
Pydantic schemas for Scanner API
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ScannerLoginRequest(BaseModel):
    """Login request for scanner operators"""
    username: str = Field(..., description="Scanner operator username")
    password: str = Field(..., description="Scanner operator password")
    gate_number: str = Field(..., description="Gate number (Gate 1-4 or Main Entrance)")
    device_id: Optional[str] = Field(None, description="Scanner device identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "scanner1",
                "password": "scanner123",
                "gate_number": "Gate 1",
                "device_id": "device-abc123"
            }
        }


class GateInfo(BaseModel):
    """Gate configuration information"""
    gate_number: str
    name: str
    location: str
    date: Optional[str] = None
    time: Optional[str] = None
    allowed_passes: List[str]
    session_type: Optional[str] = None


class ScannerLoginResponse(BaseModel):
    """Login response with JWT token and gate info"""
    success: bool = Field(..., description="Login success status")
    token: str = Field(..., description="JWT access token")
    expires_at: datetime = Field(..., description="Token expiration timestamp")
    operator: str = Field(..., description="Operator username")
    gate_info: GateInfo = Field(..., description="Gate configuration")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_at": "2025-11-25T18:00:00",
                "operator": "scanner1",
                "gate_info": {
                    "gate_number": "Gate 1",
                    "name": "Gate 1 - Exhibition Day 1",
                    "location": "Exhibition Hall",
                    "date": "2025-11-25",
                    "time": "1100-1730",
                    "allowed_passes": ["exhibition_day1", "exhibitor_pass"],
                    "session_type": "exhibition_day1"
                }
            }
        }


class EntryDownload(BaseModel):
    """Entry data for offline scanner use"""
    entry_id: int
    name: str
    organization: str
    phone: str
    email: str
    id_type: str
    id_number: str
    qr_signature: str

    # Pass allocations
    exhibition_day1: bool
    exhibition_day2: bool
    interactive_sessions: bool
    plenary: bool
    is_exhibitor: bool


class EntriesDownloadResponse(BaseModel):
    """Response for entries download"""
    success: bool
    count: int
    last_updated: datetime
    entries: List[EntryDownload]

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "count": 250,
                "last_updated": "2025-11-25T10:00:00",
                "entries": [
                    {
                        "entry_id": 1,
                        "name": "John Doe",
                        "organization": "IIT Delhi",
                        "phone": "9876543210",
                        "email": "john@example.com",
                        "id_type": "Aadhaar",
                        "id_number": "1234-5678-9012",
                        "qr_signature": "abc123def456",
                        "exhibition_day1": True,
                        "exhibition_day2": False,
                        "interactive_sessions": False,
                        "plenary": False,
                        "is_exhibitor": False
                    }
                ]
            }
        }


class CheckInCreate(BaseModel):
    """Single check-in record"""
    entry_id: int = Field(..., description="Entry ID")
    session_type: str = Field(..., description="Session type (exhibition_day1, etc.)")
    gate_number: str = Field(..., description="Gate number")
    gate_location: str = Field(..., description="Gate location")
    check_in_time: datetime = Field(..., description="Check-in timestamp")
    scanner_device_id: str = Field(..., description="Scanner device ID")
    scanner_operator: str = Field(..., description="Scanner operator username")
    qr_data: Optional[str] = Field(None, description="Raw QR code data")

    class Config:
        json_schema_extra = {
            "example": {
                "entry_id": 1,
                "session_type": "exhibition_day1",
                "gate_number": "Gate 1",
                "gate_location": "Exhibition Hall",
                "check_in_time": "2025-11-25T11:30:00",
                "scanner_device_id": "device-abc123",
                "scanner_operator": "scanner1",
                "qr_data": "1:exhibition_day1:abc123def456"
            }
        }


class CheckInBatch(BaseModel):
    """Batch check-in upload request"""
    checkins: List[CheckInCreate] = Field(..., description="List of check-ins to upload")

    class Config:
        json_schema_extra = {
            "example": {
                "checkins": [
                    {
                        "entry_id": 1,
                        "session_type": "exhibition_day1",
                        "gate_number": "Gate 1",
                        "gate_location": "Exhibition Hall",
                        "check_in_time": "2025-11-25T11:30:00",
                        "scanner_device_id": "device-abc123",
                        "scanner_operator": "scanner1"
                    }
                ]
            }
        }


class CheckInBatchResponse(BaseModel):
    """Batch check-in upload response"""
    success: bool
    total: int = Field(..., description="Total check-ins in batch")
    uploaded: int = Field(..., description="Successfully uploaded")
    duplicates: int = Field(..., description="Duplicate check-ins skipped")
    errors: int = Field(..., description="Check-ins with errors")
    error_details: Optional[List[str]] = Field(None, description="Error messages")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "total": 50,
                "uploaded": 48,
                "duplicates": 2,
                "errors": 0,
                "error_details": []
            }
        }


class QRVerifyRequest(BaseModel):
    """QR code verification request"""
    qr_data: str = Field(..., description="Raw QR code data")
    gate_number: str = Field(..., description="Gate number")

    class Config:
        json_schema_extra = {
            "example": {
                "qr_data": "1:exhibition_day1:abc123def456",
                "gate_number": "Gate 1"
            }
        }


class QRVerifyResponse(BaseModel):
    """QR code verification response"""
    valid: bool
    allowed: bool
    entry_id: Optional[int] = None
    name: Optional[str] = None
    organization: Optional[str] = None
    pass_type: Optional[str] = None
    message: str
    reason: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "allowed": True,
                "entry_id": 1,
                "name": "John Doe",
                "organization": "IIT Delhi",
                "pass_type": "exhibition_day1",
                "message": "Entry granted",
                "reason": None
            }
        }


class ScannerStats(BaseModel):
    """Scanner statistics"""
    gate_number: str
    total_scans: int
    successful_scans: int
    rejected_scans: int
    unique_entries: int
    last_scan_time: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "gate_number": "Gate 1",
                "total_scans": 150,
                "successful_scans": 145,
                "rejected_scans": 5,
                "unique_entries": 140,
                "last_scan_time": "2025-11-25T12:00:00"
            }
        }
