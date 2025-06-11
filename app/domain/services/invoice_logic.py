# app/domain/services/invoice_logic.py
import logging
import random
from typing import List

from faker import Faker

from app.domain.entities.invoice import Invoice

logger = logging.getLogger(__name__)

# initialize Faker with Brazilian locale
fake = Faker('pt_BR')

def generate_random_invoices(quantity: int) -> List[Invoice]:
    """
    Generate a list of random invoices.
    :param quantity: Number of invoices to generate.
    :return: List of Invoice objects.
    """
    invoices = []
    for _ in range(quantity):
        name = fake.name()  # Generate a random Brazilian name
        tax_id = fake.cpf()  # Generate a random CPF (Brazilian tax ID)
        amount = random.randint(5000, 50000)  # Amount between R$50.00 and R$500.00 (in cents)
        invoices.append(
            Invoice(
                amount=amount,
                name=name,
                tax_id=tax_id
            )
        )
    logger.info(f"Generated {len(invoices)} random invoices.")
    return invoices