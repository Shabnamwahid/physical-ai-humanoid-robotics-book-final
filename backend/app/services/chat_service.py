from typing import List, Optional, Dict, Any
import logging
import uuid
from datetime import datetime
import hashlib
import openai
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.config.database import get_qdrant_client, get_db_session
from app.models.response import DocumentChunk
from app.services.database_service import DatabaseService

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.qdrant_client = get_qdrant_client()
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.db_service = DatabaseService()

            

    async def get_relevant_context(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        """Retrieve relevant context from the vector database"""
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.encode([query])[0].tolist()

            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=settings.TEXTBOOK_CONTENT_COLLECTION,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True,
                with_vectors=False,
            )

            # Convert results to DocumentChunk objects
            chunks = []
            for hit in search_results:
                chunk = DocumentChunk(
                    id=hit.id,
                    content=hit.payload.get("content", ""),
                    metadata=hit.payload.get("metadata", {}),
                    score=hit.score
                )
                chunks.append(chunk)

            return chunks

        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []

    async def get_conversation_history(self, db: AsyncSession, conversation_id: str) -> List[Dict[str, str]]:
        """Retrieve conversation history from database"""
        try:
            # Get conversation history from database
            messages = await self.db_service.get_conversation_history(db, conversation_id, limit=settings.CONTEXT_WINDOW)

            # Convert to the format expected by the LLM
            history = []
            for msg in reversed(messages):  # Reverse to get chronological order
                history.append({
                    "role": msg.role,
                    "content": msg.content
                })

            return history
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {e}")
            return []

    async def generate_response(self, query: str, context: List[DocumentChunk],
                               conversation_history: List[Dict] = None,
                               max_tokens: int = None, temperature: float = None) -> str:
        """Generate response using LLM with retrieved context"""
        try:
            # Prepare context from retrieved documents
            context_text = "\n\n".join([chunk.content for chunk in context])

            # Prepare conversation history if available
            history_context = ""
            if conversation_history and len(conversation_history) > 0:
                history_items = []
                for msg in conversation_history[-settings.CONTEXT_WINDOW:]:
                    history_items.append(f"{msg['role']}: {msg['content']}")

                if history_items:
                    history_context = "\n".join(history_items)
                    history_context = f"\nPrevious conversation:\n{history_context}\n\n"

            # Construct the full prompt
            prompt = f"""You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
            Use the following context to answer the user's question.
            If the context doesn't contain enough information, say so clearly.

            Context:
            {context_text}

            {history_context}
            Question: {query}

            Answer:"""

            # Use OpenAI API if key is available, otherwise use a local model or mock
            if settings.OPENAI_API_KEY:
                response = openai.ChatCompletion.create(
                    model=settings.LLM_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens or settings.MAX_TOKENS,
                    temperature=temperature or settings.TEMPERATURE
                )
                return response.choices[0].message['content'].strip()
            else:
                # Fallback: return context directly (in production, use a local model)
                return f"Context-based response: Based on the textbook content, {query} is related to the following concepts: {context_text[:500]}..."

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again."

    async def chat(self, query: str, conversation_id: Optional[str] = None,
                   top_k: int = 5, max_tokens: int = None,
                   temperature: float = None, context_window: int = 3) -> Dict[str, Any]:
        """Main chat method that orchestrates the entire process"""
        # Generate new conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        # Get database session
        async for db in get_db_session():
            # Retrieve conversation from database or create new one
            conversation = await self.db_service.get_conversation(db, conversation_id)
            if not conversation:
                conversation = await self.db_service.create_conversation(db)

            # Retrieve relevant context
            context = await self.get_relevant_context(query, top_k)

            # Retrieve conversation history from database
            conversation_history = await self.get_conversation_history(db, conversation_id)

            # Generate response
            response_text = await self.generate_response(
                query, context, conversation_history, max_tokens, temperature
            )

            # Add user message to conversation
            await self.db_service.add_message(
                db, conversation_id, "user", query,
                sources=[chunk.metadata.get("source", "") for chunk in context if chunk.metadata.get("source")]
            )

            # Add AI response to conversation
            sources = [chunk.metadata.get("source", "") for chunk in context if chunk.metadata.get("source")]
            confidence = None
            if context:
                avg_score = sum(chunk.score for chunk in context if chunk.score) / len([c for c in context if c.score])
                confidence = min(1.0, avg_score * 2)  # Normalize score to 0-1 range

            await self.db_service.add_message(
                db, conversation_id, "assistant", response_text,
                sources=sources,
                confidence=confidence
            )

            # Extract sources from context
            sources = [chunk.metadata.get("source", "") for chunk in context if chunk.metadata.get("source")]

            # Calculate confidence based on scores
            confidence = None
            if context:
                avg_score = sum(chunk.score for chunk in context if chunk.score) / len([c for c in context if c.score])
                confidence = min(1.0, avg_score * 2)  # Normalize score to 0-1 range

            return {
                "response": response_text,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow(),
                "sources": sources,
                "confidence": confidence
            }