# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Setting:
    STARK_PROJECT_ID: str = os.getenv("STARK_PROJECT_ID")
    STARK_PRIVATE_KEY_VALUE: str = os.getenv("STARK_PRIVATE_KEY_VALUE")
    ENVIRONMENT = os.getenv("STARK_ENVIRONMENT", "sandbox")
    STARK_WEBHOOK_URL = os.getenv("STARK_WEBHOOK_URL", "https://api.localhost:8000/v2/webhook")


settings = Setting()