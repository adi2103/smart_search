# WealthTech Smart Search API

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repo-url>
cd project_20250915_2114_smart_search

# Set API key (recommended: .env file)
cp .env.example .env
nano .env  # Edit: GEMINI_API_KEY=your-actual-gemini-api-key

# Start application
docker compose up -d
```

**Alternative: Environment Variable**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
docker compose up -d
```

### 2. Verify Setup
```bash
curl http://localhost:8000/health  # Should return: {"status":"healthy"}
open http://localhost:8000/docs    # Interactive API documentation
```

## 📡 API Usage

### Endpoints
- `POST /clients/{id}/documents` - Upload documents
- `POST /clients/{id}/notes` - Upload meeting notes  
- `GET /search?q=query&type=document|note` - Hybrid search
- `GET /health` - Health check

### Examples
```bash
# Upload document
curl -X POST "http://localhost:8000/clients/1/documents" \
  -H "Content-Type: application/json" \
  -d '{"title": "Investment Analysis", "content": "Portfolio diversification strategies..."}'

# Upload note
curl -X POST "http://localhost:8000/clients/1/notes" \
  -H "Content-Type: application/json" \
  -d '{"content": "Client meeting on retirement planning. Discussed 401k options..."}'

# Search
curl "http://localhost:8000/search?q=portfolio%20diversification"
curl "http://localhost:8000/search?q=retirement&type=note"
```

### Response Format
```json
{
  "query": "portfolio diversification",
  "results": [
    {
      "id": 1,
      "type": "document", 
      "title": "Investment Analysis",
      "summary": "Analysis covering portfolio diversification strategies...",
      "content": "Full document content...",
      "score": 0.85
    }
  ]
}
```

## 🔍 Search Features

- **Full-Text Search**: PostgreSQL FTS with keyword matching
- **Semantic Search**: Vector similarity using sentence-transformers + pgvector
- **Hybrid Search**: Combines both methods with Reciprocal Rank Fusion (RRF)
- **AI Summaries**: Gemini API (default), BART, or extractive summarization

### Switch AI Methods
```bash
export SUMMARIZER="bart"        # Local BART model
export SUMMARIZER="extractive"  # Simple extraction
export SUMMARIZER="gemini"      # Gemini API (default)
docker compose restart api
```

## 🧪 Testing

```bash
# Run all tests inside Docker
docker compose exec api python -m pytest tests/ -v

# Unit tests (17 tests, ~10s)
docker compose exec api python -m pytest tests/test_unit.py -v

# Integration tests (11 tests, ~25s) 
docker compose exec api python -m pytest tests/test_integration.py -v
```

## 🏗️ Architecture

```
src/
├── main.py              # FastAPI app
├── config.py            # Configuration
├── database.py          # DB connection
├── api/                 # Endpoints & schemas
├── models/              # SQLAlchemy models
└── utils/               # AI utilities (embeddings, summarization, search)
```

**Tech Stack**: FastAPI, PostgreSQL + pgvector, sentence-transformers, Docker Compose

## 📚 Documentation

- **Interactive**: http://localhost:8000/docs (Swagger UI)
- **Static**: [docs/API.md](docs/API.md)
- **Update**: `./scripts/update-docs.sh` (auto-updates via GitHub Actions)

## 🆘 Troubleshooting

```bash
# Restart containers
docker compose down && docker compose up -d

# Check logs
docker compose logs api
docker compose logs db

# Verify API key is set
echo $GEMINI_API_KEY
```
