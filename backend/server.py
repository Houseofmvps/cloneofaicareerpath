from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
import anthropic
import PyPDF2
import io
import json
import re
import lxml.html

# Import data from centralized data module
from data.roles import AI_ROLES, GLOBAL_HIRING
from data.courses import COURSE_DATABASE, get_courses_for_role, get_scrimba_courses
from data.pricing import PRICING, FREE_LIMITS

# Email notifications
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logging.warning("Resend not available. Email notifications will be disabled.")

# OCR support for image-based PDFs
try:
    import pytesseract
    from pdf2image import convert_from_bytes
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("OCR libraries not available. Image-based PDFs won't be supported.")

# PDF and DOCX generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
if 'MONGO_URL' not in os.environ:
    raise ValueError("MONGO_URL environment variable is not set")
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Config
if 'JWT_SECRET' not in os.environ:
    logging.warning("JWT_SECRET not set! Using insecure default for development only.")
JWT_SECRET = os.environ.get('JWT_SECRET', 'career-lift-secret-key')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Claude API
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

# Resend Email Config
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')
if RESEND_AVAILABLE and RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
    logging.info("Resend email service configured")
else:
    logging.warning("Resend API key not configured. Email notifications disabled.")

# Adzuna Job API Config
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID', '')
ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY', '')
JOOBLE_API_KEY = os.environ.get('JOOBLE_API_KEY', '')
if ADZUNA_APP_ID and ADZUNA_APP_KEY:
    logging.info("Adzuna Job API configured")
else:
    logging.warning("Adzuna API keys not configured. Using mock job data.")

if JOOBLE_API_KEY:
    logging.info("Jooble Job API configured")
else:
    logging.warning("Jooble API key not configured.")

# HTTP client for external APIs
import httpx

# ============================================
# JOB DISCOVERY SERVICE (Adzuna + RemoteOK)
# ============================================
from services.job_discovery import job_discovery


app = FastAPI(title="CareerLift AI - Career Transition Platform")
api_router = APIRouter(prefix="/api")
security = HTTPBearer()

# Import modular routers
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

# Include modular routers in the API router
api_router.include_router(auth_router)
api_router.include_router(interview_router)
api_router.include_router(payments_router)
api_router.include_router(cover_letter_router)
api_router.include_router(jobs_router)
api_router.include_router(learning_router)
api_router.include_router(cv_router)
api_router.include_router(analysis_router)
api_router.include_router(dashboard_router)
api_router.include_router(roles_router)
api_router.include_router(resume_router)
api_router.include_router(user_router)
api_router.include_router(analytics_router)

# Paddle Config (kept for backward compatibility, config moved to config.py)
PADDLE_API_KEY = os.environ.get('PADDLE_API_KEY', '')
PADDLE_WEBHOOK_SECRET = os.environ.get('PADDLE_WEBHOOK_SECRET', '')

# Pricing and Free Limits imported from data.pricing module

# Pydantic Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    subscription_tier: str
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ResumeData(BaseModel):
    raw_text: str
    current_role: Optional[str] = None
    years_experience: Optional[int] = None
    education: Optional[str] = None
    skills: List[str] = []
    certifications: List[str] = []
    companies: List[str] = []

class BackgroundContext(BaseModel):
    current_role: str
    years_experience: int
    education_level: str
    primary_skills: List[str]
    career_goals: Optional[str] = None
    location: Optional[str] = None  # For location-aware salary data

class AnalysisRequest(BaseModel):
    resume_data: ResumeData
    target_role_id: str
    background_context: BackgroundContext

class CVGenerationRequest(BaseModel):
    resume_text: str
    target_role_id: str
    current_role: Optional[str] = None
    years_experience: Optional[int] = None
    skills: List[str] = []
    target_region: Optional[str] = "us"
    target_country: Optional[str] = "United States"
    region_name: Optional[str] = "United States"
    tier: Optional[int] = 1
    experience_level: Optional[str] = "mid"
    experience_years: Optional[str] = "3-10"
    recommended_length: Optional[str] = "1-2 pages"

class LearningPathRequest(BaseModel):
    current_role: str
    years_experience: int
    current_skills: List[str]
    target_role_id: str
    location: Optional[str] = None

class UsageResponse(BaseModel):
    cv_generations_used: int
    cv_generations_limit: int
    learning_paths_used: int
    learning_paths_limit: int
    analyses_used: int
    analyses_limit: int
    cv_credits: int
    learning_path_credits: int

# Course Database imported from data.courses module

# Helper Functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF using multiple methods:
    1. PyPDF2 for text-based PDFs
    2. OCR (pytesseract) for image-based/scanned PDFs
    """
    text = ""
    
    # Method 1: Try PyPDF2 first (fast, works for text-based PDFs)
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        
        # If we got meaningful text (more than 100 chars), return it
        if len(text.strip()) > 100:
            logging.info(f"PyPDF2 extracted {len(text)} chars successfully")
            return text.strip()
    except Exception as e:
        logging.warning(f"PyPDF2 extraction failed: {e}")
    
    # Method 2: Try OCR for image-based PDFs
    if OCR_AVAILABLE:
        try:
            logging.info("Attempting OCR extraction for image-based PDF...")
            images = convert_from_bytes(file_content)
            ocr_text = ""
            for i, img in enumerate(images):
                page_text = pytesseract.image_to_string(img)
                if page_text:
                    ocr_text += page_text + "\n"
            
            if len(ocr_text.strip()) > 50:
                logging.info(f"OCR extracted {len(ocr_text)} chars successfully")
                return ocr_text.strip()
        except Exception as e:
            logging.error(f"OCR extraction failed: {e}")
    else:
        logging.warning("OCR not available - cannot process image-based PDFs")
    
    # Return whatever we have (might be empty)
    return text.strip()

def parse_resume_text(text: str) -> Dict[str, Any]:
    """Basic resume parsing - extracts key information"""
    result = {
        "raw_text": text,
        "current_role": None,
        "years_experience": None,
        "education": None,
        "skills": [],
        "certifications": [],
        "companies": []
    }
    
    # Common skill keywords
    skill_keywords = [
        "python", "javascript", "java", "c++", "sql", "react", "node", "aws", "azure",
        "docker", "kubernetes", "machine learning", "deep learning", "tensorflow", "pytorch",
        "data analysis", "data science", "product management", "agile", "scrum", "git",
        "api", "rest", "graphql", "mongodb", "postgresql", "redis", "linux", "html", "css",
        "typescript", "go", "rust", "scala", "r", "matlab", "tableau", "power bi",
        "nlp", "computer vision", "pandas", "numpy", "scikit-learn", "keras", "spark",
        "hadoop", "airflow", "mlflow", "langchain", "openai", "llm", "rag", "vector database"
    ]
    
    text_lower = text.lower()
    found_skills = [skill for skill in skill_keywords if skill in text_lower]
    result["skills"] = list(set(found_skills))
    
    # Extract years of experience
    exp_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience[:\s]*(\d+)\+?\s*years?',
    ]
    for pattern in exp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            result["years_experience"] = int(match.group(1))
            break
    
    # Extract education
    edu_keywords = ["bachelor", "master", "phd", "mba", "b.s.", "m.s.", "b.tech", "m.tech"]
    for edu in edu_keywords:
        if edu in text_lower:
            result["education"] = edu.upper()
            break
    
    return result

def get_claude_system_prompt():
    return """You are a world-class AI career advisor specializing in helping professionals transition into AI roles.

EXPERTISE:
- 20 AI Career paths: ML Engineer, Prompt Engineer, AI PM, Data Scientist, MLOps, AI Safety, Solutions Architect, Gen AI Developer, Research Scientist, Computer Vision Engineer, NLP Engineer, RL Engineer, ML Infrastructure, AI Product Designer, AI Consultant, AI Ethics Specialist, Vibe Coder, Content Creator, Autonomous Agent Developer, AI Business Analyst
- In-demand skills: Python, ML frameworks (TensorFlow/PyTorch), LLMs, RAG, fine-tuning, APIs, cloud platforms, no-code tools (Cursor, Emergent, Make.com)
- Industry knowledge: Salary ranges, company hiring patterns, skill requirements evolution
- Realistic timelines: IT→AI (3-4 months), PM→AI PM (2-3 months), Career changer→AI (6-9 months)
- ATS optimization: Keywords, formatting, technical language placement
- CV writing: Natural authentic voice + ATS keyword optimization

YOUR ANALYSIS TASK:
Analyze the resume and desired AI role. Return ONLY valid JSON (no markdown, no code blocks) with these sections:

ROLE-SPECIFIC EXPERTISE (ALL 20 ROLES):

1. AI/ML ENGINEER - From Software Engineer: EXCELLENT (2-3 months), Salary: $150k-$250k (US)
2. PROMPT ENGINEER - From PM/Content: EXCELLENT (2-3 months), Salary: $100k-$180k (US)
3. AI PRODUCT MANAGER - From PM: EXCELLENT (2-3 months), Salary: $160k-$280k (US)
4. DATA SCIENTIST - From Analyst: EXCELLENT (3-4 months), Salary: $120k-$200k (US)
5. ML OPERATIONS ENGINEER - From DevOps: EXCELLENT (1-2 months), Salary: $140k-$220k (US)
6. AI SAFETY RESEARCHER - From ML Engineer: GOOD (6-8 months), Salary: $150k-$250k (US)
7. AI SOLUTIONS ARCHITECT - From Solutions Architect: EXCELLENT (2-3 months), Salary: $170k-$280k (US)
8. GENERATIVE AI DEVELOPER - From Full-stack: EXCELLENT (2-3 months), Salary: $130k-$220k (US)
9. AI RESEARCH SCIENTIST - From Academic/ML: GOOD (6-12 months), Salary: $160k-$300k (US)
10. COMPUTER VISION ENGINEER - From ML Engineer: GOOD (4-6 months), Salary: $140k-$240k (US)
11. NLP ENGINEER - From ML/Linguistics: GOOD (4-6 months), Salary: $140k-$240k (US)
12. REINFORCEMENT LEARNING ENGINEER - From ML/Game Dev: CHALLENGING (6-9 months), Salary: $150k-$260k (US)
13. AI/ML INFRASTRUCTURE ENGINEER - From DevOps/Backend: GOOD (3-5 months), Salary: $160k-$260k (US)
14. AI PRODUCT DESIGNER - From Product Designer: GOOD (3-5 months), Salary: $120k-$200k (US)
15. AI CONSULTANT - From Management Consulting: EXCELLENT (2-4 months), Salary: $150k-$300k (US)
16. AI ETHICS SPECIALIST - From Policy/Philosophy: GOOD (4-6 months), Salary: $130k-$220k (US)
17. VIBE CODER / AI AUTOMATION BUILDER - From Any tech: EXCELLENT (2-4 weeks!), Salary: $80k-$150k (US)
18. AI CONTENT CREATOR - From Writing/Marketing: EXCELLENT (1-2 months), Salary: $40k-$150k (US)
19. AUTONOMOUS AGENT DEVELOPER - From Full-stack: GOOD (3-6 months), Salary: $140k-$250k (US)
20. AI BUSINESS ANALYST - From Business Analyst: EXCELLENT (2-3 months), Salary: $100k-$180k (US)

CRITICAL RULES FOR NATURAL AUTHENTIC CV:
- Sounds like a real person, not a robot
- Uses achievement stories with personality
- Conversational yet professional
- Shows genuine impact and why it matters
- Uses language like "I led", "I built", "I improved"
- Includes context: "Why did this matter? Who did it help?"
- Example GOOD: "Led a small team that redesigned our API, cutting response times by 40%. Customers noticed the speed improvement immediately, and support tickets dropped by 25%."
- Example BAD: "Led API optimization initiative. Implemented caching layer. Achieved 40% latency reduction."

CRITICAL RULES FOR ATS OPTIMIZED CV (90+ SCORE):
- Maximum keyword density (AI, ML, Python, TensorFlow, PyTorch, LLM, RAG, etc.)
- Scannable bullet format with metrics
- Skills concentrated at top
- Every bullet: Action verb + Achievement + Metric
- Example: "Led ML pipeline architecture using Python and TensorFlow. Deployed 3 production models. Achieved 98% accuracy. Reduced training time by 60%."

RESPOND WITH THIS EXACT JSON STRUCTURE:
{
    "career_fit": {
        "rating": "EXCELLENT|GOOD|FEASIBLE|CHALLENGING",
        "score": 85,
        "explanation": "150-200 word detailed explanation of fit",
        "timeline_weeks": 12,
        "salary_if_hired_today": "$X - $Y"
    },
    "ats_score": {
        "score": 75,
        "explanation": "Why this score - what's missing",
        "hurts_score": ["specific issue 1", "specific issue 2"],
        "helps_score": ["strength 1", "strength 2"],
        "quick_fixes": ["specific fix 1", "specific fix 2", "specific fix 3"]
    },
    "transferable_skills": [
        {
            "skill": "Python",
            "rating": "VERY_HIGH|HIGH|MEDIUM|LOW",
            "explanation": "50-100 words on how this skill applies to target AI role with specific examples"
        }
    ],
    "skill_gaps": [
        {
            "skill": "MLOps",
            "priority": "CRITICAL|HIGH|MEDIUM",
            "months_to_learn": 2,
            "difficulty": "EASY|MODERATE|HARD",
            "resources": ["Specific course/book 1", "Resource 2"]
        }
    ],
    "learning_path": {
        "total_weeks": 16,
        "hours_per_week": 15,
        "weeks": [
            {
                "week": 1,
                "focus": "Weeks 1-4: Foundation topic",
                "hours": 60,
                "courses": ["Specific course name"],
                "milestones": ["Concrete milestone"],
                "skills_developed": ["skill1", "skill2"]
            },
            {
                "week": 5,
                "focus": "Weeks 5-8: Core skills topic",
                "hours": 60,
                "courses": ["Specific course"],
                "milestones": ["Concrete milestone"],
                "skills_developed": ["skill3"]
            },
            {
                "week": 9,
                "focus": "Weeks 9-12: Advanced topic",
                "hours": 60,
                "courses": ["Advanced course"],
                "milestones": ["Build project X"],
                "skills_developed": ["skill4"]
            },
            {
                "week": 13,
                "focus": "Weeks 13-16: Portfolio & job prep",
                "hours": 60,
                "courses": ["Interview prep"],
                "milestones": ["Complete portfolio"],
                "skills_developed": ["skill5"]
            }
        ]
    },
    "next_steps": {
        "this_week": ["5 specific actionable items"],
        "this_month": ["2-3 concrete milestones"],
        "next_3_months": ["major deliverables"]
    },
    "cv_natural": {
        "summary": "Natural, conversational 3-4 sentence professional summary that sounds human",
        "experience_bullets": ["Achievement story bullet 1 with context and impact", "Story bullet 2", "Story bullet 3"],
        "skills_section": "Naturally formatted skills section"
    },
    "cv_ats_optimized": {
        "summary": "Keyword-rich, ATS-optimized summary with target role keywords",
        "experience_bullets": ["Action + Achievement + Metric bullet 1", "Keyword-dense bullet 2", "Technical bullet 3"],
        "skills_section": "ATS-friendly keyword-optimized skills section"
    },
    "alternative_roles": [
        {
            "role_id": "role_id_from_20",
            "role_name": "Role Name",
            "fit_score": 90,
            "timeline_weeks": 8,
            "reason": "Why this role might be a better fit"
        }
    ],
    "warning_flags": [
        {
            "obstacle": "Specific challenge they'll face",
            "how_to_overcome": "Actionable advice",
            "resources": ["Helpful resource"]
        }
    ]
}

Be specific, realistic, and actionable. Use real course names, real timelines, real salary data."""

async def analyze_with_claude(resume_data: Dict, target_role: Dict, background: Dict) -> Dict:
    """Call Claude API for career analysis with global salary data"""
    # Mock fallback if API not configured
    if not claude_client:
        logging.warning("Claude API not configured. Using mock analysis data.")
        return {
            "role_readiness_score": 65,
            "years_gap": max(0, 3 - resume_data.get('years_experience', 0)),
            "skills_match_score": 70,
            "critical_skills_gap": ["System Design", "Advanced Algorithms", "Cloud Architecture"],
            "strengths": ["Strong programming foundations", "Eagerness to learn", "Relevant background"],
            "weaknesses": ["Lack of production experience", "Limited system design exposure"],
            "learning_time_weeks": 12,
            "salary_potential": target_role.get('salary', {}).get('us', '$100k - $150k'),
            "market_demand_rating": "High",
            "career_strategy": [
                "Focus on building 2-3 end-to-end projects",
                "Contribute to open source repositories",
                "Network with professionals in the field"
            ],
            "recommended_focus_areas": [
                "System Design patterns",
                "Cloud infrastructure (AWS/GCP)",
                "CI/CD pipelines"
            ]
        }
    
    # Get location-specific salary data
    location = background.get('location', 'us').lower()
    salary_data = target_role.get('salary', {})
    location_salary = salary_data.get(location, salary_data.get('us', target_role.get('salary_range', 'N/A')))
    
    # Get companies and courses for the role
    companies = target_role.get('companies', [])
    courses = target_role.get('courses', [])
    from_background = target_role.get('from_background', {})
    
    user_message = f"""
Analyze this candidate for transition to: {target_role['name']}

RESUME DATA:
- Raw Text: {resume_data.get('raw_text', 'Not provided')[:3000]}
- Current Role: {resume_data.get('current_role', 'Not specified')}
- Years Experience: {resume_data.get('years_experience', 'Not specified')}
- Education: {resume_data.get('education', 'Not specified')}
- Detected Skills: {', '.join(resume_data.get('skills', []))}

BACKGROUND CONTEXT:
- Current Role: {background.get('current_role', 'Not specified')}
- Years Experience: {background.get('years_experience', 'Not specified')}
- Education Level: {background.get('education_level', 'Not specified')}
- Primary Skills: {', '.join(background.get('primary_skills', []))}
- Career Goals: {background.get('career_goals', 'Not specified')}
- Location: {background.get('location', 'US')}

TARGET ROLE DETAILS:
- Role: {target_role['name']}
- Description: {target_role.get('description', 'N/A')}
- Required Skills: {', '.join(target_role.get('top_skills', ['General Tech Skills']))}
- Location-specific Salary: {location_salary}
- Global Salary Ranges: US: {salary_data.get('us', 'N/A')}, India: {salary_data.get('india', 'N/A')}, Europe: {salary_data.get('europe', 'N/A')}
- Top Companies Hiring: {', '.join(companies[:5])}
- Recommended Courses: {', '.join(courses[:3])}
- Transition Estimates: {json.dumps(from_background)}

Provide a comprehensive analysis in the exact JSON format specified. Use the global salary data and company information. Be specific, actionable, and realistic.
"""
    
    try:
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=6000,
            system=get_claude_system_prompt(),
            messages=[{"role": "user", "content": user_message}]
        )
        
        response_text = response.content[0].text
        # Clean up response - remove any markdown code blocks
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
    except Exception as e:
        logging.error(f"Claude API error: {e}")
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

# Auth routes moved to routes/auth.py

# Roles Routes moved to routes/roles.py

# Resume Routes moved to routes/resume.py

# Analysis, Usage, and Dashboard routes moved to routes/analysis.py and routes/dashboard.py

# Payment routes moved to routes/payments.py

# Hiring patterns moved to routes/roles.py

# CV routes moved to routes/cv.py

# ============================================
# STANDALONE LEARNING PATH GENERATOR
# ============================================


def get_courses_for_role(role_id: str, difficulty: str = None) -> list:
    """Get relevant courses for a specific role"""
    courses = []
    for course_id, course in COURSE_DATABASE.items():
        if "all" in course["for_roles"] or role_id in course["for_roles"]:
            if difficulty is None or course["difficulty"].lower().startswith(difficulty.lower()):
                courses.append({
                    "course_id": course_id,
                    **course
                })
    # Sort: Recommended first, then free, then paid
    courses.sort(key=lambda x: (
        0 if x.get("recommended") else 1,
        0 if x.get("cost", "").lower() == "free" else 1,
        -x.get("rating", 0)
    ))
    return courses

@api_router.get("/courses")
async def get_courses_api(
    role_id: Optional[str] = Query(None, description="Filter by role ID"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    platform: Optional[str] = Query(None, description="Filter by platform (e.g., Scrimba)"),
    free_only: bool = Query(False, description="Show only free courses")
):
    """Get courses from the database with optional filters"""
    courses = []
    
    for course_id, course in COURSE_DATABASE.items():
        # Role filter
        if role_id and role_id not in course.get("for_roles", []) and "all" not in course.get("for_roles", []):
            continue
        
        # Difficulty filter
        if difficulty and not course.get("difficulty", "").lower().startswith(difficulty.lower()):
            continue
        
        # Platform filter
        if platform and course.get("platform", "").lower() != platform.lower():
            continue
        
        # Free only filter
        if free_only and course.get("cost", "").lower() != "free":
            continue
        
        courses.append({
            "course_id": course_id,
            **course
        })
    
    # Sort: Recommended first, then free, then by rating
    courses.sort(key=lambda x: (
        0 if x.get("recommended") else 1,
        0 if x.get("cost", "").lower() == "free" else 1,
        -x.get("rating", 0)
    ))
    
    # Get Scrimba courses count for stats
    scrimba_count = len([c for c in courses if c.get("platform") == "Scrimba"])
    free_count = len([c for c in courses if c.get("cost", "").lower() == "free"])
    
    return {
        "courses": courses,
        "total": len(courses),
        "scrimba_count": scrimba_count,
        "free_count": free_count
    }

@api_router.get("/courses/scrimba")
async def get_scrimba_courses():
    """Get all Scrimba courses with affiliate links"""
    courses = []
    for course_id, course in COURSE_DATABASE.items():
        if course.get("platform") == "Scrimba":
            courses.append({
                "course_id": course_id,
                **course
            })
    
    # Sort: Free first, then by rating
    courses.sort(key=lambda x: (
        0 if x.get("cost", "").lower() == "free" else 1,
        -x.get("rating", 0)
    ))
    
    free_courses = [c for c in courses if c.get("cost", "").lower() == "free"]
    pro_courses = [c for c in courses if c.get("cost", "").lower() != "free"]
    
    return {
        "courses": courses,
        "total": len(courses),
        "free_courses": free_courses,
        "pro_courses": pro_courses,
        "free_count": len(free_courses),
        "pro_count": len(pro_courses)
    }

def get_learning_path_prompt():
    return """You are an expert AI career advisor creating personalized 16-week learning paths.

IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON object.
Keep course descriptions short (under 100 characters).

CRITICAL: INCLUDE SCRIMBA COURSES as "⭐ Recommended" options alongside free courses.
Scrimba offers hands-on, interactive AI courses that accelerate learning.

ROLE-SPECIFIC GUIDANCE:

For "Machine Learning Engineer" role:
- Focus on classical ML algorithms (regression, classification, clustering, ensemble methods)
- Deep learning fundamentals (neural networks, CNNs, RNNs)
- Model training, evaluation, and optimization
- Feature engineering and data preprocessing
- MLOps: model deployment, monitoring, versioning
- Math foundations: linear algebra, calculus, statistics
- Tools: Scikit-learn, PyTorch/TensorFlow, MLflow, Kubeflow
- INCLUDE: Scrimba Open-source AI Models, Scrimba Intro to Mistral AI

For "AI Engineer" role:
- Focus on LLM APIs (OpenAI, Anthropic, Google)
- Building AI-powered applications and integrations
- RAG (Retrieval Augmented Generation) architectures
- Vector databases (Pinecone, Weaviate, Chroma)
- AI Agents and autonomous systems
- Prompt engineering and optimization
- Full-stack integration of AI features
- Tools: LangChain, LlamaIndex, OpenAI SDK, Vercel AI SDK
- MUST INCLUDE: Scrimba AI Engineer Path as primary recommendation

Return this exact structure:
{
    "total_weeks": 16,
    "hours_per_week": 15,
    "total_hours": 240,
    "difficulty_progression": "Beginner → Intermediate → Advanced → Projects",
    "weeks": [
        {
            "week": 1,
            "phase": "Foundation",
            "focus": "Topic for this week",
            "hours": 15,
            "difficulty": "Beginner",
            "courses": [
                {
                    "name": "Course Name",
                    "url": "https://example.com/course",
                    "platform": "Platform Name",
                    "duration_hours": 10,
                    "cost": "Free",
                    "why_recommended": "Brief reason",
                    "badge": "🆓 Free or ⭐ Recommended"
                }
            ],
            "project": {
                "name": "Project Name",
                "description": "What to build"
            },
            "milestone": "What you'll achieve"
        }
    ],
    "career_readiness_checklist": ["Item 1", "Item 2", "Item 3"]
}

USE THESE VERIFIED COURSE URLs:

SCRIMBA COURSES (INCLUDE AS ⭐ RECOMMENDED):
- AI Engineer Path: https://scrimba.com/the-ai-engineer-path-c02v?via=u436b310 (11.2 hrs, Pro - BEST for AI Engineers)
- Intro to AI Engineering: https://scrimba.com/learn/introtoaiengineering?via=u436b310 (1.5 hrs, FREE)
- Learn AI Agents: https://scrimba.com/learn/aiagents?via=u436b310 (2 hrs, Pro)
- Learn RAG: https://scrimba.com/learn/rag?via=u436b310 (1.5 hrs, Pro)
- Learn Context Engineering: https://scrimba.com/learn/contextengineering?via=u436b310 (1 hr, Pro)
- Intro to Claude AI: https://scrimba.com/learn/introtoclaudeai?via=u436b310 (48 min, FREE)
- Intro to Mistral AI: https://scrimba.com/learn/introtomistral?via=u436b310 (1.4 hrs, FREE)
- Learn LangChain.js: https://scrimba.com/learn/langchain?via=u436b310 (1.5 hrs, FREE)
- Open-source AI Models: https://scrimba.com/learn/opensourceai?via=u436b310 (38 min, Pro)
- Build Support Agent: https://scrimba.com/learn/buildsupportagent?via=u436b310 (2 hrs, Pro)
- Deploy AI Apps: https://scrimba.com/learn/deployaiapps?via=u436b310 (50 min, FREE)
- Prompt Engineering: https://scrimba.com/learn/promptengineering?via=u436b310 (3.1 hrs, Pro)

FOR ML ENGINEER:
- Python: https://www.coursera.org/specializations/python
- Andrew Ng ML: https://www.coursera.org/specializations/machine-learning-introduction
- Stanford CS229: https://cs229.stanford.edu/
- Fast.ai: https://course.fast.ai/
- Deep Learning: https://www.coursera.org/specializations/deep-learning
- Hands-On ML: https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/
- MLOps: https://www.coursera.org/specializations/mlops-fundamentals
- Kaggle: https://www.kaggle.com/learn
- StatQuest: https://www.youtube.com/@statquest

FOR AI ENGINEER:
- LangChain: https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/
- LLM Foundations: https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/
- Building AI Apps: https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/
- RAG: https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/
- LlamaIndex: https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/
- Vector DBs: https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/
- AI Agents: https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
- OpenAI Cookbook: https://cookbook.openai.com/
- Hugging Face: https://huggingface.co/learn/nlp-course
"""

def generate_fallback_learning_path(target_role: str, skills: List[str]) -> dict:
    """Generate a complete fallback learning path when AI generation fails"""
    
    target_lower = target_role.lower()
    
    # ML Engineer specific courses - WITH SCRIMBA
    ml_engineer_courses = [
        {"name": "Python for Everybody", "url": "https://www.coursera.org/specializations/python", "platform": "Coursera", "duration_hours": 10, "cost": "Free", "why_recommended": "Essential foundation", "badge": "🆓 Free"},
        {"name": "Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "platform": "Coursera", "duration_hours": 15, "cost": "$49/mo", "why_recommended": "Industry standard ML course by Andrew Ng", "badge": "🎓 Essential"},
        {"name": "Intro to Mistral AI", "url": "https://scrimba.com/learn/introtomistral?via=u436b310", "platform": "Scrimba", "duration_hours": 1.4, "cost": "Free", "why_recommended": "Learn open-source LLMs with RAG and function calling", "badge": "🆓 Free"},
        {"name": "Hands-On ML with Scikit-Learn", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "platform": "O'Reilly", "duration_hours": 20, "cost": "$39/mo", "why_recommended": "Practical ML implementation", "badge": "📚 Book"},
        {"name": "Fast.ai Practical Deep Learning", "url": "https://course.fast.ai/", "platform": "Fast.ai", "duration_hours": 12, "cost": "Free", "why_recommended": "Hands-on deep learning", "badge": "🆓 Free"},
        {"name": "Open-source AI Models", "url": "https://scrimba.com/learn/opensourceai?via=u436b310", "platform": "Scrimba", "duration_hours": 0.6, "cost": "Pro Subscription", "why_recommended": "Hugging Face and Ollama integration", "badge": "⭐ Recommended"},
        {"name": "Deep Learning Specialization", "url": "https://www.coursera.org/specializations/deep-learning", "platform": "Coursera", "duration_hours": 15, "cost": "$49/mo", "why_recommended": "Comprehensive DL coverage", "badge": "🎓 Essential"},
        {"name": "MLOps Fundamentals", "url": "https://www.coursera.org/specializations/mlops-fundamentals", "platform": "Coursera", "duration_hours": 12, "cost": "$49/mo", "why_recommended": "Production ML systems", "badge": "🎓 Essential"},
        {"name": "Deploy AI Apps with Cloudflare", "url": "https://scrimba.com/learn/deployaiapps?via=u436b310", "platform": "Scrimba", "duration_hours": 0.8, "cost": "Free", "why_recommended": "Edge deployment for AI", "badge": "🆓 Free"},
        {"name": "Kaggle Learn", "url": "https://www.kaggle.com/learn", "platform": "Kaggle", "duration_hours": 8, "cost": "Free", "why_recommended": "Practical ML competitions", "badge": "🆓 Free"},
        {"name": "StatQuest ML Playlist", "url": "https://www.youtube.com/@statquest", "platform": "YouTube", "duration_hours": 10, "cost": "Free", "why_recommended": "Math intuition for ML", "badge": "🆓 Free"},
    ]
    
    # AI Engineer specific courses - WITH SCRIMBA
    ai_engineer_courses = [
        {"name": "Python for Everybody", "url": "https://www.coursera.org/specializations/python", "platform": "Coursera", "duration_hours": 10, "cost": "Free", "why_recommended": "Essential foundation", "badge": "🆓 Free"},
        {"name": "The AI Engineer Path", "url": "https://scrimba.com/the-ai-engineer-path-c02v?via=u436b310", "platform": "Scrimba", "duration_hours": 11.2, "cost": "Pro Subscription", "why_recommended": "Comprehensive AI engineering curriculum with hands-on projects", "badge": "⭐ Recommended"},
        {"name": "Intro to AI Engineering", "url": "https://scrimba.com/learn/introtoaiengineering?via=u436b310", "platform": "Scrimba", "duration_hours": 1.5, "cost": "Free", "why_recommended": "Great free intro to LLM app development", "badge": "🆓 Free"},
        {"name": "ChatGPT Prompt Engineering", "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/", "platform": "DeepLearning.AI", "duration_hours": 2, "cost": "Free", "why_recommended": "Master prompt engineering", "badge": "🆓 Free"},
        {"name": "Learn LangChain.js", "url": "https://scrimba.com/learn/langchain?via=u436b310", "platform": "Scrimba", "duration_hours": 1.5, "cost": "Free", "why_recommended": "Hands-on LangChain with interactive coding", "badge": "🆓 Free"},
        {"name": "Learn AI Agents", "url": "https://scrimba.com/learn/aiagents?via=u436b310", "platform": "Scrimba", "duration_hours": 2, "cost": "Pro Subscription", "why_recommended": "Build autonomous AI agents", "badge": "⭐ Recommended"},
        {"name": "Learn RAG", "url": "https://scrimba.com/learn/rag?via=u436b310", "platform": "Scrimba", "duration_hours": 1.5, "cost": "Pro Subscription", "why_recommended": "Master RAG architecture", "badge": "⭐ Recommended"},
        {"name": "Intro to Claude AI", "url": "https://scrimba.com/learn/introtoclaudeai?via=u436b310", "platform": "Scrimba", "duration_hours": 0.8, "cost": "Free", "why_recommended": "Learn Anthropic's Claude API", "badge": "🆓 Free"},
        {"name": "Deploy AI Apps", "url": "https://scrimba.com/learn/deployaiapps?via=u436b310", "platform": "Scrimba", "duration_hours": 0.8, "cost": "Free", "why_recommended": "Deploy to production", "badge": "🆓 Free"},
        {"name": "Build Support Agent", "url": "https://scrimba.com/learn/buildsupportagent?via=u436b310", "platform": "Scrimba", "duration_hours": 2, "cost": "Pro Subscription", "why_recommended": "Real-world agent project", "badge": "⭐ Recommended"},
    ]
    
    # Choose courses based on role
    if "ml engineer" in target_lower or "machine learning" in target_lower:
        base_courses = ml_engineer_courses
        focus_areas = [
            "Python & ML Foundations", "Statistical Learning Basics", "Supervised Learning Algorithms",
            "Unsupervised Learning", "Neural Network Fundamentals", "Deep Learning with PyTorch",
            "CNN & Computer Vision", "RNN & Sequence Models", "Feature Engineering",
            "Model Evaluation & Tuning", "MLOps & Deployment", "ML System Design",
            "Advanced Topics & Research", "Portfolio Projects", "Interview Prep", "Job Search"
        ]
        checklist = [
            "Build 3-5 ML portfolio projects with GitHub",
            "Complete 50+ Kaggle competitions or notebooks",
            "Implement classic ML algorithms from scratch",
            "Deploy at least one model to production",
            "Practice ML system design interviews",
            "Contribute to open source ML projects"
        ]
    elif "ai engineer" in target_lower:
        base_courses = ai_engineer_courses
        focus_areas = [
            "Python & API Fundamentals", "LLM Basics & Prompt Engineering", "OpenAI API Deep Dive",
            "LangChain Fundamentals", "Building Chat Applications", "RAG Architecture Basics",
            "Vector Databases & Embeddings", "Advanced RAG Techniques", "AI Agents Introduction",
            "Multi-Agent Systems", "Production AI Systems", "LLM Evaluation & Testing",
            "Advanced AI Patterns", "Portfolio Projects", "Interview Prep", "Job Search"
        ]
        checklist = [
            "Build 3-5 AI applications with LLM integration",
            "Implement RAG system with vector database",
            "Create an AI agent that completes tasks",
            "Deploy AI app to production (Vercel, Railway)",
            "Contribute to LangChain or similar projects",
            "Master at least 2 LLM providers (OpenAI, Anthropic)"
        ]
    else:
        base_courses = ml_engineer_courses
        focus_areas = [
            "Python Foundations", "ML Basics", "Core Skills Development",
            "Intermediate Concepts", "Advanced Topics", "Specialization",
            "Deep Dive", "Projects Phase 1", "Projects Phase 2",
            "Industry Applications", "Production Systems", "Optimization",
            "Advanced Applications", "Portfolio Building", "Interview Prep", "Job Search"
        ]
        checklist = [
            "Build 3-5 portfolio projects",
            "Update LinkedIn with AI/ML keywords",
            "Practice 50+ LeetCode problems",
            "Contribute to open source AI projects",
            "Network with AI professionals",
            "Prepare behavioral interview stories"
        ]
    
    phases = ["Foundation", "Foundation", "Core Skills", "Core Skills", "Intermediate", "Intermediate", 
              "Advanced", "Advanced", "Specialization", "Specialization", "Projects", "Projects",
              "Interview Prep", "Interview Prep", "Job Search", "Job Search"]
    
    difficulties = ["Beginner", "Beginner", "Beginner", "Intermediate", "Intermediate", "Intermediate",
                   "Intermediate", "Advanced", "Advanced", "Advanced", "Advanced", "Advanced",
                   "Advanced", "Advanced", "Advanced", "Advanced"]
    
    weeks = []
    for i in range(16):
        week_num = i + 1
        course_idx = i % len(base_courses)
        
        weeks.append({
            "week": week_num,
            "phase": phases[i],
            "focus": focus_areas[i],
            "hours": 15,
            "difficulty": difficulties[i],
            "courses": [base_courses[course_idx], base_courses[(course_idx + 1) % len(base_courses)]],
            "project": {
                "name": f"Week {week_num} Project",
                "description": f"Apply {focus_areas[i]} concepts to build a practical project"
            },
            "milestone": f"Complete {phases[i]} phase: {focus_areas[i]}"
        })
    
    return {
        "total_weeks": 16,
        "hours_per_week": 15,
        "total_hours": 240,
        "difficulty_progression": "Beginner → Intermediate → Advanced → Projects",
        "weeks": weeks,
        "career_readiness_checklist": checklist,
        "note": "This is a recommended path - courses may vary based on availability"
    }

# Learning path routes moved to routes/learning.py

# ============================================
# ANALYTICS & TRACKING - Moved to routes/analytics.py
# ============================================

# User Profile - Moved to routes/user.py

# Cover letter routes moved to routes/cover_letter.py

# Jobs/Auto-Apply routes moved to routes/jobs.py

# Health check
@api_router.get("/")
async def root():
    return {"message": "CareerLift AI API", "status": "healthy"}

@api_router.get("/health")
async def health():
    return {"status": "healthy", "claude_configured": bool(ANTHROPIC_API_KEY)}

from fastapi.staticfiles import StaticFiles

# Include router
app.include_router(api_router)

# Serve static files from frontend build if they exist (Production)
frontend_build_dir = Path(__file__).parent / "frontend/build"
if frontend_build_dir.exists():
    # Serve static assets
    app.mount("/static", StaticFiles(directory=start_dir / "static"), name="static")
    
    # Serve main index.html for React router
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Allow API calls to pass through
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
            
        file_path = frontend_build_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
            
        return FileResponse(frontend_build_dir / "index.html")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Download-Success", "X-Remaining-Downloads", "X-Usage-Message"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
