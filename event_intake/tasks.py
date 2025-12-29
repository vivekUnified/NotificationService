from celery import shared_task
from traffic_control.celery import app

@shared_task
def publish_event(event_data):
    """
    Publish event to the processing queue.
    We use send_task to avoid direct dependency on notification_processor app.
    """
    # This sends the task to the queue to be picked up by the 'worker' service
    # The task name must match the one defined in notification_processor/tasks.py
    # app.send_task('notification_processor.tasks.process_event', args=[event_data])
    
    # For local dev / eager mode to work, we need to access the task from the registry
    # if we want to avoid direct import.
    if app.conf.task_always_eager:
         # In eager mode, tasks are in the registry if apps are loaded
         app.tasks['notification_processor.tasks.process_event'].delay(event_data)
    else:
         app.send_task('notification_processor.tasks.process_event', args=[event_data])
    
    return f"Event {event_data.get('event_type')} published."
