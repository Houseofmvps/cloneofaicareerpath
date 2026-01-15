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
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Config
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

class JobDiscoveryService:
    """Service to discover jobs from multiple APIs"""
    
    # API Endpoints
    ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"
    REMOTEOK_URL = "https://remoteok.com/api"
    REMOTIVE_URL = "https://remotive.com/api/remote-jobs"
    ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"
    JOBICY_URL = "https://jobicy.com/api/v2/remote-jobs"
    JOOBLE_URL = "https://jooble.org/api"  # POST with API key in URL
    
    # AI-specific job title keywords - ONLY show jobs matching these
    AI_ROLE_KEYWORDS = [
        # Core AI/ML titles
        "ai ", "ai/", "a]i", " ai", "artificial intelligence", 
        "machine learning", "ml ", "ml/", " ml", "/ml",
        "deep learning", "data scientist", "data science",
        "nlp", "natural language", "computer vision",
        "mlops", "ml ops", "llm", "large language model",
        "prompt engineer", "generative ai", "genai", "gen ai",
        "neural network", "reinforcement learning",
        "ai research", "ai engineer", "ml engineer", "ml platform",
        "ai product", "ai safety", "predictive", "recommendation",
        "autonomous", "robotics", "cv engineer",
        # ML frameworks (strong signal)
        "tensorflow", "pytorch", "keras", "scikit",
        # AI companies (strong signal for any role there)
        "openai", "anthropic", "deepmind", "stability ai", "hugging face",
        "midjourney", "cohere", "ai21"
    ]
    
    # Exclude these roles even if they match keywords
    NON_AI_ROLES = [
        "video editor", "content marketing", "paid search", "sponsorship",
        "executive assistant", "virtual assistant", "customer support",
        "sales representative", "recruiter", "hr ", "human resources", "accountant",
        "bookkeeper", "admin", "receptionist", "site reliability",
        "sre", "devops", "web analyst", "frontend engineer", "backend engineer",
        "full stack", "fullstack", "product engineer", "software engineer",
        "business systems analyst", "systems analyst", "business analyst",
        "cloud engineer", "controls analyst", "policy analyst", "pilots"
    ]
    
    # These override NON_AI_ROLES if present
    STRONG_AI_SIGNALS = [
        "ai ", "ai/", " ai", "machine learning", "ml ", "ml/", "/ml",
        "data scientist", "deep learning", "nlp", "computer vision",
        "llm", "generative ai", "neural", "pytorch", "tensorflow"
    ]
    
    # Company logo emojis mapping
    COMPANY_LOGOS = {
        "google": "🔍", "meta": "📱", "amazon": "📦", "microsoft": "💻",
        "apple": "🍎", "netflix": "🎬", "stripe": "💳", "openai": "🤖",
        "anthropic": "🧠", "notion": "📝", "slack": "💬", "spotify": "🎵",
        "airbnb": "🏠", "uber": "🚗", "salesforce": "☁️", "adobe": "🎨",
        "nvidia": "🎮", "tesla": "⚡", "default": "🏢"
    }
    
    # Easy Apply URL patterns (jobs with quick application)
    EASY_APPLY_PATTERNS = [
        "linkedin.com/jobs", "indeed.com/apply", "lever.co", "greenhouse.io",
        "workable.com", "bamboohr.com", "ashbyhq.com", "jobs.smartrecruiters",
        "myworkdayjobs.com", "icims.com", "apply.workable.com"
    ]
    
    @classmethod
    def is_ai_role(cls, job_title: str, description: str = "", tags: list = None) -> bool:
        """Check if job is AI/ML related - strict filtering"""
        title_lower = job_title.lower()
        
        # Check for strong AI signals in title first (these always pass)
        if any(signal in title_lower for signal in cls.STRONG_AI_SIGNALS):
            return True
        
        # Exclude generic tech roles without AI in title
        if any(excl in title_lower for excl in cls.NON_AI_ROLES):
            return False
        
        # Check title for AI keywords
        if any(keyword in title_lower for keyword in cls.AI_ROLE_KEYWORDS):
            return True
        
        # Check tags (for RemoteOK) - require strong AI signal
        if tags:
            tags_str = " ".join(tags).lower()
            if any(signal in tags_str for signal in cls.STRONG_AI_SIGNALS):
                return True
        
        # Check description for strong AI signals
        if description:
            desc_lower = description.lower()
            if any(signal in desc_lower for signal in cls.STRONG_AI_SIGNALS):
                # Also check title isn't completely unrelated
                tech_terms = ["engineer", "developer", "scientist", "analyst", "researcher"]
                if any(term in title_lower for term in tech_terms):
                    return True
        
        return False
    
    @classmethod
    def get_company_logo(cls, company_name: str) -> str:
        """Get emoji logo for company"""
        company_lower = company_name.lower()
        for key, emoji in cls.COMPANY_LOGOS.items():
            if key in company_lower:
                return emoji
        return cls.COMPANY_LOGOS["default"]
    
    @classmethod
    def is_easy_apply(cls, url: str) -> bool:
        """Check if job URL supports easy apply"""
        if not url:
            return False
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in cls.EASY_APPLY_PATTERNS)
    
    @classmethod
    def detect_ats_type(cls, url: str) -> Optional[str]:
        """Detect ATS type from URL for pre-fill support"""
        if not url:
            return None
        url_lower = url.lower()
        ats_patterns = {
            "greenhouse": ["greenhouse.io", "boards.greenhouse"],
            "lever": ["lever.co", "jobs.lever"],
            "workday": ["myworkdayjobs.com", "workday.com"],
            "icims": ["icims.com"],
            "smartrecruiters": ["smartrecruiters.com"],
            "ashby": ["ashbyhq.com"],
            "workable": ["workable.com", "apply.workable"]
        }
        for ats, patterns in ats_patterns.items():
            if any(p in url_lower for p in patterns):
                return ats
        return None
    
    @classmethod
    async def search_adzuna(
        cls,
        keywords: str,
        location: str = "us",
        page: int = 1,
        results_per_page: int = 20,
        salary_min: Optional[int] = None,
        remote_only: bool = False
    ) -> List[Dict]:
        """Search jobs from Adzuna API - AI/ML roles only"""
        if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
            logging.warning("Adzuna API keys not configured")
            return []
        
        # Map location to Adzuna country code
        country_map = {
            "us": "us", "usa": "us", "united states": "us",
            "uk": "gb", "united kingdom": "gb", "england": "gb",
            "canada": "ca", "germany": "de", "france": "fr",
            "india": "in", "australia": "au", "remote": "us"
        }
        country = country_map.get(location.lower().split(",")[0].strip(), "us")
        
        # Always include AI/ML in search to get relevant results
        ai_keywords = ["AI", "machine learning", "data scientist", "ML engineer"]
        search_query = keywords
        # If user search doesn't contain AI terms, add them
        if not any(ai_kw.lower() in keywords.lower() for ai_kw in ai_keywords):
            search_query = f"{keywords} AI machine learning"
        if remote_only:
            search_query += " remote"
        
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": search_query,
            "results_per_page": min(results_per_page * 3, 50)  # Fetch more to filter
        }
        
        if salary_min:
            params["salary_min"] = salary_min
        
        url = f"{cls.ADZUNA_BASE_URL}/jobs/{country}/search/{page}"
        
        jobs = []
        try:
            logging.info(f"Adzuna search: {url} with query: {search_query}")
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                logging.info(f"Adzuna returned {len(data.get('results', []))} jobs, filtering for AI roles...")
                for job_data in data.get("results", []):
                    title = job_data.get("title", "")
                    description = job_data.get("description", "")
                    # Only include AI/ML related jobs
                    if cls.is_ai_role(title, description):
                        job = cls._parse_adzuna_job(job_data)
                        jobs.append(job)
                        if len(jobs) >= results_per_page:
                            break
                
                logging.info(f"Filtered to {len(jobs)} AI-specific jobs")
                    
        except Exception as e:
            logging.error(f"Adzuna API error: {e}")
        
        return jobs
    
    @classmethod
    async def search_multiple_queries(cls, location: str = "us", limit: int = 50) -> List[Dict]:
        """Search for multiple AI-specific queries to get more diverse results"""
        ai_queries = [
            "AI Engineer",
            "Machine Learning Engineer", 
            "Data Scientist",
            "ML Engineer",
            "NLP Engineer",
            "Computer Vision",
            "MLOps Engineer",
            "Deep Learning",
            "LLM Engineer"
        ]
        
        all_jobs = []
        seen_ids = set()
        
        # Run searches in parallel (limited to avoid rate limits)
        async with httpx.AsyncClient(timeout=20.0) as client:
            for query in ai_queries[:5]:  # Top 5 queries
                if len(all_jobs) >= limit:
                    break
                    
                try:
                    params = {
                        "app_id": ADZUNA_APP_ID,
                        "app_key": ADZUNA_APP_KEY,
                        "what": query,
                        "results_per_page": 20
                    }
                    
                    country_map = {"us": "us", "uk": "gb", "canada": "ca", "india": "in"}
                    country = country_map.get(location.lower(), "us")
                    url = f"{cls.ADZUNA_BASE_URL}/jobs/{country}/search/1"
                    
                    response = await client.get(url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        for job_data in data.get("results", []):
                            job_id = job_data.get("id")
                            if job_id and job_id not in seen_ids:
                                seen_ids.add(job_id)
                                title = job_data.get("title", "")
                                description = job_data.get("description", "")
                                if cls.is_ai_role(title, description):
                                    job = cls._parse_adzuna_job(job_data)
                                    all_jobs.append(job)
                except Exception as e:
                    logging.error(f"Multi-query search error for '{query}': {e}")
                    continue
        
        return all_jobs[:limit]
    
    @classmethod
    def _parse_adzuna_job(cls, job_data: dict) -> Dict:
        """Parse Adzuna job response into standard format"""
        company = job_data.get("company", {}).get("display_name", "Unknown Company")
        location = job_data.get("location", {}).get("display_name", "Unknown Location")
        redirect_url = job_data.get("redirect_url", "")
        
        # Format salary
        salary_min = job_data.get("salary_min")
        salary_max = job_data.get("salary_max")
        if salary_min and salary_max:
            salary_range = f"${int(salary_min/1000)}K - ${int(salary_max/1000)}K"
        elif salary_min:
            salary_range = f"${int(salary_min/1000)}K+"
        else:
            salary_range = "Competitive"
        
        # Parse date
        created = job_data.get("created", "")
        try:
            posted_date = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime("%Y-%m-%d")
        except:
            posted_date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract skills and clean description
        raw_description = job_data.get("description", "")
        clean_description = cls._strip_html(raw_description)
        skills = cls._extract_skills(clean_description)
        
        return {
            "id": f"adzuna_{job_data.get('id', uuid.uuid4().hex[:8])}",
            "title": job_data.get("title", "Unknown Title"),
            "company": company,
            "location": location,
            "salary_range": salary_range,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "posted_date": posted_date,
            "match_score": 0,  # Will be calculated later
            "required_skills": skills[:5],
            "job_url": redirect_url,
            "company_logo": cls.get_company_logo(company),
            "description": clean_description[:500],
            "source": "adzuna",
            "is_easy_apply": cls.is_easy_apply(redirect_url),
            "ats_type": cls.detect_ats_type(redirect_url),
            "contract_type": job_data.get("contract_type", ""),
            "category": job_data.get("category", {}).get("label", "")
        }
    
    @classmethod
    async def search_remoteok(cls, keywords: str, limit: int = 20) -> List[Dict]:
        """Search jobs from RemoteOK API - AI/ML roles only"""
        jobs = []
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # RemoteOK returns JSON array
                response = await client.get(
                    cls.REMOTEOK_URL,
                    headers={"User-Agent": "TechShiftAI/1.0"}
                )
                response.raise_for_status()
                data = response.json()
                
                # First item is metadata, skip it
                job_listings = data[1:] if len(data) > 1 else []
                
                logging.info(f"RemoteOK returned {len(job_listings)} total jobs, filtering for AI roles...")
                
                for job_data in job_listings[:100]:  # Check more jobs to find AI roles
                    title = job_data.get("position", "")
                    description = job_data.get("description", "")
                    tags = job_data.get("tags", [])
                    
                    # ONLY include AI/ML related jobs
                    if cls.is_ai_role(title, description, tags):
                        job = cls._parse_remoteok_job(job_data)
                        jobs.append(job)
                        if len(jobs) >= limit:
                            break
                
                logging.info(f"Filtered to {len(jobs)} AI-specific jobs from RemoteOK")
                            
        except Exception as e:
            logging.error(f"RemoteOK API error: {e}")
        
        return jobs
    
    @classmethod
    def _parse_remoteok_job(cls, job_data: dict) -> Dict:
        """Parse RemoteOK job response into standard format"""
        company = job_data.get("company", "Unknown Company")
        
        # Format salary
        salary_min = job_data.get("salary_min")
        salary_max = job_data.get("salary_max")
        if salary_min and salary_max:
            salary_range = f"${int(salary_min/1000)}K - ${int(salary_max/1000)}K"
        elif salary_min:
            salary_range = f"${int(salary_min/1000)}K+"
        else:
            salary_range = "Competitive"
        
        # Parse date
        epoch = job_data.get("epoch", 0)
        posted_date = datetime.fromtimestamp(epoch).strftime("%Y-%m-%d") if epoch else datetime.now().strftime("%Y-%m-%d")
        
        # Clean HTML from description
        raw_description = job_data.get("description", "")
        clean_description = cls._strip_html(raw_description)[:500]
        
        return {
            "id": f"remoteok_{job_data.get('id', uuid.uuid4().hex[:8])}",
            "title": job_data.get("position", "Unknown Title"),
            "company": company,
            "location": job_data.get("location", "Remote (Worldwide)") or "Remote (Worldwide)",
            "salary_range": salary_range,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "posted_date": posted_date,
            "match_score": 0,
            "required_skills": job_data.get("tags", [])[:5],
            "job_url": job_data.get("url", f"https://remoteok.com/l/{job_data.get('id', '')}"),
            "company_logo": cls.get_company_logo(company),
            "description": clean_description,
            "source": "remoteok",
            "is_easy_apply": True,  # RemoteOK has simple apply
            "ats_type": None,
            "contract_type": "Remote",
            "category": "Remote Tech"
        }
    
    @classmethod
    def _strip_html(cls, text: str) -> str:
        """Remove HTML tags and clean up text"""
        import re
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', ' ', text)
        # Replace HTML entities
        clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        clean = clean.replace('&nbsp;', ' ').replace('&quot;', '"')
        # Clean up whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    @classmethod
    def _extract_skills(cls, text: str) -> List[str]:
        """Extract skills from job description"""
        skill_keywords = [
            "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++",
            "React", "Node.js", "FastAPI", "Django", "Flask", "Spring",
            "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Terraform",
            "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "PyTorch", "TensorFlow", "Keras", "Scikit-learn",
            "LLM", "GPT", "RAG", "LangChain", "Transformers",
            "REST API", "GraphQL", "Microservices", "CI/CD",
            "Agile", "Scrum", "Git", "Linux", "SQL"
        ]
        
        text_lower = text.lower()
        found = []
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                found.append(skill)
        return found
    
    # ============================================
    # REMOTIVE API - Remote tech jobs
    # ============================================
    @classmethod
    async def search_remotive(cls, keywords: str = "", limit: int = 20) -> List[Dict]:
        """Search jobs from Remotive API (free, no key needed)"""
        jobs = []
        try:
            params = {"limit": 100}  # Fetch more to filter
            if keywords:
                # Remotive uses category filter
                category_map = {
                    "ai": "data", "ml": "data", "machine learning": "data",
                    "data": "data", "engineer": "software-dev", "developer": "software-dev"
                }
                for kw, cat in category_map.items():
                    if kw in keywords.lower():
                        params["category"] = cat
                        break
            
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(cls.REMOTIVE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                logging.info(f"Remotive API returned {len(data.get('jobs', []))} total jobs")
                
                for job_data in data.get("jobs", [])[:100]:
                    title = job_data.get("title", "")
                    description = job_data.get("description", "") or ""
                    tags = job_data.get("tags", []) or []
                    
                    # Ensure tags is list of strings
                    if isinstance(tags, list):
                        tags = [str(t) for t in tags if t]
                    else:
                        tags = []
                    
                    if cls.is_ai_role(title, description, tags):
                        job = {
                            "id": f"remotive_{job_data.get('id', uuid.uuid4().hex[:8])}",
                            "title": title,
                            "company": job_data.get("company_name", "Unknown"),
                            "location": job_data.get("candidate_required_location", "Remote") or "Remote",
                            "salary_range": job_data.get("salary", "Competitive") or "Competitive",
                            "salary_min": None,
                            "salary_max": None,
                            "posted_date": str(job_data.get("publication_date", ""))[:10] if job_data.get("publication_date") else datetime.now().strftime("%Y-%m-%d"),
                            "match_score": 0,
                            "required_skills": tags[:5],
                            "job_url": job_data.get("url", ""),
                            "company_logo": cls.get_company_logo(job_data.get("company_name", "")),
                            "description": cls._strip_html(description)[:500],
                            "source": "remotive",
                            "is_easy_apply": True,
                            "ats_type": None,
                            "contract_type": job_data.get("job_type", "Remote") or "Remote",
                            "category": job_data.get("category", "")
                        }
                        jobs.append(job)
                        if len(jobs) >= limit:
                            break
                
                logging.info(f"Remotive returned {len(jobs)} AI jobs")
                
        except Exception as e:
            logging.error(f"Remotive API error: {e}")
        
        return jobs
    
    # ============================================
    # ARBEITNOW API - EU/Global tech jobs
    # ============================================
    @classmethod
    async def search_arbeitnow(cls, keywords: str = "", limit: int = 20) -> List[Dict]:
        """Search jobs from Arbeitnow API (free, no key needed)"""
        jobs = []
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(cls.ARBEITNOW_URL)
                response.raise_for_status()
                data = response.json()
                
                for job_data in data.get("data", [])[:100]:
                    title = job_data.get("title", "")
                    description = job_data.get("description", "")
                    tags = job_data.get("tags", []) or []
                    
                    # Ensure tags is a list of strings
                    if isinstance(tags, list):
                        tags = [str(t) for t in tags if t]
                    else:
                        tags = []
                    
                    if cls.is_ai_role(title, description, tags):
                        # Parse job types safely
                        job_types = job_data.get("job_types", [])
                        if isinstance(job_types, list) and len(job_types) > 0:
                            contract_type = str(job_types[0])
                        else:
                            contract_type = "Remote"
                        
                        job = {
                            "id": f"arbeitnow_{job_data.get('slug', uuid.uuid4().hex[:8])}",
                            "title": title,
                            "company": job_data.get("company_name", "Unknown"),
                            "location": job_data.get("location", "Remote") or "Remote",
                            "salary_range": "Competitive",
                            "salary_min": None,
                            "salary_max": None,
                            "posted_date": str(job_data.get("created_at", ""))[:10] if job_data.get("created_at") else datetime.now().strftime("%Y-%m-%d"),
                            "match_score": 0,
                            "required_skills": tags[:5],
                            "job_url": job_data.get("url", ""),
                            "company_logo": cls.get_company_logo(job_data.get("company_name", "")),
                            "description": cls._strip_html(description)[:500],
                            "source": "arbeitnow",
                            "is_easy_apply": True,
                            "ats_type": None,
                            "contract_type": contract_type,
                            "category": "EU Tech"
                        }
                        jobs.append(job)
                        if len(jobs) >= limit:
                            break
                
                logging.info(f"Arbeitnow returned {len(jobs)} AI jobs")
                
        except Exception as e:
            logging.error(f"Arbeitnow API error: {e}")
        
        return jobs
    
    # ============================================
    # JOBICY API - Remote jobs
    # ============================================
    @classmethod
    async def search_jobicy(cls, keywords: str = "", limit: int = 20) -> List[Dict]:
        """Search jobs from Jobicy API (free, no key needed)"""
        jobs = []
        try:
            # Jobicy API params: count, geo, industry, tag
            params = {"count": "50"}
            
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(cls.JOBICY_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                for job_data in data.get("jobs", [])[:100]:
                    title = job_data.get("jobTitle", "")
                    description = job_data.get("jobDescription", "")
                    
                    if cls.is_ai_role(title, description):
                        # Parse salary
                        salary_min = job_data.get("annualSalaryMin")
                        salary_max = job_data.get("annualSalaryMax")
                        if salary_min and salary_max:
                            salary_range = f"${int(salary_min/1000)}K - ${int(salary_max/1000)}K"
                        elif salary_min:
                            salary_range = f"${int(salary_min/1000)}K+"
                        else:
                            salary_range = "Competitive"
                        
                        job = {
                            "id": f"jobicy_{job_data.get('id', uuid.uuid4().hex[:8])}",
                            "title": title,
                            "company": job_data.get("companyName", "Unknown"),
                            "location": job_data.get("jobGeo", "Remote"),
                            "salary_range": salary_range,
                            "salary_min": salary_min,
                            "salary_max": salary_max,
                            "posted_date": job_data.get("pubDate", "")[:10] if job_data.get("pubDate") else datetime.now().strftime("%Y-%m-%d"),
                            "match_score": 0,
                            "required_skills": cls._extract_skills(description)[:5],
                            "job_url": job_data.get("url", ""),
                            "company_logo": cls.get_company_logo(job_data.get("companyName", "")),
                            "description": cls._strip_html(description)[:500],
                            "source": "jobicy",
                            "is_easy_apply": True,
                            "ats_type": None,
                            "contract_type": job_data.get("jobType", "Remote"),
                            "category": job_data.get("jobIndustry", "Remote Tech")
                        }
                        jobs.append(job)
                        if len(jobs) >= limit:
                            break
                
                logging.info(f"Jobicy returned {len(jobs)} AI jobs")
                
        except Exception as e:
            logging.error(f"Jobicy API error: {e}")
        
        return jobs
    
    # ============================================
    # JOOBLE API - Global job aggregator (40+ countries)
    # ============================================
    @classmethod
    async def search_jooble(cls, keywords: str = "AI Engineer", location: str = "", limit: int = 20) -> List[Dict]:
        """Search jobs from Jooble API (requires API key)"""
        if not JOOBLE_API_KEY:
            return []
        
        jobs = []
        try:
            # Jooble uses POST with JSON body
            url = f"{cls.JOOBLE_URL}/{JOOBLE_API_KEY}"
            
            # Add AI keywords to search
            search_keywords = keywords
            if not any(kw in keywords.lower() for kw in ["ai", "ml", "machine learning", "data scientist"]):
                search_keywords = f"{keywords} AI machine learning"
            
            payload = {
                "keywords": search_keywords,
                "location": location if location and location != "us" else "",
                "page": 1
            }
            
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                logging.info(f"Jooble API returned {len(data.get('jobs', []))} total jobs")
                
                for job_data in data.get("jobs", [])[:100]:
                    title = job_data.get("title", "")
                    snippet = job_data.get("snippet", "")
                    
                    if cls.is_ai_role(title, snippet):
                        # Parse salary if available
                        salary = job_data.get("salary", "")
                        salary_range = salary if salary else "Competitive"
                        
                        # Parse date
                        updated = job_data.get("updated", "")
                        posted_date = updated[:10] if updated else datetime.now().strftime("%Y-%m-%d")
                        
                        job = {
                            "id": f"jooble_{uuid.uuid4().hex[:8]}",
                            "title": title,
                            "company": job_data.get("company", "Unknown"),
                            "location": job_data.get("location", "Remote") or "Remote",
                            "salary_range": salary_range,
                            "salary_min": None,
                            "salary_max": None,
                            "posted_date": posted_date,
                            "match_score": 0,
                            "required_skills": cls._extract_skills(snippet)[:5],
                            "job_url": job_data.get("link", ""),
                            "company_logo": cls.get_company_logo(job_data.get("company", "")),
                            "description": cls._strip_html(snippet)[:500],
                            "source": "jooble",
                            "is_easy_apply": False,
                            "ats_type": cls.detect_ats_type(job_data.get("link", "")),
                            "contract_type": job_data.get("type", "Full-time"),
                            "category": "Global Jobs"
                        }
                        jobs.append(job)
                        if len(jobs) >= limit:
                            break
                
                logging.info(f"Jooble returned {len(jobs)} AI jobs")
                
        except Exception as e:
            logging.error(f"Jooble API error: {e}")
        
        return jobs
    
    @classmethod
    async def search_all(
        cls,
        keywords: str,
        location: str = "us",
        salary_min: Optional[int] = None,
        remote_only: bool = False,
        limit: int = 50
    ) -> List[Dict]:
        """Search jobs from ALL sources and combine results"""
        all_jobs = []
        
        # Search ALL APIs in parallel for maximum coverage
        tasks = [
            # Original APIs
            cls.search_adzuna(
                keywords=keywords,
                location=location,
                salary_min=salary_min,
                remote_only=remote_only,
                results_per_page=20
            ),
            cls.search_remoteok(keywords=keywords, limit=15),
            
            # Additional free APIs
            cls.search_remotive(keywords=keywords, limit=15),
            cls.search_arbeitnow(keywords=keywords, limit=15),
            cls.search_jobicy(keywords=keywords, limit=15),
            
            # Jooble (global aggregator - 40+ countries)
            cls.search_jooble(keywords=keywords, location=location, limit=20),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect results from all sources
        source_counts = {}
        for result in results:
            if isinstance(result, list):
                for job in result:
                    source = job.get("source", "unknown")
                    source_counts[source] = source_counts.get(source, 0) + 1
                all_jobs.extend(result)
            elif isinstance(result, Exception):
                logging.error(f"Job search error: {result}")
        
        # Log source breakdown
        logging.info(f"Job sources: {source_counts}, Total: {len(all_jobs)}")
        
        # Remove duplicates by title+company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = f"{job['title'].lower()}_{job['company'].lower()}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs[:limit]
    
    @classmethod
    def calculate_match_score(cls, job: Dict, user_skills: List[str], target_roles: List[str]) -> int:
        """Calculate job match score based on user profile - optimized for AI roles"""
        score = 60  # Higher base score since we already filtered for AI jobs
        
        job_title_lower = job.get("title", "").lower()
        job_skills = [s.lower() for s in job.get("required_skills", [])]
        job_description = job.get("description", "").lower()
        job_tags = " ".join(job_skills)
        
        # ============================================
        # REALISTIC SCORING ALGORITHM
        # Base: 40, Max: 95 (realistic range 45-85 for most users)
        # ============================================
        score = 40  # Conservative base
        
        # 1. SENIORITY LEVEL MATCH (Critical - up to +20 or -15)
        # Detect job seniority
        job_seniority = "mid"  # default
        if any(word in job_title_lower for word in ["principal", "staff", "distinguished", "director", "vp", "head of", "chief"]):
            job_seniority = "principal"  # 10+ years
        elif any(word in job_title_lower for word in ["senior", "sr.", "sr ", "lead", "manager"]):
            job_seniority = "senior"  # 5-10 years
        elif any(word in job_title_lower for word in ["junior", "jr.", "jr ", "entry", "associate", "intern"]):
            job_seniority = "junior"  # 0-2 years
        
        # Detect user seniority from preferences or assume mid-career
        user_seniority = "mid"  # Default assumption for mid-career professional
        user_years = 0
        if target_roles:
            role_text = " ".join(target_roles).lower()
            if any(word in role_text for word in ["principal", "staff", "director"]):
                user_seniority = "principal"
                user_years = 10
            elif any(word in role_text for word in ["senior", "lead"]):
                user_seniority = "senior"
                user_years = 6
            elif any(word in role_text for word in ["junior", "entry", "associate"]):
                user_seniority = "junior"
                user_years = 1
            else:
                user_seniority = "mid"
                user_years = 4
        
        # Seniority match scoring
        seniority_levels = {"junior": 1, "mid": 2, "senior": 3, "principal": 4}
        user_level = seniority_levels.get(user_seniority, 2)
        job_level = seniority_levels.get(job_seniority, 2)
        level_diff = job_level - user_level
        
        if level_diff == 0:
            score += 20  # Perfect match
        elif level_diff == 1:
            score += 10  # Stretch role (one level up) - achievable
        elif level_diff == -1:
            score += 15  # Slight step down - good fit
        elif level_diff >= 2:
            score -= 10  # Too senior for user (Principal when user is mid)
        elif level_diff <= -2:
            score += 5   # Too junior - overqualified
        
        # 2. ROLE/TITLE RELEVANCE (up to +15)
        ai_role_keywords = {
            "ai engineer": 15, "ml engineer": 15, "machine learning engineer": 15,
            "data scientist": 12, "mlops": 12, "deep learning": 12,
            "nlp engineer": 12, "computer vision": 12, "llm": 10,
            "ai/ml": 10, "applied scientist": 10, "research scientist": 8
        }
        
        role_bonus = 0
        for keyword, points in ai_role_keywords.items():
            if keyword in job_title_lower:
                role_bonus = max(role_bonus, points)
        score += role_bonus
        
        # 3. USER'S TARGET ROLE MATCH (up to +10)
        if target_roles:
            for role in target_roles:
                role_words = [w.lower() for w in role.split() if len(w) > 2]
                matches = sum(1 for word in role_words if word in job_title_lower)
                if matches >= 2:
                    score += 10
                    break
                elif matches == 1:
                    score += 5
                    break
        
        # 4. SKILLS MATCH (up to +15) - Be strict, require actual overlap
        if user_skills and len(user_skills) > 0:
            user_skills_lower = [s.lower().strip() for s in user_skills]
            searchable_text = f"{job_tags} {job_description}"
            
            matching_count = 0
            for skill in user_skills_lower:
                if len(skill) > 2 and skill in searchable_text:
                    matching_count += 1
            
            # Calculate percentage match
            if len(user_skills_lower) > 0:
                match_ratio = matching_count / len(user_skills_lower)
                if match_ratio >= 0.6:
                    score += 15  # 60%+ skills match
                elif match_ratio >= 0.4:
                    score += 10  # 40-60% skills match
                elif match_ratio >= 0.2:
                    score += 5   # 20-40% skills match
        else:
            # No user skills - don't give free points, slight penalty
            score += 0
        
        # 5. LOCATION/REMOTE PREFERENCE (up to +5)
        if "remote" in job.get("location", "").lower():
            score += 5
        
        # 6. SALARY REALITY CHECK (-5 to +3)
        # High salary jobs typically require more experience
        salary_min = job.get("salary_min")
        if salary_min:
            if salary_min >= 250000 and user_seniority in ["junior", "mid"]:
                score -= 5  # Unrealistic salary expectation
            elif salary_min >= 150000 and user_seniority == "junior":
                score -= 3  # Stretch salary for junior
            elif 100000 <= salary_min <= 180000 and user_seniority == "mid":
                score += 3  # Sweet spot for mid-career
        
        # 7. COMPANY TIER (small bonus, +3 max)
        top_ai_companies = ["openai", "anthropic", "google", "meta", "deepmind", "nvidia"]
        if any(company in job.get("company", "").lower() for company in top_ai_companies):
            # Top companies are harder to get into - slight boost for visibility but realistic
            if user_seniority in ["senior", "principal"]:
                score += 3
            else:
                score += 1  # Harder for mid/junior to get into top companies
        
        # Ensure score stays in realistic range (35-92)
        score = max(35, min(score, 92))
        
        return score

# Create global instance
job_discovery = JobDiscoveryService()

# Create the main app
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
    if not claude_client:
        raise HTTPException(status_code=500, detail="Claude API not configured")
    
    # Get location-specific salary data
    location = background.get('location', 'us').lower()
    salary_data = target_role.get('salary', {})
    location_salary = salary_data.get(location, salary_data.get('us', target_role['salary_range']))
    
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
- Description: {target_role['description']}
- Required Skills: {', '.join(target_role['top_skills'])}
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

# Include router
app.include_router(api_router)

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
