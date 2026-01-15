"""
Routes package - Export all routers
"""
from routes.auth import router as auth_router
from routes.interview import router as interview_router
from routes.payments import router as payments_router
from routes.cover_letter import router as cover_letter_router
from routes.jobs import router as jobs_router
from routes.learning import router as learning_router
from routes.cv import router as cv_router
from routes.analysis import router as analysis_router
from routes.dashboard import router as dashboard_router
from routes.roles import router as roles_router
from routes.resume import router as resume_router
from routes.user import router as user_router
from routes.analytics import router as analytics_router

__all__ = [
    "auth_router",
    "interview_router", 
    "payments_router",
    "cover_letter_router",
    "jobs_router",
    "learning_router",
    "cv_router",
    "analysis_router",
    "dashboard_router",
    "roles_router",
    "resume_router",
    "user_router",
    "analytics_router"
]
