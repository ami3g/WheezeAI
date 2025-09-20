from sqlalchemy.orm import Session
from backend.models.organization import Organization
from backend.schemas.organization import OrganizationCreate

def create_organization(db: Session, org: OrganizationCreate) -> Organization:
    db_org = Organization(name=org.name, description=org.description)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def get_organization(db: Session, org_id: int) -> Organization | None:
    return db.query(Organization).filter(Organization.id == org_id).first()


def list_organizations(db: Session) -> list[Organization]:
    return db.query(Organization).all()
