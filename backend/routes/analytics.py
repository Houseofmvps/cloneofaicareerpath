"""
Analytics routes - Tracking and dashboard analytics
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

from auth import get_current_user
from database import db

router = APIRouter(prefix="/analytics", tags=["analytics"])


class CourseClickEvent(BaseModel):
    course_id: str
    course_name: str
    course_url: str
    learning_path_id: Optional[str] = None


@router.post("/course-click")
async def track_course_click(event: CourseClickEvent, user: dict = Depends(get_current_user)):
    """Track when user clicks on a course link"""
    await db.analytics.insert_one({
        "type": "course_click",
        "user_id": user["id"],
        "course_id": event.course_id,
        "course_name": event.course_name,
        "course_url": event.course_url,
        "learning_path_id": event.learning_path_id,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    return {"tracked": True}


@router.get("/dashboard")
async def get_analytics_dashboard(user: dict = Depends(get_current_user)):
    """Get user's personal analytics"""
    user_id = user["id"]
    
    # Count CV generations
    cv_count = await db.cv_generations.count_documents({"user_id": user_id})
    
    # Count learning paths
    lp_count = await db.learning_paths.count_documents({"user_id": user_id})
    
    # Count analyses
    analysis_count = await db.analyses.count_documents({"user_id": user_id})
    
    # Count downloads
    download_count = await db.downloads.count_documents({"user_id": user_id})
    
    # Get download breakdown
    pdf_downloads = await db.downloads.count_documents({"user_id": user_id, "format": "pdf"})
    docx_downloads = await db.downloads.count_documents({"user_id": user_id, "format": "docx"})
    
    # Get course clicks
    course_clicks = await db.analytics.count_documents({"user_id": user_id, "type": "course_click"})
    
    # Get most clicked courses
    pipeline = [
        {"$match": {"user_id": user_id, "type": "course_click"}},
        {"$group": {"_id": "$course_name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    top_courses = await db.analytics.aggregate(pipeline).to_list(length=5)
    
    return {
        "cv_generations": cv_count,
        "learning_paths": lp_count,
        "analyses": analysis_count,
        "total_downloads": download_count,
        "downloads_by_format": {
            "pdf": pdf_downloads,
            "docx": docx_downloads
        },
        "course_clicks": course_clicks,
        "top_courses": [{"name": c["_id"], "clicks": c["count"]} for c in top_courses]
    }
