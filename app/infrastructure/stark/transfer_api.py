import starkbank


DESTINATION_ACCOUNT = {
    "bank_code": "20018183",
    "branch_code": "0001",
    "account_number": "6341320293482496",
    "name": "Stark Bank S.A.",
    "tax_id": "20.018.183/0001-80",
    "account_type": "payment"
}


def send_transfer(amount: int):
    try:
        fee = int(amount * 0.01) # tax simulated as 1% of the amount
        net_amount = amount - fee
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
        return created[0]  # Return the created transfer object
    except Exception as e:
        print(f"Error sending transfer: {str(e)}")
        raise

