from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class IngestResponse(BaseModel):
    success: bool
    document_id: str
    message: str
    embedding_created: bool


class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    detail: str


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    count: int
    query: str


class DocumentChunk(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    score: Optional[float] = None