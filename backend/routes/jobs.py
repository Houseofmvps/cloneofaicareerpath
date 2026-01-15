"""
Jobs/Auto-Apply routes - Job search, applications, preferences
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import uuid
import logging
import asyncio

from auth import get_current_user
from database import db
from config import ADZUNA_APP_ID, ADZUNA_APP_KEY, RESEND_API_KEY, SENDER_EMAIL

# Import resend for email notifications
try:
    import resend
    RESEND_AVAILABLE = bool(RESEND_API_KEY)
    if RESEND_AVAILABLE:
        resend.api_key = RESEND_API_KEY
except ImportError:
    RESEND_AVAILABLE = False

router = APIRouter(tags=["jobs"])


# Models
class JobPreferencesRequest(BaseModel):
    target_roles: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    remote_preference: str = "remote"
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    company_types: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
    auto_apply_enabled: bool = True


class StatusUpdate(BaseModel):
    status: str


class JobApplyRequest(BaseModel):
    job_id: str
    job_title: str
    company: str
    job_description: Optional[str] = None
    job_url: str
    cover_letter_tone: str = "professional"


# Mock job data
MOCK_JOBS = [
    {
        "id": "job_001",
        "title": "Senior AI/ML Engineer",
        "company": "OpenAI",
        "location": "San Francisco, CA (Remote)",
        "salary_range": "$200K - $350K",
        "posted_date": "2025-01-05",
        "match_score": 92,
        "required_skills": ["Python", "PyTorch", "LLMs", "Distributed Systems"],
        "job_url": "https://openai.com/careers",
        "company_logo": "🤖"
    },
    {
        "id": "job_002",
        "title": "MLOps Engineer",
        "company": "Google",
        "location": "Mountain View, CA (Hybrid)",
        "salary_range": "$180K - $280K",
        "posted_date": "2025-01-04",
        "match_score": 88,
        "required_skills": ["Kubernetes", "TensorFlow", "GCP", "Python"],
        "job_url": "https://careers.google.com",
        "company_logo": "🔍"
    },
    {
        "id": "job_003",
        "title": "Prompt Engineer",
        "company": "Anthropic",
        "location": "San Francisco, CA (Remote)",
        "salary_range": "$150K - $220K",
        "posted_date": "2025-01-03",
        "match_score": 95,
        "required_skills": ["LLMs", "Prompt Engineering", "Python", "RAG"],
        "job_url": "https://anthropic.com/careers",
        "company_logo": "🧠"
    },
    {
        "id": "job_004",
        "title": "Data Scientist - AI",
        "company": "Meta",
        "location": "Menlo Park, CA (Hybrid)",
        "salary_range": "$170K - $250K",
        "posted_date": "2025-01-02",
        "match_score": 85,
        "required_skills": ["Python", "SQL", "PyTorch", "Statistics"],
        "job_url": "https://metacareers.com",
        "company_logo": "📱"
    },
    {
        "id": "job_005",
        "title": "AI Research Engineer",
        "company": "Amazon (AWS AI)",
        "location": "Seattle, WA (Hybrid)",
        "salary_range": "$160K - $270K",
        "posted_date": "2025-01-01",
        "match_score": 82,
        "required_skills": ["Python", "Deep Learning", "AWS", "Research"],
        "job_url": "https://amazon.jobs",
        "company_logo": "📦"
    },
]


# Email notification helper
async def send_interview_notification_email(user_email: str, user_name: str, job_title: str, 
                                            company: str, interview_date: str, job_url: str):
    """Send interview notification email"""
    if not RESEND_AVAILABLE:
        return {"success": False, "error": "Email service not configured"}
    
    try:
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>🎉 Interview Scheduled!</h2>
            <p>Hi {user_name},</p>
            <p>Great news! <strong>{company}</strong> wants to interview you for the 
            <strong>{job_title}</strong> position.</p>
            <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Interview Date:</strong> {interview_date}</p>
                <p><strong>Position:</strong> {job_title}</p>
                <p><strong>Company:</strong> {company}</p>
            </div>
            <p>Good luck with your interview!</p>
        </div>
        """
        
        result = resend.Emails.send({
            "from": SENDER_EMAIL,
            "to": user_email,
            "subject": f"🎉 Interview Scheduled: {job_title} at {company}",
            "html": html_content
        })
        
        await db.notifications.insert_one({
            "user_email": user_email,
            "job_title": job_title,
            "company": company,
            "type": "interview_scheduled",
            "sent_at": datetime.now(timezone.utc).isoformat()
        })
        
        return {"success": True, "id": result.get("id")}
    except Exception as e:
        logging.error(f"Failed to send interview notification: {e}")
        return {"success": False, "error": str(e)}


@router.post("/auto-apply/preferences")
async def save_job_preferences(
    request: JobPreferencesRequest,
    user: dict = Depends(get_current_user)
):
    """Save user's auto-apply job preferences"""
    preferences = {
        "user_id": user["id"],
        "target_roles": request.target_roles,
        "locations": request.locations,
        "remote_preference": request.remote_preference,
        "min_salary": request.min_salary,
        "max_salary": request.max_salary,
        "company_types": request.company_types,
        "tech_stack": request.tech_stack,
        "experience_years": request.experience_years,
        "auto_apply_enabled": request.auto_apply_enabled,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.job_preferences.update_one(
        {"user_id": user["id"]},
        {"$set": preferences},
        upsert=True
    )
    
    return {"message": "Preferences saved successfully", "preferences": preferences}


@router.get("/auto-apply/preferences")
async def get_job_preferences(user: dict = Depends(get_current_user)):
    """Get user's auto-apply job preferences"""
    preferences = await db.job_preferences.find_one(
        {"user_id": user["id"]},
        {"_id": 0}
    )
    return {"preferences": preferences or {}}


@router.get("/auto-apply/matching-jobs")
async def get_matching_jobs(
    user: dict = Depends(get_current_user),
    keywords: Optional[str] = Query(None, description="Search keywords"),
    location: Optional[str] = Query("us", description="Location filter"),
    remote_only: bool = Query(False, description="Remote jobs only"),
    use_mock: bool = Query(False, description="Use mock data")
):
    """Get jobs matching user's preferences"""
    # Import job_discovery from server (circular import workaround)
    from server import job_discovery, ADZUNA_APP_ID as API_ID, ADZUNA_APP_KEY as API_KEY
    
    preferences = await db.job_preferences.find_one(
        {"user_id": user["id"]},
        {"_id": 0}
    )
    
    if use_mock or (not API_ID and not API_KEY):
        return {
            "jobs": MOCK_JOBS.copy(),
            "total_count": len(MOCK_JOBS),
            "last_scan": datetime.now(timezone.utc).isoformat(),
            "sources": ["mock"],
            "is_mock": True
        }
    
    search_keywords = keywords
    if not search_keywords and preferences:
        target_roles = preferences.get("target_roles", [])
        if target_roles:
            search_keywords = " ".join(target_roles[:2])
    
    if not search_keywords:
        search_keywords = "AI ML Engineer"
    
    search_location = location
    if preferences and preferences.get("locations"):
        search_location = preferences["locations"][0]
    
    is_remote = remote_only or (preferences and preferences.get("remote_preference") == "remote")
    salary_min = preferences.get("min_salary") if preferences else None
    
    try:
        jobs = await job_discovery.search_all(
            keywords=search_keywords,
            location=search_location,
            salary_min=salary_min,
            remote_only=is_remote,
            limit=50
        )
        
        user_skills = preferences.get("tech_stack", []) if preferences else []
        target_roles = preferences.get("target_roles", []) if preferences else []
        
        for job in jobs:
            job["match_score"] = job_discovery.calculate_match_score(job, user_skills, target_roles)
        
        jobs.sort(key=lambda x: x["match_score"], reverse=True)
        sources = list(set(j.get("source", "unknown") for j in jobs))
        
        return {
            "jobs": jobs,
            "total_count": len(jobs),
            "last_scan": datetime.now(timezone.utc).isoformat(),
            "sources": sources,
            "is_mock": False
        }
        
    except Exception as e:
        logging.error(f"Job search failed: {e}")
        return {
            "jobs": MOCK_JOBS,
            "total_count": len(MOCK_JOBS),
            "sources": ["mock"],
            "is_mock": True,
            "error": str(e)
        }


@router.get("/auto-apply/search")
async def search_jobs(
    keywords: str = Query(..., description="Search keywords"),
    location: str = Query("us", description="Location"),
    salary_min: Optional[int] = Query(None, description="Minimum salary"),
    remote_only: bool = Query(False, description="Remote jobs only"),
    page: int = Query(1, ge=1, description="Page number"),
    user: dict = Depends(get_current_user)
):
    """Search jobs with custom filters"""
    from server import job_discovery
    
    try:
        jobs = await job_discovery.search_all(
            keywords=keywords,
            location=location,
            salary_min=salary_min,
            remote_only=remote_only,
            limit=30
        )
        
        preferences = await db.job_preferences.find_one({"user_id": user["id"]}, {"_id": 0})
        user_skills = preferences.get("tech_stack", []) if preferences else []
        target_roles = preferences.get("target_roles", []) if preferences else []
        
        for job in jobs:
            job["match_score"] = job_discovery.calculate_match_score(job, user_skills, target_roles)
        
        jobs.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "jobs": jobs,
            "total_count": len(jobs),
            "search_query": keywords,
            "location": location,
            "sources": list(set(j.get("source", "unknown") for j in jobs))
        }
        
    except Exception as e:
        logging.error(f"Job search error: {e}")
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")


@router.post("/auto-apply/apply/{job_id}")
async def apply_to_job(
    job_id: str,
    job_data: Optional[Dict[str, Any]] = None,
    user: dict = Depends(get_current_user)
):
    """Track job application"""
    existing = await db.job_applications.find_one({
        "user_id": user["id"],
        "job_id": job_id
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    
    job = next((j for j in MOCK_JOBS if j["id"] == job_id), None)
    is_mock = job is not None
    
    if not job:
        cached_job = await db.cached_jobs.find_one({"id": job_id}, {"_id": 0})
        if cached_job:
            job = cached_job
        elif job_data:
            job = job_data
        else:
            job = {"id": job_id, "title": "External Job", "company": "External Company", "match_score": 0}
    
    application = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "job_id": job_id,
        "job_title": job.get("title", "Unknown"),
        "company": job.get("company", "Unknown"),
        "location": job.get("location", ""),
        "salary_range": job.get("salary_range", ""),
        "job_url": job.get("job_url", ""),
        "status": "applied",
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "match_score": job.get("match_score", 0),
        "source": job.get("source", "mock" if is_mock else "external"),
        "is_mock": is_mock
    }
    
    await db.job_applications.insert_one(application)
    
    return {
        "message": f"Application tracked: {job.get('title')} at {job.get('company')}",
        "application": {k: v for k, v in application.items() if k != "_id"},
        "job_url": job.get("job_url", ""),
        "is_real_job": not is_mock
    }


@router.patch("/auto-apply/applications/{application_id}/status")
async def update_application_status(
    application_id: str,
    status_update: StatusUpdate,
    user: dict = Depends(get_current_user)
):
    """Update application status"""
    valid_statuses = ["pending", "applied", "viewed", "interview_scheduled", "offer", "rejected"]
    
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    result = await db.job_applications.update_one(
        {"id": application_id, "user_id": user["id"]},
        {"$set": {"status": status_update.status, "status_updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return {"message": f"Status updated to {status_update.status}"}


@router.get("/auto-apply/applications")
async def get_applications(user: dict = Depends(get_current_user)):
    """Get user's job applications"""
    applications = await db.job_applications.find(
        {"user_id": user["id"]},
        {"_id": 0}
    ).sort("applied_at", -1).to_list(100)
    
    user_doc = await db.users.find_one({"id": user["id"]}, {"_id": 0, "email": 1, "name": 1})
    notif_prefs = await db.notification_preferences.find_one({"user_id": user["id"]}, {"_id": 0})
    send_notifications = notif_prefs.get("email_interview_alerts", True) if notif_prefs else True
    
    for app in applications:
        applied_at = datetime.fromisoformat(app["applied_at"].replace('Z', '+00:00'))
        days_since = (datetime.now(timezone.utc) - applied_at).days
        previous_status = app.get("status", "applied")
        
        if days_since >= 3:
            app["status"] = "viewed"
            app["company_viewed_at"] = (applied_at + timedelta(days=1)).isoformat()
        if days_since >= 5 and app.get("match_score", 0) >= 90:
            app["status"] = "interview_scheduled"
            app["interview_date"] = (applied_at + timedelta(days=7)).isoformat()
            
            if previous_status != "interview_scheduled" and send_notifications and user_doc:
                existing_notif = await db.notifications.find_one({
                    "user_email": user_doc["email"],
                    "job_title": app["job_title"],
                    "company": app["company"],
                    "type": "interview_scheduled"
                })
                
                if not existing_notif:
                    interview_date_str = datetime.fromisoformat(app["interview_date"].replace('Z', '+00:00')).strftime("%B %d, %Y")
                    asyncio.create_task(send_interview_notification_email(
                        user_email=user_doc["email"],
                        user_name=user_doc.get("name", "User"),
                        job_title=app["job_title"],
                        company=app["company"],
                        interview_date=interview_date_str,
                        job_url=app.get("job_url", "")
                    ))
    
    total = len(applications)
    viewed = len([a for a in applications if a.get("status") in ["viewed", "interview_scheduled"]])
    interviews = len([a for a in applications if a.get("status") == "interview_scheduled"])
    
    return {
        "applications": applications,
        "stats": {
            "total_applications": total,
            "applications_viewed": viewed,
            "interviews_scheduled": interviews,
            "callback_rate": round((viewed / total * 100) if total > 0 else 0, 1)
        }
    }


@router.get("/auto-apply/dashboard")
async def get_auto_apply_dashboard(user: dict = Depends(get_current_user)):
    """Get auto-apply dashboard with stats"""
    from server import job_discovery
    
    preferences = await db.job_preferences.find_one({"user_id": user["id"]}, {"_id": 0})
    applications = await db.job_applications.find(
        {"user_id": user["id"]},
        {"_id": 0}
    ).sort("applied_at", -1).to_list(100)
    
    total = len(applications)
    this_week = len([a for a in applications 
                     if (datetime.now(timezone.utc) - datetime.fromisoformat(a["applied_at"].replace('Z', '+00:00'))).days <= 7])
    
    matching_jobs = MOCK_JOBS[:5]
    is_mock = True
    
    if ADZUNA_APP_ID and ADZUNA_APP_KEY:
        try:
            search_keywords = "AI ML Engineer"
            if preferences and preferences.get("target_roles"):
                search_keywords = " ".join(preferences["target_roles"][:2])
            
            jobs = await job_discovery.search_all(keywords=search_keywords, location="us", limit=8)
            
            user_skills = preferences.get("tech_stack", []) if preferences else []
            target_roles = preferences.get("target_roles", []) if preferences else []
            
            for job in jobs:
                job["match_score"] = job_discovery.calculate_match_score(job, user_skills, target_roles)
            
            jobs.sort(key=lambda x: x["match_score"], reverse=True)
            matching_jobs = jobs[:5]
            is_mock = False
        except Exception as e:
            logging.error(f"Dashboard job fetch failed: {e}")
    
    avg_score = round(sum(j["match_score"] for j in matching_jobs) / len(matching_jobs), 1) if matching_jobs else 0
    
    return {
        "preferences": preferences or {},
        "auto_apply_enabled": preferences.get("auto_apply_enabled", False) if preferences else False,
        "matching_jobs": matching_jobs,
        "recent_applications": applications[:10],
        "stats": {
            "total_applications": total,
            "applications_this_week": this_week,
            "matching_jobs_count": len(matching_jobs),
            "avg_match_score": avg_score
        },
        "is_mock": is_mock
    }


@router.post("/auto-apply/notification-preferences")
async def save_notification_preferences(
    preferences: dict,
    user: dict = Depends(get_current_user)
):
    """Save notification preferences"""
    await db.notification_preferences.update_one(
        {"user_id": user["id"]},
        {"$set": {
            "user_id": user["id"],
            "email_weekly_summary": preferences.get("email_weekly_summary", False),
            "email_interview_alerts": preferences.get("email_interview_alerts", True),
            "email_status_updates": preferences.get("email_status_updates", True),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }},
        upsert=True
    )
    return {"message": "Notification preferences saved"}


@router.get("/auto-apply/notification-preferences")
async def get_notification_preferences(user: dict = Depends(get_current_user)):
    """Get notification preferences"""
    prefs = await db.notification_preferences.find_one({"user_id": user["id"]}, {"_id": 0})
    return prefs or {"email_weekly_summary": False, "email_interview_alerts": True, "email_status_updates": True}
