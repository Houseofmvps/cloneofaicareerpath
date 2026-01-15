"""Learning path related models"""
from pydantic import BaseModel
from typing import List, Optional


class LearningPathRequest(BaseModel):
    current_role: str
    years_experience: int = 0
    current_skills: List[str] = []
    target_role_id: str
    location: str = "us"


class LearningPathDownloadRequest(BaseModel):
    format: str = "pdf"


class LearningPathDownloadDirectRequest(BaseModel):
    path_data: dict
    target_role: str = ""
    user_name: str = "User"


class WeekProgressUpdate(BaseModel):
    week: int
    completed: bool


class CourseProgressUpdate(BaseModel):
    """Track individual course completion within a week"""
    week: int
    course_index: int
    completed: bool
    notes: Optional[str] = None


class SavedCourse(BaseModel):
    """Model for saving a course to user's profile"""
    course_name: str
    course_url: str
    platform: str
    week: int
    learning_path_id: str
    notes: Optional[str] = None
