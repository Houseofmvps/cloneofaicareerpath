"""
Authentication routes - Register, Login, Me
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
import uuid

from auth import hash_password, verify_password, create_token, get_current_user
from database import db
from config import FREE_LIMITS

router = APIRouter(prefix="/auth", tags=["auth"])


# Models
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
    token_type: str = "bearer"
    user: UserResponse


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "password_hash": hash_password(user_data.password),
        "subscription_tier": "free",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "usage": {
            "cv_generations": 0,
            "learning_paths": 0,
            "analyses": 0,
            "reset_date": datetime.now(timezone.utc).isoformat()
        },
        "credits": {
            "cv_downloads": FREE_LIMITS["cv_generations"],
            "learning_path_downloads": FREE_LIMITS["learning_paths"],
            "analysis": FREE_LIMITS["analyses"]
        },
        "learning_progress": {},
        "notification_prefs": {"weekly_job_digest": False}
    }
    
    await db.users.insert_one(user)
    
    token = create_token(user_id)
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            email=user["email"],
            name=user["name"],
            subscription_tier=user["subscription_tier"],
            created_at=user["created_at"]
        )
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login with email and password"""
    user = await db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user["id"])
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            subscription_tier=user.get("subscription_tier", "free"),
            created_at=user.get("created_at", "")
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        subscription_tier=user.get("subscription_tier", "free"),
        created_at=user.get("created_at", "")
    )
