import asyncio
import os
import sys
from pathlib import Path

# Add the backend app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ingest_service import IngestService
from app.config.database import lifespan
from app.config.settings import settings


async def ingest_textbook_content():
    """Ingest all textbook content into the vector database"""

    # Initialize services
    ingest_service = IngestService()

    # Path to textbook content
    docs_dir = Path("../docs")  # Relative to the backend directory

    # Process each chapter
    for chapter_dir in docs_dir.iterdir():
        if chapter_dir.is_dir() and chapter_dir.name.startswith("chapter"):
            print(f"Processing chapter: {chapter_dir.name}")

            # Process each markdown file in the chapter
            for md_file in chapter_dir.glob("*.md"):
                print(f"  Processing file: {md_file.name}")

                try:
                    # Read the content
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Create source identifier
                    source = f"{chapter_dir.name}/{md_file.name}"

                    # Extract chapter and section from filename/path
                    chapter = chapter_dir.name.replace("chapter-", "").replace("-", " ").title()
                    section = md_file.stem  # filename without extension

                    # Ingest the content
                    result = await ingest_service.ingest_content(
                        content=content,
                        source=source,
                        chapter=chapter,
                        section=section
                    )

                    print(f"    Result: {result['message']}")

                except Exception as e:
                    print(f"    Error processing {md_file.name}: {e}")

    print("Textbook content ingestion completed!")


if __name__ == "__main__":
    # Initialize the database connection
    asyncio.run(ingest_textbook_content())