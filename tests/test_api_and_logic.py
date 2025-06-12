import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app 


# Initialize the FastAPI test client
client = TestClient(app)

# --- Mocks to Simulate StarkBank Behavior ---

mock_webhook_payload_credited = {
    "event": {
        "log": {
            "id": "59616010000002",
            "type": "credited", 
            "invoice": {
                "id": "inv_simulacao_21945",
                "amount": 21945,
                "name": "Cliente Teste",
                "taxId": "00000000000",
                "status": "paid",
                "created": "2024-06-10T14:00:00.000Z"
            }
        },
        "id": "59616010000001",
        "subscription": "invoice",
        "type": "credited", 
        "isDelivered": False, 
        "created": "2024-06-10T14:00:00.000Z"
    }
}

# Payload for webhook with unhandled event (e.g., subscription different from invoice)
mock_webhook_payload_unhandled_subscription = {
    "event": {
        "log": {
            "id": "log_unhandled_id",
            "type": "some_unhandled_log_type", 
        },
        "id": "event_unhandled_id",
        "subscription": "unhandled-subscription", 
        "type": "some_unhandled_event_type", 
        "isDelivered": False,
        "created": "2024-06-10T14:00:00.000Z"
    }
}


@pytest.fixture(autouse=True)
def mock_starkbank_user():
    # Mocks the StarkBank user configuration so that calls do not fail
    with patch('starkbank.user', new_callable=MagicMock) as mock_user:
        mock_user.environment = "sandbox"
        mock_user.id = "mock_project_id"
        mock_user.private_key = "mock_private_key"
        yield mock_user

@pytest.fixture
def mock_starkbank_transfer_create():
    with patch('app.infrastructure.stark.transfer_api.starkbank.transfer.create', new_callable=AsyncMock) as mock_create:
        yield mock_create



@pytest.mark.asyncio
async def test_starkbank_webhook_invoice_credited_success(mock_starkbank_transfer_create):
    mock_event_from_sdk = AsyncMock()
    mock_event_from_sdk.id = mock_webhook_payload_credited["event"]["id"]
    mock_event_from_sdk.subscription = mock_webhook_payload_credited["event"]["subscription"]
    
   
    mock_event_from_sdk.is_delivered = False 
    
    # Mocking the log and the invoice inside the event
    mock_event_from_sdk.log = AsyncMock()
    mock_event_from_sdk.log.type = "credited" 
    mock_event_from_sdk.log.invoice = AsyncMock() 
    mock_event_from_sdk.log.invoice.id = mock_webhook_payload_credited["event"]["log"]["invoice"]["id"]
    mock_event_from_sdk.log.invoice.amount = mock_webhook_payload_credited["event"]["log"]["invoice"]["amount"]
    mock_event_from_sdk.log.invoice.name = mock_webhook_payload_credited["event"]["log"]["invoice"]["name"]
    mock_event_from_sdk.log.invoice.taxId = mock_webhook_payload_credited["event"]["log"]["invoice"]["taxId"]
    
    with patch('app.infrastructure.stark.webhook_api.starkbank.event.parse', return_value=mock_event_from_sdk) as mock_event_parse:
        response = client.post( 
            "/v2/webhook",
            json=mock_webhook_payload_credited,
            headers={"Digital-Signature": "s=mock_signature_for_sdk_success"}
        )
    
    assert response.status_code == 200
    response_data = response.json() 
    assert response_data["status"] == "success" 
    assert "Webhook processed successfully, transfer initiated." in response_data["message"]
    mock_starkbank_transfer_create.assert_called_once()


@pytest.mark.asyncio
async def test_starkbank_webhook_unhandled_event():
    # Use the mocked payload for unhandled subscriptions
    mock_payload_unhandled = mock_webhook_payload_unhandled_subscription
    
    mock_event_from_sdk = AsyncMock()
    mock_event_from_sdk.id = mock_payload_unhandled["event"]["id"]
    mock_event_from_sdk.subscription = mock_payload_unhandled["event"]["subscription"]
    mock_event_from_sdk.is_delivered = False 
    
    mock_event_from_sdk.log = AsyncMock() 
    mock_event_from_sdk.log.type = mock_payload_unhandled["event"]["type"]
    
    with patch('app.infrastructure.stark.webhook_api.starkbank.event.parse', return_value=mock_event_from_sdk) as mock_event_parse:
        response = client.post( 
            "/v2/webhook",
            json=mock_payload_unhandled,
            headers={"Digital-Signature": "s=mock_signature_for_sdk_success_unhandled"}
        )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "skipped"     
    assert response_data["message"] == f"Unhandled event type: {mock_payload_unhandled['event']['type']}."

# Add a test for the 'created' scenario
@pytest.mark.asyncio
async def test_starkbank_webhook_invoice_created_event():
    mock_event_from_sdk = AsyncMock()
    mock_event_from_sdk.id = "mock_created_invoice_id"
    mock_event_from_sdk.subscription = "invoice"
    mock_event_from_sdk.is_delivered = False 
    
    mock_event_from_sdk.log = AsyncMock()
    mock_event_from_sdk.log.type = "created" 
    mock_event_from_sdk.log.invoice = AsyncMock()
    mock_event_from_sdk.log.invoice.id = "mock_invoice_created"
    mock_event_from_sdk.log.invoice.amount = 10000
    
    with patch('app.infrastructure.stark.webhook_api.starkbank.event.parse', return_value=mock_event_from_sdk) as mock_event_parse:
        response = client.post(
            "/v2/webhook",
            json={
                "event": {
                    "log": {"type": "created", "invoice": {"id": "mock_invoice_created", "amount": 10000}},
                    "subscription": "invoice",
                    "id": "mock_created_invoice_id",
                    "isDelivered": False
                }
            },
            headers={"Digital-Signature": "s=mock_signature_for_sdk_success_created"}
        )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "skipped"
    assert response_data["message"] == "Unhandled invoice event type: created."
    # Ensure that the transfer was not called
    with patch('app.infrastructure.stark.transfer_api.starkbank.transfer.create', new_callable=AsyncMock) as mock_create_transfer:
        # mock_create_transfer should not be called for 'created' events
        mock_create_transfer.assert_not_called()

# Test for is_delivered True
@pytest.mark.asyncio
async def test_starkbank_webhook_event_already_delivered():
    mock_event_from_sdk = AsyncMock()
    mock_event_from_sdk.id = "mock_already_delivered_id"
    mock_event_from_sdk.subscription = "invoice"
    mock_event_from_sdk.is_delivered = True 
    mock_event_from_sdk.log = AsyncMock() 

    with patch('app.infrastructure.stark.webhook_api.starkbank.event.parse', return_value=mock_event_from_sdk) as mock_event_parse:
        response = client.post(
            "/v2/webhook",
            json={
                "event": {
                    "log": {}, 
                    "subscription": "invoice",
                    "id": "mock_already_delivered_id",
                    "isDelivered": True
                }
            },
            headers={"Digital-Signature": "s=mock_signature_for_sdk_success_delivered"}
        )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "skipped"
    assert response_data["message"] == f"Event already delivered."
    # Ensure that the transfer was not called
    with patch('app.infrastructure.stark.transfer_api.starkbank.transfer.create', new_callable=AsyncMock) as mock_create_transfer:
        mock_create_transfer.assert_not_called()