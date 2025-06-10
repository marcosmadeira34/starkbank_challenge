# app/scheduler/invoice_job.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.domain.services.invoice_logic import generate_random_invoices
from app.infrastructure.stark.invoice_api import issue_invoice

from random import randint


def invoice_job():
    """
    Job to generate and issue random invoices.
    This function generates a batch of random invoices and issues them using the StarkBank API.
    """
    print("Starting routine to issue random invoices...")
    try:
        invoices = generate_random_invoices(randint(8, 12))  # Generate between 1 and 5 invoices
        for invoice in invoices:
            issue_invoice(invoice)
        print(f"Successfully issued {len(invoices)} invoices job.")
    except Exception as e:
        print(f"Error issuing invoices job: {str(e)}")


def start_invoice_scheduler():
    """
    Start the background scheduler to run the invoice job periodically.
    The job is scheduled to run every 10 minutes.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(invoice_job, 'interval', hours=3)
    scheduler.start()
    print("Invoice scheduler job started.") 