from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

from config import settings

engine = create_async_engine(
    url=settings.DB_URL,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
