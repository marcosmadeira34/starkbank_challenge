# app/presentation/schemas/webhook.py

from pydantic import BaseModel
from typing import Dict, Any

class WebhookPayload(BaseModel):
    """Model for incoming webhook payload"""
    event: str
    log: Dict[str, Any]



class WebhookResponseSuccess(BaseModel):
    """Response model for successful webhook handling"""
    status: str
    message: str