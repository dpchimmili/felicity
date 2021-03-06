from typing import AsyncGenerator
from asyncio import current_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from felicity.core.config import settings


async_engine = create_async_engine(settings.SQLALCHEMY_ASYNC_DATABASE_URI, pool_pre_ping=True, echo=False, future=True)
async_session_factory = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)
AsyncSessionScoped = async_scoped_session(async_session_factory, scopefunc=current_task)


#  Async Dependency
async def get_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session


# or
async def get_db() -> AsyncGenerator:
    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except async_session_factory as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
