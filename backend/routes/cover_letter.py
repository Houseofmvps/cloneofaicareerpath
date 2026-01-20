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
    """System prompt for cover letter generation - Natural, human-sounding variations"""
    return """You are an expert career coach who writes authentic, compelling cover letters for tech professionals. Your letters sound natural and human - never robotic or templated.

Generate 3 DISTINCT cover letter variations. Each should feel like it was written by a real person who genuinely cares about the role.

WRITING STYLE GUIDELINES:
- Write conversationally but professionally (like talking to a colleague, not a robot)
- Use contractions naturally (I'm, I've, you're) to sound human
- Vary sentence length - mix short punchy sentences with longer explanatory ones
- Use active voice and strong verbs
- NO corporate jargon, buzzwords, or clichés ("synergy," "leverage," "dynamic team player")
- NO generic openings like "I am writing to express my interest..."
- Show personality while staying professional

VARIATION 1 - "TECHNICAL DEPTH"
Tone: Conversational but technically credible
Focus: Demonstrate deep technical expertise through specific examples
Opening: Lead with a technical observation about their product/stack or a relevant project you built
Example: "I've been following [Company]'s work on [specific tech]. When I saw you're hiring, I knew I had to reach out - I recently built something similar that [specific achievement]."

VARIATION 2 - "IMPACT & RESULTS"  
Tone: Confident and results-oriented (but not arrogant)
Focus: Quantifiable business impact and problem-solving
Opening: Lead with a relevant achievement or problem you've solved
Example: "Last quarter, I reduced our ML model's inference time by 60%, saving $200K annually. When I saw [Company] is tackling [similar challenge], I got excited."

VARIATION 3 - "AUTHENTIC CONNECTION"
Tone: Warm, genuine, story-driven
Focus: Personal connection to company mission and collaborative mindset
Opening: Lead with why you care about what they're building
Example: "I've been a [Company] user for [time] and [specific feature] changed how I work. The chance to build this is why I got into ML."

CRITICAL REQUIREMENTS:
1. **Sound Human**: Read each letter aloud - if it sounds like a robot wrote it, rewrite it
2. **Be Specific**: Use actual numbers, technologies, and project names from the resume
3. **Show, Don't Tell**: Instead of "I'm passionate," say "I spent weekends building X because..."
4. **Natural Keywords**: Weave in 6-8 keywords from job description organically
5. **Length**: 250-300 words (shorter is better - hiring managers are busy)

AVOID:
- "I am writing to apply for..."
- "I am excited to submit my application..."
- "I believe I would be a great fit..."
- Listing skills without context
- Generic enthusiasm ("passionate," "excited," "thrilled")
- Overly formal language

OUTPUT FORMAT (JSON):
{
    "versions": [
        {
            "version_name": "Technical Depth",
            "tone_applied": "conversational_technical",
            "emphasis_area": "technical_expertise",
            "cover_letter": "[Full letter text]",
            "key_highlights": ["achievement 1", "achievement 2", "achievement 3"],
            "keywords_used": ["keyword1", "keyword2", ...],
            "word_count": 280,
            "ats_score": 90
        },
        {
            "version_name": "Impact & Results",
            "tone_applied": "confident_results",
            "emphasis_area": "business_impact",
            "cover_letter": "[Full letter text]",
            "key_highlights": ["impact 1", "impact 2", "impact 3"],
            "keywords_used": ["keyword1", "keyword2", ...],
            "word_count": 270,
            "ats_score": 88
        },
        {
            "version_name": "Authentic Connection",
            "tone_applied": "warm_genuine",
            "emphasis_area": "culture_mission_fit",
            "cover_letter": "[Full letter text]",
            "key_highlights": ["connection 1", "connection 2", "connection 3"],
            "keywords_used": ["keyword1", "keyword2", ...],
            "word_count": 265,
            "ats_score": 85
        }
    ],
    "company_research": {
        "company_name": "Company Name",
        "products_mentioned": ["product1", "product2"],
        "why_compelling": "Brief note on what makes this company interesting"
    },
    "job_match_analysis": {
        "match_score": 85,
        "matching_skills": ["skill1", "skill2", "skill3"],
        "skills_emphasized": ["skill1", "skill2", "skill3"],
        "potential_gaps": ["gap1"]
    }
}

REMEMBER: Write like a human, not a corporate robot. Be specific, be authentic, be concise.
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
Generate 3 DISTINCT cover letter variations for this job application:

COMPANY: {request.company_name or "Not specified"}
TARGET ROLE: {request.target_role or "AI/ML Position"}

JOB DESCRIPTION:
{request.job_description[:4000]}

CANDIDATE'S RESUME:
{request.resume_text[:4000]}

IMPORTANT REQUIREMENTS:
1. Generate all 3 variations as specified in the system prompt:
   - Technical Expert (professional tone)
   - Problem Solver (confident tone)
   - Culture Champion (story-driven tone)

2. Each variation must:
   - Be 300-350 words
   - Have a unique opening hook
   - Include specific company research
   - Use 8-12 keywords from the job description
   - Reference specific examples from the resume with metrics
   - Feel completely different from the other variations

3. Research the company based on the company name and job description to include:
   - Specific products, technologies, or initiatives
   - Company mission, values, or culture
   - Recent news or developments (if inferable from context)

Make these the BEST, most personalized cover letters that will get interviews.
"""
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",  # Sonnet handles complex variations better
            max_tokens=4000,  # Optimized for 3 variations
            system=get_cover_letter_prompt(),
            messages=[{"role": "user", "content": user_message}]
        )
        
        response_text = response.content[0].text
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        
        cover_letter_data = json.loads(response_text)
        
        # Validate that we have 3 versions
        if "versions" not in cover_letter_data or len(cover_letter_data.get("versions", [])) != 3:
            logging.error(f"Cover letter did not return 3 variations: {cover_letter_data.keys()}")
            raise HTTPException(status_code=500, detail="Failed to generate 3 cover letter variations")
            
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


class CoverLetterDownloadRequest(BaseModel):
    cover_letter_id: str
    version_index: int = 0
    format: str = "pdf"


@router.post("/download")
async def download_cover_letter(
    request: CoverLetterDownloadRequest,
    user: dict = Depends(get_current_user)
):
    """Download cover letter as PDF or DOCX"""
    cover_letter = await db.cover_letters.find_one(
        {"id": request.cover_letter_id, "user_id": user["id"]},
        {"_id": 0}
    )
    
    if not cover_letter:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    
    versions = cover_letter.get("versions", [])
    if request.version_index >= len(versions):
        raise HTTPException(status_code=400, detail="Invalid version index")
    
    version = versions[request.version_index]
    cover_letter_text = version.get("cover_letter", "")
    
    file_id = str(uuid.uuid4())[:8]
    
    if request.format == "docx":
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
