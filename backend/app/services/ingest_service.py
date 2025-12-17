from typing import List, Optional, Dict, Any
import logging
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.config.database import get_qdrant_client, get_db_session
from app.utils.text_processor import chunk_text
from app.services.database_service import DatabaseService

logger = logging.getLogger(__name__)


class IngestService:
    def __init__(self):
        self.qdrant_client = get_qdrant_client()
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.db_service = DatabaseService()

    async def ingest_content(self, content: str, source: str,
                           metadata: Optional[Dict] = None,
                           chapter: Optional[str] = None,
                           section: Optional[str] = None) -> Dict[str, Any]:
        """Ingest content into the vector database and track in PostgreSQL"""
        try:
            # Set default metadata if not provided
            if metadata is None:
                metadata = {}

            # Add chapter and section to metadata if provided
            if chapter:
                metadata['chapter'] = chapter
            if section:
                metadata['section'] = section

            # Get database session
            async for db in get_db_session():
                # Check if document already exists in database
                existing_doc = await self.db_service.get_document_by_source(db, source)
                if existing_doc:
                    return {
                        "success": True,
                        "document_id": existing_doc.id,
                        "message": f"Document {source} already exists in database",
                        "embedding_created": existing_doc.embedding_created
                    }

                # Create document record in database (not yet processed)
                document = await self.db_service.create_document(
                    db, source,
                    title=section or source.split('/')[-1].replace('.md', '').replace('-', ' ').title(),
                    content_preview=content[:100] + "..." if len(content) > 100 else content,
                    chapter=chapter,
                    section=section,
                    metadata=metadata
                )

                # Chunk the content into smaller pieces
                chunks = chunk_text(content, chunk_size=512, overlap=64)

                # Process each chunk
                successful_chunks = 0
                for i, chunk in enumerate(chunks):
                    # Generate embedding for the chunk
                    embedding = self.embedding_model.encode([chunk])[0].tolist()

                    # Create metadata for this specific chunk
                    chunk_metadata = {
                        **metadata,
                        'source': source,
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        'created_at': datetime.utcnow().isoformat(),
                        'content_preview': chunk[:100] + "..." if len(chunk) > 100 else chunk,
                        'document_id': document.id  # Link to document record
                    }

                    # Generate a unique ID for this chunk
                    chunk_id = str(uuid.uuid5(
                        uuid.NAMESPACE_DNS,
                        f"{source}_{i}_{chunk[:50]}"
                    ))

                    # Upsert into Qdrant
                    self.qdrant_client.upsert(
                        collection_name=settings.TEXTBOOK_CONTENT_COLLECTION,
                        points=[
                            models.PointStruct(
                                id=chunk_id,
                                vector=embedding,
                                payload={
                                    'content': chunk,
                                    'metadata': chunk_metadata
                                }
                            )
                        ]
                    )

                    successful_chunks += 1

                # Update document record to mark as processed
                updated_doc = await self.db_service.update_document_processed(db, source)

                return {
                    "success": True,
                    "document_id": updated_doc.id,
                    "message": f"Successfully ingested {successful_chunks} chunks from {source}",
                    "embedding_created": successful_chunks > 0
                }

        except Exception as e:
            logger.error(f"Error ingesting content: {e}")
            return {
                "success": False,
                "document_id": "",
                "message": f"Error ingesting content: {str(e)}",
                "embedding_created": False
            }

    async def batch_ingest(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ingest multiple contents in batch"""
        results = []
        for content_data in contents:
            result = await self.ingest_content(
                content=content_data.get('content', ''),
                source=content_data.get('source', 'unknown'),
                metadata=content_data.get('metadata'),
                chapter=content_data.get('chapter'),
                section=content_data.get('section')
            )
            results.append(result)
        return results

    async def check_content_exists(self, content: str, source: str) -> bool:
        """Check if content already exists in the database"""
        try:
            # Get database session
            async for db in get_db_session():
                # Check if document exists in database
                existing_doc = await self.db_service.get_document_by_source(db, source)
                if existing_doc:
                    return True

            # If not in database, check Qdrant
            # Generate embedding for the content
            embedding = self.embedding_model.encode([content])[0].tolist()

            # Search for similar content
            search_results = self.qdrant_client.search(
                collection_name=settings.TEXTBOOK_CONTENT_COLLECTION,
                query_vector=embedding,
                limit=1,
                with_payload=True,
                score_threshold=0.95  # High threshold for near-duplicate detection
            )

            # Check if any result matches the same source
            for hit in search_results:
                if hit.payload.get('metadata', {}).get('source') == source:
                    return True

            return False

        except Exception as e:
            logger.error(f"Error checking content existence: {e}")
            return False

    async def get_documents_by_chapter(self, chapter: str) -> List[Dict[str, Any]]:
        """Get all documents for a specific chapter"""
        try:
            async for db in get_db_session():
                documents = await self.db_service.get_documents_by_chapter(db, chapter)

                result = []
                for doc in documents:
                    result.append({
                        "id": doc.id,
                        "source": doc.source,
                        "title": doc.title,
                        "chapter": doc.chapter,
                        "section": doc.section,
                        "created_at": doc.created_at,
                        "processed_at": doc.processed_at,
                        "is_processed": doc.is_processed,
                        "metadata": doc.metadata_info
                    })

                return result
        except Exception as e:
            logger.error(f"Error getting documents by chapter: {e}")
            return []