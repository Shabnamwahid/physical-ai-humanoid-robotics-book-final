# Physical AI & Humanoid Robotics Textbook

[![Deploy to GitHub Pages](https://github.com/your-username/physical-ai-humanoid-robotics-book-q4/actions/workflows/deploy.yml/badge.svg)](https://github.com/your-username/physical-ai-humanoid-robotics-book-q4/actions/workflows/deploy.yml)

A comprehensive Docusaurus-based textbook covering Physical AI and Humanoid Robotics with an integrated RAG (Retrieval-Augmented Generation) chatbot.

## Overview

This project provides a complete educational resource on Physical AI and Humanoid Robotics, featuring:

- Complete textbook content covering 8 chapters
- Interactive Docusaurus-based frontend
- AI-powered chatbot for answering questions about the content
- Vector database for semantic search
- Free-tier friendly architecture

## Table of Contents

1. [Introduction to Physical AI](./docs/chapter-1-introduction-to-physical-ai/index.md)
2. [Basics of Humanoid Robotics](./docs/chapter-2-basics-of-humanoid-robotics/index.md)
3. [ROS 2 Fundamentals](./docs/chapter-3-ros-2-fundamentals/index.md)
4. [Digital Twin Simulation and Sensors](./docs/chapter-4-digital-twin-simulation/index.md)
5. [NVIDIA Isaac Sim and Navigation](./docs/chapter-5-nvidia-isaac-sim/index.md)
6. [Vision-Language-Action (VLA)](./docs/chapter-6-vision-language-action/index.md)
7. [Conversational Robotics & AI](./docs/chapter-7-conversational-robotics/index.md)
8. [Capstone Project](./docs/chapter-8-capstone-project/index.md)

## Architecture

The system consists of three main components:

### Frontend
- **Framework**: Docusaurus
- **Deployment**: GitHub Pages
- **Features**: AI chat widget, responsive design, search functionality

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon) for metadata
- **Vector Database**: Qdrant for content embeddings
- **AI Models**: Sentence Transformers for embeddings, OpenAI or local models for generation

### AI/ML Components
- **Embedding Model**: all-MiniLM-L6-v2 (or configurable)
- **Generation Model**: GPT-3.5-turbo or configurable
- **Retrieval**: Vector similarity search in Qdrant

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- Docker (for Qdrant)
- Access to OpenAI API (optional, can use local models)

### Frontend Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/physical-ai-humanoid-robotics-book-q4.git
cd physical-ai-humanoid-robotics-book-q4
```

2. Install frontend dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start the backend:
```bash
uvicorn app.main:app --reload
```

### Qdrant Setup

1. Start Qdrant using Docker:
```bash
docker-compose -f docker-compose.qdrant.yml up -d
```

### Content Ingestion

1. After starting both the backend and Qdrant, run the setup script:
```bash
cd backend
python setup_textbook.py
```

This will ingest all textbook content into the vector database.

## Environment Variables

### Backend (.env)

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
OPENAI_API_KEY=your_openai_api_key  # Optional, for better responses
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

## API Endpoints

### Chat API
- `POST /api/v1/chat` - Main chat endpoint
- `GET /api/v1/chat/health` - Chat service health check

### Ingest API
- `POST /api/v1/ingest` - Ingest content
- `POST /api/v1/ingest/batch` - Batch ingest
- `GET /api/v1/ingest/health` - Ingest service health check

### General
- `GET /` - Root endpoint
- `GET /health` - General health check

## Development

### Adding New Content

1. Add your markdown content to the `docs/` directory following the existing structure
2. Update the `sidebars.js` file to include new content in the navigation
3. Run the ingestion script to add content to the vector database

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend build test:
```bash
npm run build
```

## Deployment

### GitHub Pages

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/deploy.yml`.

### Backend Deployment

For backend deployment, you can use platforms like:
- Railway
- Render
- Google Cloud Run
- AWS Fargate

Make sure to update the `CHATBOT_API_URL` environment variable in the frontend config to point to your deployed backend.

## Project Structure

```
physical-ai-humanoid-robotics-book-q4/
├── docs/                    # Textbook content in markdown
│   ├── chapter-1-introduction-to-physical-ai/
│   ├── chapter-2-basics-of-humanoid-robotics/
│   ├── ...
│   └── appendices/
├── src/
│   ├── components/         # React components
│   │   └── ChatWidget/     # AI chat widget
│   ├── plugins/            # Docusaurus plugins
│   │   └── docusaurus-plugin-ai-chat/
│   └── css/                # Custom styles
├── backend/                # FastAPI backend
│   ├── app/                # Application code
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   ├── routes/         # API routes
│   │   └── utils/          # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container configuration
├── .github/
│   └── workflows/          # CI/CD workflows
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Navigation configuration
└── package.json            # Frontend dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue in the GitHub repository.

## Acknowledgments

- The Docusaurus team for the excellent documentation framework
- The Qdrant team for the vector database
- The Hugging Face team for the sentence transformers
- All contributors to open source libraries used in this project