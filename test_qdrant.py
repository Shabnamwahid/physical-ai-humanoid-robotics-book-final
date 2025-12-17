import asyncio
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import uuid

# Configuration
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "textbook_content_test"

async def test_qdrant_connection():
    """Test Qdrant connection and basic operations"""
    print("Testing Qdrant connection...")

    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=QDRANT_URL,
            prefer_grpc=False
        )

        print(f"Connected to Qdrant at {QDRANT_URL}")

        # Test 1: Check if collection exists, create if not
        try:
            collection_info = client.get_collection(COLLECTION_NAME)
            print(f"Collection '{COLLECTION_NAME}' exists")
        except:
            print(f"Creating collection '{COLLECTION_NAME}'...")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )
            print(f"Collection '{COLLECTION_NAME}' created successfully")

        # Test 2: Initialize embedding model
        print("Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Test 3: Add a test document
        print("Adding test document...")
        test_content = "Physical AI represents the convergence of artificial intelligence with the physical world through robotic systems."

        # Generate embedding
        embedding = model.encode([test_content])[0].tolist()

        # Create a test point
        test_point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "content": test_content,
                "metadata": {
                    "source": "test_document",
                    "chapter": "Introduction",
                    "section": "Definition",
                    "created_at": "2023-12-01T00:00:00Z"
                }
            }
        )

        # Upload the point
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[test_point]
        )

        print("Test document added successfully")

        # Test 4: Search for similar content
        print("Testing search functionality...")
        search_embedding = model.encode(["What is Physical AI?"])[0].tolist()

        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=search_embedding,
            limit=1,
            with_payload=True
        )

        if search_results:
            result = search_results[0]
            print(f"Search successful! Found: {result.payload['content'][:50]}...")
            print(f"Similarity score: {result.score}")
        else:
            print("No results found")

        # Test 5: Check collection info
        collection_info = client.get_collection(COLLECTION_NAME)
        print(f"Collection points count: {collection_info.points_count}")

        print("\nAll tests passed! Qdrant is ready for use.")

        return True

    except Exception as e:
        print(f"Error during Qdrant testing: {e}")
        return False

async def cleanup_test_data():
    """Clean up test data"""
    try:
        client = QdrantClient(url=QDRANT_URL, prefer_grpc=False)

        # Delete the test collection
        client.delete_collection(COLLECTION_NAME)
        print(f"Test collection '{COLLECTION_NAME}' deleted")

    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    print("Starting Qdrant setup test...\n")

    success = asyncio.run(test_qdrant_connection())

    if success:
        print("\nWould you like to clean up test data? (y/n): ", end="")
        # Note: In an automated script, you might skip cleanup
        # For this test, we'll leave the data for the actual application to use
        print("Skipping cleanup - test data will be used by the application")
    else:
        print("\nTests failed. Please check your Qdrant setup.")