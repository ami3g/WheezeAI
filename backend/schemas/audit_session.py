from pydantic import BaseModel
from datetime import datetime

class AuditSessionBase(BaseModel):
    organization_id: int
    name: str
    description: str | None = None
    status: str | None = None

class AuditSessionCreate(AuditSessionBase):
    pass

class AuditSessionRead(AuditSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
