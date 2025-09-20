from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db import Base

class OrganizationInvite(Base):
    __tablename__ = "organization_invites"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, accepted, declined
