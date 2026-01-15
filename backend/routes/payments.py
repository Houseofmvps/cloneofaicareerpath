"""
Payment routes - Paddle checkout, webhooks, subscriptions (MOCKED)
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime, timezone
import uuid
import logging

from auth import get_current_user
from database import db
from config import PRICING, FREE_LIMITS

router = APIRouter(prefix="/payments", tags=["payments"])


class CheckoutRequest(BaseModel):
    product_type: str  # cv_single, cv_bulk_50, pro_monthly


@router.post("/checkout")
async def create_checkout(
    request: CheckoutRequest,
    user: dict = Depends(get_current_user)
):
    """Create Paddle checkout session - returns checkout URL (MOCKED)"""
    checkout_id = str(uuid.uuid4())
    
    product = PRICING.get(request.product_type)
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product type")
    
    checkout_data = {
        "checkout_id": checkout_id,
        "checkout_url": f"https://checkout.paddle.com/checkout/{checkout_id}",
        "product_type": request.product_type,
        "price": product["price"],
        "currency": product["currency"],
        "user_email": user["email"],
        "paddle_price_id": product.get("paddle_price_id"),
        "is_mock": True,
        "message": "Mock checkout - In production, Paddle handles payment securely."
    }
    
    await db.checkouts.insert_one({
        "checkout_id": checkout_id,
        "user_id": user["id"],
        "product_type": request.product_type,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    return checkout_data


@router.post("/webhook")
async def paddle_webhook(payload: Dict[str, Any]):
    """
    Paddle webhook handler - processes payment events
    
    Events handled:
    - transaction.completed: One-time payment successful
    - subscription.created: New subscription
    - subscription.updated: Subscription changed
    - subscription.cancelled: User cancelled
    - subscription.payment_failed: Billing issue
    """
    event_type = payload.get("event_type", "")
    data = payload.get("data", {})
    
    logging.info(f"Paddle webhook received: {event_type}")
    
    customer_email = data.get("customer", {}).get("email") or data.get("customer_email")
    
    if event_type == "transaction.completed":
        product_id = data.get("items", [{}])[0].get("price_id", "")
        
        if customer_email:
            user = await db.users.find_one({"email": customer_email}, {"_id": 0})
            if user:
                if "cv_single" in product_id:
                    await db.users.update_one(
                        {"email": customer_email},
                        {"$inc": {"cv_credits": 1}, "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
                    )
                elif "cv_bulk" in product_id:
                    await db.users.update_one(
                        {"email": customer_email},
                        {
                            "$inc": {"cv_credits": 50, "learning_path_credits": 3, "analysis_credits": 3},
                            "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
                        }
                    )
                
                await db.payments.insert_one({
                    "id": str(uuid.uuid4()),
                    "user_id": user["id"],
                    "paddle_transaction_id": data.get("id"),
                    "amount": data.get("details", {}).get("totals", {}).get("total"),
                    "currency": data.get("currency_code", "USD"),
                    "product_type": product_id,
                    "status": "completed",
                    "created_at": datetime.now(timezone.utc).isoformat()
                })
    
    elif event_type in ["subscription.created", "subscription.activated"]:
        if customer_email:
            await db.users.update_one(
                {"email": customer_email},
                {
                    "$set": {
                        "subscription_tier": "pro",
                        "paddle_subscription_id": data.get("id"),
                        "paddle_customer_id": data.get("customer_id"),
                        "subscription_status": "active",
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    
    elif event_type == "subscription.updated":
        status = data.get("status", "active")
        if customer_email:
            tier = "pro" if status == "active" else "free"
            await db.users.update_one(
                {"email": customer_email},
                {
                    "$set": {
                        "subscription_tier": tier,
                        "subscription_status": status,
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    
    elif event_type == "subscription.cancelled":
        if customer_email:
            await db.users.update_one(
                {"email": customer_email},
                {
                    "$set": {
                        "subscription_tier": "free",
                        "subscription_status": "cancelled",
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    
    elif event_type == "subscription.payment_failed":
        if customer_email:
            await db.users.update_one(
                {"email": customer_email},
                {
                    "$set": {
                        "subscription_status": "past_due",
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    
    return {"received": True, "event_type": event_type}


@router.post("/mock-upgrade")
async def mock_upgrade(user: dict = Depends(get_current_user)):
    """Mock upgrade to Pro tier for testing"""
    await db.users.update_one(
        {"id": user["id"]},
        {
            "$set": {
                "subscription_tier": "pro",
                "subscription_status": "active",
                "paddle_subscription_id": f"mock_sub_{uuid.uuid4().hex[:8]}",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    return {"message": "Upgraded to Pro (mock)", "subscription_tier": "pro"}


@router.post("/mock-purchase")
async def mock_purchase(
    product_type: str = Query(..., description="cv_single, cv_bulk_50"),
    user: dict = Depends(get_current_user)
):
    """Mock one-time purchase for testing"""
    product = PRICING.get(product_type)
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product type")
    
    if product_type == "cv_single":
        await db.users.update_one(
            {"id": user["id"]},
            {
                "$inc": {"cv_credits": 1},
                "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
            }
        )
        return {"message": f"Purchased {product_type} (mock)", "credits_added": 1}
    elif product_type == "cv_bulk_50":
        await db.users.update_one(
            {"id": user["id"]},
            {
                "$inc": {"cv_credits": 50, "learning_path_credits": 3, "analysis_credits": 3},
                "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
            }
        )
        return {
            "message": f"Purchased {product_type} (mock)",
            "cv_credits_added": 50,
            "learning_paths_added": 3,
            "analyses_added": 3
        }
    
    return {"message": f"Unknown product type: {product_type}"}


@router.get("/pricing")
async def get_pricing():
    """Get pricing information"""
    return {
        "pricing": PRICING,
        "free_limits": FREE_LIMITS,
        "currency": "USD"
    }


@router.get("/subscription")
async def get_subscription(user: dict = Depends(get_current_user)):
    """Get user's subscription status"""
    return {
        "subscription_tier": user.get("subscription_tier", "free"),
        "subscription_status": user.get("subscription_status", "none"),
        "paddle_subscription_id": user.get("paddle_subscription_id"),
        "cv_credits": user.get("cv_credits", 0),
        "learning_path_credits": user.get("learning_path_credits", 0),
        "analysis_credits": user.get("analysis_credits", 0)
    }
