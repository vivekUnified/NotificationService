from fastapi import APIRouter, status
from app.models.event import EventCreate
from app.tasks.worker import process_event

router = APIRouter()

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def create_event(event: EventCreate):
    """
    Receive an event and queue it for processing.
    """
    process_event.delay(event.dict())
    return {"status": "accepted", "message": "Event queued"}
