
import asyncio
import httpx
import logging
import uuid
import os
import re
from datetime import datetime, timezone
from typing import List, Dict, Optional
import lxml.html  # Changed from server.py which might have lazy import

# Re-import role definitions or move them here?
# Let's keep them here if possible, or import from data.roles
# But JobDiscoveryService was using its own constants mostly.

ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID', '')
ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY', '')
JOOBLE_API_KEY = os.environ.get('JOOBLE_API_KEY', '')

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
        
        # Exclude generic tech roles without AI in title UNLESS description has strong AI signals
        if any(excl in title_lower for excl in cls.NON_AI_ROLES):
            # If excluded (e.g. "Software Engineer"), strict check on description
            if description:
                desc_lower = description.lower()
                if any(signal in desc_lower for signal in cls.STRONG_AI_SIGNALS):
                    # Also check title isn't completely unrelated (must be technical)
                    tech_terms = ["engineer", "developer", "scientist", "analyst", "researcher"]
                    if any(term in title_lower for term in tech_terms):
                        return True
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
        """Remove HTML tags and clean up text using lxml"""
        if not text:
            return ""
        try:
            # lxml is robust and handles malformed HTML better than regex
            return lxml.html.fromstring(text).text_content().strip()
        except Exception:
            # Fallback for very broken HTML or plain text
            return text.strip()
    
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
            
        # Assuming user is mid-level/senior transitioner (common for this app)
        if job_seniority == "senior":
            score += 10
        elif job_seniority == "mid":
            score += 15
        elif job_seniority == "junior":
            score += 5
            
        # 2. ROLE TITLE MATCH (High impact - up to +25)
        # Check if job title matches user's target roles
        role_matched = False
        if target_roles:
            for target in target_roles:
                target_words = target.lower().split()
                # Check if important words from target role appear in job title
                match_count = sum(1 for word in target_words if word in job_title_lower)
                if match_count >= len(target_words) - 1: # Allow 1 missing word
                    score += 25
                    role_matched = True
                    break
                elif match_count > 0:
                    score += 10
        else:
            # Default behavior if no target roles: match generic AI terms
            if "ai" in job_title_lower or "machine learning" in job_title_lower or "data scientist" in job_title_lower:
                score += 15
        
        # 3. SKILL MATCHING (Medium impact - up to +20)
        # Check if user skills appear in job description/requirements
        if user_skills:
            matched_skills = [s for s in user_skills if s.lower() in job_description or s.lower() in job_tags]
            match_percentage = len(matched_skills) / len(user_skills)
            score += int(match_percentage * 20)
        else:
            # If no user skills, look for popular tech stack in job
            popular_stack = ["python", "pytorch", "tensorflow", "aws", "docker", "react", "fastapi"]
            matched_popular = [s for s in popular_stack if s in job_description]
            if len(matched_popular) >= 3:
                score += 10
        
        # 4. KEYWORD BONUSES (Small impact - up to +10)
        # Bonus for hot keywords
        hot_keywords = ["generative ai", "llm", "gpt", "transformer", "hugging face", "remote"]
        for keyword in hot_keywords:
            if keyword in job_description:
                score += 2
        
        # Cap score at 95 (nobody is perfect) and floor at 40
        return min(max(int(score), 40), 95)

# Create singleton instance
job_discovery = JobDiscoveryService()
