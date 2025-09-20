from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.audit_session import AuditSessionCreate, AuditSessionRead
from backend.services.audit_session import create_audit_session, get_audit_session, list_audit_sessions
from backend.db import SessionLocal
from backend.utils.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/audit_sessions/", response_model=AuditSessionRead)
def create_session(session: AuditSessionCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return create_audit_session(db, session)

@router.get("/audit_sessions/{session_id}", response_model=AuditSessionRead)
def read_session(session_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    session = get_audit_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Audit session not found")
    return session

@router.get("/audit_sessions/", response_model=list[AuditSessionRead])
def list_sessions(organization_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return list_audit_sessions(db, organization_id)
