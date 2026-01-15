"""
Resume routes - Resume parsing, extraction, and scanning
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import io
import logging
import re
import os
import json

router = APIRouter(tags=["resume"])

# Imports
from auth import get_current_user
from database import db
from data.pricing import FREE_LIMITS
from data.roles import AI_ROLES

# Anthropic for AI scanning
import anthropic
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')


async def analyze_resume_for_role(resume_text: str, role_id: str) -> Dict[str, Any]:
    """
    Shared function to analyze a resume against a target role.
    Used by both Resume Scanner and CV Generator for consistent scoring.
    """
    # Get target role info
    role = next((r for r in AI_ROLES if r["id"] == role_id), None)
    if not role:
        return {"error": "Invalid role"}
    
    role_name = role["name"]
    role_skills = role.get("top_skills", [])
    
    # Build the analysis prompt
    prompt = f"""Analyze this resume for a {role_name} position. Be accurate and consistent in scoring.

RESUME:
{resume_text[:4000]}

TARGET ROLE: {role_name}
KEY SKILLS NEEDED: {', '.join(role_skills)}

SCORING CRITERIA:
- ATS Score (0-100): Check for proper formatting, relevant keywords, clear structure, no graphics/tables issues
- Human Appeal (0-100): Storytelling quality, quantified achievements, clarity, professional tone
- Keyword Match: What percentage of required skills are mentioned?

Analyze and return a JSON object with these exact fields:
{{
    "ats_score": <0-100 integer>,
    "human_appeal_score": <0-100 integer>,
    "keyword_match_percent": <0-100 integer>,
    "overall_grade": "<A+/A/B+/B/C+/C/D/F>",
    "keywords_found": ["keywords", "actually", "found", "in", "resume"],
    "keywords_missing": ["important", "missing", "keywords"],
    "strengths": ["3-4 specific strengths"],
    "improvements": ["4-5 specific actionable improvements"],
    "formatting_issues": ["any ATS issues found"],
    "quick_wins": ["2-3 easy fixes"]
}}

Be HONEST and CONSISTENT. A good resume should score 80-95. Only exceptional resumes score 95+.
Return ONLY valid JSON."""

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text.strip()
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())
        else:
            raise ValueError("No valid JSON in response")
            
    except Exception as e:
        logging.error(f"Resume analysis error: {e}")
        # Fallback analysis
        resume_lower = resume_text.lower()
        keywords_found = [s for s in role_skills if s.lower() in resume_lower]
        keywords_missing = [s for s in role_skills if s.lower() not in resume_lower]
        keyword_match = int(len(keywords_found) / max(len(role_skills), 1) * 100)
        
        return {
            "ats_score": min(75, 50 + keyword_match // 3),
            "human_appeal_score": 65,
            "keyword_match_percent": keyword_match,
            "overall_grade": "B" if keyword_match > 50 else "C",
            "keywords_found": keywords_found,
            "keywords_missing": keywords_missing,
            "strengths": ["Resume provided for analysis"],
            "improvements": [f"Add missing keywords: {', '.join(keywords_missing[:3])}"],
            "formatting_issues": [],
            "quick_wins": ["Add more relevant keywords"]
        }


def get_extract_text_from_pdf():
    """Deferred import to avoid circular dependency"""
    from server import extract_text_from_pdf
    return extract_text_from_pdf


def get_parse_resume_text():
    """Deferred import to avoid circular dependency"""
    from server import parse_resume_text
    return parse_resume_text


class ResumeScanRequest(BaseModel):
    resume_text: str
    target_role_id: str
    

class ResumeScanResponse(BaseModel):
    ats_score: int
    human_appeal_score: int
    keyword_match_percent: int
    overall_grade: str
    keywords_found: List[str]
    keywords_missing: List[str]
    strengths: List[str]
    improvements: List[str]
    formatting_issues: List[str]
    quick_wins: List[str]
    target_role: str
    scan_id: str


@router.post("/resume/parse")
async def parse_resume(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """Parse resume from file upload or text input"""
    if not file and not text:
        raise HTTPException(status_code=400, detail="Provide either file or text")
    
    extract_text_from_pdf = get_extract_text_from_pdf()
    parse_resume_text = get_parse_resume_text()
    
    resume_text = ""
    
    if file:
        content = await file.read()
        if file.filename.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith(('.doc', '.docx')):
            try:
                import mammoth
                result = mammoth.extract_raw_text(io.BytesIO(content))
                resume_text = result.value
            except Exception as e:
                logging.error(f"DOCX extraction error: {e}")
                resume_text = content.decode('utf-8', errors='ignore')
        else:
            resume_text = content.decode('utf-8', errors='ignore')
    else:
        resume_text = text
    
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")
    
    parsed = parse_resume_text(resume_text)
    
    # Extract skills and experience for Learning Path auto-fill
    extracted_skills = []
    current_role = ""
    years_experience = 0
    
    if parsed:
        # Get skills
        if parsed.get("skills"):
            if isinstance(parsed["skills"], list):
                extracted_skills = parsed["skills"][:20]
            elif isinstance(parsed["skills"], str):
                extracted_skills = [s.strip() for s in parsed["skills"].split(",")][:20]
        
        # Get current role from experience
        if parsed.get("experience") and len(parsed["experience"]) > 0:
            exp = parsed["experience"][0]
            current_role = exp.get("title", "") or exp.get("role", "") or ""
        
        # Estimate years of experience
        if parsed.get("experience"):
            total_years = 0
            for exp in parsed["experience"]:
                duration = exp.get("duration", "")
                if duration:
                    year_matches = re.findall(r'(\d{4})', duration)
                    if len(year_matches) >= 2:
                        total_years += int(year_matches[-1]) - int(year_matches[0])
                    elif "year" in duration.lower():
                        num_match = re.search(r'(\d+)', duration)
                        if num_match:
                            total_years += int(num_match.group(1))
            years_experience = total_years if total_years > 0 else len(parsed["experience"]) * 2
    
    return {
        "resume_data": parsed,
        "text": resume_text[:2000],
        "extracted_skills": extracted_skills,
        "current_role": current_role,
        "years_experience": years_experience
    }


@router.post("/resume/scan")
async def scan_resume(request: ResumeScanRequest, user: dict = Depends(get_current_user)):
    """
    AI-powered resume scanner - analyzes resume against target role
    Returns ATS score, keyword analysis, and actionable improvements
    Free: 2 scans/month | Pro: Unlimited
    """
    user_id = user["id"]
    is_pro = user.get("subscription_tier") == "pro"
    
    # Check usage limits
    current_month = datetime.now(timezone.utc)
    usage = await db.usage.find_one({
        "user_id": user_id,
        "month": current_month.month,
        "year": current_month.year
    })
    
    scans_used = usage.get("resume_scans_used", 0) if usage else 0
    scan_limit = 999 if is_pro else FREE_LIMITS.get("resume_scans", 2)
    
    if scans_used >= scan_limit:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Monthly scan limit reached",
                "scans_used": scans_used,
                "scans_limit": scan_limit,
                "upgrade_cta": "Upgrade to Pro for unlimited scans"
            }
        )
    
    # Get target role info
    role = next((r for r in AI_ROLES if r["id"] == request.target_role_id), None)
    if not role:
        raise HTTPException(status_code=400, detail="Invalid target role")
    
    role_name = role["name"]
    
    # Use shared analysis function for consistent scoring
    scan_result = await analyze_resume_for_role(request.resume_text, request.target_role_id)
    
    # Generate scan ID and save to database
    from uuid import uuid4
    scan_id = str(uuid4())
    
    scan_record = {
        "id": scan_id,
        "user_id": user_id,
        "target_role_id": request.target_role_id,
        "target_role": role_name,
        "ats_score": scan_result.get("ats_score", 0),
        "human_appeal_score": scan_result.get("human_appeal_score", 0),
        "keyword_match_percent": scan_result.get("keyword_match_percent", 0),
        "overall_grade": scan_result.get("overall_grade", "N/A"),
        "keywords_found": scan_result.get("keywords_found", []),
        "keywords_missing": scan_result.get("keywords_missing", []),
        "strengths": scan_result.get("strengths", []),
        "improvements": scan_result.get("improvements", []),
        "formatting_issues": scan_result.get("formatting_issues", []),
        "quick_wins": scan_result.get("quick_wins", []),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.resume_scans.insert_one(scan_record)
    
    # Update usage
    await db.usage.update_one(
        {
            "user_id": user_id,
            "month": current_month.month,
            "year": current_month.year
        },
        {
            "$inc": {"resume_scans_used": 1},
            "$setOnInsert": {
                "user_id": user_id,
                "month": current_month.month,
                "year": current_month.year
            }
        },
        upsert=True
    )
    
    return {
        **scan_result,
        "target_role": role_name,
        "scan_id": scan_id,
        "usage": {
            "scans_used": scans_used + 1,
            "scans_limit": scan_limit
        }
    }


@router.get("/resume/scan/history")
async def get_scan_history(user: dict = Depends(get_current_user)):
    """Get user's resume scan history"""
    scans = await db.resume_scans.find(
        {"user_id": user["id"]},
        {"_id": 0}
    ).sort("created_at", -1).limit(10).to_list(10)
    
    return {"scans": scans, "total": len(scans)}


@router.get("/resume/scan/usage")
async def get_scan_usage(user: dict = Depends(get_current_user)):
    """Get current month's scan usage"""
    user_id = user["id"]
    is_pro = user.get("subscription_tier") == "pro"
    
    current_month = datetime.now(timezone.utc)
    usage = await db.usage.find_one({
        "user_id": user_id,
        "month": current_month.month,
        "year": current_month.year
    })
    
    scans_used = usage.get("resume_scans_used", 0) if usage else 0
    scan_limit = 999 if is_pro else FREE_LIMITS.get("resume_scans", 2)
    
    return {
        "scans_used": scans_used,
        "scans_limit": scan_limit,
        "is_pro": is_pro,
        "can_scan": scans_used < scan_limit
    }
