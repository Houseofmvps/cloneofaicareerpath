"""
Pricing and Limits Configuration Module
Contains pricing tiers and free tier limits.
"""

# Pricing Configuration
PRICING = {
    # Subscription
    "pro_monthly": {
        "price": 29, 
        "currency": "USD", 
        "paddle_price_id": "pri_pro_monthly",
        "features": ["Unlimited CV Generation", "Unlimited Learning Paths", "Unlimited Analysis", "Priority AI Response", "Priority Support"]
    },
    # Pay-per-use CV
    "cv_single": {
        "price": 0.5, 
        "currency": "USD", 
        "paddle_price_id": "pri_cv_single",
        "cv_credits": 1
    },
    # Bundle
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
    "cv_generations": 2,      # 2 free CV downloads per month
    "learning_paths": 1,      # 1 free learning path per month (view only, no PDF/DOCX)
    "analyses": 1,            # 1 free career analysis per month
    "resume_scans": 2         # 2 free resume scans per month
}


def get_feature_limit(feature: str, is_pro: bool = False) -> int:
    """Get the limit for a specific feature based on subscription tier"""
    if is_pro:
        return 999  # Unlimited for pro users
    return FREE_LIMITS.get(feature, 0)


def get_pricing_info(price_id: str) -> dict:
    """Get pricing information for a specific price ID"""
    return PRICING.get(price_id, {})
