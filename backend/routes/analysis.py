"""
Analysis routes - Career gap analysis, usage tracking
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timezone
import uuid

from auth import get_current_user
from database import db
from config import FREE_LIMITS

router = APIRouter(tags=["analysis"])


# Models
class ResumeData(BaseModel):
    name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    education: List[Dict] = []
    experience: List[Dict] = []
    skills: List[str] = []
    certifications: List[str] = []
    summary: Optional[str] = ""


class BackgroundContext(BaseModel):
    years_in_current_field: int = 0
    current_industry: str = ""
    target_timeline_months: int = 6
    available_hours_per_week: int = 10
    learning_style: str = "mixed"
    budget_for_learning: str = "moderate"
    has_portfolio: bool = False
    has_github: bool = False
    willing_to_relocate: bool = False
    preferred_company_size: str = "any"


class AnalysisRequest(BaseModel):
    resume_data: ResumeData
    target_role_id: str
    background_context: BackgroundContext


class UsageResponse(BaseModel):
    cv_generations_used: int
    cv_generations_limit: int
    learning_paths_used: int
    learning_paths_limit: int
    analyses_used: int
    analyses_limit: int
    cv_credits: int = 0
    learning_path_credits: int = 0


@router.post("/analyze")
async def analyze_career(
    request: AnalysisRequest,
    user: dict = Depends(get_current_user)
):
    """Perform career gap analysis"""
    # Import required from server
    from server import AI_ROLES, analyze_with_claude
    
    current_month = datetime.now(timezone.utc)
    usage = await db.usage.find_one({
        "user_id": user["id"],
        "month": current_month.month,
        "year": current_month.year
    }, {"_id": 0})
    
    if not usage:
        usage = {"analyses_used": 0}
        await db.usage.insert_one({
            "user_id": user["id"],
            "month": current_month.month,
            "year": current_month.year,
            "analyses_used": 0
        })
    
    is_pro = user.get("subscription_tier") == "pro"
    if not is_pro and usage.get("analyses_used", 0) >= FREE_LIMITS.get("analyses", 1):
        raise HTTPException(
            status_code=403, 
            detail="Analysis limit reached. Upgrade to Pro for unlimited analyses."
        )
    
    target_role = next((r for r in AI_ROLES if r["id"] == request.target_role_id), None)
    if not target_role:
        raise HTTPException(status_code=404, detail="Target role not found")
    
    analysis_result = await analyze_with_claude(
        request.resume_data.model_dump(),
        target_role,
        request.background_context.model_dump()
    )
    
    analysis_id = str(uuid.uuid4())
    
    await db.analyses.insert_one({
        "id": analysis_id,
        "user_id": user["id"],
        "resume_data": request.resume_data.model_dump(),
        "target_role": target_role,
        "background_context": request.background_context.model_dump(),
        "analysis_result": analysis_result,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    await db.usage.update_one(
        {"user_id": user["id"], "month": current_month.month, "year": current_month.year},
        {"$inc": {"analyses_used": 1}},
        upsert=True
    )
    
    return {
        "analysis_id": analysis_id,
        "target_role": target_role,
        "analysis": analysis_result
    }


@router.get("/analyses")
async def get_analyses(user: dict = Depends(get_current_user)):
    """Get user's analysis history"""
    analyses = await db.analyses.find(
        {"user_id": user["id"]},
        {"_id": 0}
    ).sort("created_at", -1).to_list(50)
    return {"analyses": analyses}


@router.get("/analyses/{analysis_id}")
async def get_analysis(analysis_id: str, user: dict = Depends(get_current_user)):
    """Get specific analysis"""
    analysis = await db.analyses.find_one(
        {"id": analysis_id, "user_id": user["id"]},
        {"_id": 0}
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.get("/usage", response_model=UsageResponse)
async def get_usage(user: dict = Depends(get_current_user)):
    """Get user's usage statistics"""
    current_month = datetime.now(timezone.utc)
    usage = await db.usage.find_one({
        "user_id": user["id"],
        "month": current_month.month,
        "year": current_month.year
    }, {"_id": 0})
    
    if not usage:
        usage = {
            "cv_generations_used": 0,
            "learning_paths_used": 0,
            "analyses_used": 0
        }
    
    is_pro = user.get("subscription_tier") == "pro"
    
    return UsageResponse(
        cv_generations_used=usage.get("cv_generations_used", 0),
        cv_generations_limit=999 if is_pro else FREE_LIMITS.get("cv_generations", 2),
        learning_paths_used=usage.get("learning_paths_used", 0),
        learning_paths_limit=999 if is_pro else FREE_LIMITS.get("learning_paths", 1),
        analyses_used=usage.get("analyses_used", 0),
        analyses_limit=999 if is_pro else FREE_LIMITS.get("analyses", 1),
        cv_credits=user.get("cv_credits", 0),
        learning_path_credits=user.get("learning_path_credits", 0)
    )
