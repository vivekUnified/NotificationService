from celery import shared_task
from celery.utils.log import get_task_logger
from .services import ChannelFactory
from .models import NotificationLog

logger = get_task_logger(__name__)

@shared_task
def send_message(user_id, channel, destination, content):
    """
    Delivers the message using the appropriate channel adapter.
    Logs the result to the database.
    """
    logger.info(f"Attempting delivery to {user_id} via {channel}")
    
    service = ChannelFactory.get_service(channel)
    if not service:
        logger.error(f"Unsupported channel: {channel}")
        NotificationLog.objects.create(
            user_id=user_id,
            channel=channel,
            destination=destination,
            content=content,
            status='failed',
            error_message="Unsupported channel"
        )
        return False

    try:
        success = service.send(destination, content)
        status = 'sent' if success else 'failed'
        error_msg = None if success else "Delivery failed at provider"
        
        NotificationLog.objects.create(
            user_id=user_id,
            channel=channel,
            destination=destination,
            content=content,
            status=status,
            error_message=error_msg
        )
        return success
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        NotificationLog.objects.create(
            user_id=user_id,
            channel=channel,
            destination=destination,
            content=content,
            status='failed',
            error_message=str(e)
        )
        return False
