# app/infrastructure/stark/transfer_api.py
import starkbank
import logging

logger = logging.getLogger(__name__)


DESTINATION_ACCOUNT = {
    "bank_code": "20018183",
    "branch_code": "0001",
    "account_number": "6341320293482496",
    "name": "Stark Bank S.A.",
    "tax_id": "20.018.183/0001-80",
    "account_type": "payment"
}


async def send_transfer(invoice_id: str, amount: int):
    logger.debug(f"Attempting to send transfer for invoice ID: {invoice_id}")
    logger.debug(f"Initial transfer amount received: {amount} (type: {type(amount)})")
    
    if isinstance(amount, list):
        logger.warning(f"Amount for transfer was a list ({amount}), expected int. Using first element.")
        amount = amount[0]
        logger.debug(f"Amount after list conversion: {amount} (type: {type(amount)})")

    try:
        # Calculate the fee and net amount for the transfer
        if not isinstance(amount, int):
            raise ValueError(f"Expected amount to be an int, got {type(amount)} with value {amount}")
        if amount <= 0:
            raise ValueError(f"Invalid amount for transfer: {amount}. Must be a positive integer.")
        logger.debug(f"Calculating fee for transfer amount: {amount} cents.")
        # Assuming a 1% fee for the transfer

        fee = int(amount * 0.01)
        net_amount = amount - fee
        logger.debug(f"Net amount for transfer: {net_amount} cents.")

        # Create a transfer object with the necessary details
        transfer = starkbank.Transfer(
            amount=net_amount,
            bank_code=DESTINATION_ACCOUNT["bank_code"],
            branch_code=DESTINATION_ACCOUNT["branch_code"],
            account_number=DESTINATION_ACCOUNT["account_number"],
            tax_id=DESTINATION_ACCOUNT["tax_id"],
            name=DESTINATION_ACCOUNT["name"],
            account_type=DESTINATION_ACCOUNT["account_type"],
            tags=["transfer"]
        )

        created = starkbank.transfer.create([transfer])
        logger.info(f"Transfer created successfully: {created[0].id} for invoice {invoice_id}")
        return created[0]
    except Exception as e:
        logger.critical(f"Error sending transfer for invoice {invoice_id}: {str(e)}")
        logger.debug("Raising exception to be handled by the caller.")
        raise