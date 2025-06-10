# app/presentation/routes/webhook.py
from fastapi import APIRouter, Header, HTTPException, Request
from app.infrastructure.stark.webhook_api import handle_webhook
from app.presentation.schemas.webhook import WebhookPayload 

router = APIRouter()

@router.post("/webhook", response_model=WebhookPayload)
async def starkbank_webhook(
    request: Request,
    digital_signature: str = Header(..., alias="Digital-Signature")
):
    return await handle_webhook(request, digital_signature)