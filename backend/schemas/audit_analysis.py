from pydantic import BaseModel
from datetime import datetime

class AuditAnalysisBase(BaseModel):
    audit_session_id: int
    status: str | None = None
    result: str | None = None

class AuditAnalysisCreate(AuditAnalysisBase):
    pass

class AuditAnalysisRead(AuditAnalysisBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
