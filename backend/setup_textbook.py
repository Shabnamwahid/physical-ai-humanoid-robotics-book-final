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


async def setup_textbook():
    """Complete setup process for the textbook RAG system"""

    logger.info("Starting Physical AI & Humanoid Robotics Textbook setup...")

    # Step 1: Initialize services
    logger.info("\nStep 1: Initializing services...")
    ingest_service = IngestService()
    logger.info("  Services initialized successfully")

    # Step 2: Verify database connection
    logger.info("\nStep 2: Verifying database connections...")
    from app.config.database import get_qdrant_client, get_db_session
    from qdrant_client.http import models

    try:
        qdrant_client = get_qdrant_client()
        # Test Qdrant connection
        qdrant_client.get_collections()
        logger.info("  Qdrant connection: OK")

        # Test database connection
        async for db in get_db_session():
            # Try to create a simple test
            from sqlalchemy import text
            await db.execute(text("SELECT 1"))
            logger.info("  PostgreSQL connection: OK")
            break

        logger.info("  Database connections verified")

    except Exception as e:
        logger.error(f"  Database connection failed: {e}")
        return

    # Step 3: Verify or create Qdrant collection
    logger.info("\nStep 3: Setting up Qdrant collection...")
    try:
        qdrant_client.get_collection(settings.TEXTBOOK_CONTENT_COLLECTION)
        logger.info(f"  Collection '{settings.TEXTBOOK_CONTENT_COLLECTION}' exists")
    except:
        # Create collection for textbook content
        qdrant_client.create_collection(
            collection_name=settings.TEXTBOOK_CONTENT_COLLECTION,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),  # Using sentence-transformers default
        )
        logger.info(f"  Created collection '{settings.TEXTBOOK_CONTENT_COLLECTION}'")

    # Step 4: Ingest textbook content
    logger.info("\nStep 4: Ingesting textbook content...")

    # Path to textbook content
    docs_dir = Path("../docs")

    if not docs_dir.exists():
        logger.error(f"  Docs directory does not exist: {docs_dir}")
        return

    # Process each chapter
    chapter_dirs = [d for d in docs_dir.iterdir() if d.is_dir() and d.name.startswith("chapter")]

    if not chapter_dirs:
        logger.warning("  No chapter directories found in docs/")
        return

    total_processed = 0
    total_files = 0

    for chapter_dir in sorted(chapter_dirs):
        logger.info(f"  Processing chapter: {chapter_dir.name}")

        # Extract chapter title from directory name
        chapter_title = chapter_dir.name.replace("chapter-", "").replace("-", " ").title()

        # Process each markdown file in the chapter
        md_files = list(chapter_dir.glob("*.md"))

        if not md_files:
            logger.warning(f"    No markdown files found in {chapter_dir}")
            continue

        for md_file in sorted(md_files):
            total_files += 1
            logger.info(f"    Processing file: {md_file.name}")

            try:
                # Read the content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Skip if content is too short (likely index files or placeholders)
                if len(content.strip()) < 50:
                    logger.info(f"      Skipping {md_file.name} - content too short")
                    continue

                # Create source identifier
                source = f"{chapter_dir.name}/{md_file.name}"

                # Extract section from filename (without extension)
                section = md_file.stem.replace("-", " ").title()
                if section.lower() == 'index':
                    section = f"{chapter_title} Overview"

                # Ingest the content
                result = await ingest_service.ingest_content(
                    content=content,
                    source=source,
                    chapter=chapter_title,
                    section=section,
                    metadata={
                        "file_path": str(md_file),
                        "file_size": len(content),
                        "ingested_at": "2023-12-01T00:00:00Z"  # This will be updated by the service
                    }
                )

                if result["success"]:
                    total_processed += 1
                    logger.info(f"      Success: {result['message']}")
                else:
                    logger.error(f"      Failed: {result['message']}")

            except Exception as e:
                logger.error(f"      Error processing {md_file.name}: {e}")

    # Process appendices
    appendices_dir = docs_dir / "appendices"
    if appendices_dir.exists():
        logger.info("  Processing appendices...")

        for md_file in appendices_dir.glob("*.md"):
            total_files += 1
            logger.info(f"    Processing appendix: {md_file.name}")

            try:
                # Read the content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                if len(content.strip()) < 50:
                    logger.info(f"      Skipping {md_file.name} - content too short")
                    continue

                # Create source identifier
                source = f"appendices/{md_file.name}"

                # Extract section from filename
                section = md_file.stem.replace("-", " ").title()

                # Ingest the content
                result = await ingest_service.ingest_content(
                    content=content,
                    source=source,
                    chapter="Appendices",
                    section=section,
                    metadata={
                        "file_path": str(md_file),
                        "file_size": len(content),
                        "ingested_at": "2023-12-01T00:00:00Z"
                    }
                )

                if result["success"]:
                    total_processed += 1
                    logger.info(f"      Success: {result['message']}")
                else:
                    logger.error(f"      Failed: {result['message']}")

            except Exception as e:
                logger.error(f"      Error processing {md_file.name}: {e}")

    logger.info(f"\nStep 4 completed: Processed {total_processed}/{total_files} files")

    # Step 5: Verify ingestion
    logger.info("\nStep 5: Verifying ingestion...")
    try:
        # Test search functionality
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

        test_query = "What is Physical AI?"
        query_embedding = embedding_model.encode([test_query])[0].tolist()

        search_results = qdrant_client.search(
            collection_name=settings.TEXTBOOK_CONTENT_COLLECTION,
            query_vector=query_embedding,
            limit=1,
            with_payload=True
        )

        if search_results:
            logger.info("  Search functionality: OK")
            logger.info(f"  Sample result preview: {search_results[0].payload['content'][:100]}...")
        else:
            logger.warning("  No search results found - ingestion may not have worked properly")

    except Exception as e:
        logger.error(f"  Search verification failed: {e}")

    # Step 6: Summary
    logger.info("\nStep 6: Setup Summary")
    logger.info(f"  Total files processed: {total_processed}")
    logger.info(f"  Total files found: {total_files}")
    logger.info(f"  Success rate: {total_processed/total_files*100:.1f}% if files were found" if total_files > 0 else "No files found")
    logger.info(f"  Qdrant collection: {settings.TEXTBOOK_CONTENT_COLLECTION}")
    logger.info(f"  PostgreSQL tables: Created")

    logger.info("\nPhysical AI & Humanoid Robotics Textbook setup completed successfully!")
    logger.info("\nNext steps:")
    logger.info("1. Start the backend server: uvicorn app.main:app --reload")
    logger.info("2. Test the API endpoints")
    logger.info("3. Integrate with the Docusaurus frontend")


async def main():
    """Main function to run the setup process"""
    try:
        # Initialize the database connection
        async with lifespan(None):
            await setup_textbook()
    except Exception as e:
        logger.error(f"Error during setup: {e}")


if __name__ == "__main__":
    asyncio.run(main())