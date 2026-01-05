# Notification Service

A modern notification system built with FastAPI and React.

## Running Locally (No Docker)

### Prerequisites

Ensure you have the following installed and running:
1.  **PostgreSQL** (Port 5432) - Create DB `notification_db`.
2.  **Redis** (Port 6379).
3.  **RabbitMQ** (Port 5672).
4.  **Node.js 20+** (Use `nvm use 20`).
5.  **Python 3.10+**.

### 1. Setup Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file if needed (see app/core/config.py for defaults)
# start API server
uvicorn app.main:app --reload
```

### 2. Start Worker

```bash
# In a new terminal
celery -A app.tasks.celery_app worker -l info
```

### 3. Start Frontend

```bash
cd client
nvm use 20
npm install
npm run dev
```

Visit **http://localhost:5173** for the Dashboard.