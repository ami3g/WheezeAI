from sqlalchemy import Column, Integer, ForeignKey
from backend.db import Base

class UserOrganization(Base):
    __tablename__ = "user_organizations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
