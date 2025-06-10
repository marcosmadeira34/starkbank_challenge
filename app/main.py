# app/main.py
from fastapi import FastAPI
from app.presentation.routes import webhook
from app.scheduler.invoice_job import start_invoice_scheduler
from app.infrastructure.stark.client import initialize_stark_client


# Create the FastAPI app instance
app = FastAPI(
    title="StarkBank Webhook API",
    description="API for handling StarkBank webhook events",
    version="1.0.0",
    contact={
        "name": "Marcos Vinicius Madeira",
        "email": "mmadeirasilva5@gmail.com",
    }
)
# Include the router 
app.include_router(webhook.router, prefix="/v2", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "Welcome to the StarkBank Webhook API!"}


@app.on_event("startup")
async def startup_event():
    """
    Startup event to initialize the StarkBank client and start the scheduler.
    """
    initialize_stark_client()
    start_invoice_scheduler()
    print("StarkBank Webhook API started and scheduler is running.")