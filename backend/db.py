from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.user import Base
from backend.models.audit_log import AuditLog
from backend.models.organization import Organization
from backend.models.user_organization import UserOrganization
from backend.models.organization_invite import OrganizationInvite
from backend.models.audit_session import AuditSession
from backend.models.audit_data import AuditData
from backend.models.audit_analysis import AuditAnalysis

DATABASE_URL = "postgresql://postgres:mysecretpassword@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
