# Notification System Walkthrough

## Overview
We have built a **Decoupled Notification System** using Django, Celery, and Redis (Architecture matched).
Since a local Docker environment was unavailable, the system was configured to run with **SQLite** and **Celery Eager Mode** for verification.

## Architecture Components Implemented

1.  **Event Intake Service (`event_intake`)**
    *   **Endpoint**: `POST /api/events/`
    *   **Logic**: Validates payload and publishes to Celery queue.
    *   **Decoupling**: Uses `app.send_task` (or `app.tasks` lookup in eager mode) to avoid depending on downstream apps.

2.  **Notification Processing (`notification_processor`)**
    *   **Generator**: [process_event](notification_processor/tasks.py#9-25) task. Formats the message.
    *   **Router**: [route_notification](/notification_processor/tasks.py#26-66) task.
    *   **Logic**:
        *   Checks **User Preferences** (PostgreSQL/SQLite).
        *   Checks **Rate Limits** (Redis - configured to fail-open if Redis is missing).
        *   Dispatches to Delivery Gateway.

3.  **Delivery Gateway (`delivery_gateway`)**
    *   **Adapters**: Email, Slack, In-App, Teams (Stub implementations).
    *   **Logging**: Records status in [NotificationLog](delivery_gateway/models.py#3-21).

4.  **Supporting Services**
    *   **User Preferences**: Stores channel opt-ins.
    *   **Rate Limiter**: Configured in [traffic_control/utils.py](traffic_control/utils.py).

## Verification Results

We verified the flow using [verify_flow.py](verify_flow.py), which simulated:
1.  Setting up user preferences for Email and Slack.
2.  Sending an `ORDER_CREATED` event.
3.  Waiting for processing.
4.  Checking [NotificationLog](delivery_gateway/models.py#3-21) for successful delivery.

**Output:**
```
Found 2 notification logs:
 - email: sent
 - slack: sent
```

## How to Run Locally

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Migrations**:
    ```bash
    # Ensure Eager mode if Redis is not running
    export CELERY_TASK_ALWAYS_EAGER=True
    python manage.py migrate
    ```

3.  **Start Server**:
    ```bash
    export CELERY_TASK_ALWAYS_EAGER=True
    python manage.py runserver
    ```

4.  **Run Verification**:
    ```bash
    python verify_flow.py
    ```

## Notes on Local Dev
*   **Redis**: If running without Redis, the Rate Limiter will log an error but allow the request (Fail Open).
*   **Celery**: In `ALWAYS_EAGER=True` mode, tasks run synchronously.
*   **Task Discovery**: We added a workaround in [traffic_control/urls.py](traffic_control/urls.py) to force task registration in Eager mode.
