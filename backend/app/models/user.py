"""
User model - Organizations and admin accounts
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class User(Base):
    """
    User account for organizations
    
    Each organization has:
    - Login credentials (username/password)
    - Entry quota (max allowed entries)
    - Allowed pass types (which passes they can generate)
    - Role (user/admin/scanner)
    """
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, index=True)
    password_hash = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=False)
    max_entries = Column(Integer, nullable=False, default=0)  # For exhibitors (admin bulk upload)
    role = Column(String(50), default="user")  # 'user', 'admin', 'scanner'

    # Separate quotas for each pass type (for visitor organizations)
    quota_ex_day1 = Column(Integer, nullable=False, default=0)
    quota_ex_day2 = Column(Integer, nullable=False, default=0)
    quota_interactive = Column(Integer, nullable=False, default=0)
    quota_plenary = Column(Integer, nullable=False, default=0)

    # Allowed pass types (5 types - NO dinner_invitation)
    # Example: {
    #   "exhibition_day1": true,
    #   "exhibition_day2": true,
    #   "interactive_sessions": false,
    #   "interactive_sessions": true,
    #   "plenary": false
    # }
    allowed_passes = Column(JSON, default={})
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}', organization='{self.organization}', role='{self.role}')>"
    
    @property
    def entries_count(self):
        """Count of entries created by this user"""
        return len(self.entries) if self.entries else 0
    
    @property
    def remaining_quota(self):
        """Remaining entry quota"""
        return self.max_entries - self.entries_count
    
    def can_generate_pass(self, pass_type: str) -> bool:
        """Check if user is allowed to generate this pass type"""
        if not self.allowed_passes:
            return False
        return self.allowed_passes.get(pass_type, False)
