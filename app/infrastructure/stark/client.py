# app/infrastructure/stark/client.py
import starkbank
from app.core.config import settings
from colorama import Fore, Style
from starkcore import error as starkcore
import logging


logger = logging.getLogger(__name__)

def initialize_stark_client():
    try:
        with open(settings.STARK_PRIVATE_KEY_PATH, "r") as file:
            private_key = file.read()

        starkbank.user = starkbank.Project(
            environment=settings.ENVIRONMENT,
            id=settings.STARK_PROJECT_ID,
            private_key=private_key
        )

        logger.info(f"StarkBank client initialized with project ID: {starkbank.user.id}")
    except Exception as e:
        logger.critical(f"Error initializing StarkBank client: {e}", exc_info=True)
        raise 


# Create a webhook client 
def initialize_webhook_client():
    """
    Initializes the StarkBank webhook client with the specified URL and subscriptions.
    If a webhook with the same URL and subscriptions already exists, it reuses that webhook.
    If no matching webhook is found, it creates a new one.
    """
    
    webhook_url = settings.STARK_WEBHOOK_URL
    desired_subscriptions = ['boleto', 'invoice', 'transfer']
    logger.info(f"Attempting to initialize webhook for URL: {webhook_url} with subscriptions: {desired_subscriptions}")

    try:
        # 1. Query ALL webhooks (without the 'url' argument)
        # Use a reasonable `limit` if you have many webhooks to avoid loading everything
        all_existing_webhooks = starkbank.webhook.query(user=starkbank.user) # Removido 'url=webhook_url'
        
        found_webhook = None
        for webhook in all_existing_webhooks:
            # 2. Locally filter by URL and check if the webhook has ALL the desired subscriptions
            if webhook.url == webhook_url and all(sub in webhook.subscriptions for sub in desired_subscriptions):
                found_webhook = webhook
                break  # Found it, can exit the loop
        
        if found_webhook:
            # If a matching webhook was found, it is reused
            logger.info(f"Webhook client already exists with URL: {webhook_url}, ID: {found_webhook.id}. Reusing it.")
        else:
            # If NO matching webhook was found, create a new one
            new_webhook = starkbank.webhook.create(
                url=webhook_url,
                subscriptions=desired_subscriptions,
                user=starkbank.user
            )
            logger.info(f"Webhook client created with ID: {new_webhook.id}, URL: {new_webhook.url}")
            
    except starkcore as e:
        if any(err.code == 'invalidUrl' and 'already registered' in err.message for err in e.errors):
            logger.warning(f"Webhook URL {webhook_url} is already registered. This might happen during \
                           development restarts. Please ensure the webhook is unique or handle reuse carefully.")
        else:
            print(Fore.LIGHTRED_EX + f"Error initializing webhook client: {e}" + Style.RESET_ALL)
            raise 
    except Exception as e:
        logger.error(f"Unexpected error initializing webhook client: {e}", exc_info=True)
        raise 



