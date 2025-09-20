# WealthTech Smart Search API

## 🚀 Quick Start with Docker

### 1. Clone Repository
```bash
git clone <repo-url>
cd project_20250915_2114_smart_search
```

### 2. Set API Key (Recommended: .env File)
```bash
# Copy template and edit with your actual API key
cp .env.example .env
nano .env  # Edit: GEMINI_API_KEY=your-actual-gemini-api-key

# Start application
docker compose up -d
```

**Alternative: Environment Variable**
```bash
# Set API key directly (temporary)
export GEMINI_API_KEY="your-gemini-api-key-here"
docker compose up -d
```

### 3. Verify Setup
```bash
# Check health
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Access interactive API docs
open http://localhost:8000/docs
```

### 4. Various summarization methods
```bash
# Use abstractive BART model summarization (local, no API key needed)
export SUMMARIZER="bart"
docker compose restart api

# Use extractive Sumy model (local, no API key needed)
export SUMMARIZER="extractive"
docker compose restart api

# Back to Gemini (default)
export SUMMARIZER="gemini"
docker compose restart api
```

### 2. Access the API
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Interactive Docs**: http://localhost:8000/docs

## 📡 API Endpoints

- `POST /clients/{id}/documents` - Upload documents
- `POST /clients/{id}/notes` - Upload meeting notes  
- `GET /search?q=query&type=document|note` - Hybrid search
- `GET /health` - Health check

## 🔍 Example API Usage

### Upload Document
```bash
curl -X POST "http://localhost:8000/clients/1/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Investment Portfolio Analysis",
    "content": "This comprehensive analysis covers portfolio diversification strategies, risk assessment methodologies, and performance optimization techniques for institutional investors."
  }'
```

### Upload Meeting Note
```bash
curl -X POST "http://localhost:8000/clients/1/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Client meeting focused on retirement planning. Discussed 401k rollover options and asset allocation strategy. Client prefers moderate risk tolerance with 60/40 stock/bond allocation."
  }'
```

### Search Documents and Notes
```bash
# Search all content
curl "http://localhost:8000/search?q=portfolio%20diversification"

# Search only documents
curl "http://localhost:8000/search?q=investment&type=document"

# Search only notes
curl "http://localhost:8000/search?q=retirement&type=note"
```

### Example Search Response
```json
{
  "query": "portfolio diversification",
  "results": [
    {
      "id": 1,
      "type": "document",
      "title": "Investment Portfolio Analysis",
      "summary": "Comprehensive analysis covering portfolio diversification strategies and risk assessment for institutional investors.",
      "content": "This comprehensive analysis covers...",
      "score": 0.85
    }
  ]
}
```

## 🏗️ Architecture

```
src/
├── main.py              # FastAPI app entry point
├── config.py            # Settings and configuration  
├── database.py          # Database connection
├── api/                 # API endpoints and schemas
│   ├── documents.py     # Document upload
│   ├── notes.py         # Notes upload
│   ├── search.py        # Hybrid search
│   └── schemas.py       # Request/response models
├── models/              # Database models
│   └── database.py      # SQLAlchemy models
└── utils/               # Utilities and AI functions
    ├── validation.py    # Input validation
    ├── embedder.py      # Text embeddings
    ├── summarizer.py    # Text summarization
    └── search_utils.py  # Search ranking (RRF)
```

## 🧪 Testing

```bash
# Run unit tests (fast, ~14s)
python -m pytest tests/test_unit.py -v

# Run integration tests (requires API running, ~90s)
python -m pytest tests/test_integration.py -v

# Run with coverage
python -m pytest tests/test_unit.py --cov=src --cov-report=term-missing
```

## 🔧 Tech Stack

- **API**: FastAPI + Pydantic + SQLAlchemy
- **Database**: PostgreSQL 16 with pgvector extension
- **AI**: Gemini API (default), BART, Extractive summarization
- **Embeddings**: sentence-transformers (local)
- **Search**: Hybrid FTS + pg vector search with Reciprocal Rank Fusion
- **Deployment**: Docker Compose

## 🔍 Search Features

### Full-Text Keyword Search
- PostgreSQL FTS with ranking
- Exact keyword matching
- Phrase search support

### Semantic Vector Search  
- sentence-transformers embeddings
- pgvector similarity search
- Context-aware matching

### Hybrid Search
- Combines FTS + vector results
- Reciprocal Rank Fusion (RRF) algorithm
- Optimized relevance scoring

### Document Summaries
- **Gemini API**: Advanced AI summarization (default)
- **BART**: Local transformer model
- **Extractive**: Simple sentence extraction

## 📚 API Documentation

- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative format)
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Markdown Docs**: [docs/API.md](docs/API.md) (Static documentation)

## 🆘 Troubleshooting

**Database Issues?**
```bash
docker compose down
docker compose up -d
```

**Check Logs:**
```bash
docker compose logs api
docker compose logs db
```


## Testing

### Running Tests

```bash
# Run unit tests (fast, ~14s)
python -m pytest tests/test_unit.py -v

# Run integration tests (requires API running, ~90s)
python -m pytest tests/test_integration.py -v

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/test_unit.py --cov=app --cov-report=term-missing
```

### Test Coverage
- **Unit Tests**: Core business logic, edge cases, regression prevention
- **Integration Tests**: Complete API functionality via HTTP requests
- **Combined**: Comprehensive system validation
