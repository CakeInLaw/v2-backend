from typing import AsyncIterator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.settings import settings


__all__ = ["engine", "get_session", "AsyncSession", "Session"]


engine = create_async_engine(settings.db.connection_url, echo=settings.db.ECHO)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]
