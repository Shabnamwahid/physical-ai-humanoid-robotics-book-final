from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    metadata_info = Column(JSON)  # Additional metadata about the conversation

    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    metadata_info = Column(JSON)  # Additional metadata about the message
    sources = Column(JSON)  # Sources referenced in the response
    confidence = Column(Integer)  # Confidence score (0-100)

    # Relationship back to conversation
    conversation = relationship("Conversation", back_populates="messages")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String, nullable=False)  # Source file/URL
    title = Column(String, nullable=True)
    content_preview = Column(String)  # First 100 chars of content
    chapter = Column(String)  # Chapter identifier
    section = Column(String)  # Section identifier
    created_at = Column(DateTime, server_default=func.now())
    processed_at = Column(DateTime)
    is_processed = Column(Boolean, default=False)
    metadata_info = Column(JSON)  # Additional metadata
    qdrant_id = Column(String)  # ID in Qdrant vector database
    embedding_model = Column(String)  # Model used for embedding
    embedding_created = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    last_active = Column(DateTime, server_default=func.now(), onupdate=func.now())
    preferences = Column(JSON)  # User preferences
    metadata_info = Column(JSON)  # Additional metadata


class EmbeddingCache(Base):
    __tablename__ = "embedding_cache"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    text_hash = Column(String, unique=True, nullable=False)  # Hash of the original text
    text_content = Column(Text, nullable=False)  # Original text
    embedding = Column(JSON, nullable=False)  # Embedding vector as JSON
    model_name = Column(String, nullable=False)  # Name of the embedding model used
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)  # When the cache entry expires