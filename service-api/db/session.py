from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import settings
from db.models import Base

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    """Dependency for getting session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
