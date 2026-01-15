"""
Cover Letter routes - Generation, history, download
"""
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timezone
import uuid
import re
import json
import logging
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY
from docx import Document

from auth import get_current_user
from database import db
from config import ANTHROPIC_API_KEY, DOWNLOADS_DIR

# Import anthropic
import anthropic
claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

router = APIRouter(prefix="/cover-letter", tags=["cover-letter"])


class CoverLetterRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=50)
    company_name: Optional[str] = ""
    target_role: Optional[str] = ""
    tone: Optional[str] = "professional"


def get_cover_letter_prompt():
    """System prompt for cover letter generation - Optimized single version"""
    return """You are an expert cover letter writer specializing in AI/ML job applications.

Your task is to generate ONE PERFECT cover letter that:
1. Is highly personalized to the specific job description
2. Highlights the most relevant transferable skills from the resume
3. Demonstrates genuine interest and knowledge about the company
4. Is ATS-optimized with relevant keywords from the job posting
5. Balances technical expertise with problem-solving ability and culture fit

TONE OPTIONS (apply the requested tone):
- "professional": Corporate, formal tone suitable for big tech companies
- "confident": Bold, assertive tone suitable for startups  
- "story-driven": Personal narrative tone suitable for mission-driven companies

COVER LETTER STRUCTURE:
1. OPENING HOOK (2-3 sentences): Grab attention with a specific achievement or insight about the company
2. VALUE PROPOSITION (1 paragraph): Your most relevant skills and how they solve their problems
3. PROOF POINTS (1-2 paragraphs): Specific examples with metrics from your experience
4. COMPANY ALIGNMENT (1 paragraph): Why THIS company, demonstrate research
5. CLOSING (2-3 sentences): Clear call to action, availability

OUTPUT FORMAT (JSON):
{
    "cover_letter": {
        "content": "Full cover letter text here (300-400 words)...",
        "tone_applied": "professional",
        "word_count": 350,
        "key_highlights": ["highlight1", "highlight2", "highlight3"],
        "keywords_used": ["keyword1", "keyword2", "keyword3"],
        "ats_score": 92
    },
    "company_research": {
        "company_name": "Company Name",
        "industry": "AI/Tech",
        "notable_products": ["product1", "product2"],
        "culture_notes": "Brief culture analysis",
        "why_good_fit": "Why candidate fits this company"
    },
    "job_match_analysis": {
        "match_score": 85,
        "matching_skills": ["skill1", "skill2"],
        "skills_emphasized": ["skill1", "skill2"],
        "potential_gaps": ["gap1"]
    }
}

CRITICAL RULES:
- Output ONLY valid JSON
- Cover letter should be 300-400 words
- Use specific examples and metrics from the resume
- Include 5-10 keywords from the job description naturally
- Never use generic phrases like "I am writing to apply..."
- Start with a compelling hook that shows company knowledge
- Every paragraph should add value
"""


@router.post("/generate")
async def generate_cover_letter(
    request: CoverLetterRequest,
    user: dict = Depends(get_current_user)
):
    """Generate personalized cover letters based on resume and job description"""
    
    current_month = datetime.now(timezone.utc)
    usage = await db.usage.find_one({
        "user_id": user["id"],
        "month": current_month.month,
        "year": current_month.year
    }, {"_id": 0})
    
    if not usage:
        usage = {"cover_letters_used": 0}
        await db.usage.update_one(
            {"user_id": user["id"], "month": current_month.month, "year": current_month.year},
            {"$set": {"cover_letters_used": 0}},
            upsert=True
        )
    
    cover_letters_used = usage.get("cover_letters_used", 0)
    is_pro = user.get("subscription_tier") == "pro"
    
    if not is_pro and cover_letters_used >= 1:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Cover letter limit reached",
                "used": cover_letters_used,
                "limit": 1,
                "upgrade_options": {"pro": "$9.99/month unlimited"}
            }
        )
    
    user_message = f"""
Generate ONE perfect cover letter for this job application:

COMPANY: {request.company_name or "Not specified"}
TARGET ROLE: {request.target_role or "AI/ML Position"}
REQUESTED TONE: {request.tone}

JOB DESCRIPTION:
{request.job_description[:3000]}

CANDIDATE'S RESUME:
{request.resume_text[:3000]}

Create the BEST possible cover letter that:
- Perfectly matches this specific job
- Highlights the candidate's most relevant experience
- Uses keywords from the job description
- Shows genuine knowledge of the company
- Applies the "{request.tone}" tone throughout
"""
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,  # Reduced from 4000 - only need 1 version
            system=get_cover_letter_prompt(),
            messages=[{"role": "user", "content": user_message}]
        )
        
        response_text = response.content[0].text
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        
        cover_letter_data = json.loads(response_text)
        
        # Transform to consistent format (single version in versions array for backward compatibility)
        if "cover_letter" in cover_letter_data and isinstance(cover_letter_data["cover_letter"], dict):
            cl = cover_letter_data["cover_letter"]
            cover_letter_data["versions"] = [{
                "version_name": "Optimized",
                "tone_applied": cl.get("tone_applied", request.tone),
                "cover_letter": cl.get("content", ""),
                "key_highlights": cl.get("key_highlights", []),
                "keywords_used": cl.get("keywords_used", []),
                "word_count": cl.get("word_count", 350),
                "ats_score": cl.get("ats_score", 90)
            }]
            
    except json.JSONDecodeError as e:
        logging.error(f"Cover letter JSON parse error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse cover letter response")
    except Exception as e:
        logging.error(f"Cover letter generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")
    
    if not is_pro:
        await db.usage.update_one(
            {"user_id": user["id"], "month": current_month.month, "year": current_month.year},
            {"$inc": {"cover_letters_used": 1}},
            upsert=True
        )
    
    cover_letter_id = str(uuid.uuid4())
    await db.cover_letters.insert_one({
        "id": cover_letter_id,
        "user_id": user["id"],
        "company_name": request.company_name,
        "target_role": request.target_role,
        "tone": request.tone,
        "job_description": request.job_description[:1000],
        "versions": cover_letter_data.get("versions", []),
        "company_research": cover_letter_data.get("company_research", {}),
        "job_match_analysis": cover_letter_data.get("job_match_analysis", {}),
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    return {
        "cover_letter_id": cover_letter_id,
        "company_name": request.company_name,
        "target_role": request.target_role,
        "tone": request.tone,
        "versions": cover_letter_data.get("versions", []),
        "company_research": cover_letter_data.get("company_research", {}),
        "job_match_analysis": cover_letter_data.get("job_match_analysis", {}),
        "usage": {
            "used": cover_letters_used + 1 if not is_pro else cover_letters_used,
            "limit": 999 if is_pro else 1
        }
    }


@router.get("/history")
async def get_cover_letter_history(user: dict = Depends(get_current_user)):
    """Get user's cover letter history"""
    cover_letters = await db.cover_letters.find(
        {"user_id": user["id"]},
        {"_id": 0}
    ).sort("created_at", -1).to_list(50)
    return {"cover_letters": cover_letters}


@router.get("/{cover_letter_id}")
async def get_cover_letter(cover_letter_id: str, user: dict = Depends(get_current_user)):
    """Get specific cover letter"""
    cover_letter = await db.cover_letters.find_one(
        {"id": cover_letter_id, "user_id": user["id"]},
        {"_id": 0}
    )
    if not cover_letter:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    return cover_letter


@router.post("/download")
async def download_cover_letter(
    cover_letter_id: str = Form(...),
    version_index: int = Form(0),
    format: str = Form("pdf"),
    user: dict = Depends(get_current_user)
):
    """Download cover letter as PDF or DOCX"""
    cover_letter = await db.cover_letters.find_one(
        {"id": cover_letter_id, "user_id": user["id"]},
        {"_id": 0}
    )
    
    if not cover_letter:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    
    versions = cover_letter.get("versions", [])
    if version_index >= len(versions):
        raise HTTPException(status_code=400, detail="Invalid version index")
    
    version = versions[version_index]
    cover_letter_text = version.get("cover_letter", "")
    
    file_id = str(uuid.uuid4())[:8]
    
    if format == "docx":
        filename = f"cover_letter_{file_id}.docx"
        filepath = DOWNLOADS_DIR / filename
        
        doc = Document()
        doc.add_paragraph(cover_letter_text)
        doc.save(str(filepath))
    else:
        filename = f"cover_letter_{file_id}.pdf"
        filepath = DOWNLOADS_DIR / filename
        
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        styles = getSampleStyleSheet()
        body_style = ParagraphStyle(
            'CoverLetterBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=16,
            spaceAfter=12,
            alignment=TA_JUSTIFY
        )
        
        story = []
        paragraphs = cover_letter_text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), body_style))
                story.append(Spacer(1, 12))
        
        doc.build(story)
    
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "X-Download-Success": "true"
        }
    )
