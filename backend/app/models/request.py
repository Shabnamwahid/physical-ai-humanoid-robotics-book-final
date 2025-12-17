from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's message/question")
    conversation_id: Optional[str] = Field(None, description="ID of the conversation for context")
    max_tokens: Optional[int] = Field(None, ge=1, le=4000, description="Maximum tokens for the response")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Temperature for response generation")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of similar documents to retrieve")
    context_window: Optional[int] = Field(3, ge=1, le=10, description="Number of previous messages to include as context")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI's response to the user's message")
    conversation_id: str = Field(..., description="ID of the conversation")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the response")
    sources: Optional[List[str]] = Field(None, description="Sources referenced in the response")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score of the response")


class IngestRequest(BaseModel):
    content: str = Field(..., min_length=1, description="Content to be ingested")
    source: str = Field(..., description="Source identifier for the content")
    metadata: Optional[dict] = Field(None, description="Additional metadata for the content")
    chapter: Optional[str] = Field(None, description="Chapter this content belongs to")
    section: Optional[str] = Field(None, description="Section this content belongs to")


class IngestResponse(BaseModel):
    success: bool = Field(..., description="Whether the ingestion was successful")
    document_id: str = Field(..., description="ID of the ingested document")
    message: str = Field(..., description="Status message")
    embedding_created: bool = Field(..., description="Whether an embedding was created")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status of the service")
    service: str = Field(..., description="Name of the service")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the check")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")