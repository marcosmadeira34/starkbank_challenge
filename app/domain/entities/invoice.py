from datetime import datetime
from uuid import uuid4

class Invoice:
    def __init__(self, amount: int, name: str, tax_id: str, expiration: int = 3600):
        self.id = str(uuid4())
        self.amount = amount
        self.name = name
        self.tax_id = tax_id
        self.expiration = expiration  # em segundos
        self.created_at = datetime.now()

    def is_valid(self):
        return all(
            [
                isinstance(self.amount, int) and self.amount > 0,
                isinstance(self.name, str) and self.name.strip() != "",
                isinstance(self.tax_id, str) and len(self.tax_id) in [11, 14]  # CPF ou CNPJ
            ])