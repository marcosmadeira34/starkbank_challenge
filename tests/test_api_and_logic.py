# ./tests/test_api_and_logic.py
import pytest
from fastapi.testclient import TestClient
import starkbank
from unittest.mock import patch, MagicMock
from app.main import app
from app.presentation.schemas.webhook import WebhookResponseSuccess
from app.domain.entities.invoice import Invoic

# Initialize the FastAPI test client
client = TestClient(app)