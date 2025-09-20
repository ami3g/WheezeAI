from pydantic import BaseModel

class OrganizationBase(BaseModel):
    name: str
    description: str | None = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationRead(OrganizationBase):
    id: int
    class Config:
        from_attributes = True
