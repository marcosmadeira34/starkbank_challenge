# app/main.py
from fastapi import FastAPI
from app.presentation.routes import webhook
from app.scheduler.invoice_job import start_invoice_scheduler
from app.infrastructure.stark.client import initialize_stark_client, initialize_webhook_client
import logging
import sys
from time import sleep

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    stream=sys.stdout, # Directs logs to the console (standard output)
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


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
    logger.info("Application startup initiated.")
    initialize_stark_client()
    # Wait for the StarkBank client to be initialized
    sleep(1)
    initialize_webhook_client()
    # Wait for the webhook client to be initialized
    sleep(1)  
    start_invoice_scheduler()
    logger.info("Application startup complete.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event to clean up resources if necessary.
    """
    logger.info("Application shutdown initiated.")
    # Logic to clean up resources if needed
    logger.info("Application shutdown complete.")
    