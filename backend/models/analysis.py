"""Analysis related models"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeData(BaseModel):
    skills: List[str] = []
    experience_years: int = 0
    current_role: str = ""
    education: str = ""
    achievements: List[str] = []


class BackgroundContext(BaseModel):
    current_industry: str = ""
    motivation: str = ""
    timeline_preference: str = "3-6 months"
    learning_style: str = "self-paced"
    budget: str = "moderate"


class AnalysisRequest(BaseModel):
    target_role_id: str
    resume: Optional[ResumeData] = None
    background: Optional[BackgroundContext] = None
