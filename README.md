# Decoupled Notification System

A Django-based notification system designed with a modular architecture, separating event intake, notification processing, and delivery. Supports multiple channels (Email, Slack, In-App, Teams) and includes user preference management and rate limiting.

## Project Structure

*   **`traffic_control`**: Main Django project configuration.
*   **`event_intake`**: API to receive event payloads and publish them to the Message Queue.
*   **`notification_processor`**: Consumes events, formatting them and routing based on rules.
*   **`delivery_gateway`**: Handles actual delivery to external providers (stubbed).
*   **`user_preferences`**: Manages user channel settings.

## Getting Started

### Prerequisites

*   **Docker** and **Docker Compose** installed.
*   (Optional) Python 3.11+ for local development without Docker.

### Running with Docker (Recommended)

This sets up the full stack: Django (Web + Worker), PostgreSQL, Redis, and RabbitMQ.

1.  **Build and Start Services:**
    ```bash
    docker-compose up --build
    ```

2.  **Access the API:**
    The Event Intake API will be available at `http://localhost:8000/api/events/`.

3.  **Check Logs:**
    To see the processing flow (Intake -> Celery Worker -> Delivery), verify the logs:
    ```bash
    docker-compose logs -f worker
    ```

### Connecting to PostgreSQL

The PostgreSQL database is running in a Docker container named `db`.

**Credentials:**
*   **Host**: `localhost` (mapped port 5432) or `db` (internal Docker network)
*   **Port**: `5432`
*   **Username**: `postgres`
*   **Password**: `postgres`
*   **Database**: `notification_db`

**Connection URL:**
```
postgres://postgres:postgres@localhost:5432/notification_db
```

To connect via CLI:
```bash
docker-compose exec db psql -U postgres -d notification_db
```

### Running Locally (Without Docker)

For development or verification without the full container stack, the system is configured to fallback to **SQLite** and **Celery Eager Mode** (synchronous task execution).

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Apply Migrations:**
    ```bash
    # Set this to force eager mode
    export CELERY_TASK_ALWAYS_EAGER=True
    python manage.py migrate
    ```

3.  **Run Server:**
    ```bash
    export CELERY_TASK_ALWAYS_EAGER=True
    python manage.py runserver
    ```

4.  **Verify Flow:**
    Run the included verification script to simulate traffic:
    ```bash
    python verify_flow.py
    ```

## deployment

To deploy this system to a production environment (e.g., AWS, GCP, DigitalOcean):

1.  **Database**:
    *   Provision a managed PostgreSQL instance (e.g., AWS RDS).
    *   Update `DATABASE_URL` environment variable to point to the production DB.

2.  **Broker & Cache**:
    *   Provision a managed Redis or RabbitMQ instance (e.g., AWS ElastiCache, Amazon MQ).
    *   Update `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`.

3.  **Application (Web & Worker)**:
    *   Build the Docker image: `docker build -t notification-service .`
    *   Run containers (likely via Kubernetes/ECS) using the image.
    *   Ensure to set `DEBUG=0` and provide a proper `SECRET_KEY`.

4.  **Migrations**:
    *   Run migrations as part of the deployment pipeline or in an init container:
        ```bash
        python manage.py migrate
        ```
