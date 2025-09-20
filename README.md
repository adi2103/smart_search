# WealthTech Smart Search API

## 🚀 Quick Start with Docker

### 1. Set API Key & Run
```bash
# Set your Gemini API key (shared separately for security)
export GEMINI_API_KEY="your-gemini-api-key-here"

# Start the application
docker compose up -d
```

### 2. Access the API
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health  
- **Interactive Docs**: http://localhost:8000/docs

### 3. Optional: Switch AI Methods
```bash
# Use BART (local, no API key needed)
export SUMMARIZER="bart"
docker compose restart api

# Use extractive (local, no API key needed)  
export SUMMARIZER="extractive"
docker compose restart api

# Back to Gemini (default)
export SUMMARIZER="gemini"
docker compose restart api
```

## 📡 API Endpoints

- `POST /clients/{id}/documents` - Upload documents
- `POST /clients/{id}/notes` - Upload meeting notes  
- `GET /search?q=query&type=document|note` - Hybrid search
- `GET /health` - Health check

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
- **Search**: Hybrid FTS + vector with Reciprocal Rank Fusion
- **Deployment**: Docker Compose

## 🆘 Troubleshooting

**API Key Error?**
```bash
export GEMINI_API_KEY="your-key-here"
docker compose restart api
```

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
