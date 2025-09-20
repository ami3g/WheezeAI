from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.audit_analysis import AuditAnalysisCreate, AuditAnalysisRead
from backend.services.audit_analysis import create_audit_analysis, get_audit_analysis, list_audit_analyses
from backend.db import SessionLocal
from backend.utils.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from backend.services.audit_log import create_audit_log
from backend.schemas.audit_log import AuditLogCreate

@router.post("/audit_analyses/", response_model=AuditAnalysisRead)
def create_analysis(analysis: AuditAnalysisCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Only admin or auditor can create analyses
    if current_user.role not in ["admin", "auditor"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    result = create_audit_analysis(db, analysis)
    # Log the action
    log = AuditLogCreate(action="create_audit_analysis", details=f"Created analysis for session {analysis.audit_session_id}")
    create_audit_log(db, user_id=current_user.id, audit_log=log)
    return result

@router.get("/audit_analyses/{analysis_id}", response_model=AuditAnalysisRead)
def read_analysis(analysis_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    analysis = get_audit_analysis(db, analysis_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Audit analysis not found")
    return analysis

@router.get("/audit_analyses/", response_model=list[AuditAnalysisRead])
def list_analyses(audit_session_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return list_audit_analyses(db, audit_session_id)
