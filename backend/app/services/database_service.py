from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.database import Conversation, Message, Document, User, EmbeddingCache
from app.config.database import get_db_session

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self):
        pass

    async def create_conversation(self, db: AsyncSession, metadata: Optional[Dict] = None) -> Conversation:
        """Create a new conversation record"""
        try:
            conversation = Conversation(metadata_info=metadata)
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)
            return conversation
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating conversation: {e}")
            raise

    async def get_conversation(self, db: AsyncSession, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        try:
            result = await db.execute(
                select(Conversation)
                .options(selectinload(Conversation.messages))
                .where(Conversation.id == conversation_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting conversation: {e}")
            raise

    async def add_message(self, db: AsyncSession, conversation_id: str, role: str,
                         content: str, sources: Optional[List[str]] = None,
                         confidence: Optional[float] = None,
                         metadata: Optional[Dict] = None) -> Message:
        """Add a message to a conversation"""
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                sources=sources,
                confidence=int(confidence * 100) if confidence else None,  # Store as integer percentage
                metadata_info=metadata
            )
            db.add(message)
            await db.commit()
            await db.refresh(message)
            return message
        except Exception as e:
            await db.rollback()
            logger.error(f"Error adding message: {e}")
            raise

    async def get_conversation_history(self, db: AsyncSession, conversation_id: str,
                                     limit: int = 10) -> List[Message]:
        """Get conversation history"""
        try:
            result = await db.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            raise

    async def create_document(self, db: AsyncSession, source: str, title: Optional[str] = None,
                             content_preview: Optional[str] = None, chapter: Optional[str] = None,
                             section: Optional[str] = None, metadata: Optional[Dict] = None,
                             qdrant_id: Optional[str] = None, embedding_model: Optional[str] = None) -> Document:
        """Create a document record"""
        try:
            document = Document(
                source=source,
                title=title,
                content_preview=content_preview,
                chapter=chapter,
                section=section,
                metadata_info=metadata,
                qdrant_id=qdrant_id,
                embedding_model=embedding_model
            )
            db.add(document)
            await db.commit()
            await db.refresh(document)
            return document
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating document: {e}")
            raise

    async def get_document_by_source(self, db: AsyncSession, source: str) -> Optional[Document]:
        """Get a document by source"""
        try:
            result = await db.execute(
                select(Document).where(Document.source == source)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting document by source: {e}")
            raise

    async def update_document_processed(self, db: AsyncSession, source: str) -> Optional[Document]:
        """Mark a document as processed"""
        try:
            stmt = (
                update(Document)
                .where(Document.source == source)
                .values(processed_at=datetime.utcnow(), is_processed=True)
            )
            await db.execute(stmt)
            await db.commit()

            # Return the updated document
            return await self.get_document_by_source(db, source)
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating document processed status: {e}")
            raise

    async def create_user(self, db: AsyncSession, username: str, email: str,
                         preferences: Optional[Dict] = None, metadata: Optional[Dict] = None) -> User:
        """Create a user record"""
        try:
            user = User(
                username=username,
                email=email,
                preferences=preferences,
                metadata_info=metadata
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating user: {e}")
            raise

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email"""
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            raise

    async def cache_embedding(self, db: AsyncSession, text_hash: str, text_content: str,
                             embedding: List[float], model_name: str,
                             expires_at: Optional[datetime] = None) -> EmbeddingCache:
        """Cache an embedding to avoid recomputation"""
        try:
            cache_entry = EmbeddingCache(
                text_hash=text_hash,
                text_content=text_content,
                embedding=embedding,
                model_name=model_name,
                expires_at=expires_at
            )
            db.add(cache_entry)
            await db.commit()
            await db.refresh(cache_entry)
            return cache_entry
        except Exception as e:
            await db.rollback()
            logger.error(f"Error caching embedding: {e}")
            raise

    async def get_cached_embedding(self, db: AsyncSession, text_hash: str) -> Optional[EmbeddingCache]:
        """Get a cached embedding by text hash"""
        try:
            result = await db.execute(
                select(EmbeddingCache)
                .where(EmbeddingCache.text_hash == text_hash)
                .where(EmbeddingCache.expires_at.is_(None) | (EmbeddingCache.expires_at > datetime.utcnow()))
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting cached embedding: {e}")
            raise

    async def get_recent_conversations(self, db: AsyncSession, user_email: str,
                                     limit: int = 10) -> List[Conversation]:
        """Get recent conversations for a user (would need user association in real implementation)"""
        try:
            # This is a simplified version - in a full implementation, you'd have a user_id field
            result = await db.execute(
                select(Conversation)
                .order_by(Conversation.updated_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting recent conversations: {e}")
            raise

    async def get_documents_by_chapter(self, db: AsyncSession, chapter: str) -> List[Document]:
        """Get all documents for a specific chapter"""
        try:
            result = await db.execute(
                select(Document)
                .where(Document.chapter == chapter)
                .order_by(Document.section)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting documents by chapter: {e}")
            raise