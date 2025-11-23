"""
Entry model - Attendee registrations
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Entry(Base):
    """
    Attendee entry/registration
    
    Each entry has:
    - Personal details (name, phone, email, govt ID)
    - Optional photo
    - Pass allocations (5 boolean flags)
    - Pass generation tracking
    """
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), ForeignKey("users.username", ondelete="CASCADE"), nullable=False, index=True)
    
    # Personal information
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    id_type = Column(String(50), nullable=False)  # 'Aadhaar', 'PAN', 'Passport', 'Driving License'
    id_number = Column(String(100), nullable=False, unique=True, index=True)
    photo_url = Column(String(500), nullable=True)  # Optional photo path
    
    # Pass allocation (4 types - NO dinner_invitation flag)
    # User can select multiple passes when registering
    exhibition_day1 = Column(Boolean, default=False)           # EP-25.png
    exhibition_day2 = Column(Boolean, default=False)           # EP-26.png or EP-25n26.png
    interactive_sessions = Column(Boolean, default=False)      # EP-INTERACTIVE.png (combines both sessions)
    plenary = Column(Boolean, default=False)                   # EP-PLENARY.png

    # Exhibitor flag - for bulk uploaded exhibitors (gets combined pass EP-25n26.png)
    is_exhibitor_pass = Column(Boolean, default=False)         # True = Exhibitor (EP-25n26.png), False = Visitor (EP-25.png + EP-26.png)

    # Pass generation tracking (which passes have been generated)
    pass_generated_exhibition_day1 = Column(Boolean, default=False)
    pass_generated_exhibition_day2 = Column(Boolean, default=False)
    pass_generated_interactive_sessions = Column(Boolean, default=False)
    pass_generated_plenary = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="entries")
    check_ins = relationship("CheckIn", back_populates="entry", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Entry(id={self.id}, name='{self.name}', organization='{self.user.organization if self.user else 'N/A'}')>"
    
    @property
    def is_exhibitor(self) -> bool:
        """Check if this is an exhibitor pass (from bulk upload)"""
        return self.is_exhibitor_pass
    
    @property
    def needs_interactive_pass(self) -> bool:
        """Check if needs interactive sessions pass"""
        return self.interactive_sessions
    
    @property
    def pass_types_needed(self) -> list:
        """Get list of pass files needed for this entry"""
        passes = []
        
        # Exhibitor gets both-day pass
        if self.is_exhibitor:
            passes.append("EP-25n26.png")
        else:
            # Visitor gets individual day passes
            if self.exhibition_day1:
                passes.append("EP-25.png")
            if self.exhibition_day2:
                passes.append("EP-26.png")
        
        # Interactive sessions (covers both panels)
        if self.needs_interactive_pass:
            passes.append("EP-INTERACTIVE.png")
        
        # Plenary session
        if self.plenary:
            passes.append("EP-PLENARY.png")
        
        return passes
