import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/locker_dev"
)

engine = create_async_engine(
    DATABASE_URL,
)  # echo=True
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
