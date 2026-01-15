"""Models package initialization"""
from models.user import UserCreate, UserLogin, UserResponse
from models.token import TokenResponse
from models.analysis import AnalysisRequest, BackgroundContext, ResumeData
from models.cv import CVGenerationRequest, CVDownloadRequest, CVDownloadDirectRequest
from models.learning_path import (
    LearningPathRequest, 
    LearningPathDownloadRequest,
    LearningPathDownloadDirectRequest,
    WeekProgressUpdate,
    CourseProgressUpdate,
    SavedCourse
)
from models.cover_letter import CoverLetterRequest, CoverLetterResponse
from models.auto_apply import JobPreferencesRequest, JobApplyRequest, StatusUpdate
from models.payments import CheckoutRequest
from models.common import UsageResponse
