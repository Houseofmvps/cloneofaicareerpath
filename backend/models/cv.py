"""CV generation related models"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class CVGenerationRequest(BaseModel):
    target_role_id: str
    experience_years: int = 0
    current_role: str = ""
    skills: List[str] = []
    achievements: List[str] = []
    education: str = ""
    location: str = "us"
    country: str = ""
    include_photo: bool = False
    experiences: Optional[List[Dict]] = None


class CVDownloadRequest(BaseModel):
    format: str = "pdf"
    cv_version: str = "ats"


class CVDownloadDirectRequest(BaseModel):
    cv_data: dict
    cv_version: str = "ats"
    target_role: str = ""
