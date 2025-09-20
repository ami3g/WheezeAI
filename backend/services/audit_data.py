from sqlalchemy.orm import Session
from backend.models.audit_data import AuditData
from backend.schemas.audit_data import AuditDataCreate

def create_audit_data(db: Session, data: AuditDataCreate) -> AuditData:
    db_data = AuditData(
        audit_session_id=data.audit_session_id,
        data_type=data.data_type,
        content=data.content,
        description=data.description
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_audit_data(db: Session, data_id: int) -> AuditData | None:
    return db.query(AuditData).filter(AuditData.id == data_id).first()


def list_audit_data(db: Session, audit_session_id: int) -> list[AuditData]:
    return db.query(AuditData).filter(AuditData.audit_session_id == audit_session_id).all()
