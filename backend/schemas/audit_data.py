from pydantic import BaseModel
from datetime import datetime

class AuditDataBase(BaseModel):
    audit_session_id: int
    data_type: str
    content: str
    description: str | None = None

class AuditDataCreate(AuditDataBase):
    pass

class AuditDataRead(AuditDataBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
