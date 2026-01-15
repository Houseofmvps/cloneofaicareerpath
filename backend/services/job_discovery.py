"""
Job Discovery Service - Multi-source job aggregation
Integrates: Adzuna, RemoteOK, Remotive, Arbeitnow, Jobicy, Jooble
"""
import logging
import asyncio
import uuid
import re
import httpx
from datetime import datetime
from typing import List, Dict, Optional

from config import ADZUNA_APP_ID, ADZUNA_APP_KEY, JOOBLE_API_KEY


class JobDiscoveryService:
    """Service to discover jobs from multiple APIs"""
    
    # API Endpoints
    ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api"
    REMOTEOK_URL = "https://remoteok.com/api"
    REMOTIVE_URL = "https://remotive.com/api/remote-jobs"
    ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"
    JOBICY_URL = "https://jobicy.com/api/v2/remote-jobs"
    JOOBLE_URL = "https://jooble.org/api"
    
    # AI-specific job title keywords
    AI_ROLE_KEYWORDS = [
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
        "tensorflow", "pytorch", "keras", "scikit",
        "openai", "anthropic", "deepmind", "stability ai", "hugging face",
        "midjourney", "cohere", "ai21"
    ]
    
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
    
    STRONG_AI_SIGNALS = [
        "ai ", "ai/", " ai", "machine learning", "ml ", "ml/", "/ml",
        "data scientist", "deep learning", "nlp", "computer vision",
        "llm", "generative ai", "neural", "pytorch", "tensorflow"
    ]
    
    COMPANY_LOGOS = {
        "google": "🔍", "meta": "📱", "amazon": "📦", "microsoft": "💻",
        "apple": "🍎", "netflix": "🎬", "stripe": "💳", "openai": "🤖",
        "anthropic": "🧠", "notion": "📝", "slack": "💬", "spotify": "🎵",
        "airbnb": "🏠", "uber": "🚗", "salesforce": "☁️", "adobe": "🎨",
        "nvidia": "🎮", "tesla": "⚡", "default": "🏢"
    }
    
    EASY_APPLY_PATTERNS = [
        "linkedin.com/jobs", "indeed.com/apply", "lever.co", "greenhouse.io",
        "workable.com", "bamboohr.com", "ashbyhq.com", "jobs.smartrecruiters",
        "myworkdayjobs.com", "icims.com", "apply.workable.com"
    ]
    
    @classmethod
    def is_ai_role(cls, job_title: str, description: str = "", tags: list = None) -> bool:
        """Check if job is AI/ML related"""
        title_lower = job_title.lower()
        
        if any(signal in title_lower for signal in cls.STRONG_AI_SIGNALS):
            return True
        
        if any(excl in title_lower for excl in cls.NON_AI_ROLES):
            return False
        
        if any(keyword in title_lower for keyword in cls.AI_ROLE_KEYWORDS):
            return True
        
        if tags:
            tags_str = " ".join(tags).lower()
            if any(signal in tags_str for signal in cls.STRONG_AI_SIGNALS):
                return True
        
        if description:
            desc_lower = description.lower()
            if any(signal in desc_lower for signal in cls.STRONG_AI_SIGNALS):
                tech_terms = ["engineer", "developer", "scientist", "analyst", "researcher"]
                if any(term in title_lower for term in tech_terms):
                    return True
        
        return False
    
    @classmethod
    def get_company_logo(cls, company_name: str) -> str:
        company_lower = company_name.lower()
        for key, emoji in cls.COMPANY_LOGOS.items():
            if key in company_lower:
                return emoji
        return cls.COMPANY_LOGOS["default"]
    
    @classmethod
    def is_easy_apply(cls, url: str) -> bool:
        if not url:
            return False
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in cls.EASY_APPLY_PATTERNS)
    
    @classmethod
    def detect_ats_type(cls, url: str) -> Optional[str]:
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
    def _strip_html(cls, text: str) -> str:
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        clean = clean.replace('&nbsp;', ' ').replace('&quot;', '"')
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    @classmethod
    def _extract_skills(cls, text: str) -> List[str]:
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
        if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
            return []
        
        country_map = {
            "us": "us", "usa": "us", "united states": "us",
            "uk": "gb", "united kingdom": "gb", "england": "gb",
            "canada": "ca", "germany": "de", "france": "fr",
            "india": "in", "australia": "au", "remote": "us"
        }
        country = country_map.get(location.lower().split(",")[0].strip(), "us")
        
        ai_keywords = ["AI", "machine learning", "data scientist", "ML engineer"]
        search_query = keywords
        if not any(ai_kw.lower() in keywords.lower() for ai_kw in ai_keywords):
            search_query = f"{keywords} AI machine learning"
        if remote_only:
            search_query += " remote"
        
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": search_query,
            "results_per_page": min(results_per_page * 3, 50)
        }
        
        if salary_min:
            params["salary_min"] = salary_min
        
        url = f"{cls.ADZUNA_BASE_URL}/jobs/{country}/search/{page}"
        
        jobs = []
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for job_data in data.get("results", []):
                    title = job_data.get("title", "")
                    description = job_data.get("description", "")
                    if cls.is_ai_role(title, description):
                        job = cls._parse_adzuna_job(job_data)
                        jobs.append(job)
                        if len(jobs) >= results_per_page:
                            break
        except Exception as e:
            logging.error(f"Adzuna API error: {e}")
        
        return jobs
    
    @classmethod
    def _parse_adzuna_job(cls, job_data: dict) -> Dict:
        company = job_data.get("company", {}).get("display_name", "Unknown Company")
        location = job_data.get("location", {}).get("display_name", "Unknown Location")
        redirect_url = job_data.get("redirect_url", "")
        
        salary_min = job_data.get("salary_min")
        salary_max = job_data.get("salary_max")
        if salary_min and salary_max:
            salary_range = f"${int(salary_min/1000)}K - ${int(salary_max/1000)}K"
        elif salary_min:
            salary_range = f"${int(salary_min/1000)}K+"
        else:
            salary_range = "Competitive"
        
        created = job_data.get("created", "")
        try:
            posted_date = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime("%Y-%m-%d")
        except:
            posted_date = datetime.now().strftime("%Y-%m-%d")
        
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
            "match_score": 0,
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
        jobs = []
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    cls.REMOTEOK_URL,
                    headers={"User-Agent": "TechShiftAI/1.0"}
                )
                response.raise_for_status()
                data = response.json()
                
                job_listings = data[1:] if len(data) > 1 else []
                
                for job_data in job_listings[:100]:
                    title = job_data.get("position", "")
                    description = job_data.get("description", "")
                    tags = job_data.get("tags", [])
                    
                    if cls.is_ai_role(title, description, tags):
                        job = cls._parse_remoteok_job(job_data)
                        jobs.append(job)
                        if len(jobs) >= limit:
                            break
        except Exception as e:
            logging.error(f"RemoteOK API error: {e}")
        
        return jobs
    
    @classmethod
    def _parse_remoteok_job(cls, job_data: dict) -> Dict:
        company = job_data.get("company", "Unknown Company")
        
        salary_min = job_data.get("salary_min")
        salary_max = job_data.get("salary_max")
        if salary_min and salary_max:
            salary_range = f"${int(salary_min/1000)}K - ${int(salary_max/1000)}K"
        elif salary_min:
            salary_range = f"${int(salary_min/1000)}K+"
        else:
            salary_range = "Competitive"
        
        epoch = job_data.get("epoch", 0)
        posted_date = datetime.fromtimestamp(epoch).strftime("%Y-%m-%d") if epoch else datetime.now().strftime("%Y-%m-%d")
        
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
            "is_easy_apply": True,
            "ats_type": None,
            "contract_type": "Remote",
            "category": "Remote Tech"
        }
    
    @classmethod
    async def search_remotive(cls, keywords: str = "", limit: int = 20) -> List[Dict]:
        jobs = []
        try:
            params = {"limit": 100}
            if keywords:
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
                
                for job_data in data.get("jobs", [])[:100]:
                    title = job_data.get("title", "")
                    description = job_data.get("description", "") or ""
                    tags = job_data.get("tags", []) or []
                    
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
        except Exception as e:
            logging.error(f"Remotive API error: {e}")
        
        return jobs
    
    @classmethod
    async def search_arbeitnow(cls, keywords: str = "", limit: int = 20) -> List[Dict]:
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
                    
                    if isinstance(tags, list):
                        tags = [str(t) for t in tags if t]
                    else:
                        tags = []
                    
                    if cls.is_ai_role(title, description, tags):
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
        except Exception as e:
            logging.error(f"Arbeitnow API error: {e}")
        
        return jobs
    
    @classmethod
    async def search_jobicy(cls, keywords: str = "", limit: int = 20) -> List[Dict]:
        jobs = []
        try:
            params = {"count": "50"}
            
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                response = await client.get(cls.JOBICY_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                for job_data in data.get("jobs", [])[:100]:
                    title = job_data.get("jobTitle", "")
                    description = job_data.get("jobDescription", "")
                    
                    if cls.is_ai_role(title, description):
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
        except Exception as e:
            logging.error(f"Jobicy API error: {e}")
        
        return jobs
    
    @classmethod
    async def search_jooble(cls, keywords: str = "AI Engineer", location: str = "", limit: int = 20) -> List[Dict]:
        if not JOOBLE_API_KEY:
            return []
        
        jobs = []
        try:
            url = f"{cls.JOOBLE_URL}/{JOOBLE_API_KEY}"
            
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
                
                for job_data in data.get("jobs", [])[:100]:
                    title = job_data.get("title", "")
                    snippet = job_data.get("snippet", "")
                    
                    if cls.is_ai_role(title, snippet):
                        salary = job_data.get("salary", "")
                        salary_range = salary if salary else "Competitive"
                        
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
        tasks = [
            cls.search_adzuna(
                keywords=keywords,
                location=location,
                salary_min=salary_min,
                remote_only=remote_only,
                results_per_page=20
            ),
            cls.search_remoteok(keywords=keywords, limit=15),
            cls.search_remotive(keywords=keywords, limit=15),
            cls.search_arbeitnow(keywords=keywords, limit=15),
            cls.search_jobicy(keywords=keywords, limit=15),
            cls.search_jooble(keywords=keywords, location=location, limit=20),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_jobs = []
        source_counts = {}
        for result in results:
            if isinstance(result, list):
                for job in result:
                    source = job.get("source", "unknown")
                    source_counts[source] = source_counts.get(source, 0) + 1
                all_jobs.extend(result)
            elif isinstance(result, Exception):
                logging.error(f"Job search error: {result}")
        
        logging.info(f"Job sources: {source_counts}, Total: {len(all_jobs)}")
        
        # Remove duplicates
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
        """Calculate job match score based on user profile"""
        job_title_lower = job.get("title", "").lower()
        job_skills = [s.lower() for s in job.get("required_skills", [])]
        job_description = job.get("description", "").lower()
        job_tags = " ".join(job_skills)
        
        score = 40  # Conservative base
        
        # 1. SENIORITY LEVEL MATCH
        job_seniority = "mid"
        if any(word in job_title_lower for word in ["principal", "staff", "distinguished", "director", "vp", "head of", "chief"]):
            job_seniority = "principal"
        elif any(word in job_title_lower for word in ["senior", "sr.", "sr ", "lead", "manager"]):
            job_seniority = "senior"
        elif any(word in job_title_lower for word in ["junior", "jr.", "jr ", "entry", "associate", "intern"]):
            job_seniority = "junior"
        
        user_seniority = "mid"
        if target_roles:
            role_text = " ".join(target_roles).lower()
            if any(word in role_text for word in ["principal", "staff", "director"]):
                user_seniority = "principal"
            elif any(word in role_text for word in ["senior", "lead"]):
                user_seniority = "senior"
            elif any(word in role_text for word in ["junior", "entry", "associate"]):
                user_seniority = "junior"
        
        seniority_levels = {"junior": 1, "mid": 2, "senior": 3, "principal": 4}
        user_level = seniority_levels.get(user_seniority, 2)
        job_level = seniority_levels.get(job_seniority, 2)
        level_diff = job_level - user_level
        
        if level_diff == 0:
            score += 20
        elif level_diff == 1:
            score += 10
        elif level_diff == -1:
            score += 15
        elif level_diff >= 2:
            score -= 10
        elif level_diff <= -2:
            score += 5
        
        # 2. ROLE/TITLE RELEVANCE
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
        
        # 3. USER'S TARGET ROLE MATCH
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
        
        # 4. SKILLS MATCH
        if user_skills and len(user_skills) > 0:
            user_skills_lower = [s.lower().strip() for s in user_skills]
            searchable_text = f"{job_tags} {job_description}"
            
            matching_count = 0
            for skill in user_skills_lower:
                if len(skill) > 2 and skill in searchable_text:
                    matching_count += 1
            
            if len(user_skills_lower) > 0:
                match_ratio = matching_count / len(user_skills_lower)
                if match_ratio >= 0.6:
                    score += 15
                elif match_ratio >= 0.4:
                    score += 10
                elif match_ratio >= 0.2:
                    score += 5
        
        # 5. LOCATION/REMOTE PREFERENCE
        if "remote" in job.get("location", "").lower():
            score += 5
        
        # 6. SALARY REALITY CHECK
        salary_min = job.get("salary_min")
        if salary_min:
            if salary_min >= 250000 and user_seniority in ["junior", "mid"]:
                score -= 5
            elif salary_min >= 150000 and user_seniority == "junior":
                score -= 3
            elif 100000 <= salary_min <= 180000 and user_seniority == "mid":
                score += 3
        
        # 7. COMPANY TIER
        top_ai_companies = ["openai", "anthropic", "google", "meta", "deepmind", "nvidia"]
        if any(company in job.get("company", "").lower() for company in top_ai_companies):
            if user_seniority in ["senior", "principal"]:
                score += 3
            else:
                score += 1
        
        return max(35, min(score, 92))


# Create global instance
job_discovery = JobDiscoveryService()
