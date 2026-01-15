"""Cover letter related models"""
from pydantic import BaseModel
from typing import List, Optional


class CoverLetterRequest(BaseModel):
    target_role_id: str
    company_name: str = ""
    job_description: str = ""
    skills: List[str] = []
    achievements: List[str] = []
    tone: str = "professional"


class CoverLetterResponse(BaseModel):
    id: str
    letters: List[dict]
    target_role: str
    company_name: str
    created_at: str
