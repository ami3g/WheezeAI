from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.organization_invite import OrganizationInviteCreate, OrganizationInviteRead
from backend.services.organization_invite import create_invite, get_invite, list_invites, accept_invite
from backend.db import SessionLocal
from backend.utils.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/organization_invites/", response_model=OrganizationInviteRead)
def create_org_invite(invite: OrganizationInviteCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return create_invite(db, invite)

@router.get("/organization_invites/{invite_id}", response_model=OrganizationInviteRead)
def read_org_invite(invite_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    invite = get_invite(db, invite_id)
    if invite is None:
        raise HTTPException(status_code=404, detail="Invite not found")
    return invite

@router.get("/organization_invites/", response_model=list[OrganizationInviteRead])
def list_org_invites(organization_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return list_invites(db, organization_id)

@router.post("/organization_invites/{invite_id}/accept", response_model=OrganizationInviteRead)
def accept_org_invite(invite_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    invite = accept_invite(db, invite_id, user_id=current_user)
    if invite is None:
        raise HTTPException(status_code=400, detail="Invite cannot be accepted")
    return invite
