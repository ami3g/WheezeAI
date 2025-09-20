from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db import Base

class AuditAnalysis(Base):
    __tablename__ = "audit_analyses"
    id = Column(Integer, primary_key=True, index=True)
    audit_session_id = Column(Integer, ForeignKey("audit_sessions.id"), nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    result = Column(Text)  # AI findings, summary, or JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    audit_session = relationship("AuditSession")
