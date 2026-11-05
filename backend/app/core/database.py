"""SQLAlchemy async engine + session factory."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _make_engine():
    settings.ensure_dirs()
    url = settings.db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    return create_async_engine(
        url,
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )


engine = _make_engine()
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
