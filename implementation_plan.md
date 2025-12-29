# Decoupled Notification System Implementation Plan

## Goal Description
Build a scalable, decoupled, and user-centric notification system based on the provided architecture. The system will handle event intake, message generation, routing based on user preferences and rate limits, and delivery via multiple channels.

## User Review Required
> [!IMPORTANT]
> - I am assuming a **Modular Monolith** structure for simplicity in a single repo, where different services are just different Django apps independent of each other as much as possible, deployed via `docker-compose` scaling.
> - **Celery** will be used as the message queue/task runner instead of raw Kafka/RabbitMQ consumers for easier integration with Django, but it fulfills the architectural requirement of decoupling.
> - **PostgreSQL**, **Redis**, and **RabbitMQ** will be set up using Docker Compose.

## Proposed Changes

### Project Structure
- `traffic_control/` (Django Project Root)
- Apps:
    - `event_intake`: Handling API requests.
    - `notification_processor`: Generator and Router logic.
    - `user_preferences`: Managing user channel settings.
    - `delivery_gateway`: Interface for Email, Slack, etc.
    - `monitoring`: Audit logging.

### Infrastructure
#### [NEW] [Dockerfile](file:///Users/Vivek.kushwaha/Documents/NotificationService/Dockerfile)
- Python 3.11 Slim base.
- Installs `requirements.txt`.
- Entrypoint script for running different commands.

#### [NEW] [docker-compose.yml](file:///Users/Vivek.kushwaha/Documents/NotificationService/docker-compose.yml)
- Services:
    - `web`: Django API (Event Intake).
    - `worker`: Celery worker (Notification Generator & Router).
    - `postgres`: Primary DB.
    - `redis`: Cache & Rate Limiting.
    - `rabbitmq`: Message Broker.

### Django Apps

#### [NEW] `event_intake`
- `views.py`: `POST /events/` endpoint.
- `serializers.py`: Validate payload (using DRF or plain Django).
- `tasks.py`: Define `publish_event` (pushed to queue).

#### [NEW] `user_preferences`
- `models.py`: `UserPreference` (User ID -> Channels, Opt-ins).
- `services.py`: `check_preference(user_id, channel)`.

#### [NEW] `notification_processor`
- `tasks.py`:
    - `process_event_task`: Acts as **Notification Generator**. Formats message. Calls Router.
    - `route_notification_task`: Acts as **Notification Router**. Checks `user_preferences` and Rate Limits (Redis). Dispatches to Gateway.

#### [NEW] `delivery_gateway`
- `services.py`: Classes for `EmailService`, `SlackService`, etc. (Mock implementations logging to stdout/DB).
- `tasks.py`: `send_message_task`.

## Verification Plan

### Automated Tests
- **Unit Tests**: Test each app's logic (Intake validation, Router preference checking).
- **Integration Test**:
    1.  Start stack with `docker-compose up`.
    2.  Run a script `verify_flow.py` that parses a sample event to `localhost:8000/api/events/`.
    3.  Check logs or an `AuditLog` table to verify the message was "delivered".

### Manual Verification
- Send a CURL request to the Event Intake service.
- Observe Docker logs for the `worker` container to see the chain: Intake -> Generator -> Router -> Delivery.
