# app/infrastructure/stark/invoice_api.py
import logging
import starkbank
from app.domain.entities.invoice import Invoice


logger = logging.getLogger(__name__)



def issue_invoice(invoice: Invoice):
    """
    Issues an invoice using the StarkBank API.
    Args:
        invoice (Invoice): The invoice object containing details to be issued.
    Returns:
        starkbank.Invoice: The created invoice object from the StarkBank API.
    Raises:
        ValueError: If the invoice cannot be issued.
        Exception: If there is an error during the API call.
    """        
    try:
        # Log invoice details before issuing
        logger.debug(f"Preparing to issue invoice for ID: {invoice.id}")
        logger.debug(f"Invoice amount: {invoice.amount}, name: {invoice.name}, tax_id: {invoice.tax_id}")
        
        # Create a StarkBank Invoice object
        stark_invoice = starkbank.Invoice(
            amount=invoice.amount,
            name=invoice.name,
            tax_id=invoice.tax_id,
            expiration=invoice.expiration,
            tags=["auto-generated"]
        )
        # Send the invoice to StarkBank API
        created = starkbank.invoice.create([stark_invoice])
        logger.info(f"Invoice issued: {created[0].id} for {created[0].amount} cents.")

        if not created:
            raise ValueError("Failed to issue invoice api")
        return created[0]  # Return the created invoice object
    except Exception as e:
        # Log any error that occurs during the process
        logger.error(f"Error issuing invoice via StarkBank API: {str(e)}", exc_info=True)
        raise
    