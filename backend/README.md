# Physical AI & Humanoid Robotics RAG Chatbot Backend

This is the backend service for the Physical AI & Humanoid Robotics textbook RAG (Retrieval-Augmented Generation) chatbot. It provides APIs for chatting with the textbook content and ingesting new content into the vector database.

## Architecture

The backend is built with FastAPI and follows a service-oriented architecture:

- **API Layer**: FastAPI routes handling HTTP requests
- **Service Layer**: Business logic for chat and content ingestion
- **Data Layer**: Qdrant vector database and Neon PostgreSQL
- **Utility Layer**: Text processing and helper functions

## Features

- RAG-based Q&A system for textbook content
- Content ingestion pipeline
- Vector similarity search
- Conversation history management
- API rate limiting and health checks

## Prerequisites

- Python 3.8+
- Qdrant vector database
- Neon PostgreSQL database (optional for this implementation)
- OpenAI API key (optional, fallback to local models)

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Create a `.env` file with the following variables:

```env
# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here  # Optional

# Neon PostgreSQL Configuration
NEON_DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/dbname

# API Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# AI Configuration
OPENAI_API_KEY=your_openai_api_key  # Optional
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7

# Application Configuration
TEXTBOOK_CONTENT_COLLECTION=textbook_content
CONVERSATION_HISTORY_COLLECTION=conversations
CONTEXT_WINDOW=5

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001", "https://your-domain.com"]
```

## Running the Application

### Development

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```bash
# Build the image
docker build -t rag-chatbot-backend .

# Run the container
docker run -p 8000:8000 -e QDRANT_URL=http://your-qdrant-url rag-chatbot-backend
```

## API Endpoints

### Chat API

- `POST /api/v1/chat` - Main chat endpoint
- `GET /api/v1/chat/health` - Health check for chat service

### Ingest API

- `POST /api/v1/ingest` - Ingest single content
- `POST /api/v1/ingest/batch` - Ingest multiple contents
- `GET /api/v1/ingest/health` - Health check for ingest service

### General API

- `GET /` - Root endpoint
- `GET /health` - General health check

## Ingesting Textbook Content

To ingest the textbook content:

```bash
python ingest_textbook.py
```

This will process all markdown files in the `../docs` directory and add them to the vector database.

## Testing

Run the tests:

```bash
pytest
```

## Environment Setup

### Qdrant

You can run Qdrant locally using Docker:

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### Neon PostgreSQL

1. Create a Neon project at [neon.tech](https://neon.tech)
2. Get the connection string and add it to your `.env` file

## API Usage Examples

### Chat Request

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?",
    "top_k": 5,
    "temperature": 0.7
  }'
```

### Ingest Request

```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Physical AI represents the convergence of artificial intelligence with the physical world through robotic systems...",
    "source": "chapter-1-introduction/1.1-defining-physical-ai.md",
    "chapter": "Introduction to Physical AI",
    "section": "Defining Physical AI"
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py      # Configuration settings
│   │   └── database.py      # Database connections
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request.py       # Request models
│   │   └── response.py      # Response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py  # Chat business logic
│   │   └── ingest_service.py # Ingest business logic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py          # Chat API routes
│   │   └── ingest.py        # Ingest API routes
│   └── utils/
│       ├── __init__.py
│       └── text_processor.py # Text processing utilities
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── ingest_textbook.py      # Script to ingest textbook content
└── README.md               # This file
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Error**: Ensure Qdrant is running and the URL is correct
2. **Memory Issues**: The embedding model may require significant memory; consider using a smaller model
3. **API Rate Limits**: If using OpenAI, ensure you're within rate limits

### Logs

Check the application logs for any errors:

```bash
tail -f logs/app.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.