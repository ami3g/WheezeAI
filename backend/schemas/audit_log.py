from pydantic import BaseModel
from datetime import datetime

class AuditLogBase(BaseModel):
    action: str
    details: str | None = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogRead(AuditLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
