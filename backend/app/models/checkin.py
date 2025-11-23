"""
CheckIn model - Gate entry records
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class CheckIn(Base):
    """
    Check-in record when attendee scans QR at gate
    
    Records:
    - Which session/gate
    - When they checked in
    - Which scanner/operator
    - Verification status
    """
    __tablename__ = "check_ins"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entry_id = Column(Integer, ForeignKey("entries.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session types (5 options - NO 'dinner')
    # Options: 'exhibition_day1', 'exhibition_day2',
    #          'interactive_sessions', 'interactive_sessions', 'plenary'
    session_type = Column(String(50), nullable=False, index=True)
    session_name = Column(String(255), nullable=True)  # Human-readable name
    
    check_in_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Gate information
    gate_number = Column(String(50), nullable=True)      # 'Gate 1', 'Gate 2', 'Gate 3', 'Gate 4'
    gate_location = Column(String(255), nullable=True)   # 'Exhibition Hall', 'Zorawar Hall'
    
    # Scanner information
    scanner_device_id = Column(String(100), nullable=True)
    scanner_operator = Column(String(100), nullable=True)
    
    verification_status = Column(String(50), default="verified")  # 'verified', 'manual_override', 'flagged'
    notes = Column(String(1000), nullable=True)  # Any special notes
    
    # Relationships
    entry = relationship("Entry", back_populates="check_ins")
    
    def __repr__(self):
        return f"<CheckIn(id={self.id}, entry_id={self.entry_id}, session='{self.session_type}', time='{self.check_in_time}')>"
    
    @property
    def attendee_name(self):
        """Get attendee name"""
        return self.entry.name if self.entry else "Unknown"
    
    @property
    def organization(self):
        """Get attendee organization"""
        return self.entry.user.organization if self.entry and self.entry.user else "Unknown"
