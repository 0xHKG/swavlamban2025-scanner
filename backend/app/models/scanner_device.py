"""
ScannerDevice model - Mobile scanner registration
"""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class ScannerDevice(Base):
    """
    Scanner device (mobile app) registration
    
    Tracks:
    - Device ID and name
    - Assigned gate/location
    - Operator username
    - Last sync time
    """
    __tablename__ = "scanner_devices"

    device_id = Column(String(100), primary_key=True, index=True)
    device_name = Column(String(255), nullable=False)
    
    # Gate assignment
    gate_number = Column(String(50), nullable=True)      # 'Gate 1', 'Gate 2', 'Gate 3', 'Gate 4'
    gate_location = Column(String(255), nullable=True)   # 'Exhibition Hall', 'Zorawar Hall'
    
    operator_username = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ScannerDevice(device_id='{self.device_id}', gate='{self.gate_number}', operator='{self.operator_username}')>"
