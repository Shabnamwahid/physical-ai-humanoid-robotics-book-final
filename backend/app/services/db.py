from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# Async PostgreSQL URL (Neon ke liye)
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.NEON_USER}:"
    f"{settings.NEON_PASSWORD}@"
    f"{settings.NEON_HOST}:"
    f"{settings.NEON_PORT}/"
    f"{settings.NEON_DB}"
)

# Async engine banao
engine = create_async_engine(DATABASE_URL, echo=False)  # echo=True rakho agar logs chahte ho

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency for routes (get_db_session)
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session