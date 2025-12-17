# RAG Chatbot Architecture for Physical AI & Humanoid Robotics Textbook

## Overview
This document details the architecture for the Retrieval-Augmented Generation (RAG) chatbot that will power the intelligent Q&A functionality for the textbook. The system will use Qdrant for vector storage, Neon PostgreSQL for metadata, and FastAPI for the backend API.

## Architecture Components

### 1. FastAPI Backend Service
**Location**: `backend/app/`

#### Core Components:
- **Main Application**: `main.py` - Entry point with API routes
- **Models**: `models/` - Pydantic models for request/response validation
- **Services**: `services/` - Business logic for chat and retrieval
- **Utils**: `utils/` - Helper functions and utilities
- **Config**: `config/` - Configuration management

#### API Endpoints:
- `POST /chat` - Main chat endpoint with context
- `POST /embed` - Text embedding endpoint
- `GET /health` - Health check endpoint
- `POST /ingest` - Document ingestion endpoint

### 2. Qdrant Vector Database
**Purpose**: Store and retrieve textbook content embeddings for semantic search

#### Collection Structure:
- **Collection Name**: `textbook_content`
- **Vector Size**: 1536 (for OpenAI embeddings) or 384 (for open-source alternatives)
- **Payload Schema**:
  ```json
  {
    "chapter": "string",
    "section": "string",
    "content": "string",
    "page_reference": "string",
    "source_file": "string"
  }
  ```

#### Search Strategy:
- Semantic similarity search using cosine distance
- Hybrid search combining keyword and semantic matching
- Re-ranking for improved relevance

### 3. Neon PostgreSQL Database
**Purpose**: Store metadata, conversation history, and user data

#### Tables:
- **documents**: Track ingested textbook content
  - id, title, chapter, section, file_path, created_at
- **conversations**: Store conversation history
  - id, user_id, created_at, updated_at
- **messages**: Individual messages in conversations
  - id, conversation_id, role, content, timestamp
- **embeddings_cache**: Cache for computed embeddings
  - id, text_hash, embedding_vector, created_at

### 4. Content Processing Pipeline
**Location**: `backend/app/pipeline/`

#### Components:
- **Document Loader**: Parse textbook content from various formats
- **Text Chunker**: Split content into semantic chunks
- **Embedding Generator**: Create vector embeddings for chunks
- **Indexer**: Store embeddings in Qdrant with metadata

## Implementation Details

### FastAPI Application Structure
```
backend/
├── app/
│   ├── main.py
│   ├── config/
│   │   ├── settings.py
│   │   └── database.py
│   ├── models/
│   │   ├── request.py
│   │   └── response.py
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── retrieval_service.py
│   │   └── embedding_service.py
│   ├── routes/
│   │   ├── chat.py
│   │   └── ingest.py
│   └── utils/
│       ├── text_processor.py
│       └── validators.py
├── requirements.txt
└── Dockerfile
```

### Dependencies
```txt
fastapi==0.104.1
uvicorn==0.24.0
qdrant-client==1.7.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
pydantic==2.5.0
openai==1.3.4
sentence-transformers==2.3.0
python-multipart==0.0.6
python-dotenv==1.0.0
```

### Configuration Management
Environment variables for free-tier optimization:
- `QDRANT_URL` - Qdrant instance URL
- `NEON_DATABASE_URL` - Neon PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key (or alternative)
- `EMBEDDING_MODEL` - Model for generating embeddings
- `MAX_TOKENS` - Maximum response tokens
- `TEMPERATURE` - LLM temperature setting

## Free-Tier Optimization Strategies

### 1. Resource Management
- Use minimal container resources
- Implement connection pooling
- Cache frequently accessed embeddings
- Implement request rate limiting

### 2. Cost Optimization
- Batch operations where possible
- Use open-source embedding models if OpenAI costs are too high
- Implement efficient indexing strategies
- Use serverless functions for background tasks

### 3. Performance Optimization
- Asynchronous processing for non-critical operations
- Efficient vector search with appropriate filters
- Proper indexing on database fields
- Caching of common queries

## Security Considerations

### 1. Input Validation
- Sanitize all user inputs
- Validate document uploads
- Implement proper error handling

### 2. Authentication
- Optional authentication for personalized features
- Rate limiting to prevent abuse
- Secure API key management

### 3. Data Privacy
- No storage of sensitive user information
- Clear data retention policies
- Secure data transmission

## Deployment Architecture

### Backend Deployment Options (Free-Tier Friendly)
1. **Railway**: Container-based deployment with PostgreSQL addon
2. **Render**: Web service deployment with free tier
3. **Fly.io**: Container deployment with volume storage
4. **PythonAnywhere**: Python-based hosting

### Frontend Integration
- Docusaurus plugin for chat widget
- REST API calls from frontend
- WebSocket support for real-time features (if needed)

## Error Handling and Monitoring

### Error Handling
- Comprehensive exception handling
- Graceful degradation when services are unavailable
- User-friendly error messages
- Proper logging for debugging

### Monitoring
- Basic health checks
- Performance metrics
- Error tracking
- Usage analytics

## Future Scalability Considerations

### Horizontal Scaling
- Stateless service design
- Database connection pooling
- Caching layer implementation
- Load balancing capabilities

### Feature Extensions
- Multi-language support
- Advanced analytics
- Personalized learning paths
- Collaborative features

This architecture provides a robust foundation for the RAG chatbot while maintaining free-tier compatibility and ensuring scalability for future enhancements.