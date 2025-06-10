import starkbank


DESTINATION_ACCOUNT = {
    "bank_code": "20018183",
    "branch_code": "0001",
    "account_number": "6341320293482496",
    "name": "Stark Bank S.A.",
    "tax_id": "20.018.183/0001-80",
    "account_type": "payment"
}


def send_transfer(invoice_id: str, amount: int):
    print(f"DEBUG (send_transfer): Initial amount type: {type(amount)}, value: {amount}")
    if isinstance(amount, list):
        amount = amount[0]
        print(f"DEBUG (send_transfer): Amount after list conversion: {type(amount)}, value: {amount}")

    print(f"Preparing to send transfer for amount: {amount} cents")

    try:
        fee = int(amount * 0.01)
        print(f"DEBUG (send_transfer): Fee calculated: {fee} (type: {type(fee)})")
        net_amount = amount - fee
        print(f"DEBUG (send_transfer): Net amount calculated: {net_amount} (type: {type(net_amount)})")

        transfer = starkbank.Transfer(
            amount=net_amount,
            bank_code=DESTINATION_ACCOUNT["bank_code"],
            branch_code=DESTINATION_ACCOUNT["branch_code"],
            account_number=DESTINATION_ACCOUNT["account_number"],
            tax_id=DESTINATION_ACCOUNT["tax_id"],
            name=DESTINATION_ACCOUNT["name"],
            account_type=DESTINATION_ACCOUNT["account_type"],
            tags=["invoice-payment"]
        )

        created = starkbank.transfer.create([transfer])
        print(f"Transfer sent: {created[0].id} for {created[0].amount} cents")  
        return created[0]
    except Exception as e:
        print(f"Error sending transfer: {str(e)}")
        raise