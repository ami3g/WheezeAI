import csv
from io import StringIO, BytesIO
from sqlalchemy.orm import Session
from backend.models.audit_analysis import AuditAnalysis
from backend.models.audit_data import AuditData

# CSV export

def generate_csv_report(db: Session, audit_session_id: int) -> str:
    analyses = db.query(AuditAnalysis).filter(AuditAnalysis.audit_session_id == audit_session_id).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Analysis ID", "Status", "Result", "Created At", "Updated At"])
    for a in analyses:
        writer.writerow([a.id, a.status, a.result, a.created_at, a.updated_at])
    return output.getvalue()

# PDF export (simple text PDF)

def generate_pdf_report(db: Session, audit_session_id: int) -> bytes:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        raise RuntimeError("reportlab is required for PDF export")
    analyses = db.query(AuditAnalysis).filter(AuditAnalysis.audit_session_id == audit_session_id).all()
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    textobject = c.beginText(40, 750)
    textobject.textLine(f"Audit Analyses for Session {audit_session_id}")
    for a in analyses:
        textobject.textLine(f"ID: {a.id} | Status: {a.status} | Result: {a.result}")
    c.drawText(textobject)
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
