"""
Dashboard routes - Career progress dashboard
"""
from fastapi import APIRouter, Depends
from datetime import datetime, timezone, timedelta
import logging

from auth import get_current_user
from database import db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/career-progress")
async def get_career_progress_dashboard(user: dict = Depends(get_current_user)):
    """Get comprehensive career transition dashboard data"""
    from server import job_discovery
    
    # 1. Get user's career analysis
    latest_analysis = await db.analyses.find_one(
        {"user_id": user["id"]},
        {"_id": 0},
        sort=[("created_at", -1)]
    )
    
    # 2. Get learning path progress
    latest_learning_path = await db.learning_paths.find_one(
        {"user_id": user["id"]},
        {"_id": 0},
        sort=[("created_at", -1)]
    )
    
    # 3. Get resume generations
    resume_count = await db.cv_generations.count_documents({"user_id": user["id"]})
    latest_resume = await db.cv_generations.find_one(
        {"user_id": user["id"]},
        {"_id": 0, "country": 1, "format_type": 1, "created_at": 1},
        sort=[("created_at", -1)]
    )
    
    # 4. Get cover letter generations
    cover_letter_count = await db.cover_letters.count_documents({"user_id": user["id"]})
    
    # 5. Get job applications
    applications = await db.job_applications.find(
        {"user_id": user["id"]},
        {"_id": 0}
    ).sort("applied_at", -1).to_list(100)
    
    # Calculate application funnel
    total_applied = len(applications)
    viewed = len([a for a in applications if a.get("status") in ["viewed", "interview_scheduled", "offer"]])
    interviews = len([a for a in applications if a.get("status") in ["interview_scheduled", "offer"]])
    offers = len([a for a in applications if a.get("status") == "offer"])
    
    # This week's applications
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    apps_this_week = len([a for a in applications 
                         if datetime.fromisoformat(a["applied_at"].replace('Z', '+00:00')) > week_ago])
    
    # 6. Calculate overall progress
    analysis_done = latest_analysis is not None
    learning_started = latest_learning_path is not None
    resume_ready = resume_count > 0
    applying_active = total_applied > 0
    interviews_scheduled = interviews > 0
    
    stages_completed = sum([analysis_done, learning_started, resume_ready, applying_active, interviews_scheduled])
    overall_progress = (stages_completed / 5) * 100
    
    # 7. Extract best role match from analysis
    best_role = None
    gap_score = 0
    skills_to_learn = []
    if latest_analysis and latest_analysis.get("analysis_result"):
        result = latest_analysis["analysis_result"]
        role_scores = result.get("role_specific_scores", {})
        if role_scores:
            best_role_name = max(role_scores, key=lambda k: role_scores[k].get("overall_fit", 0))
            best_role = {
                "name": best_role_name,
                "fit_score": role_scores[best_role_name].get("overall_fit", 0),
                "readiness": role_scores[best_role_name].get("readiness_assessment", "")
            }
        gap_score = result.get("skill_gap_overview", {}).get("overall_gap_score", 0)
        skills_to_learn = result.get("skill_gap_overview", {}).get("priority_learning", [])[:6]
    
    # 8. Calculate learning progress
    learning_progress = {
        "current_week": 0,
        "total_weeks": 16,
        "courses_completed": 0,
        "total_courses": 0,
        "percentage": 0
    }
    if latest_learning_path and latest_learning_path.get("learning_path"):
        path = latest_learning_path["learning_path"]
        weeks = path.get("weekly_curriculum", [])
        learning_progress["total_weeks"] = len(weeks)
        total_courses = sum(len(w.get("courses", [])) for w in weeks)
        learning_progress["total_courses"] = total_courses
        saved_progress = latest_learning_path.get("progress", {})
        learning_progress["current_week"] = saved_progress.get("current_week", 1)
        learning_progress["courses_completed"] = saved_progress.get("courses_completed", 0)
        if learning_progress["total_weeks"] > 0:
            learning_progress["percentage"] = (learning_progress["current_week"] / learning_progress["total_weeks"]) * 100
    
    # 9. Response rate
    response_rate = round((viewed / total_applied * 100), 1) if total_applied > 0 else 0
    
    # 10. Salary estimates
    current_salary = 95000
    target_salary = 165000
    
    # 11. Day tracking
    user_created = user.get("created_at", datetime.now(timezone.utc).isoformat())
    try:
        start_date = datetime.fromisoformat(user_created.replace('Z', '+00:00'))
    except:
        start_date = datetime.now(timezone.utc)
    days_since_start = (datetime.now(timezone.utc) - start_date).days
    day_of_90 = min(days_since_start + 1, 90)
    
    # 12. Daily actions
    daily_actions = []
    
    if not analysis_done:
        daily_actions.append({
            "type": "analysis",
            "title": "Complete your career analysis",
            "description": "Upload your resume to discover your best AI role match",
            "priority": 1,
            "link": "/analyze"
        })
    elif not learning_started:
        daily_actions.append({
            "type": "learning",
            "title": "Start your personalized learning path",
            "description": f"Begin your journey to becoming a {best_role['name'] if best_role else 'AI professional'}",
            "priority": 1,
            "link": "/learning-path"
        })
    elif not resume_ready:
        daily_actions.append({
            "type": "resume",
            "title": "Generate your AI-optimized resume",
            "description": "Create an ATS-friendly resume tailored for AI roles",
            "priority": 1,
            "link": "/cv-generator"
        })
    else:
        daily_actions.append({
            "type": "apply",
            "title": "Apply to 3 high-match jobs today",
            "description": "Cover letters ready • One-click apply available",
            "priority": 1,
            "link": "/auto-apply"
        })
        
        if learning_progress["percentage"] < 100:
            daily_actions.append({
                "type": "learning",
                "title": f"Continue Week {learning_progress['current_week']} of your learning path",
                "description": f"{learning_progress['percentage']:.0f}% complete • Stay on track!",
                "priority": 2,
                "link": "/learning-path"
            })
    
    # 13. Hot jobs
    hot_jobs = []
    try:
        preferences = await db.job_preferences.find_one({"user_id": user["id"]}, {"_id": 0})
        user_skills = preferences.get("tech_stack", []) if preferences else []
        target_roles = preferences.get("target_roles", []) if preferences else []
        
        jobs = await job_discovery.search_all(
            keywords=target_roles[0] if target_roles else "AI Engineer",
            location="us",
            limit=10
        )
        
        for job in jobs:
            job["match_score"] = job_discovery.calculate_match_score(job, user_skills, target_roles)
        
        jobs.sort(key=lambda x: x["match_score"], reverse=True)
        hot_jobs = jobs[:3]
    except Exception as e:
        logging.error(f"Failed to fetch hot jobs: {e}")
    
    return {
        "user": {
            "name": user.get("name", "User"),
            "email": user.get("email"),
            "subscription_tier": user.get("subscription_tier", "free"),
            "days_since_start": day_of_90
        },
        "progress": {
            "day_of_90": day_of_90,
            "overall_percentage": round(overall_progress, 1),
            "stages": {
                "analysis": {"done": analysis_done, "label": "Analysis"},
                "learning": {"done": learning_started, "label": "Learning"},
                "resume": {"done": resume_ready, "label": "Resume"},
                "applying": {"done": applying_active, "label": "Applying"},
                "interviews": {"done": interviews_scheduled, "label": "Interviews"}
            }
        },
        "career_fit": {
            "best_role": best_role,
            "gap_score": gap_score,
            "skills_to_learn": skills_to_learn
        },
        "learning": learning_progress,
        "applications": {
            "total_applied": total_applied,
            "this_week": apps_this_week,
            "funnel": {
                "applied": total_applied,
                "viewed": viewed,
                "interviews": interviews,
                "offers": offers
            },
            "response_rate": response_rate,
            "industry_avg_rate": 8,
            "recent": applications[:5]
        },
        "documents": {
            "resumes_generated": resume_count,
            "cover_letters_generated": cover_letter_count,
            "latest_resume": latest_resume
        },
        "market_value": {
            "current_estimate": current_salary,
            "target_salary": target_salary,
            "potential_increase": target_salary - current_salary,
            "increase_percentage": round(((target_salary - current_salary) / current_salary) * 100, 1)
        },
        "daily_actions": daily_actions,
        "hot_jobs": hot_jobs
    }
