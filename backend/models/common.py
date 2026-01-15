"""Common/shared models"""
from pydantic import BaseModel


class UsageResponse(BaseModel):
    analyses_used: int = 0
    analyses_limit: int = 1
    cv_generations_used: int = 0
    cv_limit: int = 2
    cv_credits: int = 0
    learning_paths_used: int = 0
    learning_paths_limit: int = 1
    learning_path_credits: int = 0
    analysis_credits: int = 0
    subscription_tier: str = "free"
