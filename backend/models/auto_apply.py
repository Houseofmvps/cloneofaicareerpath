"""Auto-apply / Job search related models"""
from pydantic import BaseModel
from typing import List, Optional


class JobPreferencesRequest(BaseModel):
    target_roles: List[str] = []
    skills: List[str] = []
    min_salary: int = 0
    max_salary: int = 0
    locations: List[str] = []
    remote_only: bool = False
    experience_level: str = "mid"
    auto_apply_enabled: bool = False


class JobApplyRequest(BaseModel):
    job_title: str
    company: str
    job_url: str
    job_description: str = ""
    skills: List[str] = []
    achievements: List[str] = []


class StatusUpdate(BaseModel):
    status: str
