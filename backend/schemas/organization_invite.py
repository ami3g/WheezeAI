from pydantic import BaseModel, EmailStr

class OrganizationInviteBase(BaseModel):
    organization_id: int
    email: EmailStr

class OrganizationInviteCreate(OrganizationInviteBase):
    pass

class OrganizationInviteRead(OrganizationInviteBase):
    id: int
    status: str
    class Config:
        from_attributes = True
