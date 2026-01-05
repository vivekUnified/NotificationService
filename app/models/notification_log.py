from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class NotificationLogBase(SQLModel):
    user_id: str = Field(index=True)
    channel: str
    destination: str
    content: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class NotificationLog(NotificationLogBase, table=True):
    __tablename__ = "notification_log"
    id: Optional[int] = Field(default=None, primary_key=True)

class NotificationLogRead(NotificationLogBase):
    id: int
