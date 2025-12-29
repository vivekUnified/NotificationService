import os
import django
import time
import requests
import sys

# Setup Django environment for direct DB access if needed, 
# although we will mostly test via API.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic_control.settings")
django.setup()

from user_preferences.models import UserPreference
from delivery_gateway.models import NotificationLog

def verify_flow():
    user_id = "test_user_123"
    api_url = "http://localhost:8000/api/events/"
    
    # 1. Setup Preferences
    print("Setting up user preferences...")
    UserPreference.objects.filter(user_id=user_id).delete()
    UserPreference.objects.create(user_id=user_id, channel='email', destination='user@example.com', enabled=True)
    UserPreference.objects.create(user_id=user_id, channel='slack', destination='#general', enabled=True)
    
    # 2. Send Event
    payload = {
        "event_type": "ORDER_CREATED",
        "user_id": user_id,
        "payload": {"order_id": "999", "amount": 50.0},
        "source": "checkout_service"
    }
    
    print(f"Sending event to {api_url}...")
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 202:
            print("Event accepted by API.")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Is the server running?")
        return

    # 3. Wait for processing (Celery is async)
    print("Waiting for processing (10s)...")
    time.sleep(10)
    
    # 4. Check Logs
    print("Checking Notification Logs...")
    logs = NotificationLog.objects.filter(user_id=user_id)
    if logs.exists():
        print(f"Found {logs.count()} notification logs:")
        for log in logs:
            print(f" - {log.channel}: {log.status}")
    else:
        print("No notification logs found. Processing might have failed or is too slow.")
        # Check if rate limit was hit? (First run shouldn't be)

if __name__ == "__main__":
    verify_flow()
