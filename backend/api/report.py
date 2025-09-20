from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from backend.services.report import generate_csv_report, generate_pdf_report
from backend.db import SessionLocal
from backend.utils.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reports/audit_analysis/csv", response_class=Response)
def get_audit_analysis_csv(audit_session_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    csv_data = generate_csv_report(db, audit_session_id)
    return Response(content=csv_data, media_type="text/csv")

@router.get("/reports/audit_analysis/pdf", response_class=Response)
def get_audit_analysis_pdf(audit_session_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    pdf_data = generate_pdf_report(db, audit_session_id)
    return Response(content=pdf_data, media_type="application/pdf")
