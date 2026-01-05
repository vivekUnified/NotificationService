from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.session import get_session
from app.models.user_preference import UserPreference, UserPreferenceCreate, UserPreferenceRead

router = APIRouter()

@router.post("/", response_model=UserPreferenceRead)
async def create_preference(
    preference: UserPreferenceCreate, 
    session: AsyncSession = Depends(get_session)
):
    db_pref = UserPreference.from_orm(preference)
    session.add(db_pref)
    await session.commit()
    await session.refresh(db_pref)
    return db_pref

@router.get("/", response_model=List[UserPreferenceRead])
async def read_preferences(
    skip: int = 0, 
    limit: int = 100, 
    session: AsyncSession = Depends(get_session)
):
    result = await session.exec(select(UserPreference).offset(skip).limit(limit))
    return result.all()

@router.get("/{user_id}", response_model=List[UserPreferenceRead])
async def read_user_preferences(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.exec(select(UserPreference).where(UserPreference.user_id == user_id))
    return result.all()
