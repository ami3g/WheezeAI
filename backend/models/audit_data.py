from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db import Base

class AuditData(Base):
    __tablename__ = "audit_data"
    id = Column(Integer, primary_key=True, index=True)
    audit_session_id = Column(Integer, ForeignKey("audit_sessions.id"), nullable=False)
    data_type = Column(String, nullable=False)  # e.g., log, config, finding, evidence
    content = Column(Text, nullable=False)      # raw data, text, or JSON
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    audit_session = relationship("AuditSession")
