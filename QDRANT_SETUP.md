# Qdrant Vector Database Setup for Physical AI Textbook

This document provides instructions for setting up Qdrant, the vector database used for the Physical AI & Humanoid Robotics textbook RAG system.

## Overview

Qdrant is a vector similarity search engine that enables efficient retrieval of textbook content based on semantic similarity. It powers the RAG (Retrieval-Augmented Generation) system that allows users to ask questions about the textbook content.

## Prerequisites

- Docker and Docker Compose (for containerized deployment)
- At least 2GB of available disk space
- 4GB RAM recommended for optimal performance

## Installation Options

### Option 1: Docker Compose (Recommended)

1. Create the Qdrant container using the provided docker-compose file:

```bash
docker-compose -f docker-compose.qdrant.yml up -d
```

2. Verify that Qdrant is running:

```bash
docker ps | grep qdrant
```

3. Check the logs:

```bash
docker logs qdrant-physical-ai
```

### Option 2: Docker Run

```bash
docker run -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  --name qdrant-physical-ai \
  qdrant/qdrant:latest
```

### Option 3: Direct Installation

For detailed installation instructions on different platforms, visit the [Qdrant documentation](https://qdrant.tech/documentation/).

## Configuration

### Environment Variables

Set the following environment variables:

```bash
# In your .env file
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here  # Optional for basic setup
```

### Collection Setup

The backend application will automatically create the required collection:

- **Collection Name**: `textbook_content`
- **Vector Size**: 384 (for all-MiniLM-L6-v2 embeddings)
- **Distance Function**: Cosine

## API Access

### Health Check

```bash
curl http://localhost:6333/health
```

### Check Collections

```bash
curl http://localhost:6333/collections
```

### Collection Information

```bash
curl http://localhost:6333/collections/textbook_content
```

## Security

### API Key (Optional)

For production deployments, you can set an API key:

```bash
# In docker-compose file or environment
QDRANT_API_KEY=your_strong_api_key_here
```

Then include it in requests:

```bash
curl -H "api-key: your_api_key_here" \
  http://localhost:6333/collections
```

## Performance Tuning

### Memory Settings

For better performance, you can adjust Qdrant settings in a custom config:

```yaml
# qdrant_config.yaml
storage:
  # How many shards should be kept in memory
  optimizers:
    # Interval between forced flushes
    flush_interval_sec: 5
    # Maximum number of segments in a single shard
    max_segment_number: 5
```

### Docker Resources

Limit resources in production:

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant-physical-ai
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage:z
    environment:
      - QDRANT_API_KEY=${QDRANT_API_KEY:-}
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
    restart: unless-stopped
```

## Data Persistence

The Docker Compose setup includes volume persistence:

- Data is stored in the `qdrant_storage` volume
- Data persists between container restarts
- Backup by copying the volume: `docker volume cp qdrant_storage backup_location`

## Backup and Restore

### Backup

```bash
# Stop the container
docker stop qdrant-physical-ai

# Copy the storage volume
docker run --rm -v qdrant_storage:/from -v $(pwd)/backup:/to alpine ash -c "cd /from && tar cvf /to/qdrant_backup.tar ."

# Start the container again
docker start qdrant-physical-ai
```

### Restore

```bash
# Stop the container
docker stop qdrant-physical-ai

# Clear existing data and restore backup
docker run --rm -v qdrant_storage:/to -v $(pwd)/backup:/from alpine ash -c "cd /from && tar xvf qdrant_backup.tar -C /to"

# Start the container
docker start qdrant-physical-ai
```

## Monitoring

### Health Checks

The application includes health check endpoints:

```bash
# Backend health check
curl http://localhost:8000/health

# Qdrant health check
curl http://localhost:6333/health
```

### Metrics

Qdrant provides metrics at:

```bash
curl http://localhost:6333/metrics
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Check if Qdrant is already running: `docker ps | grep qdrant`
   - Change ports in docker-compose if needed

2. **Insufficient Disk Space**
   - Check disk usage: `docker system df`
   - Clean up unused containers: `docker system prune`

3. **Connection Refused**
   - Verify Qdrant is running: `docker logs qdrant-physical-ai`
   - Check firewall settings

4. **High Memory Usage**
   - Monitor with: `docker stats qdrant-physical-ai`
   - Adjust resources in docker-compose file

### Logs

Check Qdrant logs:

```bash
docker logs qdrant-physical-ai
```

For real-time logs:

```bash
docker logs -f qdrant-physical-ai
```

## Integration with Backend

The FastAPI backend automatically connects to Qdrant using the configuration in `backend/app/config/settings.py`.

### Collection Schema

The `textbook_content` collection stores documents with the following structure:

```json
{
  "content": "Text content from the textbook",
  "metadata": {
    "source": "chapter-1-introduction/1.1-defining-physical-ai.md",
    "chapter": "Introduction to Physical AI",
    "section": "Defining Physical AI",
    "created_at": "2023-12-01T10:00:00Z",
    "chunk_index": 0,
    "total_chunks": 5
  }
}
```

## Scaling

### Horizontal Scaling

For high availability, you can run Qdrant in cluster mode:

```yaml
version: '3.8'

services:
  qdrant-0:
    image: qdrant/qdrant:latest
    container_name: qdrant-0
    ports:
      - "6333:6333"
      - "6334:6334"
    command: ["--bootstrap", "qdrant-0:6335", "--uri", "http://qdrant-0:6335"]
    volumes:
      - qdrant_0_storage:/qdrant/storage:z

  qdrant-1:
    image: qdrant/qdrant:latest
    container_name: qdrant-1
    ports:
      - "6335:6333"
      - "6336:6334"
    command: ["--bootstrap", "qdrant-0:6335", "--uri", "http://qdrant-1:6335"]
    volumes:
      - qdrant_1_storage:/qdrant/storage:z
```

## Development vs Production

### Development

- Use default settings
- No authentication required
- Local storage volume

### Production

- Enable API key authentication
- Use persistent storage
- Configure resource limits
- Set up monitoring
- Implement backup procedures

## Testing the Setup

After starting Qdrant, test the connection:

```bash
# Check if Qdrant is responding
curl http://localhost:6333

# List collections (should be empty initially)
curl http://localhost:6333/collections

# The backend will automatically create the textbook_content collection when it starts
```

## Next Steps

Once Qdrant is set up, proceed with:

1. Starting the FastAPI backend
2. Running the content ingestion script
3. Testing the RAG functionality

For detailed API documentation, visit the Qdrant documentation at [qdrant.tech](https://qdrant.tech/documentation/).