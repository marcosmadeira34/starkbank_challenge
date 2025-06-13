# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()


def read_private_key_file():
    with open("/app/private_key.pem", "r") as f:
        return f.read()

class Setting:
    STARK_PROJECT_ID: str = os.getenv("STARK_PROJECT_ID")
    STARK_PRIVATE_KEY_VALUE: str = read_private_key_file()
    ENVIRONMENT = os.getenv("STARK_ENVIRONMENT", "sandbox")
    STARK_WEBHOOK_URL = os.getenv("STARK_WEBHOOK_URL", "https://api.localhost:8000/v2/webhook")


settings = Setting()