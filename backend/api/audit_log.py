from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.audit_log import AuditLogCreate, AuditLogRead
from backend.services.audit_log import create_audit_log, get_audit_logs
from backend.db import SessionLocal
from backend.utils.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/audit_logs/", response_model=AuditLogRead)
def create_log(audit_log: AuditLogCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_audit_log(db, user_id=current_user.id, audit_log=audit_log)


@router.get("/audit_logs/", response_model=list[AuditLogRead])
def list_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_audit_logs(db, user_id=current_user.id)
