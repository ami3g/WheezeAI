from sqlalchemy.orm import Session
from backend.models.audit_session import AuditSession
from backend.schemas.audit_session import AuditSessionCreate

def create_audit_session(db: Session, session: AuditSessionCreate) -> AuditSession:
    db_session = AuditSession(
        organization_id=session.organization_id,
        name=session.name,
        description=session.description,
        status=session.status or "open"
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_audit_session(db: Session, session_id: int) -> AuditSession | None:
    return db.query(AuditSession).filter(AuditSession.id == session_id).first()


def list_audit_sessions(db: Session, organization_id: int) -> list[AuditSession]:
    return db.query(AuditSession).filter(AuditSession.organization_id == organization_id).all()
