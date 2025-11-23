"""
AuditLog model - Security and compliance audit trail
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.sql import func
from ..core.database import Base


class AuditLog(Base):
    """
    Audit log for all system actions
    
    Records:
    - Who did what
    - When they did it
    - What changed
    - From where (IP address)
    """
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    table_name = Column(String(100), nullable=True)
    record_id = Column(Integer, nullable=True)
    
    # JSON field to store changes
    # Example: {"old": {"name": "John"}, "new": {"name": "John Doe"}}
    changes = Column(JSON, nullable=True)
    
    ip_address = Column(String(50), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, user='{self.username}', action='{self.action}', time='{self.timestamp}')>"
