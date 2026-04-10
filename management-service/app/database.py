from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_factory = async_sessionmaker[AsyncSession](engine, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
