# app/presentation/schemas/webhook.py

from pydantic import BaseModel
from typing import Dict, Any

class WebhookPayload(BaseModel):
    event: str
    log: Dict[str, Any]
