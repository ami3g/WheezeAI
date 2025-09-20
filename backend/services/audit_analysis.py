from sqlalchemy.orm import Session
from backend.models.audit_analysis import AuditAnalysis
from backend.schemas.audit_analysis import AuditAnalysisCreate


def mock_ai_analyze(audit_session_id: int, db: Session) -> str:
    # Example: aggregate all audit data for the session and return a summary
    from backend.models.audit_data import AuditData
    data_items = db.query(AuditData).filter(AuditData.audit_session_id == audit_session_id).all()
    summary = f"AI found {len(data_items)} items. "
    if data_items:
        summary += "Sample: " + (data_items[0].content[:100] if data_items[0].content else "No content")
    else:
        summary += "No data available."
    return summary

def create_audit_analysis(db: Session, analysis: AuditAnalysisCreate) -> AuditAnalysis:
    # Simulate AI analysis
    ai_result = mock_ai_analyze(analysis.audit_session_id, db)
    db_analysis = AuditAnalysis(
        audit_session_id=analysis.audit_session_id,
        status="completed",
        result=ai_result
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def get_audit_analysis(db: Session, analysis_id: int) -> AuditAnalysis | None:
    return db.query(AuditAnalysis).filter(AuditAnalysis.id == analysis_id).first()


def list_audit_analyses(db: Session, audit_session_id: int) -> list[AuditAnalysis]:
    return db.query(AuditAnalysis).filter(AuditAnalysis.audit_session_id == audit_session_id).all()
