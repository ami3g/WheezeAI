from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.organization import OrganizationCreate, OrganizationRead
from backend.services.organization import create_organization, get_organization, list_organizations
from backend.db import SessionLocal
from backend.utils.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/organizations/", response_model=OrganizationRead)
def create_org(org: OrganizationCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return create_organization(db, org)

@router.get("/organizations/{org_id}", response_model=OrganizationRead)
def read_org(org_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    org = get_organization(db, org_id)
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.get("/organizations/", response_model=list[OrganizationRead])
def list_orgs(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return list_organizations(db)
