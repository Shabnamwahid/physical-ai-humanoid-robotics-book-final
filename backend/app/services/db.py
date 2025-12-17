import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.NEON_USER}:{settings.NEON_PASSWORD}"
    f"@{settings.NEON_HOST}:{settings.NEON_PORT}/{settings.NEON_DB}"
)

# async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# async session
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# helper database object
class Database:
    def __init__(self, engine):
        self.engine = engine

    async def connect(self):
        # test connection
        async with self.engine.begin() as conn:
            await conn.run_sync(lambda x: None)  # simple ping

database = Database(engine)

# dependency for routes
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
