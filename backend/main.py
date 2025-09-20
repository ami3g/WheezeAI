
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.user import User
from backend.db import SessionLocal, Base


from backend.api.user import router as user_router
from backend.api.audit_log import router as audit_log_router
from backend.api.organization import router as organization_router
from backend.api.organization_invite import router as organization_invite_router
from backend.api.audit_session import router as audit_session_router
from backend.api.audit_data import router as audit_data_router

from backend.api.report import router as report_router
from backend.api.audit_analysis import router as audit_analysis_router

tags_metadata = [
    {"name": "User", "description": "User management and authentication."},
    {"name": "AuditLog", "description": "Audit trail logging."},
    {"name": "Organization", "description": "Organization and team management."},
    {"name": "AuditSession", "description": "Audit session management."},
    {"name": "AuditData", "description": "Flexible audit data collection."},
    {"name": "AuditAnalysis", "description": "AI-powered audit analysis."},
    {"name": "Report", "description": "Reporting endpoints (CSV/PDF)."}
]

app = FastAPI(openapi_tags=tags_metadata)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(audit_log_router)
app.include_router(organization_router)
app.include_router(organization_invite_router)
app.include_router(audit_session_router)
app.include_router(audit_data_router)

app.include_router(audit_analysis_router)
app.include_router(report_router)



@app.get("/health")
def health_check():
    return {"status": "ok"}