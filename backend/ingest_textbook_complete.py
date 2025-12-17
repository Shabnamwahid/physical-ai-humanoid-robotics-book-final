import asyncio
import os
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


async def ingest_textbook_content():
    """Ingest all textbook content into the vector database"""

    logger.info("Starting textbook content ingestion...")

    # Initialize services
    ingest_service = IngestService()

    # Path to textbook content
    docs_dir = Path("../docs")  # Relative to the backend directory

    if not docs_dir.exists():
        logger.error(f"Docs directory does not exist: {docs_dir}")
        return

    # Process each chapter
    chapter_dirs = [d for d in docs_dir.iterdir() if d.is_dir() and d.name.startswith("chapter")]

    if not chapter_dirs:
        logger.warning("No chapter directories found in docs/")
        return

    for chapter_dir in sorted(chapter_dirs):
        logger.info(f"Processing chapter: {chapter_dir.name}")

        # Extract chapter title from directory name
        chapter_title = chapter_dir.name.replace("chapter-", "").replace("-", " ").title()

        # Process each markdown file in the chapter
        md_files = list(chapter_dir.glob("*.md"))

        if not md_files:
            logger.warning(f"No markdown files found in {chapter_dir}")
            continue

        for md_file in sorted(md_files):
            logger.info(f"  Processing file: {md_file.name}")

            try:
                # Read the content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Skip if content is too short (likely index files or placeholders)
                if len(content.strip()) < 50:
                    logger.info(f"    Skipping {md_file.name} - content too short")
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

                logger.info(f"    Result: {result['message']}")

            except Exception as e:
                logger.error(f"    Error processing {md_file.name}: {e}")

    # Process appendices
    appendices_dir = docs_dir / "appendices"
    if appendices_dir.exists():
        logger.info("Processing appendices...")

        for md_file in appendices_dir.glob("*.md"):
            logger.info(f"  Processing appendix: {md_file.name}")

            try:
                # Read the content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                if len(content.strip()) < 50:
                    logger.info(f"    Skipping {md_file.name} - content too short")
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

                logger.info(f"    Result: {result['message']}")

            except Exception as e:
                logger.error(f"    Error processing {md_file.name}: {e}")

    logger.info("Textbook content ingestion completed!")


async def main():
    """Main function to run the ingestion process"""
    try:
        # Initialize the database connection
        async with lifespan(None):
            await ingest_textbook_content()
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")


if __name__ == "__main__":
    asyncio.run(main())