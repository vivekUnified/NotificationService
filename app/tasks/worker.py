from celery.utils.log import get_task_logger
from app.tasks.celery_app import celery_app
from app.models.user_preference import UserPreference
from app.models.notification_log import NotificationLog
from app.tasks.utils import RateLimiter
from app.db.session import sync_engine
from sqlmodel import Session, select
import time

logger = get_task_logger(__name__)

# Channel Mock/Stub
class ChannelService:
    def send(self, destination: str, content: str) -> bool:
        # Simulate sending
        time.sleep(0.5)
        if "fail" in destination:
            return False
        return True

class ChannelFactory:
    @staticmethod
    def get_service(channel: str):
        # In a real app, return different implementations
        return ChannelService()

@celery_app.task(bind=True)
def process_event(self, event_data: dict):
    logger.info(f"Processing event: {event_data.get('event_type')}")
    
    user_id = event_data.get('user_id')
    # Simple formatting logic
    content = f"New event: {event_data.get('event_type')} - {event_data.get('payload', {})}"
    
    # Trigger Router
    route_notification.delay(user_id, content)

@celery_app.task
def route_notification(user_id: str, content: str):
    logger.info(f"Routing for {user_id}")
    
    channels = ['email', 'slack', 'in_app', 'teams']
    limiter = RateLimiter(limit=5, window=60)
    
    with Session(sync_engine) as session:
        for channel in channels:
            # Check Preference
            statement = select(UserPreference).where(
                UserPreference.user_id == user_id,
                UserPreference.channel == channel
            )
            pref = session.exec(statement).first()
            
            # Default to disabled if not found, as per legacy logic analysis
            if not pref or not pref.enabled:
                logger.debug(f"Channel {channel} disabled/not found for {user_id}")
                continue
                
            # Check Rate Limit
            if not limiter.is_allowed(user_id, channel):
                logger.warning(f"Rate limit exceeded for {user_id} on {channel}")
                continue
                
            # Send Message
            send_message.delay(user_id, channel, pref.destination, content)

@celery_app.task
def send_message(user_id: str, channel: str, destination: str, content: str):
    logger.info(f"Sending to {channel} for {user_id}")
    
    service = ChannelFactory.get_service(channel)
    success = service.send(destination, content)
    status = 'sent' if success else 'failed'
    error_msg = None if success else "Delivery Failed"
    
    # Log Result
    with Session(sync_engine) as session:
        log_entry = NotificationLog(
            user_id=user_id,
            channel=channel,
            destination=destination,
            content=content,
            status=status,
            error_message=error_msg
        )
        session.add(log_entry)
        session.commit()
