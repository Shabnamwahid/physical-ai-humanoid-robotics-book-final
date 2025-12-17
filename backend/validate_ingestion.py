import asyncio
import sys
from pathlib import Path
import logging

# Add the backend app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ingest_service import IngestService
from app.config.database import lifespan
from app.config.settings import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def validate_ingestion():
    """Validate that textbook content was properly ingested"""

    logger.info("Starting ingestion validation...")

    # Initialize services
    ingest_service = IngestService()

    # Test 1: Check if documents exist in the database
    logger.info("Test 1: Checking for documents in database...")

    # Get all chapters
    docs_dir = Path("../docs")
    chapter_dirs = [d for d in docs_dir.iterdir() if d.is_dir() and d.name.startswith("chapter")]

    for chapter_dir in sorted(chapter_dirs):
        chapter_title = chapter_dir.name.replace("chapter-", "").replace("-", " ").title()
        logger.info(f"  Checking chapter: {chapter_title}")

        try:
            docs = await ingest_service.get_documents_by_chapter(chapter_title)
            logger.info(f"    Found {len(docs)} documents in database for this chapter")

            for doc in docs:
                logger.info(f"      - {doc['source']}: {'Processed' if doc['is_processed'] else 'Not processed'}")

        except Exception as e:
            logger.error(f"    Error checking chapter {chapter_title}: {e}")

    # Test 2: Test the search functionality
    logger.info("\nTest 2: Testing search functionality...")

    test_queries = [
        "What is Physical AI?",
        "Humanoid robot anatomy",
        "ROS 2 architecture",
        "Gazebo simulation",
        "NVIDIA Isaac",
        "Vision Language Action systems",
        "Conversational robotics"
    ]

    # We'll test search by importing the Qdrant client directly
    from qdrant_client import QdrantClient
    from sentence_transformers import SentenceTransformer
    from app.config.settings import settings

    try:
        qdrant_client = QdrantClient(url=settings.QDRANT_URL, prefer_grpc=False)
        embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

        for query in test_queries:
            logger.info(f"  Searching for: '{query}'")

            # Generate embedding for the query
            query_embedding = embedding_model.encode([query])[0].tolist()

            # Search in Qdrant
            search_results = qdrant_client.search(
                collection_name=settings.TEXTBOOK_CONTENT_COLLECTION,
                query_vector=query_embedding,
                limit=3,
                with_payload=True
            )

            logger.info(f"    Found {len(search_results)} results")

            for i, hit in enumerate(search_results[:2]):  # Show first 2 results
                content_preview = hit.payload.get('content', '')[:100] + "..."
                source = hit.payload.get('metadata', {}).get('source', 'Unknown')
                logger.info(f"      {i+1}. Source: {source}")
                logger.info(f"         Preview: {content_preview}")

    except Exception as e:
        logger.error(f"  Error during search test: {e}")

    # Test 3: Check if collections exist
    logger.info("\nTest 3: Checking Qdrant collections...")

    try:
        qdrant_client = QdrantClient(url=settings.QDRANT_URL, prefer_grpc=False)
        collections = qdrant_client.get_collections()

        logger.info(f"  Available collections: {[col.name for col in collections.collections]}")

        # Check our textbook content collection
        try:
            collection_info = qdrant_client.get_collection(settings.TEXTBOOK_CONTENT_COLLECTION)
            logger.info(f"  '{settings.TEXTBOOK_CONTENT_COLLECTION}' collection:")
            logger.info(f"    Points count: {collection_info.points_count}")
            logger.info(f"    Config: {collection_info.config}")
        except Exception as e:
            logger.error(f"  Error accessing textbook collection: {e}")

    except Exception as e:
        logger.error(f"  Error connecting to Qdrant: {e}")

    logger.info("\nIngestion validation completed!")


async def main():
    """Main function to run the validation process"""
    try:
        # Initialize the database connection
        async with lifespan(None):
            await validate_ingestion()
    except Exception as e:
        logger.error(f"Error during validation: {e}")


if __name__ == "__main__":
    asyncio.run(main())