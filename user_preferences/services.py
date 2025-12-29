from .models import UserPreference
import logging

logger = logging.getLogger(__name__)

def check_user_preference(user_id, channel):
    """
    Check if a user has enabled a specific channel.
    Returns:
        (bool, str): (is_enabled, destination)
    """
    try:
        pref = UserPreference.objects.get(user_id=user_id, channel=channel)
        return pref.enabled, pref.destination
    except UserPreference.DoesNotExist:
        # Default behavior: if no preference set, assume disabled or default?
        # For this system, let's assume disabled if not explicitly set to avoid spam,
        # OR enabled if it's a critical system. 
        # Let's go with False for safety unless we have a default system.
        logger.debug(f"No preference found for {user_id} on {channel}. Defaulting to False.")
        return False, None
