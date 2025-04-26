import os
import posthog
import logging
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)

# Load environment variables using an absolute path
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Get PostHog configuration from environment variables
POSTHOG_API_KEY = os.getenv('PUBLIC_POSTHOG_KEY')
POSTHOG_HOST = os.getenv('PUBLIC_POSTHOG_HOST', 'https://us.i.posthog.com')

# Initialize PostHog
if POSTHOG_API_KEY:
    try:
        posthog.api_key = POSTHOG_API_KEY
        
        # Set the personal API key for the project
        # This is used for feature flags, experiments and more
        posthog.personal_api_key = POSTHOG_API_KEY
        
        # Configure the host where you're running PostHog
        posthog.host = POSTHOG_HOST
        
        logger.info(f"PostHog initialized with host: {POSTHOG_HOST}")
    except Exception as e:
        logger.error(f"Failed to initialize PostHog: {str(e)}")
else:
    logger.warning("PostHog API key not found in environment variables")

def capture(distinct_id, event, properties=None):
    """
    Capture an event for a user
    
    Args:
        distinct_id (str): The unique ID of the user
        event (str): The name of the event
        properties (dict, optional): Additional properties to send with the event
    """
    if not POSTHOG_API_KEY:
        logger.warning("PostHog not configured, event not captured")
        return
    
    try:
        posthog.capture(
            distinct_id=distinct_id,
            event=event,
            properties=properties or {}
        )
        logger.debug(f"Captured event '{event}' for user '{distinct_id}'")
    except Exception as e:
        logger.error(f"Failed to capture PostHog event: {str(e)}")

def identify(distinct_id, properties=None):
    """
    Identify a user with their properties
    
    Args:
        distinct_id (str): The unique ID of the user
        properties (dict, optional): User properties to associate
    """
    if not POSTHOG_API_KEY:
        logger.warning("PostHog not configured, user not identified")
        return
    
    try:
        posthog.identify(
            distinct_id=distinct_id,
            properties=properties or {}
        )
        logger.debug(f"Identified user '{distinct_id}'")
    except Exception as e:
        logger.error(f"Failed to identify user in PostHog: {str(e)}")

def group_identify(group_type, group_key, properties=None):
    """
    Associate a group with properties
    
    Args:
        group_type (str): The type of group (e.g., 'company', 'team')
        group_key (str): The unique identifier for the group
        properties (dict, optional): Group properties to associate
    """
    if not POSTHOG_API_KEY:
        logger.warning("PostHog not configured, group not identified")
        return
    
    try:
        posthog.group_identify(
            group_type=group_type,
            group_key=group_key,
            properties=properties or {}
        )
        logger.debug(f"Identified group '{group_key}' of type '{group_type}'")
    except Exception as e:
        logger.error(f"Failed to identify group in PostHog: {str(e)}") 