from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.audit_data import AuditDataCreate, AuditDataRead
from backend.services.audit_data import create_audit_data, get_audit_data, list_audit_data
from backend.db import SessionLocal
from backend.utils.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/audit_data/", response_model=AuditDataRead)
def create_data(data: AuditDataCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return create_audit_data(db, data)

@router.get("/audit_data/{data_id}", response_model=AuditDataRead)
def read_data(data_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    data = get_audit_data(db, data_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Audit data not found")
    return data

@router.get("/audit_data/", response_model=list[AuditDataRead])
def list_data(audit_session_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return list_audit_data(db, audit_session_id)
