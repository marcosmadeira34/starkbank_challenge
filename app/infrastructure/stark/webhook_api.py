# /app/infrastructure/stark/webhook_api.py (versão LIMPA para produção)
import starkbank
from fastapi import HTTPException
from app.infrastructure.stark.transfer_api import send_transfer
# import json -> pode remover, não é mais usado
import logging

logger = logging.getLogger(__name__)

async def handle_webhook(request, digital_signature: str):
    try:
        raw_body = await request.body()
        if not raw_body:
            logger.error("Empty request body received for webhook.")
            raise HTTPException(status_code=400, detail="Empty request body")

        content = raw_body.decode()
        logger.info("Received webhook content for processing.")

        parsed_signature = digital_signature[2:] if digital_signature.startswith("s=") else digital_signature
        if not parsed_signature:
            logger.error("Invalid or empty digital signature format provided.")
            raise HTTPException(status_code=400, detail="Invalid digital signature format.")

        logger.debug(f"Attempting to parse event with signature (first 50 chars): {parsed_signature[:50]}...")

        event = starkbank.event.parse(
            content=content,
            signature=parsed_signature
        )
        logger.info(f"Event successfully parsed and signature verified: ID={event.id}, Subscription={event.subscription}")
        logger.debug(f"Full event object structure: {event.__dict__}")

        if event.is_delivered:
            logger.info(f"Event {event.id} already marked as delivered. Skipping processing.")
            return {"status": "skipped", "message": "Event already delivered."}

        if event.subscription == "invoice":
            invoice = event.log.invoice 
            logger.info(f"Processing invoice event for ID: {invoice.id}, Amount: {invoice.amount}.")

            amount = invoice.amount
            if isinstance(amount, list):
                amount = amount[0]
                logger.warning(f"Invoice amount received as a list. Using the first element: {amount}.")

            if event.log.type == "credited":
                logger.info(f"Credited event received for invoice {invoice.id}. Initiating transfer.")
                try:
                    await send_transfer(invoice.id, amount)
                    logger.info(f"Transfer successfully initiated for invoice {invoice.id}.")
                    return {"status": "success", "message": "Webhook processed successfully, transfer initiated."}
                except Exception as transfer_exc:
                    logger.error(f"Failed to initiate transfer for invoice {invoice.id}: {str(transfer_exc)}", exc_info=True)
                    raise HTTPException(status_code=500, detail=f"Failed to process transfer for invoice {invoice.id}.")
            else:
                logger.info(f"Invoice event type '{event.log.type}' received for invoice {invoice.id}. No action taken.")
                return {"status": "skipped", "message": f"Unhandled invoice event type: {event.log.type}."}
        else: 
            logger.info(f"Unhandled event subscription: '{event.subscription}' with type: '{event.log.type}'. No specific action configured.")
            return {"status": "skipped", "message": f"Unhandled event type: {event.log.type}."}

    except starkbank.error.InvalidSignatureError as e:
        logger.error(f"StarkBank digital signature validation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=403, detail="Invalid digital signature provided. Webhook not processed.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while processing the webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error. Could not process webhook event.")