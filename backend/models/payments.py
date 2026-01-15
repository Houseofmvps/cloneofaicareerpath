"""Payments related models"""
from pydantic import BaseModel
from typing import Dict, Any


class CheckoutRequest(BaseModel):
    price_id: str
    success_url: str = ""
    cancel_url: str = ""
