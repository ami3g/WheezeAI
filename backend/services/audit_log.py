from sqlalchemy.orm import Session
from backend.models.audit_log import AuditLog
from backend.schemas.audit_log import AuditLogCreate


def create_audit_log(db: Session, user_id: int, audit_log: AuditLogCreate) -> AuditLog:
    db_log = AuditLog(
        user_id=user_id,
        action=audit_log.action,
        details=audit_log.details
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_audit_logs(db: Session, user_id: int) -> list[AuditLog]:
    return db.query(AuditLog).filter(AuditLog.user_id == user_id).all()
