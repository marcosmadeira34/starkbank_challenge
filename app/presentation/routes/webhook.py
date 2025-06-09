from fastapi import APIRouter, Header, HTTPException
from app.infrastructure.stark.webhook_api import handle_webhook
from app.schemas.webhook import WebhookPayload 

router = APIRouter()

@router.post("/starkbank")
async def starkbank_webhook(
    payload: WebhookPayload,
    digital_signature: str = Header(..., convert_underscores=False)
):
    """
    Endpoint to handle StarkBank webhook events.
    """
    try:
        return await handle_webhook(payload.dict(), digital_signature)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")