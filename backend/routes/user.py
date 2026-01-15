"""
User routes - Profile and user management
"""
from fastapi import APIRouter, Depends
from datetime import datetime, timezone

from auth import get_current_user
from database import db
from config import FREE_LIMITS

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile")
async def get_user_profile(user: dict = Depends(get_current_user)):
    """Get complete user profile with all stats"""
    user_id = user["id"]
    
    # Get current month usage
    current_month = datetime.now(timezone.utc)
    usage = await db.usage.find_one({
        "user_id": user_id,
        "month": current_month.month,
        "year": current_month.year
    }, {"_id": 0})
    
    if not usage:
        usage = {
            "cv_generations_used": 0,
            "learning_paths_used": 0,
            "analyses_used": 0
        }
    
    # Get all-time stats
    total_cvs = await db.cv_generations.count_documents({"user_id": user_id})
    total_paths = await db.learning_paths.count_documents({"user_id": user_id})
    total_analyses = await db.analyses.count_documents({"user_id": user_id})
    total_cover_letters = await db.cover_letters.count_documents({"user_id": user_id})
    
    # Get recent activity
    recent_cvs = await db.cv_generations.find(
        {"user_id": user_id},
        {"_id": 0, "id": 1, "target_role": 1, "created_at": 1}
    ).sort("created_at", -1).limit(5).to_list(5)
    
    recent_paths = await db.learning_paths.find(
        {"user_id": user_id},
        {"_id": 0, "id": 1, "target_role": 1, "created_at": 1}
    ).sort("created_at", -1).limit(5).to_list(5)
    
    is_pro = user.get("subscription_tier") == "pro"
    
    return {
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user.get("name", ""),
            "subscription_tier": user.get("subscription_tier", "free"),
            "cv_credits": user.get("cv_credits", 0),
            "created_at": user.get("created_at", "")
        },
        "usage": {
            "this_month": {
                "cv_generations": usage.get("cv_generations_used", 0),
                "learning_paths": usage.get("learning_paths_used", 0),
                "analyses": usage.get("analyses_used", 0)
            },
            "limits": {
                "cv_generations": 999 if is_pro else FREE_LIMITS.get("cv_generations", 2),
                "learning_paths": 999 if is_pro else FREE_LIMITS.get("learning_paths", 1),
                "analyses": 999 if is_pro else FREE_LIMITS.get("analyses", 1)
            }
        },
        "stats": {
            "total_cv_generations": total_cvs,
            "total_learning_paths": total_paths,
            "total_analyses": total_analyses,
            "total_cover_letters": total_cover_letters
        },
        "recent_activity": {
            "cv_generations": recent_cvs,
            "learning_paths": recent_paths
        }
    }
