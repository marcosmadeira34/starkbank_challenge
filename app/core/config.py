import os
from dotenv import load_dotenv

load_dotenv()

class Setting:
    STARK_PROJECT_ID = os.getenv("STARK_PROJECT_ID")
    STARK_PRIVATE_KEY_PATH = os.getenv("STARK_PRIVATE_KEY_PATH")
    ENVIRONMENT = os.getenv("STARK_ENVIRONMENT", "sandbox")


settings = Setting()