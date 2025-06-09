import starkbank
from app.domain.entities.invoice import Invoice

def issue_invoice(invoice: Invoice):
    
    try:
        stark_invoice = starkbank.Invoice(
            amount=invoice.amount,
            name=invoice.name,
            tax_id=invoice.tax_id,
            expiration=invoice.expiration,
            tags=["auto-generated"]
        )

        created = starkbank.invoice.create([stark_invoice])
        print(f"Invoice issued: {created[0].id} for {created[0].amount} cents")
        if not created:
            raise ValueError("Failed to issue invoice api")
        return created[0]  # Return the created invoice object
    except Exception as e:
        print(f"Error issuing invoice api: {str(e)}")
        raise
    