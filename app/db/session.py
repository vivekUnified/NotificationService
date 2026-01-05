from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from app.core.config import settings

# Async Engine for FastAPI
# Note: SQLModel/SQLAlchemy async support requires async driver, e.g. postgresql+asyncpg
# Updating config to support this or handling it here.
# For simplicity, assuming the user might fix the requirement to include asyncpg or we just use sync for now if easier?
# Plan said "Async for API". So let's use asyncpg.
DATABASE_URL_ASYNC = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL_ASYNC, echo=True, future=True)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# Sync Engine for Celery
sync_engine = create_engine(settings.DATABASE_URL, echo=True)
def get_sync_session():
    with Session(sync_engine) as session:
        yield session
