# app/scheduler/invoice_job.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.domain.services.invoice_logic import generate_random_invoices
from app.infrastructure.stark.invoice_api import issue_invoice
from random import randint
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def invoice_job():
    """
    Job to generate and issue random invoices.
    This function generates a batch of random invoices and issues them using the StarkBank API.
    """
    logger.info("Starting invoice job...")
    try:
        invoices = generate_random_invoices(randint(8, 12))  # Generate between 1 and 5 invoices
        logger.info(f"Generated {len(invoices)} invoices to issue.")
        
        # Issue each invoice using the StarkBank API
        if not invoices:
            logger.warning("No invoices generated to issue.")
            return
        logger.info("Issuing invoices...")
        
        for invoice in invoices:
            issue_invoice(invoice)
        logger.debug(f"Issued {len(invoices)} invoices successfully.")
    except Exception as e:
        logger.error(f"Error in invoice job: {str(e)}")


def start_invoice_scheduler():
    """
    Start the background scheduler to run the invoice job periodically.
    The job is scheduled to run every 1 minute for 24 hours.
    """
    scheduler = BackgroundScheduler()
    end_time = datetime.now() + timedelta(hours=24)  # Run for 1 day
    scheduler.add_job(invoice_job, 'interval', hours=3, end_date=end_time)
    scheduler.start()
    logger.info("Invoice scheduler job started.")