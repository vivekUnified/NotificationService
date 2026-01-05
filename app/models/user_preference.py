from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class UserPreferenceBase(SQLModel):
    user_id: str = Field(index=True)
    channel: str = Field(index=True)
    enabled: bool = Field(default=True)
    destination: str

class UserPreference(UserPreferenceBase, table=True):
    __tablename__ = "user_preference" # Trying to match legacy if possible, but existing was app_model
    id: Optional[int] = Field(default=None, primary_key=True)

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceRead(UserPreferenceBase):
    id: int
