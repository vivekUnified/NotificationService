from typing import List
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from app.db.session import get_session
from app.models.notification_log import NotificationLog, NotificationLogRead

router = APIRouter()

@router.get("/", response_model=List[NotificationLogRead])
async def read_logs(
    skip: int = 0, 
    limit: int = 100, 
    session: AsyncSession = Depends(get_session)
):
    # Logs are usually viewed latest first
    result = await session.exec(select(NotificationLog).order_by(desc(NotificationLog.created_at)).offset(skip).limit(limit))
    return result.all()
