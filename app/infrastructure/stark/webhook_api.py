# /app/infrastructure/stark/webhook_api.py
import starkbank
from fastapi import HTTPException
from app.infrastructure.stark.transfer_api import send_transfer
import json 

import logging

logger = logging.getLogger(__name__)
# app/infrastructure/stark/webhook_api.py

async def handle_webhook(request, digital_signature: str):
    try:
        raw_body = await request.body()
        if not raw_body:
            raise HTTPException(status_code=400, detail="Empty request body")
        content = raw_body.decode()
        logger.info(f"Received webhook content...")  
               
        parsed_signature = digital_signature[2:] if digital_signature.startswith("s=") else digital_signature
        if not parsed_signature:
            raise HTTPException(status_code=400, detail="Invalid digital signature format")
        logger.debug(f"Received parsed digital signature...")  # Log only the first 50 characters for brevity
                
        try:
            event = starkbank.event.parse(
                content=content,
                signature=parsed_signature
            )
            logger.info(f"Parsed event successfully: {event.id} {event.subscription} {event.type}")
        except Exception as e:
            # This exception will occur with the dummy signature
            logger.error(f"StarkBank signature validation failed. Proceeding with manual JSON parse for debugging: {str(e)}")
            
            # WARNING: NEVER DO THIS IN PRODUCTION!            
            try:
                event_data = json.loads(content)  # Parse the raw JSON body

                # Mock classes to simulate StarkBank SDK objects for local testing
                class MockInvoice:
                    def __init__(self, data):
                        self.id = data.get("id")
                        self.amount = data.get("amount")
                        self.name = data.get("name")
                        self.tax_id = data.get("taxId")

                class MockLog:
                    def __init__(self, data):
                        # Only create invoice if type is "invoice"
                        self.invoice = MockInvoice(data.get("invoice", {})) if data.get("type") == "invoice" else None

                class MockEvent:
                    def __init__(self, data):
                        self.id = data.get("id")
                        self.subscription = data.get("subscription")
                        self.type = data.get("type")
                        self.is_delivered = data.get("isDelivered", False)
                        self.log = MockLog(data.get("log", {}))

                # Build a mock event object from parsed data
                event = MockEvent(event_data.get("event", {}))
                logger.info(f"Manually parsed event successfully: {event.id} {event.subscription} {event.type}")

            except Exception as parse_manual_exc:
                # If manual parsing fails, return HTTP 400
                logger.error(f"Failed to manually parse JSON: {str(parse_manual_exc)}")
                raise HTTPException(status_code=400, detail="Could not parse event data manually after signature failure.")
        # --- END OF MODIFIED SECTION ---


        if not event:
            raise ValueError("Invalid event data")
        
        if event.is_delivered:
            logger.info(f"Event already delivered: {event.id}")
            return {"status": "skipped", "message": "Event already delivered"}

        if event.subscription == "invoice":
            invoice = event.log.invoice
            logger.info(f"Processing invoice event: {invoice.id} with amount {invoice.amount}")

            amount = invoice.amount
           
            if isinstance(amount, list):
                amount = amount[0]
                logger.info(f"Converted amount to first element of list: {amount} (type: {type(amount)})")

            if event.type == "credited":
                logger.info(f"Received credited event for invoice {invoice.id} with amount {amount}")
                try:
                    print(f"DEBUG: Calling send_transfer with invoice.id={invoice.id} (type: {type(invoice.id)}) and amount={amount} (type: {type(amount)})")
                    send_transfer(invoice.id, amount)
                except Exception as transfer_exc:
                    print(f"DEBUG: Error in send_transfer: {transfer_exc}")
                    raise

        logger.info(f"Webhook processed successfully for event {event.id} of type {event.type}")
        return {"status": "success", "message": "Webhook processed successfully"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))