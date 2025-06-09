from typing import List
from app.domain.entities.invoice import Invoice
from faker import Faker
import random

fake = Faker()

def generate_random_invoices(quantity: int) -> List[Invoice]:
    invoices = []
    for _ in range(quantity):
        name = fake.name()
        tax_id = fake.cpf().replace(".", "").replace("-", "")
        amount = random.randint(5000, 50000) # Valor entre R$50,00 e R$500,00
        invoices.append(
            Invoice(
                amount=amount,
                name=name,
                tax_id=tax_id
            )
        )