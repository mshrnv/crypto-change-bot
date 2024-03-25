"""Database"""
from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4

from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from bot.core.config import settings
from .models import Base

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class CConnection(Connection):
    """Connection class"""

    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"


def get_engine(url: URL | str = settings.database_url) -> AsyncEngine:
    """Returns database engine instance"""
    return create_async_engine(
        url=url,
        echo=settings.DEBUG,
        pool_size=0,
        connect_args={
            "connection_class": CConnection,
        },
    )


def get_sessionmaker(_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Returns sessionmaker instance"""
    return async_sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)


async def async_main(_engine: AsyncEngine):
    """Syncing database state"""
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


db_url = settings.database_url
engine = get_engine(url=db_url)
sessionmaker = get_sessionmaker(engine)
