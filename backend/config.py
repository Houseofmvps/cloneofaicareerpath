"""
Application configuration - Environment variables and constants
"""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB
MONGO_URL = os.environ['MONGO_URL']
DB_NAME = os.environ['DB_NAME']

# JWT Config
JWT_SECRET = os.environ.get('JWT_SECRET', 'career-lift-secret-key')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Claude API
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# Resend Email Config
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')

# Job API Config
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID', '')
ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY', '')
JOOBLE_API_KEY = os.environ.get('JOOBLE_API_KEY', '')

# Paddle Config
PADDLE_API_KEY = os.environ.get('PADDLE_API_KEY', '')
PADDLE_WEBHOOK_SECRET = os.environ.get('PADDLE_WEBHOOK_SECRET', '')

# Pricing Constants
PRICING = {
    "pro_monthly": {
        "price": 29, 
        "currency": "USD", 
        "paddle_price_id": "pri_pro_monthly",
        "features": ["Unlimited CV Generation", "Unlimited Learning Paths", "Unlimited Analysis", "Priority AI Response", "Priority Support"]
    },
    "cv_single": {
        "price": 0.5, 
        "currency": "USD", 
        "paddle_price_id": "pri_cv_single",
        "cv_credits": 1
    },
    "cv_bulk_50": {
        "price": 13.99, 
        "currency": "USD", 
        "paddle_price_id": "pri_cv_bulk_50", 
        "cv_credits": 50, 
        "learning_path_credits": 3, 
        "analysis_credits": 3,
        "description": "50 CV downloads + 3 Learning Paths + 3 Analyses"
    }
}

# Free Tier Limits (per month)
FREE_LIMITS = {
    "cv_generations": 2,
    "learning_paths": 1,
    "analyses": 1
}

# Downloads directory
DOWNLOADS_DIR = ROOT_DIR / 'downloads'
DOWNLOADS_DIR.mkdir(exist_ok=True)
