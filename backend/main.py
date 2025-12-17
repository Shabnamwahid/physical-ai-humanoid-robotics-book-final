from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routes import chat, ingest
from app.config.settings import settings
# from app.services.db import database  # ye line hata di
from qdrant_client import QdrantClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

qdrant_client: QdrantClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global qdrant_client
    logger.info("Starting RAG Chatbot API...")

    # Qdrant
    qdrant_client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        check_compatibility=False
    )

    # Database connect ki zarurat nahi abhi (Neon optional hai metadata ke liye, RAG Qdrant pe chalega)
    
    yield

    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="Physical AI & Humanoid Robotics RAG Chatbot API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
def root():
    return {"status": "RAG API running"}

@app.get("/health")
def health():
    return {"status": "ok"}