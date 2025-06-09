import starkbank
from app.core.config import settings


def initialize_stark_client():
    with open(settings.STARK_PRIVATE_KEY_PATH, "r") as file:
        private_key = file.read()

    starkbank.user = starkbank.Project(
        environment=settings.ENVIRONMENT,
        id=settings.STARK_PROJECT_ID,
        private_key=private_key
    )

