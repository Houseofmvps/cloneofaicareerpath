"""
Interview Prep routes - Questions, Feedback, History
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone, timedelta
import uuid
import random
import re
import json
import logging

from auth import get_current_user
from database import db
from config import ANTHROPIC_API_KEY
from interview_questions import ROLE_QUESTIONS, COMPANY_QUESTIONS

# Import anthropic if available
try:
    import anthropic
except ImportError:
    anthropic = None

router = APIRouter(prefix="/interview-prep", tags=["interview"])


# Models
class InterviewQuestionRequest(BaseModel):
    role_id: str
    categories: List[str] = ["technical", "behavioral", "system_design", "coding", "ml_concepts"]
    count: int = 25
    company: Optional[str] = None


class InterviewFeedbackRequest(BaseModel):
    question: str
    answer: str
    role_id: str
    category: str


# AI Roles definition (should be in models, but keeping here for now)
AI_ROLES = [
    {"id": "ml_engineer", "name": "Machine Learning Engineer"},
    {"id": "ai_engineer", "name": "AI Engineer"},
    {"id": "data_scientist", "name": "Data Scientist"},
    {"id": "prompt_engineer", "name": "Prompt Engineer"},
    {"id": "mlops_engineer", "name": "MLOps Engineer"},
    {"id": "cv_engineer", "name": "Computer Vision Engineer"},
    {"id": "nlp_engineer", "name": "NLP Engineer"},
    {"id": "ai_product_manager", "name": "AI Product Manager"},
    {"id": "ai_research_scientist", "name": "AI Research Scientist"},
]


@router.get("/companies")
async def get_interview_companies():
    """Get list of companies with interview question banks"""
    companies = []
    for comp_id, comp_data in COMPANY_QUESTIONS.items():
        companies.append({
            "id": comp_id,
            "name": comp_data.get("name", comp_id),
            "logo": comp_data.get("logo", "🏢"),
            "description": comp_data.get("description", "")
        })
    return {"companies": companies}


@router.post("/generate")
async def generate_interview_questions(
    request: InterviewQuestionRequest,
    user: dict = Depends(get_current_user)
):
    """Generate role-specific interview questions with balanced category distribution"""
    
    # Collect questions by category for balanced distribution
    categorized_questions = {cat: [] for cat in request.categories}
    
    # Get role-specific questions
    role_questions = ROLE_QUESTIONS.get(request.role_id, {})
    for category in request.categories:
        cat_questions = role_questions.get(category, [])
        for q in cat_questions:
            categorized_questions[category].append({
                **q,
                "category": category,
                "id": str(uuid.uuid4())[:8],
                "source": "role"
            })
    
    # Add company-specific questions if requested
    if request.company and request.company in COMPANY_QUESTIONS:
        comp_data = COMPANY_QUESTIONS[request.company]
        for q in comp_data.get("technical", []):
            if q.get("category") in request.categories or "technical" in request.categories:
                cat = q.get("category", "technical")
                if cat in categorized_questions:
                    categorized_questions[cat].append({
                        **q,
                        "category": cat,
                        "id": str(uuid.uuid4())[:8],
                        "company": comp_data.get("name"),
                        "source": "company"
                    })
        for q in comp_data.get("behavioral", []):
            if "behavioral" in request.categories:
                categorized_questions["behavioral"].append({
                    **q,
                    "category": "behavioral",
                    "id": str(uuid.uuid4())[:8],
                    "company": comp_data.get("name"),
                    "source": "company"
                })
    
    # Balanced distribution: allocate questions evenly across categories
    questions = []
    num_categories = len([c for c in request.categories if categorized_questions.get(c)])
    
    if num_categories > 0:
        base_per_category = max(3, request.count // num_categories)
        
        for category in request.categories:
            cat_qs = categorized_questions.get(category, [])
            if cat_qs:
                random.shuffle(cat_qs)
                questions.extend(cat_qs[:base_per_category])
    
    # Fill remaining slots
    remaining_count = request.count - len(questions)
    if remaining_count > 0:
        all_remaining = []
        for category in request.categories:
            cat_qs = categorized_questions.get(category, [])
            base_per_category = max(3, request.count // num_categories) if num_categories > 0 else 3
            all_remaining.extend(cat_qs[base_per_category:])
        
        random.shuffle(all_remaining)
        questions.extend(all_remaining[:remaining_count])
    
    random.shuffle(questions)
    questions = questions[:request.count]
    
    # AI-generated questions if needed (using Haiku for cost efficiency)
    # Haiku is suitable for this commodity task - quality validated for top-tier companies
    if len(questions) < request.count and ANTHROPIC_API_KEY and anthropic:
        try:
            role_data = next((r for r in AI_ROLES if r["id"] == request.role_id), None)
            role_name = role_data["name"] if role_data else request.role_id
            
            needed = request.count - len(questions)
            
            # Build company-aware prompt if company is specified
            company_context = ""
            if request.company:
                company_context = f" at {request.company}. These should be highly relevant to {request.company}'s specific technical challenges and culture"
            
            prompt = f"""Generate {needed} unique interview questions for a {role_name} position{company_context}.
            
Categories needed: {', '.join(request.categories)}

For each question, provide:
1. The question text
2. Difficulty level (easy/medium/hard)
3. A brief hint for the candidate
4. The category it belongs to

Return as JSON array:
[{{"question": "...", "difficulty": "medium", "hint": "...", "category": "technical"}}]"""

            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            # Using Haiku for question generation (cost-efficient, quality validated)
            # Sonnet reserved for interview feedback (premium user-facing feature)
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                ai_questions = json.loads(json_match.group())
                for q in ai_questions:
                    q["id"] = str(uuid.uuid4())[:8]
                    q["ai_generated"] = True
                questions.extend(ai_questions)
        except Exception as e:
            logging.error(f"AI question generation failed: {e}")
    
    questions = questions[:request.count]
    
    # Category breakdown
    category_counts = {}
    for q in questions:
        cat = q.get("category", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    return {
        "questions": questions,
        "role_id": request.role_id,
        "category_breakdown": category_counts,
        "total": len(questions)
    }


@router.post("/feedback")
async def get_interview_feedback(
    request: InterviewFeedbackRequest,
    user: dict = Depends(get_current_user)
):
    """Get AI feedback on interview answer"""
    
    if not ANTHROPIC_API_KEY or not anthropic:
        return {
            "score": 70,
            "strengths": ["Good structure", "Mentioned relevant concepts"],
            "improvements": ["Could add more specific examples", "Consider edge cases"],
            "sample_answer": "A strong answer would include specific examples from your experience..."
        }
    
    try:
        role_data = next((r for r in AI_ROLES if r["id"] == request.role_id), None)
        role_name = role_data["name"] if role_data else request.role_id
        
        prompt = f"""You are an expert interviewer for {role_name} positions. 
        
Evaluate this interview answer:

QUESTION ({request.category}): {request.question}

CANDIDATE'S ANSWER: {request.answer}

Provide feedback as JSON:
{{
    "score": <0-100>,
    "strengths": ["strength 1", "strength 2"],
    "improvements": ["improvement 1", "improvement 2"],
    "sample_answer": "A brief example of a strong answer..."
}}

Be constructive but honest. Score based on:
- Relevance to the question (30%)
- Technical accuracy (30%)
- Communication clarity (20%)
- Use of examples/specifics (20%)"""

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        # Using Sonnet for feedback - premium model for core user-facing feature
        # This is the key differentiator - high-quality, detailed interview feedback
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            feedback = json.loads(json_match.group())
        else:
            feedback = {
                "score": 65,
                "strengths": ["Answer provided"],
                "improvements": ["Add more detail"],
                "sample_answer": "N/A"
            }
        
        # Save to history
        await db.interview_practice.insert_one({
            "id": str(uuid.uuid4()),
            "user_id": user["id"],
            "question": request.question,
            "answer": request.answer,
            "category": request.category,
            "role_id": request.role_id,
            "score": feedback.get("score", 0),
            "feedback": feedback,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        
        return feedback
        
    except Exception as e:
        logging.error(f"Interview feedback failed: {e}")
        return {
            "score": 60,
            "strengths": ["Answer submitted successfully"],
            "improvements": ["AI feedback temporarily unavailable"],
            "sample_answer": "Please try again later."
        }


@router.get("/history")
async def get_interview_history(user: dict = Depends(get_current_user)):
    """Get user's interview practice history"""
    
    history = await db.interview_practice.find(
        {"user_id": user["id"]},
        {"_id": 0}
    ).sort("created_at", -1).limit(50).to_list(50)
    
    total = len(history)
    avg_score = sum(h.get("score", 0) for h in history) / total if total > 0 else 0
    
    # Calculate streak
    streak = 0
    if history:
        dates = set()
        for h in history:
            try:
                dt = datetime.fromisoformat(h["created_at"].replace('Z', '+00:00'))
                dates.add(dt.date())
            except:
                pass
        
        today = datetime.now(timezone.utc).date()
        while (today - timedelta(days=streak)) in dates:
            streak += 1
    
    return {
        "history": history,
        "stats": {
            "total_practiced": total,
            "avg_score": round(avg_score, 1),
            "streak": streak
        }
    }
