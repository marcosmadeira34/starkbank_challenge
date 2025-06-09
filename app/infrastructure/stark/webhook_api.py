import starkbank
import json
from fastapi import HTTPException

from app.infrastructure.stark.transfer_api import send_transfer

def handle_webhook(payload: dict, signature: str):
    try:
        events = starkbank.event.parse(
            content=payload,
            signature=signature
        )

        if not event:
            raise ValueError("Invalid event data")
        # Process the event as needed
        # For example, you can log it or perform some action based on the event type
        print(f"Received event: {event}")
        for event in events:
            if event.is_delivered:
                print(f"Event delivered: {event.id}")
                continue

            if event.subscription == "invoice":
                invoice = event.log.invoice
                print(f"Invoice event", invoice.id, invoice.amount)

                # Logic to transfer the invoice amount to the user
                if event.type == "credited":
                    amount = invoice.amount
                    print(f"Received credited event for invoice {invoice.id} with amount {amount}")
                    send_transfer(invoice.id, amount)

            starkbank.event.update(id=event.id, is_delivered=True)
            return {"status": "success", "message": "Webhook processed successfully"}
        
    except Exception as e:
        print(f"Error processing webhook_api: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))