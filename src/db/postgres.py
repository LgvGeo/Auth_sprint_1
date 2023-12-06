from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings.config import PostgresSettings

pg_settings = PostgresSettings()
dsn = (
    f'postgresql+asyncpg://{pg_settings.user}:{pg_settings.password}'
    f'@{pg_settings.host}:{pg_settings.port}/{pg_settings.db}'
)
engine = create_async_engine(dsn, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
