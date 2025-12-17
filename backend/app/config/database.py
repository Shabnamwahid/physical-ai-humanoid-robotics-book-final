from contextlib import asynccontextmanager
from typing import AsyncGenerator
from qdrant_client import QdrantClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.config.settings import settings
from app.models.database import Base
import logging

logger = logging.getLogger(__name__)

# Qdrant client
qdrant_client = None

# Database engine and session
async_engine = None
AsyncSessionFactory = None


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for Neon PostgreSQL"""
    global AsyncSessionFactory
    if AsyncSessionFactory is None:
        raise RuntimeError("Database session factory not initialized")

    async with AsyncSessionFactory() as session:
        yield session


def get_qdrant_client():
    """Get Qdrant client for vector database operations"""
    global qdrant_client
    if qdrant_client is None:
        qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False  # Set to True if using gRPC
        )
    return qdrant_client


async def init_db():
    """Initialize database connections and create tables"""
    global async_engine, AsyncSessionFactory

    # Initialize Qdrant
    qdrant_client = get_qdrant_client()

    # Test Qdrant connection
    try:
        qdrant_client.get_collections()
        logger.info("Successfully connected to Qdrant")
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")
        raise

    # Initialize Neon PostgreSQL connection
    try:
        async_engine = create_async_engine(
            settings.NEON_DATABASE_URL,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )

        AsyncSessionFactory = sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        # Create all tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Successfully connected to Neon PostgreSQL and created tables")
    except Exception as e:
        logger.error(f"Failed to connect to Neon PostgreSQL: {e}")
        raise


@asynccontextmanager
async def lifespan(app):
    """Application lifespan manager"""
    # Startup
    await init_db()

    # Create Qdrant collection if it doesn't exist
    qdrant = get_qdrant_client()
    try:
        qdrant.get_collection(settings.TEXTBOOK_CONTENT_COLLECTION)
        logger.info(f"Collection {settings.TEXTBOOK_CONTENT_COLLECTION} exists")
    except:
        # Create collection for textbook content
        qdrant.create_collection(
            collection_name=settings.TEXTBOOK_CONTENT_COLLECTION,
            vectors_config={"size": 384, "distance": "Cosine"},  # Using sentence-transformers default
        )
        logger.info(f"Created collection {settings.TEXTBOOK_CONTENT_COLLECTION}")

    yield  # Application runs here

    # Shutdown
    if async_engine:
        await async_engine.dispose()
    logger.info("Database connections closed")