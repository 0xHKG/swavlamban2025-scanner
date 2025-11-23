"""
Scanner API endpoints for QR code scanning at event gates
Provides authentication, entry downloads, and check-in uploads for offline-capable scanner devices
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime, timedelta

from ..core.database import get_db
from ..core.security import verify_password, create_access_token, decode_token
from ..models.user import User
from ..models.entry import Entry
from ..models.checkin import CheckIn
from ..models.scanner_device import ScannerDevice
from ..schemas.scanner import (
    ScannerLoginRequest,
    ScannerLoginResponse,
    GateInfo,
    EntriesDownloadResponse,
    EntryDownload,
    CheckInCreate,
    CheckInBatch,
    CheckInBatchResponse,
    QRVerifyRequest,
    QRVerifyResponse,
    ScannerStats
)


router = APIRouter(prefix="/scanner", tags=["scanner"])


# Gate configuration (must match frontend src/config/gates.ts)
GATE_CONFIG = {
    "Gate 1": {
        "name": "Gate 1 - Exhibition Day 1",
        "location": "Exhibition Hall",
        "date": "2025-11-25",
        "time": "1100-1730",
        "allowed_passes": ["exhibition_day1", "exhibitor_pass"],
        "session_type": "exhibition_day1"
    },
    "Gate 2": {
        "name": "Gate 2 - Exhibition Day 2",
        "location": "Exhibition Hall",
        "date": "2025-11-26",
        "time": "1000-1730",
        "allowed_passes": ["exhibition_day2", "exhibitor_pass"],
        "session_type": "exhibition_day2"
    },
    "Gate 3": {
        "name": "Gate 3 - Interactive Sessions",
        "location": "Zorawar Hall",
        "date": "2025-11-26",
        "time": "1030-1330",
        "allowed_passes": ["interactive_sessions"],
        "session_type": "interactive_sessions"
    },
    "Gate 4": {
        "name": "Gate 4 - Plenary Session",
        "location": "Zorawar Hall",
        "date": "2025-11-26",
        "time": "1625-1755",
        "allowed_passes": ["plenary"],
        "session_type": "plenary"
    },
    "Main Entrance": {
        "name": "Main Entrance",
        "location": "Manekshaw Centre",
        "date": None,
        "time": None,
        "allowed_passes": [],  # All passes allowed (date-based validation only)
        "session_type": None
    }
}


def verify_scanner_token(authorization: Optional[str] = Header(None)) -> dict:
    """
    Verify JWT token from Authorization header

    Args:
        authorization: Authorization header with Bearer token

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is missing or invalid
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return payload


@router.post("/login", response_model=ScannerLoginResponse)
def scanner_login(
    request: ScannerLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate scanner operator and return JWT token

    Scanner operators must have role='scanner' in the users table.
    Creates or updates scanner_device record if device_id provided.

    Returns:
        - JWT access token (8-hour expiration)
        - Gate configuration information
        - Operator details
    """
    # Validate gate number
    if request.gate_number not in GATE_CONFIG:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid gate number. Must be one of: {', '.join(GATE_CONFIG.keys())}"
        )

    # Find scanner user
    user = db.query(User).filter(
        User.username == request.username,
        User.role == "scanner",
        User.is_active == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or not authorized as scanner"
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Update last login
    user.last_login = datetime.utcnow()

    # Create or update scanner device
    if request.device_id:
        device = db.query(ScannerDevice).filter(
            ScannerDevice.device_id == request.device_id
        ).first()

        if device:
            device.operator_username = user.username
            device.gate_number = request.gate_number
            device.last_active = datetime.utcnow()
            device.is_active = True
        else:
            device = ScannerDevice(
                device_id=request.device_id,
                operator_username=user.username,
                gate_number=request.gate_number,
                is_active=True
            )
            db.add(device)

    db.commit()

    # Create JWT token (8-hour expiration for scanner shift)
    token_data = {
        "sub": user.username,
        "role": "scanner",
        "gate": request.gate_number
    }
    expires_delta = timedelta(hours=8)
    token = create_access_token(token_data, expires_delta)
    expires_at = datetime.utcnow() + expires_delta

    # Get gate configuration
    gate_config = GATE_CONFIG[request.gate_number]
    gate_info = GateInfo(
        gate_number=request.gate_number,
        name=gate_config["name"],
        location=gate_config["location"],
        date=gate_config.get("date"),
        time=gate_config.get("time"),
        allowed_passes=gate_config["allowed_passes"],
        session_type=gate_config.get("session_type")
    )

    return ScannerLoginResponse(
        success=True,
        token=token,
        expires_at=expires_at,
        operator=user.username,
        gate_info=gate_info
    )


@router.get("/entries", response_model=EntriesDownloadResponse)
def get_entries(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_scanner_token)
):
    """
    Download all valid entries for offline scanner use

    Returns all entries with their pass allocations and QR signatures
    for offline validation. Scanner app stores these in IndexedDB.

    Authentication: Requires valid scanner JWT token
    """
    # Get all active entries
    entries = db.query(Entry).all()

    # Format entries for download
    entry_list = []
    for entry in entries:
        entry_list.append(EntryDownload(
            entry_id=entry.id,
            name=entry.name,
            organization=entry.organization,
            phone=entry.phone,
            email=entry.email,
            id_type=entry.id_type,
            id_number=entry.id_number,
            qr_signature=entry.qr_signature,
            exhibition_day1=entry.exhibition_day1,
            exhibition_day2=entry.exhibition_day2,
            interactive_sessions=entry.interactive_sessions,
            plenary=entry.plenary,
            is_exhibitor=entry.is_exhibitor
        ))

    return EntriesDownloadResponse(
        success=True,
        count=len(entry_list),
        last_updated=datetime.utcnow(),
        entries=entry_list
    )


@router.post("/checkin", response_model=dict)
def create_checkin(
    checkin: CheckInCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_scanner_token)
):
    """
    Record a single check-in (online mode)

    Used when scanner has internet connectivity for immediate check-in.
    For offline mode, use /checkin/batch endpoint instead.

    Authentication: Requires valid scanner JWT token
    """
    # Check for duplicate check-in
    existing = db.query(CheckIn).filter(
        CheckIn.entry_id == checkin.entry_id,
        CheckIn.session_type == checkin.session_type
    ).first()

    if existing:
        return {
            "success": False,
            "message": "Duplicate check-in - already recorded",
            "check_in_time": existing.check_in_time.isoformat()
        }

    # Verify entry exists
    entry = db.query(Entry).filter(Entry.id == checkin.entry_id).first()
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry ID {checkin.entry_id} not found"
        )

    # Create check-in record
    new_checkin = CheckIn(
        entry_id=checkin.entry_id,
        session_type=checkin.session_type,
        gate_number=checkin.gate_number,
        gate_location=checkin.gate_location,
        check_in_time=checkin.check_in_time,
        scanner_device_id=checkin.scanner_device_id,
        scanner_operator=checkin.scanner_operator,
        qr_data=checkin.qr_data
    )

    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)

    return {
        "success": True,
        "message": "Check-in recorded successfully",
        "check_in_id": new_checkin.id,
        "entry_id": new_checkin.entry_id,
        "name": entry.name,
        "check_in_time": new_checkin.check_in_time.isoformat()
    }


@router.post("/checkin/batch", response_model=CheckInBatchResponse)
def batch_checkin(
    batch: CheckInBatch,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_scanner_token)
):
    """
    Batch upload check-ins (offline sync)

    Used when scanner comes back online to sync all pending check-ins
    from IndexedDB. Handles duplicates gracefully.

    Authentication: Requires valid scanner JWT token

    Returns:
        - Total check-ins in batch
        - Successfully uploaded count
        - Duplicate count (already exists)
        - Error count
    """
    total = len(batch.checkins)
    uploaded = 0
    duplicates = 0
    errors = 0
    error_details = []

    for checkin_data in batch.checkins:
        try:
            # Check for duplicate
            existing = db.query(CheckIn).filter(
                CheckIn.entry_id == checkin_data.entry_id,
                CheckIn.session_type == checkin_data.session_type,
                CheckIn.check_in_time == checkin_data.check_in_time
            ).first()

            if existing:
                duplicates += 1
                continue

            # Verify entry exists
            entry = db.query(Entry).filter(Entry.id == checkin_data.entry_id).first()
            if not entry:
                errors += 1
                error_details.append(f"Entry ID {checkin_data.entry_id} not found")
                continue

            # Create check-in
            new_checkin = CheckIn(
                entry_id=checkin_data.entry_id,
                session_type=checkin_data.session_type,
                gate_number=checkin_data.gate_number,
                gate_location=checkin_data.gate_location,
                check_in_time=checkin_data.check_in_time,
                scanner_device_id=checkin_data.scanner_device_id,
                scanner_operator=checkin_data.scanner_operator,
                qr_data=checkin_data.qr_data
            )

            db.add(new_checkin)
            uploaded += 1

        except Exception as e:
            errors += 1
            error_details.append(f"Entry {checkin_data.entry_id}: {str(e)}")

    # Commit all successful check-ins
    if uploaded > 0:
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            return CheckInBatchResponse(
                success=False,
                total=total,
                uploaded=0,
                duplicates=duplicates,
                errors=total - duplicates,
                error_details=[f"Database commit failed: {str(e)}"]
            )

    return CheckInBatchResponse(
        success=True,
        total=total,
        uploaded=uploaded,
        duplicates=duplicates,
        errors=errors,
        error_details=error_details if error_details else None
    )


@router.post("/verify", response_model=QRVerifyResponse)
def verify_qr_code(
    request: QRVerifyRequest,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_scanner_token)
):
    """
    Verify QR code validity (optional endpoint for online validation)

    Frontend performs validation locally using downloaded entries.
    This endpoint is optional for additional server-side verification.

    Authentication: Requires valid scanner JWT token
    """
    try:
        # Parse QR data format: "entryId:passType:signature"
        parts = request.qr_data.split(":")
        if len(parts) != 3:
            return QRVerifyResponse(
                valid=False,
                allowed=False,
                message="Invalid QR code format",
                reason="Format should be: entryId:passType:signature"
            )

        entry_id_str, pass_type, signature = parts
        entry_id = int(entry_id_str)

        # Find entry
        entry = db.query(Entry).filter(Entry.id == entry_id).first()

        if not entry:
            return QRVerifyResponse(
                valid=False,
                allowed=False,
                message="Entry not found",
                reason=f"Entry ID {entry_id} does not exist"
            )

        # Verify signature
        if entry.qr_signature != signature:
            return QRVerifyResponse(
                valid=False,
                allowed=False,
                entry_id=entry_id,
                message="Invalid QR signature",
                reason="QR code signature verification failed"
            )

        # Verify pass type allocation
        pass_allocated = False
        if pass_type == "exhibition_day1":
            pass_allocated = entry.exhibition_day1
        elif pass_type == "exhibition_day2":
            pass_allocated = entry.exhibition_day2
        elif pass_type == "interactive_sessions":
            pass_allocated = entry.interactive_sessions
        elif pass_type == "plenary":
            pass_allocated = entry.plenary
        elif pass_type == "exhibitor_pass":
            pass_allocated = entry.is_exhibitor

        if not pass_allocated:
            return QRVerifyResponse(
                valid=True,
                allowed=False,
                entry_id=entry_id,
                name=entry.name,
                organization=entry.organization,
                pass_type=pass_type,
                message="Pass not allocated",
                reason=f"This attendee does not have a {pass_type.replace('_', ' ')} pass"
            )

        # Check gate compatibility
        gate_config = GATE_CONFIG.get(request.gate_number)
        if gate_config and gate_config["allowed_passes"]:
            if pass_type not in gate_config["allowed_passes"]:
                return QRVerifyResponse(
                    valid=True,
                    allowed=False,
                    entry_id=entry_id,
                    name=entry.name,
                    organization=entry.organization,
                    pass_type=pass_type,
                    message="Wrong gate",
                    reason=f"This pass is not valid for {request.gate_number}"
                )

        # All checks passed
        return QRVerifyResponse(
            valid=True,
            allowed=True,
            entry_id=entry_id,
            name=entry.name,
            organization=entry.organization,
            pass_type=pass_type,
            message="Entry granted"
        )

    except ValueError:
        return QRVerifyResponse(
            valid=False,
            allowed=False,
            message="Invalid QR code format",
            reason="Entry ID must be numeric"
        )
    except Exception as e:
        return QRVerifyResponse(
            valid=False,
            allowed=False,
            message="Verification error",
            reason=str(e)
        )


@router.get("/stats", response_model=ScannerStats)
def get_scanner_stats(
    gate_number: Optional[str] = None,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_scanner_token)
):
    """
    Get scanner statistics (optional endpoint)

    Returns statistics for a specific gate or all gates.
    Useful for monitoring and reporting.

    Authentication: Requires valid scanner JWT token
    """
    # Use gate from token if not specified
    if not gate_number:
        gate_number = token.get("gate", "Unknown")

    # Query check-ins for this gate
    query = db.query(CheckIn)

    if gate_number != "all":
        query = query.filter(CheckIn.gate_number == gate_number)

    check_ins = query.all()

    # Calculate statistics
    total_scans = len(check_ins)
    successful_scans = total_scans  # All recorded check-ins are successful
    rejected_scans = 0  # Rejected scans are not recorded in DB

    # Count unique entries
    unique_entries = len(set(checkin.entry_id for checkin in check_ins))

    # Get last scan time
    last_scan_time = None
    if check_ins:
        last_scan_time = max(checkin.check_in_time for checkin in check_ins)

    return ScannerStats(
        gate_number=gate_number,
        total_scans=total_scans,
        successful_scans=successful_scans,
        rejected_scans=rejected_scans,
        unique_entries=unique_entries,
        last_scan_time=last_scan_time
    )
