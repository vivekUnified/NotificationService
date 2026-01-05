from typing import Any, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    event_type: str
    user_id: str
    payload: Dict[str, Any] = {}
    timestamp: Optional[datetime] = None
    source: str = "system"
