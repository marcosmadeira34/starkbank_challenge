# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Setting:
    STARK_PROJECT_ID: str = os.getenv("STARK_PROJECT_ID")
    STARK_PRIVATE_KEY_VALUE: str = os.getenv("STARK_PRIVATE_KEY_VALUE")
    ENVIRONMENT = os.getenv("STARK_ENVIRONMENT", "sandbox")
    STARK_WEBHOOK_URL = os.getenv("STARK_WEBHOOK_URL", "https//ec2-3-136-131-161.us-east-2.compute.amazonaws.com/v2/webhook")


settings = Setting()